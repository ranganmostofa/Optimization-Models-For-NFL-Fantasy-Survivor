from math import *


def probability(week_elo, home_away, schedule, week):
    probabilities = []
    # Create Probabilities List
    week_probabilities = []
    # Create List for Schedule
    total_schedule = []
    # Create List for Home Field Advantage
    total_home_field = []

    # Determine the Schedule for Each NFL Team, as Well as Home/Away for Each Match-up
    for week_idx in range(week + 1, 19):
        weekly_schedule = []
        weekly_home_field = []
        for row_idx in range(len(home_away)):
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
                team_elo_score = int(week_elo[j])
                opponent_elo_score = int(week_elo[opponent_row])
                team_elo_score += home_field_elo * int(cur_home_field[j])
                opponent_elo_score += home_field_elo * int(cur_home_field[opponent_row])
                win_probability = 1 / (1 + 10 ** ((opponent_elo_score - team_elo_score) / 400))
                current_week_probabilities.append(log(win_probability ** -1))
            week_probabilities.append(current_week_probabilities)
    probabilities.append(week_probabilities)
    return probabilities
