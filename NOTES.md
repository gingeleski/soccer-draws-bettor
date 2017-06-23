Planned refactor / redesign notes 6-4-2017

### SoccerDrawsBettor.py
- Main module, the "brain" that orchestrates everything
- Should be able to write out a "pickle" of state, in case of failure and we need to resume

### MatchEvaluator.py
- Returns None or information on a suitable match to bet
- "Dumb" module, not storing any information

### ResultEvaluator.py
- Returns WIN, LOSS, PUSH, or PENDING
- "Dumb" module, not storing any information
	
### BettingAnalyzer.py
- Stores transaction information in a table, can give stats and next amount to bet
- Writes out soccer_action_{date}_{time}.db

---

Notes dump 6-3-2017

After the bet is placed, hit

/php/query/mywagers.php

find a bet where result is "Pending" and get the bet_id

Take the cutoffDateTime, add 90 minutes to it, and that's when the first check to see if it's still pending will occur

After that, checking every 9 minutes

---

Notes dump 6-4-2017

/php/query/betslip_confirm.php
	data (array of objects)
	    {
		bet (array of objects)
                    {
			bet_id=123
		    }
             }

/php/query/mywagers.php
("data" has only pending results, looks like... "data_graded" has the finals)
	data (array of objects)
	    {
		bet (array of objects)
                    {
			bet_id=123
		    }
             }

if it was a loss, log the net profit as -1 * wager_value
if it was a win, log net profit as wager_to_win

---

First find_upcoming_games, then cache all the results of the various soccer leagues

---

6/23/2017

- Update account balance after a result has been obtained
- Betting Analyzer should record starting balance, keep some basic statistics
