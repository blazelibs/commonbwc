from os import path

from blazeweb.config import DefaultSettings

basedir = path.dirname(path.dirname(__file__))
app_package = path.basename(basedir)

class Default(DefaultSettings):
    def init(self):
        self.dirs.base = basedir
        self.app_package = app_package
        DefaultSettings.init(self)

        self.init_plugins()
        self.init_routing()

        ################################################################
        # DATABASE
        #######################################################################
        self.db.url = 'sqlite://'
        self.db.echo = False

        #######################################################################
        # TEMPLATES
        #######################################################################
        self.template.admin = 'testing.html'

    def init_plugins(self):
        # application modules from our application or supporting applications
        self.add_plugin(app_package, 'common', 'commonbwp')
        self.add_plugin(app_package, 'sqlalchemy', 'sqlalchemybwp')
        self.add_plugin(app_package, 'auth', 'authbwp')
        self.add_plugin(app_package, 'datagrid', 'datagridbwp')

    def init_routing(self):
        self.add_route('/ft1', endpoint='FormTest1')
        self.add_route('/ft2', endpoint='FormTest2')
        self.add_route('/ft2/<cancel_type>', endpoint='FormTest2')
        self.add_route('/widget/<action>', endpoint='WidgetCrud')
        self.add_route('/widget/<action>/<int:objid>', endpoint='WidgetCrud')
        self.add_route('/widget-auth/<action>', endpoint='WidgetCrudDeletePerm')
        self.add_route('/widget-auth/<action>/<int:objid>', endpoint='WidgetCrudDeletePerm')

class Dev(Default):
    def init(self):
        Default.init(self)
        self.apply_dev_settings()

class Test(Default):
    def init(self):
        Default.init(self)
        self.apply_test_settings()
