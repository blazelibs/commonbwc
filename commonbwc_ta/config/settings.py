from os import path

from blazeweb.config import DefaultSettings

basedir = path.dirname(path.dirname(__file__))
app_package = path.basename(basedir)


class Default(DefaultSettings):
    def init(self):
        self.dirs.base = basedir
        self.app_package = app_package
        DefaultSettings.init(self)

        self.init_routing()

        self.add_component(app_package, 'common', 'commonbwc')

        self.template.default = 'layout.html'

    def init_routing(self):
        self.add_route('/ft1', endpoint='FormTest1')
        self.add_route('/ft2', endpoint='FormTest2')
        self.add_route('/ft2/<cancel_type>', endpoint='FormTest2')
        self.add_route('/ectest/<int:errorcode>', endpoint='ErrorViews')


class Dev(Default):
    def init(self):
        Default.init(self)
        self.apply_dev_settings()


class Test(Default):
    def init(self):
        Default.init(self)
        self.apply_test_settings()
