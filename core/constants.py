from environs import Env

env = Env()
env.read_env('.env')

BOOKERS_LIST=env.list('BOOKERS_LIST')
BETBOOM_ANY=env.str('BETBOOM_ANY')
BETCITY_ANY=env.str('BETCITY_ANY')
FONBET_ANY=env.str('FONBET_ANY')
LEON_ANY=env.str('LEON_ANY')
LIGASTAVOK_ANY=env.str('LIGASTAVOK_ANY')
MARATHON_ANY=env.str('MARATHON_ANY')
OLIMP_ANY=env.str('OLIMP_ANY')
WINLINE_ANY=env.str('WINLINE_ANY')