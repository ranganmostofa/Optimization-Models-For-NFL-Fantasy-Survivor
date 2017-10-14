import csv
from math import *
import random as rand


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


marco_filename_elo = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Elo Rankings All Weeks.csv'
marco_filename_home_away = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Home Away.csv'
marco_filename_schedule = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Schedule.csv'

Elo_Rankings = read_csv(marco_filename_elo)
Home_Away = read_csv(marco_filename_home_away)
Schedule = read_csv(marco_filename_schedule)

week = 1


def nfl_simulation(current_week, elo_rankings, home_away, schedule):

    cur_week_elo = []
    for k in range(len(elo_rankings)):
        elo_row = elo_rankings[k]
        cur_week_elo.append(elo_row[current_week + 1])
    cur_week_elo.pop(0)

    total_schedule = []
    total_home_field = []

    # Determine the Schedule for Each NFL Team, as Well as Home/Away for Each Matchup
    for week_idx in range(current_week+1, 19):
        weekly_schedule = []
        weekly_home_field = []
        for row_idx in range(len(elo_rankings)):
            schedule_row = schedule[row_idx]
            home_field_row = home_away[row_idx]
            current_week_schedule = schedule_row[week_idx]
            current_week_home_field = home_field_row[week_idx]
            weekly_schedule.append(current_week_schedule)
            weekly_home_field.append(current_week_home_field)
        weekly_schedule.pop(0)
        weekly_home_field.pop(0)
        total_schedule.append(weekly_schedule)
        total_home_field.append(weekly_home_field)

    current_week_spreads = []
    home_field_elo = 57

    for j in range(len(total_schedule[current_week-1])):
        cur_week = total_schedule[current_week-1]
        cur_home_field = total_home_field[current_week-1]
        if cur_week[j] == "":
            spread = "Bye Week"
            current_week_spreads.append(spread)
            continue
        opponent_row = int(cur_week[j]) - 1
        team_elo_score = int(cur_week_elo[j])
        opponent_elo_score = int(cur_week_elo[opponent_row])
        team_elo_score += home_field_elo * int(cur_home_field[j])
        opponent_elo_score += home_field_elo * int(cur_home_field[opponent_row])
        spread = round((team_elo_score-opponent_elo_score)/12.5) / 2
        current_week_spreads.append(spread)

    point_differential = [0] * 32
    team_list = []
    win_loss = [0] * 32
    for i in range(len(current_week_spreads)):
        if i in team_list:
            continue
        cur_week = total_schedule[current_week - 1]
        opponent_row = int(cur_week[i]) - 1
        team_list.append(i)
        team_list.append(opponent_row)
        spread = current_week_spreads[i]
        if spread == "Bye Week":
            point_differential.append("Bye Week")
            continue
        game_result = round(rand.normalvariate(spread, 13.45))
        if game_result == 0:
            game_result = round(rand.normalvariate(spread, 13.45))
        if game_result > 0:
            win_loss[i] = 1
            win_loss[opponent_row] = 0
        else:
            win_loss[i] = 0
            win_loss[opponent_row] = 1
        point_differential[i] = game_result
        point_differential[opponent_row] = game_result * -1

    new_elo_rankings = []

    cur_week = total_schedule[current_week - 1]
    cur_home_field = total_home_field[current_week - 1]
    for j in range(len(point_differential)):
        opponent_row = int(cur_week[j]) - 1
        team_elo_score_og = int(cur_week_elo[j])
        opponent_elo_score_og = int(cur_week_elo[opponent_row])
        team_elo_score = team_elo_score_og + (home_field_elo * int(cur_home_field[j]))
        opponent_elo_score = opponent_elo_score_og + (home_field_elo * int(cur_home_field[opponent_row]))
        win_pct = 1 / (1 + 10 ** ((opponent_elo_score - team_elo_score) / 400))
        if point_differential[j] > 0:
            margin_multiplier = log(abs(point_differential[j])+1) * (2.2 / ((0.001 * (team_elo_score-opponent_elo_score)) + 2.2))
            ranking = round(team_elo_score_og + ((20 * margin_multiplier) * (1 - win_pct)))
        else:
            margin_multiplier = log(abs(point_differential[j]) + 1) * (2.2 / ((0.001 * (opponent_elo_score-team_elo_score)) + 2.2))
            ranking = round(team_elo_score_og + ((20 * margin_multiplier) * (-1*win_pct)))
        new_elo_rankings.append(ranking)

    return new_elo_rankings

nfl_simulation(week, Elo_Rankings, Home_Away, Schedule)