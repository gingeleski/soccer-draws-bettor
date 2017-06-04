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
