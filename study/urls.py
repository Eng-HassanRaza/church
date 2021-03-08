from django.urls import path, re_path, include
from django.conf.urls import handler404, handler500

from .views import (
    vsw_upload,
    vsw_browse,
    vsw_delete,
    VSWUpdateView,
    manage_scores,
    complete_the_verse,
    ctv_report,
    ctv_get_word,
    name_the_book,
    ntb_report,
)

urlpatterns = [
    path("verse-upload/", vsw_upload, name="verse-upload"),
    path("verse-browse/", vsw_browse, name="verse-browse"),
    path("verse-delete/<int:pk>/", vsw_delete, name="verse-delete"),
    path("verse-update/<int:pk>/",  VSWUpdateView.as_view(), name="verse-update"),

    path("manage-scores/", manage_scores, name="manage-scores"),

    path("complete-the-verse/", complete_the_verse, name="complete-the-verse"),
    path("ctv-get-word/",ctv_get_word, name="ctv-get-word"),
    path("ctv-report/",ctv_report, name="ctv-report"),
    path("name-the-book/", name_the_book, name="name-the-book"),
    path("ntb-report/", ntb_report, name="ntb-report"),
]

