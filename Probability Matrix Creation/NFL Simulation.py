import csv
from math import *
import random as rand
from GraphConstructor import GraphConstructor
from heap_dijkstra import dijkstra
from collections import defaultdict
from SimulationWinProbability import probability


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
Win_Total = 32 * [0]
week = 1


def nfl_simulation(current_week, elo_rankings, home_away, schedule, selected_teams, season_elo, win_total):
    cur_week_elo = []
    for k in range(len(elo_rankings)):
        elo_row = elo_rankings[k]
        cur_week_elo.append(elo_row[current_week + 1])
    cur_week_elo.pop(0)
    season_elo.append(cur_week_elo)

    total_schedule = []
    total_home_field = []

    # Determine the Schedule for Each NFL Team, as Well as Home/Away for Each Match-up
    for week_idx in range(2, 19):
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

    P = probability(cur_week_elo, home_away, schedule, current_week)
    NUM_TEAMS = 32
    START_NODE = "S"
    TERMINAL_NODE = "T"
    TERMINAL_WEIGHT = 0.00
    START_WEEK = current_week
    if current_week < 15:
        NUM_WEEKS = 4
    else:
        NUM_WEEKS = current_week - 4
    selected_nodes = selected_teams
    node_set = set(range(1, 1 + NUM_TEAMS)).difference(selected_nodes)
    G = GraphConstructor.build_graph(defaultdict(lambda: defaultdict(float)), P,
                                     tuple([START_NODE]), tuple([TERMINAL_NODE]), TERMINAL_WEIGHT, START_WEEK, node_set,
                                     NUM_WEEKS)
    dist, prev = dijkstra(G, tuple([START_NODE]))
    #selected_teams.append(dist[1])
    print(dist)

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
        spread = current_week_spreads[i]
        if spread == "Bye Week":
            team_list.append(i)
            point_differential[i] = "Bye Week"
            win_loss[i] = 0
            continue
        if i in team_list:
            continue
        cur_week = total_schedule[current_week - 1]
        opponent_row = int(cur_week[i]) - 1
        team_list.append(i)
        team_list.append(opponent_row)
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
        if point_differential[j] == "Bye Week":
            new_elo_rankings.append(int(cur_week_elo[j]))
            continue
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

    print(cur_week_elo)

    for item in range(len(win_loss)):
        win_total[item] += win_loss[item]
    if current_week == 17:
        return season_elo, win_total
    else:
        for i in range(1, len(elo_rankings)):
            teams = elo_rankings[i]
            teams[current_week+2] = new_elo_rankings[i-1]
        next_week = current_week + 1
        nfl_simulation(next_week, elo_rankings, home_away, schedule, selected_teams, season_elo, win_total)
        return season_elo, win_total

Season_Elo = nfl_simulation(week, Elo_Rankings, Home_Away, Schedule, [], [], Win_Total)

print(Season_Elo[1])

