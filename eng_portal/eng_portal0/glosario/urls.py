from django.conf.urls import url
from glosario import views

urlpatterns = [
    #url(r'^input/$', views.InputView.as_view(),name='inputting'),
    url(r'^$', views.index,name='index'),
    url(r'^glosario_list/$', views.enlistar,name='glosario_listing'),
    url(r'^create_entry/$', views.create_entry,name='create_entries'),
    url(r'^themes_list/$', views.enlistarTemas,name='themes_listing'),
    url(r'^create_themes/$', views.create_temas,name='create_themes'),
]
