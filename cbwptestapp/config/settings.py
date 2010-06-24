from os import path

from blazeweb.config import DefaultSettings

basedir = path.dirname(path.dirname(__file__))
app_package = path.basename(basedir)

class Default(DefaultSettings):
    def init(self):
        self.dirs.base = basedir
        self.app_package = app_package
        DefaultSettings.init(self)

        self.add_plugin(app_package, 'common', 'commonbwp')

    def init_routing(self):
        self.add_route('/ft1', endpoint='FormTest1')

class Dev(Default):
    def init(self):
        Default.init(self)
        self.apply_dev_settings()

class Test(Default):
    def init(self):
        Default.init(self)
        self.apply_test_settings()
