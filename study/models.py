from django.db import models
from django.conf import settings
from django.urls import reverse

class VerseStudyEntry(models.Model):
    book_title = models.CharField(max_length=512)
    chapter = models.IntegerField()
    verse_number = models.IntegerField()
    verse_text = models.TextField()

    def __str__(self):
        return self.get_unique_key()

    def get_unique_key(self, book_only=False):
        if book_only:
            return "{book_title}".format(**vars(self))

        return "{book_title}:{chapter}:{verse_number}".format(**vars(self))

    def get_absolute_url(self):
        return reverse('verse-update', args=(self.id,))

class CompleteTheVerse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(help_text="Beware this date (UTC) is adjusted to CT upon calculation (-6) whether stat is in range of last sun 00:00 to last sat 23:59.")
    stat_time_secs = models.PositiveIntegerField()
    stat_grade_level = models.IntegerField()
    stat_total_correct = models.PositiveIntegerField()
    stat_total_questions = models.PositiveIntegerField()
    stat_stars = models.PositiveIntegerField()
    stat_score = models.PositiveIntegerField()
    current_best = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Complete The Verse"
        verbose_name_plural = "Complete The Verse"

    def __str__(self):
        return "%s --> date:%s gl:%s secs:%s correct:%s/%s " % (
            str(self.user),
            str(self.created),
            str(self.stat_grade_level),
            str(self.stat_time_secs),
            str(self.stat_total_correct),
            str(self.stat_total_questions),
        )

    # mark if current best at the current gradelevel
    def save(self, *args, **kwargs):
        super(CompleteTheVerse, self).save(*args, **kwargs)
        grade_level_pwp = CompleteTheVerse.objects.filter(user=self.user)
        prev = grade_level_pwp.filter(current_best=True)
        if prev.count() > 0:
            prev = prev[0]
            if prev.stat_score < self.stat_score:
                grade_level_pwp.update(current_best=False)
                self.current_best = True
                self.save()
        else:
            self.current_best = True
            self.save()

class NameTheBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(help_text="Beware this date (UTC) is adjusted to CT upon calculation (-6) whether stat is in range of last sun 00:00 to last sat 23:59.")
    stat_time_secs = models.PositiveIntegerField()
    stat_grade_level = models.IntegerField()
    stat_total_correct = models.PositiveIntegerField()
    stat_total_questions = models.PositiveIntegerField()
    stat_stars = models.PositiveIntegerField()
    stat_score = models.PositiveIntegerField()
    current_best = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Name The Book"
        verbose_name_plural = "Name The Book"

    def __str__(self):
        return "%s --> date:%s gl:%s secs:%s correct:%s/%s " % (
            str(self.user),
            str(self.created),
            str(self.stat_grade_level),
            str(self.stat_time_secs),
            str(self.stat_total_correct),
            str(self.stat_total_questions),
        )

    # mark if current best at the current gradelevel
    def save(self, *args, **kwargs):
        super(NameTheBook, self).save(*args, **kwargs)
        grade_level_pwp = NameTheBook.objects.filter(user=self.user)
        prev = grade_level_pwp.filter(current_best=True)
        if prev.count() > 0:
            prev = prev[0]
            if prev.stat_score < self.stat_score:
                grade_level_pwp.update(current_best=False)
                self.current_best = True
                self.save()
        else:
            self.current_best = True
            self.save()
