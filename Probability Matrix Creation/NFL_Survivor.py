# NFL Survivor Fantasy Football Probability Matrix Creation Code
# Written By: Marco Bornstein
# Date Finalized: 9/3/2017
import csv
from math import *
# from gurobipy import *


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
        csv_writer = csv.writer(csv_file, delimiter=",")
        for row in data_matrix:
            csv_writer.writerow(list(row))


def normcdf(x, mu, sigma):
    # Norm CDF Code
    t = x-mu
    y = 0.5*erfc(-t/(sigma*sqrt(2.0)))
    if y > 1.0:
        y = 1.0
    return y


def normpdf(x, mu, sigma):
    # Norm PDF Code
    u = (x-mu)/abs(sigma)
    y = (1/(sqrt(2*pi)*abs(sigma)))*exp(-u*u/2)
    return y


def normdist(x, mu, sigma, f):
    # Norm Distribution Code
    if f:
        y = normcdf(x, mu, sigma)
    else:
        y = normpdf(x, mu, sigma)
    return y


# For Marco (if Marco, Leave Uncommented)
marco_filename_elo = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Elo Rankings All Weeks.csv'
marco_filename_home_away = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Home Away.csv'
marco_filename_schedule = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\2016 Schedule.csv'
marco_filename_spreads_thur = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\Thursday Night Spreads Week 1.csv'
marco_filename_spreads_sun = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\Sunday Spreads Week 1.csv'
marco_filename_spreads_mon = r'C:\Users\marco_000\Documents\Survivor Football Research\2016 Data\Monday Night Spreads Week 1.csv'
# Import in Elo, Vegas Spreads, Team Schedule, and Home/Away CSV file data
Elo_Rankings = read_csv(marco_filename_elo)
Home_Away = read_csv(marco_filename_home_away)
Schedule = read_csv(marco_filename_schedule)
Spreads = read_csv(marco_filename_spreads_thur)

# For Rangan (if Rangan, Leave Uncommented)
# rangan_filename_elo = 0
# rangan_filename_home_away = 0
# rangan_filename_schedule = 0
# rangan_filename_spreads_thur = 0
# rangan_filename_spreads_sun = 0
# rangan_filename_spreads_mon = 0
# Elo_Rankings = read_csv(rangan_filename_elo)
# Home_Away = read_csv(rangan_filename_home_away)
# Schedule = read_csv(rangan_filename_schedule)
# Spreads = read_csv(rangan_filename_spreads_thurs)

# Initialize NFL Team List
nfl_teams = []
# Set Current Week for Optimization
current_week = 1
# Create List for Weekly Elo Rankings
weekly_elo_rankings = []
# Create Probabilities List
Probabilities = []

# Find the Elo Ranking for each team in the current week
for row_idx in range(len(Elo_Rankings)):
    elo_row = Elo_Rankings[row_idx]
    current_week_elo = elo_row[current_week+1]
    weekly_elo_rankings.append(current_week_elo)
weekly_elo_rankings.pop(0)

# Find the Spreads for Each NFL Match-up and the Corresponding Win % From Norm Distribution
# Compute the Weighted Average for Each Spread
spread_win_probabilities = []
for row1 in range(1, len(Spreads)):
    spread_row_fav = Spreads[row1]
    win_prob = 0
    counter = 0
    for spread in range(2, len(spread_row_fav)):
        if spread_row_fav[spread] == "":
            continue
        if float(spread_row_fav[spread]) == 0:
            win_prob += 0.5
            counter += 1
        elif abs(float(spread_row_fav[spread])) != float(spread_row_fav[spread]):
            game_prob1 = 1 - normdist(0.5, abs(float(spread_row_fav[spread])), 13.45, 'True')
            game_prob2 = 0.5*((normdist(0.5, abs(float(spread_row_fav[spread])), 13.45, 'True')) - (normdist(-0.5, abs(float(spread_row_fav[spread])), 13.45, 'True')))
            game_prob = game_prob1 + game_prob2
            win_prob += game_prob
            counter += 1
        elif abs(float(spread_row_fav[spread])) == float(spread_row_fav[spread]):
            game_prob1_inv = 1 - normdist(0.5, abs(float(spread_row_fav[spread])), 13.45, 'True')
            game_prob2_inv = 0.5 * ((normdist(0.5, abs(float(spread_row_fav[spread])), 13.45, 'True')) - (normdist(-0.5, abs(float(spread_row_fav[spread])), 13.45, 'True')))
            game_prob_inv = game_prob1_inv + game_prob2_inv
            game_prob = 1 - game_prob_inv
            win_prob += game_prob
            counter += 1
    spread_win_probabilities.append(win_prob/counter)
    nfl_teams.append(spread_row_fav[0])

Probabilities.append(spread_win_probabilities)
# Create List for Schedule
total_schedule = []
# Create List for Home Field Advantage
total_home_field = []

# Determine the Schedule for Each NFL Team, as Well as Home/Away for Each Matchup
for week_idx in range(current_week+1, 17):
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
# Add Initial Week Schedule & Home/Away Into Full Schedule List
cur_schedule = total_schedule[0]
cur_home = total_home_field[0]
# Create List for Elo Difference Between Teams From Vegas Spreads
spread_elo_diff = []
# Create List for Elo Difference Between Teams From FiveThirtyEight
elo_538_diff = []
count = 0

# Determine the Elo Difference Between Teams for Vegas & FiveThirtyEight
for item in spread_win_probabilities:
    elo_difference = (400*log((1/item)-1)/log(10))
    opponent_idx = int(cur_schedule[count])
    elo_diff_538 = int(weekly_elo_rankings[count]) - int(weekly_elo_rankings[opponent_idx-1])
    if int(cur_home[count]) == 1:
        elo_difference += (home_field_elo*int(cur_home[count]))
        count += 1
    else:
        elo_difference -= home_field_elo
        count += 1
    spread_elo_diff.append(elo_difference)
    elo_538_diff.append(elo_diff_538)

# Determine the Difference of the Difference (538 - Vegas) and Subtract That by the 538 Elo
# Thus, We Are Favoring the Vegas Spreads, and Adjusting the 538 Elo Ratings Accordingly
# The New Elo Ratings Are Our *Adjusted FiveThirtyEight Elo Ratings*
for number in range(len(spread_elo_diff)):
    difference = elo_538_diff[number] - (-1*spread_elo_diff[number])
    weekly_elo_rankings[number] = int(weekly_elo_rankings[number]) - (0.5*difference)

# Calculate the Future Win Probabilities for Each NFL Match-up
for i in range(1, len(total_schedule)):
    cur_week = total_schedule[i]
    cur_home_field = total_home_field[i]
    current_week_probabilities = []
    for j in range(len(total_schedule[i])):
        if cur_week[j] == "":
            win_probability = 'Bye Week'
            current_week_probabilities.append(win_probability)
            continue
        opponent_row = int(cur_week[j])
        team_elo_score = int(weekly_elo_rankings[j]) + (int(cur_home_field[j])*home_field_elo)
        opponent_elo_score = int(weekly_elo_rankings[opponent_row - 1]) + (int(cur_home_field[opponent_row - 1])*home_field_elo)
        win_probability = 1 / (1 + 10 ** ((opponent_elo_score - team_elo_score) / 400))
        current_week_probabilities.append(win_probability)
    Probabilities.append(current_week_probabilities)
# Temporarily Rounding Decimals
Rounded_Probabilities = []
for i in range(0, 4):
    wk_rounded = []
    wk_p = Probabilities[i]
    for element in range(0, len(wk_p)):
        if isinstance(wk_p[element], str):
            wk_rounded.append(0)
        else:
            wk_rounded.append(round(wk_p[element], 6))
    Rounded_Probabilities.append(wk_rounded)
# Flipped Probabilities for Shortest Path
Flipped_Probabilities = []
for j in range(0, 4):
    wk_flipped = []
    wk_f = Rounded_Probabilities[j]
    for element in range(0, len(wk_f)):
        if isinstance(wk_f[element], str):
            wk_flipped.append(1)
        else:
            wk_flipped.append(1 - round(wk_f[element], 6))
    Flipped_Probabilities.append(wk_flipped)

Flipped_Probabilities2 = []
for k in range(0, 6):
    wk_flipped2 = []
    wk_f2 = Probabilities[k]
    for element in range(0, len(wk_f2)):
        if isinstance(wk_f2[element], str):
            wk_flipped2.append(1)
        else:
            wk_flipped2.append(1 - round(wk_f2[element], 6))
    Flipped_Probabilities2.append(wk_flipped2)

# print('NFL Teams (Probabilities Listed in Same Order)')
# print(nfl_teams)
# print('Week 1')
# print(Rounded_Probabilities[0])
# print('Week 2')
# print(Rounded_Probabilities[1])
# print('Week 3')
# print(Rounded_Probabilities[2])
# print('Week 4')
# print(Rounded_Probabilities[3])

write_csv('Probability Matrix 2016 Weeks 1-4.csv', Rounded_Probabilities)
write_csv('Shortest Path (Flipped) Probability Matrix 2016 Weeks 1-4.csv', Flipped_Probabilities)
write_csv('Shortest Path (Flipped) Probability Matrix 2016 Weeks 1-6.csv', Flipped_Probabilities2)
