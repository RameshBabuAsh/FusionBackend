from django.urls import include, re_path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'FPF'
urlpatterns = [
    # url used to add data
    re_path(r'^$', views.index, name='index'),
    # url(r'uploadcsv/$', views.upload_file),
    re_path(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    re_path(r'^profile/$', views.profile, name='profile'),

    re_path(r'^rspc_profile/$', views.rspc_profile, name='rspc_profile'),

    # #delete
    re_path(r'^achv/$', views.achievementDelete, name='achievement_delete'),
    re_path(r'^emp_confrence_organisedDelete/$', views.emp_confrence_organisedDelete, name='emp_confrence_organisedDelete'),
    re_path(r'^emp_consultancy_projectsDelete/$', views.emp_consultancy_projectsDelete, name='emp_consultancy_projectsDelete'),

    re_path(r'^emp_confrence_organisedDelete/$', views.emp_confrence_organisedDelete, name='emp_confrence_organisedDelete'),
    re_path(r'^emp_event_organizedDelete/$', views.emp_event_organizedDelete, name='emp_event_organizedDelete'),
    re_path(r'^emp_expert_lecturesDelete/$', views.emp_expert_lecturesDelete, name='emp_expert_lecturesDelete'),
    re_path(r'^emp_keynote_addressDelete/$', views.emp_keynote_addressDelete, name='emp_keynote_addressDelete'),
    re_path(r'^emp_mtechphd_thesisDelete/$', views.emp_mtechphd_thesisDelete, name='emp_mtechphd_thesisDelete'),
    re_path(r'^emp_patentsDelete/$', views.emp_patentsDelete, name='emp_patentsDelete'),
    re_path(r'^emp_published_booksDelete/$', views.emp_published_booksDelete, name='emp_published_booksDelete'),
    re_path(r'^emp_research_papersDelete/$', views.emp_research_papersDelete, name='emp_research_papersDelete'),
    re_path(r'^emp_research_projectsDelete/$', views.emp_research_projectsDelete, name='emp_research_projectsDelete'),
    re_path(r'^emp_session_chairDelete/$', views.emp_session_chairDelete, name='emp_session_chairDelete'),

    re_path(r'^emp_techtransferDelete/$', views.emp_techtransferDelete, name='emp_techtransferDelete'),
    re_path(r'^emp_visitsDelete/$', views.emp_visitsDelete, name='emp_visitsDelete'),
    re_path(r'^emp_consymDelete/$', views.emp_consymDelete, name='emp_consymDelete'),


    # # edit personal information
    re_path(r'^extra/$', views.view_all_extra_infos, name='extra'),
    re_path(r'^persinfo/$', views.persinfo, name='persinfo'),
    re_path(r'^journal/edit$', views.editjournal, name='editjournal'),
    re_path(r'^foreignvisit/edit$', views.editforeignvisit, name='editforeignvisit'),
    re_path(r'^indianvisit/edit$', views.editindianvisit, name='editindianvisit'),
    re_path(r'^consym/edit$', views.editconsym, name='editconsym'),
    re_path(r'^event/edit$', views.editevent, name='editevent'),
    re_path(r'^conference/edit$', views.editconference, name='editconference'),
    re_path(r'^books/edit$', views.editbooks, name='editbooks'),

    # # insert
    re_path(r'^pg/$', views.pg_insert, name='pg_insert'),
    re_path(r'^phd/$', views.phd_insert, name='phd_insert'),
    re_path(r'^fvisit/$', views.fvisit_insert, name='fvisit_insert'),
    re_path(r'^ivisit/$', views.ivisit_insert, name='ivisit_insert'),
    re_path(r'^journal/$', views.journal_insert, name='journal_insert'),
    re_path(r'^conference/$', views.conference_insert, name='conference_insert'),
    re_path(r'^book/$', views.book_insert, name='book_insert'),
    re_path(r'^consym/$', views.consym_insert, name='consym_insert'),
    re_path(r'^event/$', views.event_insert, name='event_insert'),
    re_path(r'^award/$', views.award_insert, name='award_insert'),
    re_path(r'^talk/$', views.talk_insert, name='talk_insert'),
    re_path(r'^chaired/$', views.chaired_insert, name='chaired_insert'),
    re_path(r'^keynote/$', views.keynote_insert, name='keynote_insert'),
    re_path(r'^project/$', views.project_insert, name='project_insert'),
    re_path(r'^consult_insert/$', views.consult_insert, name='consult_insert'),
    re_path(r'^patent_insert/$', views.patent_insert, name='patent_insert'),
    re_path(r'^transfer_insert/$', views.transfer_insert, name='transfer_insert'),

    # # generate report
    # url(r'^report/$', views.generate_report, name='generate_report'),
    # url(r'^rspc_report/$', views.rspc_generate_report, name='rspc_generate_report'),


]
