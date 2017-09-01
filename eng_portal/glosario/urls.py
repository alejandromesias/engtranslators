from django.conf.urls import url
from glosario import views

urlpatterns = [
    #url(r'^input/$', views.InputView.as_view(),name='inputting'),
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^glosary_search/$', views.GlosarySearchView.as_view(),name='glosary_search'),
    url(r'^entry_list/$', views.EntriesListView.as_view(),name='entry_list'),
    url(r'^entry_list/(?P<pk>[-\w]+)/$', views.EntriesDetailView.as_view(),name='entry_detail'),
    url(r'^chapters_list/$', views.ChaptersListView.as_view(),name='chapters_list'),
    url(r'^chapters_list/(?P<chapter>[-\w\s]+)/$', views.ThemesInChapterView.as_view(),name='chapter_detail'),
    url(r'^chapters_list/(?P<chapter>[-\w\s]+)/(?P<theme>[-\w\s]+)/$', views.EntriesInThemeView.as_view(),name='theme_detail'),
    url(r'^create_english_entry/$', views.EntryCreateView.as_view(),name='entry_create'),
    url(r'^entry_list/update/(?P<pk>[-\w]+)/$', views.EntryUpdateView.as_view(),name='entry_update'),
    url(r'^chapter_create/$', views.ChapterCreateView.as_view(),name='chapter_create'),
    url(r'^theme_create/$', views.ThemeCreateView.as_view(),name='theme_create'),
]
