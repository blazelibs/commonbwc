from blazeweb.application import WSGIApp
from blazeweb.middleware import minimal_wsgi_stack
from blazeweb.scripting import application_entry

import commonbwc_ta.config.settings as settingsmod


def make_wsgi(profile='Dev'):
    app = WSGIApp(settingsmod, profile)
    return minimal_wsgi_stack(app)


def script_entry():
    application_entry(make_wsgi)


if __name__ == '__main__':
    script_entry()
