# Optimization-Models-For-NFL-Fantasy-Survivor


The National Football League (NFL) has undoubtedly become the most popular sport in the U.S. In the past two years, the average TV audience for an NFL game was 17.9 million and 16.5 million respectively[1]. This extremely large interest in the NFL has created a huge market for football-related games. The market for all fantasy football games has been approximated at 70 billion dollars[2]. One major component of this market is the very popular Survivor Football competition. 
	
On espn.com, the Survivor Football game mode is named the  “Eliminator Challenge”. In only the first 34 largest public groups (there are thousands of groups), there are 470,000 members. Thus, it is without a doubt that there are well over one million people playing Survivor Football on ESPN alone. 

The large audience for Survivor Football coupled with the large market for fantasy football games has created many competitions with substantial monetary prizes for those successful at Survivor Football. Thus, discovering an algorithm to boost one’s likelihood of winning one of these competitions would be greatly sought after.

Survivor Football is a game where a player picks one NFL team per week to win its current matchup. The catch, however, is that over the course of the entire season, participants are not allowed to choose the same NFL team twice. While different competitions have different elimination settings, the goal in all competitions is to perfectly select a winning NFL team for all 17 weeks of the regular season.

With as many as 32 teams in the National Football League (NFL) and 17 weeks in the regular season, there are exactly 32!/(32 - 17)! possible pathways that a player can choose to follow, even when the aforementioned constraints have been taken into account. Due to these constraints and the goal of maximizing the number of winning picks while restricting the number of losing picks to a minimum, an optimization problem arises. There must now be an optimal path (with variables including strength of opponents in a matchup, location of the game, etc.) in selecting the correct team every week such that all constraints are satisfied. 






References:

1.	http://www.espn.com/nfl/story/_/id/18412873/nfl-tv-viewership-drops-average-8-percent-season
2.	https://www.forbes.com/sites/briangoff/2013/08/20/the-70-billion-fantasy-football-market/#4e9a7cc0755c
