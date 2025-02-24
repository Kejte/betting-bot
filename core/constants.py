from environs import Env

env = Env()
env.read_env('.env')

DEFAULT_LINK = env.str('DEFAULT_LINK')