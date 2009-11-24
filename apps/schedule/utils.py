import time, datetime

def subtract_time(day, end_time, start_time):
    # Without the date (essentially dummy), python
    # returns a tuple beyond the unix epoch.
    end_time_tuple   = time.strptime(unicode(day)+u" "+unicode(end_time),"%Y-%m-%d %H:%M:%S")
    start_time_tuple = time.strptime(unicode(day)+u" "+unicode(start_time),"%Y-%m-%d %H:%M:%S")
    end_time_float   = time.mktime(end_time_tuple)
    start_time_float = time.mktime(start_time_tuple)
    time_diff = end_time_float - start_time_float
    time_diff_float_in_hours = time_diff/3600.0
    return time_diff_float_in_hours

def add_time(day, end_time, start_time):
    num_slots = subtract_time(day,end_time,start_time) * 4
    gen_time_list = []
    gen_time = start_time
    for i in range(int(num_slots)+1):
        if gen_time <= end_time:
            gen_time_list.append(datetime.time(gen_time.hour, gen_time.minute).strftime("%H:%M"))
            gen_time_tuple  = time.strptime(unicode(day)+u" "+unicode(gen_time),"%Y-%m-%d %H:%M:%S")
            gen_time_float  = time.mktime(gen_time_tuple)
            # Add 900 seconds. Essentially for a 15 minute slot
            next_slot_float = gen_time_float + 900
            next_slot_tuple = time.localtime(next_slot_float)
            gen_time = datetime.time(next_slot_tuple.tm_hour,next_slot_tuple.tm_min)
    return gen_time_list
