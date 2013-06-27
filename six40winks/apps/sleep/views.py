# python imports
import datetime

# django imports
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic import DayArchiveView


# six40winks imports
from sleep.models import SleepPhase

# class SleepDayView(DayArchiveView):
#     queryset = SleepPhase.objects.all()
#     date_field = "date_bin"
#     make_object_list = True
#     allow_future = True
#     context_object_name = 'sleep_episodes'
#     month_format = '%m' 
    
#     def get_context_data(self, **kwargs):
#         context = super(SleepDayView, self).get_context_data(**kwargs)
#         # context.update(**kwargs)

#         day_sleep_duration = datetime.timedelta(0,0,0)
#         print day_sleep_duration, '\n'
#         for x in kwargs['object_list']:
#             print x.phase_duration()
#             if x.sleep_phase > 1 and x.sleep_phase <6:
#                 # it's either wake, rem, light, deep or general sleep
#                 day_sleep_duration += x.phase_duration()
#                 print day_sleep_duration, '\n'

#         # print self.year, self.month, self.day
#         # print self.date_field
#         return context        # self.publisher = get_object_or_404(Publisher, name=self.args[0])
#         # return Book.objects.filter(publisher=self.publisher)


def format_duration(t_delta):
    if t_delta == datetime.timedelta(0,0,0):
        total_sleep_duration_formatted = 'Unknown'
    else:
        td_hours, td_minutes =  t_delta.seconds//3600, (t_delta.seconds//60)%60
        total_sleep_duration_formatted = '%02dh %02dmn' % (td_hours, td_minutes)
    return total_sleep_duration_formatted



class SleepOverView(TemplateView):
    template_name = 'pages/sleep/sleep_overview.html'
    model = SleepPhase

    def get_day_duration(self, **kwargs):
        #  Calculate Total/REM/Deep/Light Sleep
        day_sleep_duration = datetime.timedelta(0,0,0)
        day_rem_duration = datetime.timedelta(0,0,0)
        day_light_duration = datetime.timedelta(0,0,0)
        day_deep_duration = datetime.timedelta(0,0,0)

        list_of_durations = []
        for x in SleepPhase.objects.all(): #kwargs['object_list']:
            if x.sleep_phase > 1: # and x.sleep_phase <6:
                # it's either wake, rem, light, deep or general sleep
                day_sleep_duration += x.phase_duration()
                if x.sleep_phase == 2:
                    day_rem_duration += x.phase_duration()
                if x.sleep_phase == 3:
                    day_light_duration += x.phase_duration()
                if x.sleep_phase == 4:
                    day_deep_duration += x.phase_duration()
                
                list_of_durations.append([day_sleep_duration, day_rem_duration, day_light_duration, day_deep_duration])
        print list_of_durations
        return list_of_durations

    def get_context_data(self, **kwargs):
        return {'list_of_durations': self.get_day_duration()}




class SleepDayView(ListView): 
    template_name = 'pages/sleep/sleep_day.html'
    context_object_name = 'sleep_episodes'
    
    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        day = int(self.kwargs['day'])

        first_mid_day = datetime.datetime( year, month, day, 12, 0,0)
        second_mid_day = datetime.datetime( year, month, day, 12, 0,0) + datetime.timedelta( days =1)
        queryset = SleepPhase.objects.filter( start_dt__gte = first_mid_day, end_dt__lte = second_mid_day)
        return queryset 

    def get_context_data(self, **kwargs):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        day = int(self.kwargs['day'])

        
        #  Calculate Total/REM/Deep/Light Sleep
        day_sleep_duration = datetime.timedelta(0,0,0)
        day_rem_duration = datetime.timedelta(0,0,0)
        day_light_duration = datetime.timedelta(0,0,0)
        day_deep_duration = datetime.timedelta(0,0,0)

        for x in kwargs['object_list']:
            if x.sleep_phase > 1: # and x.sleep_phase <6:
                # it's either wake, rem, light, deep or general sleep
                day_sleep_duration += x.phase_duration()
                if x.sleep_phase == 2:
                    day_rem_duration += x.phase_duration()
                if x.sleep_phase == 3:
                    day_light_duration += x.phase_duration()
                if x.sleep_phase == 4:
                    day_deep_duration += x.phase_duration()


        context = super(SleepDayView, self).get_context_data(**kwargs)
        context['date'] = datetime.date( year, month, day)

        
        context['total_sleep'] = format_duration(day_sleep_duration)
        context['total_rem'] = format_duration(day_rem_duration)
        context['total_light'] = format_duration(day_light_duration)
        context['total_deep'] = format_duration(day_deep_duration)
        
        return context
