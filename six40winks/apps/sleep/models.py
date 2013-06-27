import datetime
from datetime import datetime

from django.db import models
from django.utils import timezone



class SleepPhase(models.Model):
    '''describes the smallest differentiated unit of sleep. 
    It can be as small as 5mn recorded by zeo, or as long
    as 8h recorded by hand'''
    
    sleep_phase = models.PositiveIntegerField('Sleep Phase', help_text='0=undefined, 1=wake, 2=rem, 3=light,4=deep, 5=general sleep, 6=snooze')
    date_bin = models.DateField('date bin')
    # day which contains the nap. We define the day from Day1 12:00 (noon) to Day 2 12:00 (noon).
    # start_dt may be in Day1 or Day2, but if it's in Day2 it can't go beyond 12:00
    # if it does, a new episode will be defined inside Day3.

    start_dt = models.DateTimeField('start of sleep phase')
    # this is the start datetime of the nap/sleep episode
    # it should be in the local time of the place where the nap happened

    end_dt = models.DateTimeField('end of sleep phase')
    # this is the end datetime of the nap/sleep episode
    
    comments = models.TextField('comments on sleep phase', null=True, blank=True)

    class Meta:
        ordering =['start_dt']

    def __unicode__(self):
        fmt = '%Y/%m/%d (%H:%M:%S)'
        formatted_start_dt=self.start_dt.strftime(fmt)
        sleep_phase_dic={0:"undefined", 1: "awake", 2: "rem", 3: "light-sleep", 4: "deep-sleep", 5: "in-bed", 6:"snooze"}

        # if self.total_sleep:
        #     total_sleep = int(self.total_sleep)/60 #in minutes
        # else:
        #     total_sleep = len(base_hypnogram)*30/60 #in minutes
        the_phase = sleep_phase_dic[self.sleep_phase]
        duration = self.end_dt - self.start_dt
        return '%s -- %s -> %s' % (formatted_start_dt, duration, the_phase) # maybe we can make it 2012-03-26_18:00_20mn_nap


    def sleep_phase_name(self):
        sleep_phase_dic={0:"undefined", 1: "awake", 2: "rem", 3: "light-sleep", 4: "deep-sleep", 5: "in-bed", 6:"snooze"}
        return sleep_phase_dic[self.sleep_phase]

    def phase_duration(self):
        duration = self.end_dt - self.start_dt
        return duration



class SleepDay(models.Model):
    '''Contains an Overview of the sleep amount during
    a day (defined from noon of 1st day to noon of 2nd day'''
    date_bin = models.DateField('date bin')
    total_sleep = models.PositiveIntegerField('Total Sleep', help_text='Total hours of sleep in a day', null=True, blank = True)
    rem_sleep = models.PositiveIntegerField('REM Sleep', help_text='Total hours of REM sleep in a day', null=True, blank = True)
    light_sleep = models.PositiveIntegerField('Light Sleep', help_text='Total hours of Light sleep in a day', null=True, blank = True)
    deep_sleep = models.PositiveIntegerField('Deep Sleep', help_text='Total hours of Light sleep in a day', null=True, blank = True)

    class Meta:
        ordering =['date_bin']

    def __unicode__(self):
        return '%s -- %sh' % (self.date_bin, self.total_sleep)

    
    




    # def save(self, *args, **kwargs):
    #     ''' defines all the sleep episode characteristics
    #     based on the base_hypnogram when we save a model instance'''

    #     # count all ocurrences of 2,3,4,5. (0,1 are not sleep!)
    #     # and multiply by 30 sec. and divide by 60 sec. to get the minutes
    #     self.total_sleep = (self.base_hypnogram.count('2')+ self.base_hypnogram.count('3')+ self.base_hypnogram.count('4')+ self.base_hypnogram.count('5'))*30/60

    #     self.time_in_rem = self.base_hypnogram.count('2')*30/60 # in minutes

    #     self.time_in_light = self.base_hypnogram.count('3')*30/60 # in minutes

    #     self.time_in_deep = self.base_hypnogram.count('4')*30/60 # in minutes

    #     self.time_in_sleep = self.base_hypnogram.count('5')*30/60 # in minutes

    #     i = 1
    #     while (self.base_hypnogram[i] == '0' or self.base_hypnogram[i] == '1'):
    #         i += 1 # count how many 11001100 we have before falling asleep
    #     time_to_sleep = (i-1) # *30/60  # in minutes
    #     self.time_to_sleep = (i-1)*30/60

    #     return super(SleepEpisode, self).save(*args,**kwargs)
        
