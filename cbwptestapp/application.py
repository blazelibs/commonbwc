from os import path

from blazeweb.application import WSGIApp
from blazeweb.middleware import minimal_wsgi_stack
from blazeweb.scripting import application_entry
from sqlalchemybwp.lib.middleware import SQLAlchemyApp

import cbwptestapp.config.settings as settingsmod

def make_wsgi(profile='Dev'):
    app = WSGIApp(settingsmod, profile)
    app = SQLAlchemyApp(app)
    
    return minimal_wsgi_stack(app)

def script_entry():
    application_entry(make_wsgi)

if __name__ == '__main__':
    script_entry()
