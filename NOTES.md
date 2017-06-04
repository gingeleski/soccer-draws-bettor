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