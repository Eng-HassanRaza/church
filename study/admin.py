from django.contrib import admin

from .models import VerseStudyEntry, CompleteTheVerse, NameTheBook

@admin.register(VerseStudyEntry)
class VerseStudyEntryAdmin(admin.ModelAdmin):
    list_display = ['book_title','chapter','verse_number',]
    search_fields = ['book_title',]

@admin.register(CompleteTheVerse)
class CompleteTheVerseAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = (
        "user",
        "created",
        "stat_grade_level",
        "stat_time_secs",
        "stat_total_correct",
        "stat_total_questions",
        "stat_score",
        "current_best",
    )
    list_filter = ("created",)
    readonly_fields = ("current_best",)

@admin.register(NameTheBook)
class NameTheBookAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = (
        "user",
        "created",
        "stat_grade_level",
        "stat_time_secs",
        "stat_total_correct",
        "stat_total_questions",
        "stat_score",
        "current_best",
    )
    list_filter = ("created",)
    readonly_fields = ("current_best",)
