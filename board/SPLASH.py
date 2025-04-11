from SPLASH_CMDS import args_dict, inputs_dict, app_dir_mapping
import re

def getSplashName(app: str):
    match = re.search(r'SPLASH4-(.+)$', app)
    if match:
        return match.group(1)
    return None

def getSplashArgs(app: str):
    splash_name = getSplashName(app)
    if splash_name in args_dict:
        return args_dict[splash_name]
    return []

def getSplashInput(app: str):
    splash_name = getSplashName(app)
    if splash_name in inputs_dict:
        return inputs_dict[splash_name]
    return None

def getSplashPath(app: str):
    splash_name = getSplashName(app)
    if splash_name in app_dir_mapping:
        return app_dir_mapping[splash_name]
    return None