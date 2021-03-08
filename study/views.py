import io
import csv 
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import redirect_to_login 
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import UpdateView

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from leaderboard.leaderboard import Leaderboard

from .models import VerseStudyEntry, CompleteTheVerse, NameTheBook
from .filters import VSFilter



def vsw_browse(request):
    my_title = "King James Bible"
    template = "study/vsw_browse.html"
    qs = VerseStudyEntry.objects.all().order_by('id')
    word_filter = VSFilter(request.GET, queryset=qs)
    p = Paginator(word_filter.qs, 175)
    page = request.GET.get('page', 1)
    object_list = p.get_page(page)
    context = {"title": my_title, "object_list": object_list, "filter": word_filter}
    return render(request, template, context)

@user_passes_test(lambda u: u.is_superuser)
def vsw_delete(request, pk):
    #if request.user.groups.filter(name="Owner").count() == 0:
    #    raise Http404
    verse = get_object_or_404(VerseStudyEntry,pk=pk)
    verse.delete()
    messages.info(request, str(verse) + " is deleted successfully")
    return redirect(reverse('verse-browse')+"?"+request.META['QUERY_STRING'])

@user_passes_test(lambda u: u.is_superuser)
def vsw_edit(request, pk):
    #if request.user.groups.filter(name="Owner").count() == 0:
    #    raise Http404
    verse = get_object_or_404(VerseStudyEntry,pk=pk)
    verse.delete()
    messages.info(request, str(verse) + " is deleted successfully")
    return redirect(reverse('verse-browse')+"?"+request.META['QUERY_STRING'])

class VSWUpdateView(SuccessMessageMixin, UpdateView):
    model = VerseStudyEntry
    template_name = 'study/vsw_update.html'
    fields = ('book_title', 'chapter', 'verse_number', 'verse_text')
    success_message = 'Verse saved successfully!'

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            return request.user.is_superuser
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(VSWUpdateView, self).dispatch(
            request, *args, **kwargs)



def clear_field(content):
    if content:
        return content.strip()
    return ""

@user_passes_test(lambda u: u.is_superuser)
def vsw_upload(request):
    template = "study/vsw_upload.html"
    prompt = {
        'order': "The columns should be: Book, Chapter, Verse Number, and Verse Text."
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "Only CSV files may be uploaded.")
        return render(request, template)

    data_set = ""
    try:
        data_set = csv_file.read().decode("UTF8")
    except Exception as e:
        csv_file.seek(0)
        data_set = csv_file.read().decode("ISO-8859-1")

    io_string = io.StringIO(data_set)
    io_string_quick_check = io.StringIO(data_set)

    # header count check
    header = next(io_string)
    header_clean = [x for x in header.split(',') if not x in ['', '\r\n', '\n']]
    if len(header_clean) != 4:
        messages.error(request, "Make sure header consists of 4 elements. %s" % prompt['order'])
        return render(request, template)

    next(io_string_quick_check)
    count = 2
    for column in csv.reader(io_string_quick_check, delimiter=',', quotechar='"'):
        book_title = clear_field(column[0])
        chapter = int(clear_field(column[1]))
        verse_number = int(clear_field(column[2]))
        verse_text = clear_field(column[3])

        if len(book_title) <= 1:
            messages.error(request, "Row %d doesn't have a book title. All rejected" % (count,))
            return render(request, template)
    
        try:
            int(chapter)
        except Exception:
            messages.error(request, "Row %d doesn't have a chapter number that's integer. All rejected" % (count,))
            return render(request, template)

        try:
            int(verse_number)
        except Exception:
            messages.error(request, "Row %d doesn't have a verse number that's integer. All rejected" % (count,))
            return render(request, template)

        if len(verse_text) <= 1:
            messages.error(request, "Row %d doesn't have a verse text. All rejected" % (count,))
            return render(request, template)

        count += 1

    count = 2
    for column in csv.reader(io_string, delimiter=',', quotechar='"', skipinitialspace=True):
        book_title = clear_field(column[0])
        chapter = int(clear_field(column[1]))
        verse_number = int(clear_field(column[2]))
        verse_text = clear_field(column[3])

        with transaction.atomic():  # savepoint
            try:
                vse, created = VerseStudyEntry.objects.get_or_create(
                    book_title=book_title,
                    chapter=chapter,
                    verse_number=verse_number)
                print("Book:" + book_title + " Chapter:" + str(chapter) + " Verse num:" + str(verse_number))
                vse.verse_text = verse_text
                vse.save()
            except Exception as e:
                messages.error(request, "Skipped row %d due error: %s." % (count, str(e)))
                transaction.set_rollback(True)
        count += 1

    messages.success(request, "Upload complete.")
    return redirect("/")

@user_passes_test(lambda u: u.is_superuser)
def manage_scores(request):
    op = request.GET.get('op','')
    code = request.GET.get('code','')
    us = request.GET.get('us',None)

    if op not in ['lb','sc','sc_single','tm_single']:
        return HttpResponse("Unrecognized op: %s" % op)

    if op.endswith('_single') and not us:
        return HttpResponse("You must provide a user in single operation mode")

    if code not in ['ctv','ntb']:
        return HttpResponse("Unrecognized code: %s" % code)

    from django.core.management import call_command
    if op == 'lb':
        call_command('recover_leaderboard', code)
    elif op == 'sc':
        call_command('reset_scores', code)
    elif op == 'sc_single':
        call_command('score_zero_out', code, 'sc', us)
    elif op == 'tm_single':
        call_command('score_zero_out', code, 'tm', us)

    return HttpResponse("OK")
    

def get_active_leaderboard(game, stat):
    if game not in ['ctv','ntb']:
        raise Exception("Unsupported game: %s" % game)

    if stat not in ['sc','tm']:
        raise Exception("Unsupported stat type: %s" % stat)

    #last_sun, last_sat = last_sun_sat()
    #active_week = (last_sat + datetime.timedelta(days=1)).strftime("%Y_%m_%d")
    lb = Leaderboard('%s_%s' % (game, stat), host=settings.LEADERBOARD_REDIS_HOST)
    return lb

def get_leaderboards(request, game, user=None):
    lb_score = []
    lb_time = []
    self_rank = {}

    owner = False
    #if request.user.groups.filter(name="Owner").count() == 1:
    if request.user.is_superuser:
        owner = True

    # get top 3 for leaderboards
    lb_score_raw = get_active_leaderboard(game,'sc')
    lb_time_raw = get_active_leaderboard(game,'tm')
    score_leaders = lb_score_raw.leaders(1)[:3]
    time_leaders = lb_time_raw.leaders(1)[:3]
    for item in score_leaders:
        us = user_from_leaderboard_key(item['member'])
        church = ""
        if us:
            church = us.get_church_name_short()
        score = int(item['score'])
        rank = item['rank']
        row = [rank, us, church, score]
        if owner:
            row.append(reverse('manage-scores')+"?op=sc_single&code="+game+"&us="+str(us.pk))
        lb_score.append(row)
    for item in time_leaders:
        us = user_from_leaderboard_key(item['member'])
        church = ""
        if us:
            church = us.get_church_name_short()
        score = secs_to_mins(int(item['score']))
        rank = item['rank']
        row = [rank, us, church, score]
        if owner:
            row.append(reverse('manage-scores')+"?op=tm_single&code="+game+"&us="+str(us.pk))
        lb_time.append(row)

    # self rank
    if user:
        self_lb_key = leaderboard_key_for(user)
        church = user.get_church_name_short()
        self_rank.update({'user': user, 'church':church})

        self_data = lb_score_raw.score_and_rank_for(self_lb_key)
        if self_data['score']:
            self_score = int(self_data['score'])
            self_score_place = self_data['rank']
            if self_score_place:
                self_rank.update({'score': self_score, 'score_place': self_score_place})

        self_data = lb_time_raw.score_and_rank_for(self_lb_key)
        if self_data['score']:
            self_time = int(self_data['score'])
            self_time_place = self_data['rank']
            if self_time_place:
                self_rank.update({'time': self_time, 'time_place': self_time_place})

    return {'lb_score':lb_score, 'lb_time':lb_time, 'self_rank':self_rank}


def leaderboard_key_for(user):
    return 'user_%s' % str(user.pk)

def user_from_leaderboard_key(key):
    pk = key.decode('utf8').split('_')[1]
    try:
        user_model = get_user_model()
        user = user_model.objects.get(pk=pk)
    except Student.DoesNotExist:
        return None
    return user


def secs_to_mins(secs):
    minutes = secs // 60
    remainder = secs % 60
    if remainder > 29:
        minutes += 1
    return minutes

def complete_the_verse(request):
    template_name = "study/complete_the_verse.html"
    play = request.GET.get('play',None)
    best = 0

    # if teacher/owner
    #student = None
    #if request.user.groups.filter(name="Student").count() == 0:
    #    best = 0
    #else:
    #    student = get_object_or_404(Student, email=request.user.email)
    #    best = VocabularyPractice.objects.filter(student=student, current_best=True)
    #    if best.count() > 0:
    #        best = best[0].stat_score
    #    else:
    #        best = 0
    if request.user.is_authenticated:
        best = CompleteTheVerse.objects.filter(user=request.user, current_best=True)
        if best.count() > 0:
            best = best[0].stat_score
        else:
            best = 0

        lbs = get_leaderboards(request, 'ctv', user=request.user)
        self_rank = lbs['self_rank']

        context = {
            "title": "Complete The Verse",
            "best": best,
            "leaderboard_scores": lbs['lb_score'],
            "leaderboard_times": lbs['lb_time'],
            "self_rank": self_rank,
            "play": play
        }
        #if request.user.groups.filter(name="Owner").count() == 1:
        if request.user.is_superuser:
            context.update({"management_lb_recover_url":reverse('manage-scores')+"?op=lb&code=ctv"})
            context.update({"management_sc_reset_url":reverse('manage-scores')+"?op=sc&code=ctv"})
    else:
        context = {
            "title": "Complete The Verse",
            "best": best,
            "play": play
        }

    if not request.user.is_authenticated and play == None:
        return redirect(reverse('complete-the-verse') + "?play=1")
    return render(request, template_name, context)


# /phonics-practice/fetch/?ts=123&level=1
@api_view(['GET'])
#@authentication_classes([SessionAuthentication])
#@permission_classes([IsAuthenticated])
def ctv_get_word(request):
    level = request.GET.get('level', '')
    ts = request.GET.get('ts', '')
    pc = request.GET.get('pc', '')
    bo = request.GET.get('bo', '')
    if not ts:
        return Response({"message": "please provide ts value"})

    if not pc:
        return Response({"message": "please provide pc value"})

    if not bo:
        return Response({"message": "please provide bo value"})

    try:
        pc = int(pc)
    except Exception:
        return Response({"message": "pc must be integer"})

    try:
        bo = int(bo)
        if bo == 1:
            bo = True
        else:
            bo = False
    except Exception:
        return Response({"message": "bo must be integer"})

    try:
        level = int(level)
    except Exception:
        return Response({"message": "level must be integer"})

    qs = VerseStudyEntry.objects.all()
    count = qs.count()
    picked = {}
    attempts = 0

    if count < pc:
        return Response({"message": "err-less-than-pick-count", "images": []})

    while len(picked) != pc and attempts < 50:
        obj = qs[random.randint(0, count - 1)]
        obj_key = obj.get_unique_key(book_only=bo)
        if obj_key not in picked:
            picked.update({obj_key: obj})
            attempts = 0
        attempts += 1

    if attempts >= 50:
        raise Exception("attempts exceeded 50")  # , final data: %s" % str(picked.keys()))

    images = []
    for k, v in picked.items():
        #thumb = "https://cloudfour.com/examples/img-currentsrc/images/kitten-large.png"
        thumb = ""
        images.append({"image": thumb, "book_title": v.book_title, "chapter": v.chapter, "verse_number":v.verse_number, "verse_text": v.verse_text})

    return Response({"message": "ok", "images": images})


#@login_required
#@group_required('Suppport','Bronze', 'Owner', 'Silver', 'Gold', 'Home', 'Administrator', 'Counselor', 'Secondaryteacher', 'Districtteacher', 'Primaryteacher', 'Superintendent', 'Principal')
@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
#@permission_classes([IsAuthenticated])
def ctv_report(request):
    #if request.user.groups.filter(name="Student").count() == 0:
    #    return Response({"message": "score not submitted, not a student"})

    if not request.user.is_authenticated:
        return Response({"message": "not authorized"})

    stat_grade_level = int(request.POST.get('grade_level'))
    stat_time_secs = int(request.POST.get('time_secs'))
    stat_stars = int(request.POST.get('stars'))
    stat_total_correct = int(request.POST.get('total_correct'))
    stat_total_questions = int(request.POST.get('total_questions'))
    stat_score = int(request.POST.get('score'))

    if stat_total_questions == 0:
        return Response({"message": "score not submitted, 0 questions attempted"})

    ctv = CompleteTheVerse(
        user=request.user,
        created=timezone.now(),
        stat_grade_level=stat_grade_level,
        stat_time_secs=stat_time_secs,
        stat_stars=stat_stars,
        stat_total_correct=stat_total_correct,
        stat_total_questions=stat_total_questions,
        stat_score=stat_score
    )
    ctv.save()

    # update score at leaderboard
    lb_score = get_active_leaderboard('ctv','sc')
    current_score = lb_score.rank_for(leaderboard_key_for(request.user))
    if current_score == None or stat_score > current_score:
        lb_score.rank_member(leaderboard_key_for(request.user), stat_score)

    # update time at leaderboard
    lb_time = get_active_leaderboard('ctv','tm')
    time_played = 0
    stats = CompleteTheVerse.objects.filter(user=request.user) #created__gt=last_sat)
    if stats.count() > 0:
        time_played = stats.filter(user=request.user).aggregate(Sum('stat_time_secs'))['stat_time_secs__sum']
    lb_time.rank_member(leaderboard_key_for(request.user), time_played)

    return Response({"message": "ok"})


def name_the_book(request):
    template_name = "study/name_the_book.html"
    play = request.GET.get('play',None)
    best = 0

    # if teacher/owner
    #student = None
    #if request.user.groups.filter(name="Student").count() == 0:
    #    best = 0
    #else:
    #    student = get_object_or_404(Student, email=request.user.email)
    #    best = VocabularyPractice.objects.filter(student=student, current_best=True)
    #    if best.count() > 0:
    #        best = best[0].stat_score
    #    else:
    #        best = 0
    if request.user.is_authenticated:
        best = NameTheBook.objects.filter(user=request.user, current_best=True)
        if best.count() > 0:
            best = best[0].stat_score
        else:
            best = 0

        lbs = get_leaderboards(request, 'ntb', user=request.user)
        self_rank = lbs['self_rank']

        context = {
            "title": "Name The Book",
            "best": best,
            "leaderboard_scores": lbs['lb_score'],
            "leaderboard_times": lbs['lb_time'],
            "self_rank": self_rank,
            "play": play
        }
        #if request.user.groups.filter(name="Owner").count() == 1:
        if request.user.is_superuser:
            context.update({"management_lb_recover_url":reverse('manage-scores')+"?op=lb&code=ntb"})
            context.update({"management_sc_reset_url":reverse('manage-scores')+"?op=sc&code=ntb"})
    else:
        context = {
            "title": "Name The Book",
            "best": best,
            "play": play
        }

    if not request.user.is_authenticated and play == None:
        return redirect(reverse('name-the-book') + "?play=1")

    return render(request, template_name, context)


#@login_required
#@group_required('Suppport','Bronze', 'Owner', 'Silver', 'Gold', 'Home', 'Administrator', 'Counselor', 'Secondaryteacher', 'Districtteacher', 'Primaryteacher', 'Superintendent', 'Principal')
@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
#@permission_classes([IsAuthenticated])
def ntb_report(request):
    #if request.user.groups.filter(name="Student").count() == 0:
    #    return Response({"message": "score not submitted, not a student"})

    if not request.user.is_authenticated:
        return Response({"message": "not authorized"})

    stat_grade_level = int(request.POST.get('grade_level'))
    stat_time_secs = int(request.POST.get('time_secs'))
    stat_stars = int(request.POST.get('stars'))
    stat_total_correct = int(request.POST.get('total_correct'))
    stat_total_questions = int(request.POST.get('total_questions'))
    stat_score = int(request.POST.get('score'))

    if stat_total_questions == 0:
        return Response({"message": "score not submitted, 0 questions attempted"})

    ntb = NameTheBook(
        user=request.user,
        created=timezone.now(),
        stat_grade_level=stat_grade_level,
        stat_time_secs=stat_time_secs,
        stat_stars=stat_stars,
        stat_total_correct=stat_total_correct,
        stat_total_questions=stat_total_questions,
        stat_score=stat_score
    )
    ntb.save()

    # update score at leaderboard
    lb_score = get_active_leaderboard('ntb','sc')
    current_score = lb_score.rank_for(leaderboard_key_for(request.user))
    if current_score == None or stat_score > current_score:
        lb_score.rank_member(leaderboard_key_for(request.user), stat_score)

    # update time at leaderboard
    lb_time = get_active_leaderboard('ntb','tm')
    time_played = 0
    stats = CompleteTheVerse.objects.filter(user=request.user) #created__gt=last_sat)
    if stats.count() > 0:
        time_played = stats.filter(user=request.user).aggregate(Sum('stat_time_secs'))['stat_time_secs__sum']
    lb_time.rank_member(leaderboard_key_for(request.user), time_played)

    return Response({"message": "ok"})


