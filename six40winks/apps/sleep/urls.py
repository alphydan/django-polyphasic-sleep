from django.conf.urls import patterns, url

from sleep.views import SleepDayView, SleepOverView

urlpatterns = patterns('',
    # Example: /2012/nov/10/
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$',
        SleepDayView.as_view(),
        name="sleep_day"),
    url(r'^$', SleepOverView.as_view(), name="sleep_overview"),
    # url(r'^s/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$',
    #     SleepSDayView.as_view(),
    #     name="sleep_sday"),

)