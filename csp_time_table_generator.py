# INPUT_FILE = "input.csv"
# OUTPUT_FILE = "output.csv"


def read_data(file_name):

    with open(file_name, 'r') as file_in:

        text = file_in.read()
        lines = text.split('\n')

        data = []
        for line in lines:
            data.append(line.split(','))

    return data


def write_data(file_name, time_table, sub_count):

    write_str = ""
    count = 0

    for subject in time_table:

        sub_string = ""
        sub_string += subject + ',' + time_table[subject]["slot"] + ',' + time_table[subject]["room"]

        count += 1

        if count < sub_count:
            sub_string += '\n'

        write_str += sub_string

    with open(file_name, 'w') as file_out:
        file_out.write(write_str)


def form_time_table(time_slots, room_slots, time_table, sub_ind):

    global SUBJECTS, ROOMS

    if sub_ind == len(SUBJECTS):
        return True

    cur_sub = SUBJECTS[sub_ind]
    cur_sub_name = cur_sub[0]
    possible_slots = SUBJECTS[sub_ind][2:]

    if SUBJECTS[sub_ind][1] == 'c':

        for slot in possible_slots:

            if len(time_slots[slot]) == 0:

                time_slots[slot].append(SUBJECTS[sub_ind])

                selected_room = -1
                for room in room_slots:

                    if room_slots[room][slot] == -1:

                        room_slots[room][slot] = cur_sub
                        selected_room = room
                        break

                if selected_room == -1:
                    return False

                time_table[cur_sub_name]["slot"] = slot
                time_table[cur_sub_name]["room"] = selected_room

                if form_time_table(time_slots, room_slots, time_table, sub_ind + 1):
                    return True
                else:
                    time_slots[slot] = []
                    room_slots[selected_room][slot] = -1
                    time_table[cur_sub_name] = {'slot': -1, 'room': -1}

    else:

        for slot in possible_slots:

            if len(time_slots[slot]) == 0 or time_slots[slot][0][1] == 'o':

                time_slots[slot].append(SUBJECTS[sub_ind])

                selected_room = -1
                for room in room_slots:

                    if room_slots[room][slot] == -1:
                        room_slots[room][slot] = cur_sub
                        selected_room = room
                        break

                if selected_room == -1:
                    return False

                time_table[cur_sub_name]["slot"] = slot
                time_table[cur_sub_name]["room"] = selected_room

                if form_time_table(time_slots, room_slots, time_table, sub_ind + 1):
                    return True
                else:
                    time_slots[slot] = []
                    room_slots[selected_room][slot] = -1
                    time_table[cur_sub_name] = {'slot': -1, 'room': -1}


INPUT_FILE = input("Enter input file name: ")
OUTPUT_FILE = input("Enter output file name: ")

input_data = read_data(INPUT_FILE)

SUBJECTS = input_data[:-1]
ROOMS = input_data[-1]

time_slots = {}
room_slots = {}
time_table = {}

for sub in SUBJECTS:
    for slot in sub[2:]:

        if slot not in time_slots:
            time_slots[slot] = []

        for room in ROOMS:

            if room not in room_slots:
                room_slots[room] = {}

            if slot not in room_slots[room]:
                room_slots[room][slot] = -1

    time_table[sub[0]] = {"slot": -1, "room": -1}

result = form_time_table(time_slots, room_slots, time_table, 0)

if result:

    write_data(OUTPUT_FILE, time_table, len(SUBJECTS))

    for subject in time_table:
        print(subject, time_table[subject])
