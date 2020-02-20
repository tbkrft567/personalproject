from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.startSeason),
    url(r'^renderNewSeason$', views.renderNewSeason),
    url(r'^(?P<seasonNum>\d+)$', views.nextSeason),
    url(r'^Homepage$', views.index),
    url(r'^updateWeek$', views.updateWeek),
    url(r'^simEntireSeason$', views.simEntireSeason),
    url(r'^seeGame$', views.seeGame),
    url(r'^simGame$', views.simGame),
    url(r'^seeSchedule/(?P<teamId>\d+)$', views.seeSchedule),
    url(r'^refreshSchedule$', views.refreshSchedule),
    url(r'^seeStandings$', views.seeStandings),
    url(r'^generateSeason$', views.generateSchedule),
    url(r'^seeRoster/(?P<teamId>\d+)$', views.seeRoster),
    url(r'^refreshRoster$', views.refreshRoster),
    url(r'^recruits$', views.recruits),
    url(r'^seePlayoffs$', views.seePlayoffs),

]