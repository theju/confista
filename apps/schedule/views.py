from talk.models import Talk
from talk.views import render
from schedule.models import Slot, Day, Hall
from schedule.utils import add_time, subtract_time

def get_schedule(queryset_day, queryset_hall, queryset_slots):
    halls = queryset_hall
    days = queryset_day
    day_count = days.count()
    hall_count = halls.count()
    slots = queryset_slots

    temp_list = []
    for i in range(hall_count):
        temp_list.append((halls[i].id, i))
    hall_dict = dict(temp_list)

    temp_list = []
    for i in range(day_count):
        temp_list.append((days[i].id, i))
    day_dict = dict(temp_list)
    # Initialization of all matrix elements to 0
    schedule_matrix = []
    for day in days:
        time_intervals = add_time(day.date,
                                  day.end_time,
                                  day.start_time)
        # Minimum talk duration is 15mins, hence multiplier is 4.
        total_rows = len(time_intervals)
        row_list = []
        for i in range(total_rows):
            col_list = []
            for j in range(hall_count):
                col_list.append(0)
            row_list.append((time_intervals[i], col_list))
        schedule_matrix.append((day, row_list))

    # Assigning talk_id to matrix
    for slot in slots:
        if day_count == 1:
            num_of_rows = len(schedule_matrix[0])
        else:
            num_of_rows = len(schedule_matrix[slot.day.id - 1])
        # Time slot the talk falls in and number of slots occupied
        num_slots_for_talk = int(subtract_time(slot.day.date,
                                               slot.end_time,
                                               slot.start_time) * 4) 
        num_of_rows_from_first_row = int(subtract_time(slot.day.date,
                                                       slot.start_time,
                                                       slot.day.start_time) * 4)
        for i in range(num_slots_for_talk):
            # This is for the rowspan thingie.
            if i == 0:
                if day_count == 1:
                    schedule_matrix[0][1][num_of_rows_from_first_row + i][1][0] = ([slot, num_slots_for_talk],)
                else:
                    schedule_matrix[day_dict[slot.day.id]][1]\
                                   [num_of_rows_from_first_row + i][1]\
                                   [hall_dict[slot.hall.id]] = ([slot, num_slots_for_talk],)
            else:
                if day_count == 1:
                    schedule_matrix[0][1][num_of_rows_from_first_row + i][1][0] = 1
                else:
                    schedule_matrix[day_dict[slot.day.id]][1]\
                                   [num_of_rows_from_first_row + i][1]\
                                   [hall_dict[slot.hall.id]] = 1
    return (halls, hall_count, slots, schedule_matrix)

    
def display_schedule(request):
    halls, hall_count, slots, schedule_matrix = get_schedule(Day.objects.all(),
                                                             Hall.objects.all().order_by('id'),
                                                             Slot.objects.all())

    return render(request, 'schedule/display_schedule.html', 
                  {"halls": halls,
                   "hall_count": hall_count,
                   "slots": slots,
                   "schedule_data": schedule_matrix,
                   })

def display_schedule_by_hall(request, day, hall):
    halls, hall_count, slots, schedule_matrix = get_schedule(Day.objects.filter(id=day),
                                                             Hall.objects.filter(id=hall),
                                                             Slot.objects.filter(
                                                             Q(hall__id=hall) & Q(day__id=day)))

    return render(request, 'schedule/display_schedule.html',
                  {"halls": halls,
                   "hall_count": hall_count,
                   "slots": slots,
                   "schedule_data": schedule_matrix,
                   })
