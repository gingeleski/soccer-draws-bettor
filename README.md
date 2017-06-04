# Soccer Draws Bettor

An autonomous soccer betting system for Nitrogen Sports. At the core is a hypothesis that match draws are disliked and resultingly underestimated.

## Setup

```
# this is setup for windows, adjust for your os appropriately

git clone --recursive https://github.com/gingeleski/soccers-draws-bettor.git
cd soccers-draws-bettor
virtualenv venv

# activate the virtualenv, below is how for powershell
.\venv\scripts\activate.ps1

pip install -r nitrogen-sports-api\requirements.txt
pip install -r requirements.txt

python soccer_draws_bettor.py
```

You'll need to edit the file at `soccer-draws-bettor/modules/SystemParameters.py` to use your Nitrogen Sports username and password. Tweak other parameters as you like.

### Run (fresh start)

This is the default way to run, initializing a clean database, log, and state.

```
# for windows, adjust for your os appropriately

cd soccer-draws-bettor

# activate the virtualenv, below is how for powershell
.\venv\scripts\activate.ps1

python .\run.py
```

### Run (loading a previous state)

`TODO`

This functionality is not yet implemented. Eventually this should be able to start from a "pickle" (previous state) for the sake of fault tolerance.
