import appdirs
import toml
import os

appname = 'MusicTk'

def create():
    try:
        directory = appdirs.user_data_dir(appname)
        os.makedirs(directory)
    except FileExistsError:
        pass
    
    return directory

def write():
    path = appdirs.user_data_dir(appname)
    
    toml_string = """
[app]
app = "MusicTk"

    [app.settings]
    theme = "light"
    path = ""
    last_song_idx = 0
    last_song_name = ""
    ismini = false
"""
    parsed_toml = toml.loads(toml_string)
    with open(path+'/settings.toml', 'w') as f:
        toml.dump(parsed_toml, f)

def read():
    path = appdirs.user_data_dir(appname)
    try:
        toml.load(path+'/settings.toml')['app']['settings']
    except KeyError:
        write()
    
    app = toml.load(path+'/settings.toml')['app']
    settings = app['settings']
    
    return settings['theme'],settings['path'],settings['last_song_idx'],settings['last_song_name'],settings['ismini'] 
    
def save(theme,path,idx,name,ismini):
    path_dir = appdirs.user_data_dir(appname)
    
    data = toml.load(path_dir+'/settings.toml')
    app = data['app']
    settings = app['settings']
    settings['theme']  = theme
    settings['ismini'] = ismini
    settings['last_song_idx'] = idx
    settings['last_song_name'] = name   
    if path: settings['path'] = path

    with open(path_dir+'/settings.toml','w',encoding='utf-8') as f:
        toml.dump(data,f)   
