import csv
from math import *


def read_csv(csv_filename):
    # Read CSV File
    """
    :param csv_filename:
    :return:
    """
    csv_matrix = []
    with open(csv_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            csv_matrix.append(list(row))
    return csv_matrix


def write_csv(csv_filename, data_matrix):
    # Write CSV
    """"
    :param csv_filename:
    :param data_matrix:
    :return:
    """
    with open(csv_filename, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", lineterminator="\n")
        for row in data_matrix:
            csv_writer.writerow(list(row))


# For Marco (if Marco, Leave Uncommented)
marco_filename_elo = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Elo Rankings All Weeks.csv'
marco_filename_home_away = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Home Away.csv'
marco_filename_schedule = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Schedule.csv'
Elo_Rankings = read_csv(marco_filename_elo)
Home_Away = read_csv(marco_filename_home_away)
Schedule = read_csv(marco_filename_schedule)

Probabilities = []

for week in range(17):
    # Set Current Week for Optimization
    current_week = week + 1
    # Create Probabilities List
    Week_Probabilities = []
    # Create List for Schedule
    total_schedule = []
    # Create List for Home Field Advantage
    total_home_field = []

    cur_week_elo = []

    for k in range(len(Elo_Rankings)):
        elo_row = Elo_Rankings[k]
        cur_week_elo.append(elo_row[current_week+1])
    cur_week_elo.pop(0)

    # Determine the Schedule for Each NFL Team, as Well as Home/Away for Each Matchup
    for week_idx in range(current_week+1, 19):
        weekly_elo = []
        weekly_schedule = []
        weekly_home_field = []
        for row_idx in range(len(Elo_Rankings)):
            schedule_row = Schedule[row_idx]
            home_field_row = Home_Away[row_idx]
            current_week_schedule = schedule_row[week_idx]
            current_week_home_field = home_field_row[week_idx]
            weekly_schedule.append(current_week_schedule)
            weekly_home_field.append(current_week_home_field)
        weekly_schedule.pop(0)
        weekly_home_field.pop(0)
        total_schedule.append(weekly_schedule)
        total_home_field.append(weekly_home_field)

    # Determined Home Field Elo Advantage is 57 Points (Process Explained Elsewhere)
    home_field_elo = 57
    for i in range(len(total_schedule)):
        cur_week = total_schedule[i]
        cur_home_field = total_home_field[i]
        current_week_probabilities = []
        for j in range(len(total_schedule[i])):
            if cur_week[j] == "":
                win_probability = 0.0000000000000000000000000000001
                current_week_probabilities.append(log(win_probability ** -1))
                continue
            opponent_row = int(cur_week[j]) - 1
            team_elo_score = int(cur_week_elo[j])
            opponent_elo_score = int(cur_week_elo[opponent_row])
            team_elo_score += home_field_elo * int(cur_home_field[j])
            opponent_elo_score += home_field_elo * int(cur_home_field[opponent_row])
            win_probability = 1 / (1 + 10 ** ((opponent_elo_score - team_elo_score) / 400))
            current_week_probabilities.append(log(win_probability ** -1))
        Week_Probabilities.append(current_week_probabilities)

    if len(Week_Probabilities) < 17:
        diff = 17 - len(Week_Probabilities)
        for n in range(diff):
            Week_Probabilities.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    Probabilities.append(Week_Probabilities)

# Print Out CSVs
title = 'Elo Log Probabilities 2016.csv'
for n in range(len(Probabilities)):
        week_num = 'Week ' + str(n+1) + ' '
        write_csv((week_num + title), Probabilities[n])
