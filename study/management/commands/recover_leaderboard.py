from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
from leaderboard.leaderboard import Leaderboard

from main.models import User
from study.models import CompleteTheVerse, NameTheBook
from study.views import leaderboard_key_for

supported = ['ctv','ntb']
game_model_map = {
    'ctv': CompleteTheVerse,
    'ntb': NameTheBook 
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('code')

    def handle(self, *args, **options):
        global supported
        code = options['code']
        if code == '-1':
            to_do = supported
        else:
            if code not in supported:
                raise Exception("Unrecognized code:%s" % code)
            to_do = [code]

        for game in to_do:
            print("\nProcessing game %s"  % game_model_map[game].__name__)
            model = game_model_map[game]
            lb_score = Leaderboard('%s_sc' % (game,), host=settings.LEADERBOARD_REDIS_HOST)
            lb_time = Leaderboard('%s_tm' % (game,), host=settings.LEADERBOARD_REDIS_HOST)
            lb_score.delete_leaderboard()
            lb_time.delete_leaderboard() 

            # iterate all users who has data
            us_count = User.objects.count()
            count = 1
            for us in User.objects.all():
                #print("Processing user %d of %d" % (count, us_count))
                # find and set best score
                best = model.objects.filter(user=us,current_best=True)
                if best.count() > 0:
                    best = best[0].stat_score
                    lb_score.rank_member(leaderboard_key_for(us), best)

                # compute time and set
                time = model.objects.filter(user=us)
                if time.count() > 0:
                    time_played = time.aggregate(Sum('stat_time_secs'))['stat_time_secs__sum']
                    lb_time.rank_member(leaderboard_key_for(us), time_played)

                count += 1
