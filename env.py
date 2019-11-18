import config
Env='test'
def env():
    if Env=='dev':
        return config.Test
    elif Env=='live':
        return config.Live
    else:
        return config.Test
    
