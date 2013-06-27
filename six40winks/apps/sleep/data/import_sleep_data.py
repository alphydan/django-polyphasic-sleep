import os
import csv
import datetime as dti
from sleep.models import SleepPhase




def datetime_from_string(datetime_string):
    """ return datetime object from UTC datetime string
    Arguments:
    - `datetime_string`:
    """
    if len(str(datetime_string)) == 19: # 2011-12-11 02:30:00 format
        dt = dti.datetime.strptime(str(datetime_string), '%Y-%m-%d %H:%M:%S')
    elif len(str(datetime_string)) == 25: # 2011-12-11 02:30:00+00:00 format
        datetime_string = datetime_string[0:-6]
        dt = dti.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    else:
        print "your date is in an unknwown format"
        print "please use 2011-12-11 02:30:00+00:00 or 2011-12-11 02:30:00"
    return dt




def load_sleep_data():
    '''load the sleep data into the model'''

    curpath = os.path.abspath(os.curdir)
    full_dir_to_file = os.path.join(curpath, 'six40winks/apps/sleep/data/all_sleep_phases.csv')
    # full_dir_to_file = os.path.join(curpath, 'all_sleep_phases.csv')
    InputCSVFile = full_dir_to_file

    fiin= open(InputCSVFile,'rb') #open to read "r" in binary mode "b"
    reader = csv.reader(fiin, delimiter=',') #create a CSV reader object
    # AllSignalNames = reader.next() #get the first line
    # print AllSignalNames

    for i,row  in enumerate(reader):
        if True:
            sleep_bit = SleepPhase()
            # problem: if the period starts on the same day
            # before mid-day and ends on the same day after mid-day
            # these are different days according to our convention
            # and so 2 different entries will have to be done
            start_time = datetime_from_string(row[1])
            end_time = datetime_from_string(row[2])

            if start_time.day == end_time.day and start_time.month == end_time.month:
                # they cross the mid-day line
                mid_day = dti.datetime(start_time.year, start_time.month, start_time.day, 12, 0,0)
                if start_time < mid_day  and end_time > mid_day:
                    sleep_bit.sleep_phase = int(row[0])
                    sleep_bit.date_bin =  dti.date(start_time.year, start_time.month, start_time.day)
                    sleep_bit.start_dt = start_time
                    sleep_bit.end_dt = mid_day

                    sleep_bit.save()
                    
                    extra_sleep_bit = SleepPhase()
                    extra_sleep_bit.sleep_phase = int(row[0])
                    extra_sleep_bit.date_bin =  dti.date(end_time.year, end_time.month, end_time.day)
                    extra_sleep_bit.start_dt = mid_day
                    extra_sleep_bit.end_dt = end_time
                    extra_sleep_bit.save()

                else: # same day and month, not crossing the mid-day line
                    sleep_bit.sleep_phase = int(row[0])
                    sleep_bit.date_bin =  dti.date(start_time.year, start_time.month, start_time.day)
                    sleep_bit.start_dt = start_time
                    sleep_bit.end_dt = end_time
                    sleep_bit.save()
            
            else:
                sleep_bit.sleep_phase = int(row[0])
                sleep_bit.date_bin =  dti.date(start_time.year, start_time.month, start_time.day)
                sleep_bit.start_dt = start_time
                sleep_bit.end_dt = end_time

                sleep_bit.save()
                

                    
def create_sleep_days():
    first_date = SleepPhase.objects.order_by('date_bin')[0]
    last_date = SleepPhase.objects.order_by('-date_bin')[0]
    
    print first_date.date_bin, last_date.date_bin
    i_year = first_date.date_bin.year
    i_month = first_date.date_bin.month
    i_day =  first_date.date_bin.day

    
    experiment_length = last_date.date_bin - first_date.date_bin
    for d in range(experiment_length.days):
        given_day = dti.datetime(i_year, i_month, i_day, 12,0,0) + dti.timedelta(days = d)
        first_mid_day = dti.datetime( given_day.year, given_day.month, given_day.day, 12, 0,0)
        second_mid_day = dti.datetime( given_day.year, given_day.month, given_day.day, 12, 0,0) + dti.timedelta(days =1)
        phases_in_day = SleepPhase.objects.filter( start_dt__gte = first_mid_day, end_dt__lte = second_mid_day)
        
        #  Calculate Total/REM/Deep/Light Sleep
        day_sleep_duration = dti.timedelta(0,0,0)
        day_rem_duration = dti.timedelta(0,0,0)
        day_light_duration = dti.timedelta(0,0,0)
        day_deep_duration = dti.timedelta(0,0,0)

        for x in phases_in_day:
            if x.sleep_phase > 1: # and x.sleep_phase <6:
                # it's either wake, rem, light, deep or general sleep
                day_sleep_duration += x.phase_duration()
                if x.sleep_phase == 2:
                    day_rem_duration += x.phase_duration()
                if x.sleep_phase == 3:
                    day_light_duration += x.phase_duration()
                if x.sleep_phase == 4:
                    day_deep_duration += x.phase_duration()

        print [given_day, format_duration(day_sleep_duration)]


def format_duration(t_delta):
    if t_delta == dti.timedelta(0,0,0):
        total_sleep_duration_formatted = 'Unknown'
    else:
        td_hours, td_minutes =  t_delta.seconds//3600, (t_delta.seconds//60)%60
        total_sleep_duration_formatted = '%02dh %02dmn' % (td_hours, td_minutes)
    return total_sleep_duration_formatted

    
    

    






