import csv
from NFL_Simulation import nfl_simulation


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


marco_filename_elo = r'../Probability Matrix Inputs/2016/2016 Elo Rankings All Weeks.csv'
marco_filename_home_away = r'../Probability Matrix Inputs/2016/2016 Home Away.csv'
marco_filename_schedule = r'../Probability Matrix Inputs/2016/2016 Schedule.csv'

Elo_Rankings = read_csv(marco_filename_elo)
Home_Away = read_csv(marco_filename_home_away)
Schedule = read_csv(marco_filename_schedule)
Win_Total = 32 * [0]
week = 1
a = [1, 3, 4]
Weeks_Successful = []
Runs = []
for i in range(300):
    Results = nfl_simulation(week, Elo_Rankings, Home_Away, Schedule, [], [], Win_Total, 0, 1)
    check = Results[2]
    weeks_correct = len(check) - 1
    if len(check) == 17:
        if sum(check[16]) > 0:
            weeks_correct = 17
    Weeks_Successful.append(weeks_correct)
    print(i)

Runs.append(Weeks_Successful)
write_csv('NFL Simulations5.csv', Runs)
