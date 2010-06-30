from blazeweb.globals import user
from blazeweb.views import View, asview
from commonbwp.lib.views import CrudBase, FormMixin

import cbwptestapp.forms as forms
import cbwptestapp.model.orm as orm
from plugstack.datagrid.lib import DataGrid, Col, DateTime
from plugstack.sqlalchemy import db

class FormTest1(View, FormMixin):
    def setup_view(self):
        self.form_init(forms.NameForm)

    def form_assign_defaults(self):
        self.form.els.email.defaultval = 'foo@example.com'

    def form_on_valid(self):
        if not self.form.els.email.value:
            raise ValueError('email is empty')
        return 'Hello %s' % self.form.els.name.value

    def form_on_cancel(self):
        return 'cancelled'

    def form_on_invalid(self):
        return 'invalid'

class FormTest2(View, FormMixin):
    def setup_view(self, cancel_type=None):
        self.form_init(forms.NameForm)
        if cancel_type == 'url':
            self.cancel_url = '/somewhere'
        elif cancel_type == 'endpoint':
            self.cancel_endpoint = 'FormTest1'

    def form_on_valid(self):
        if not self.form.els.email.value:
            raise ValueError('email is empty')
        user.add_message('notice', 'Hello %s' % self.form.els.name.value)

class WidgetCrud(CrudBase):

    def init(self):
        CrudBase.init(self, 'Widget', 'Widgets', forms.WidgetForm, orm.Widget)
        self.allow_anonymous = True

    def manage_init_grid(self):
        dg = DataGrid(
            db.sess.execute,
            per_page=30,
            class_='dataTable manage'
            )
        dg.add_col(
            'id',
            orm.Widget.id,
            inresult=True
        )
        dg.add_tablecol(
            Col('Actions',
                extractor=self.manage_action_links,
                width_th='8%'
            ),
            orm.Widget.id,
            sort=None
        )
        dg.add_tablecol(
            Col('Type'),
            orm.Widget.widget_type,
            filter_on=True,
            sort='both'
        )
        dg.add_tablecol(
            Col('Color'),
            orm.Widget.color,
            filter_on=True,
            sort='both'
        )
        dg.add_tablecol(
            Col('Quantity'),
            orm.Widget.quantity,
            filter_on=True,
            sort='both'
        )
        dg.add_tablecol(
            DateTime('Created'),
            orm.Widget.createdts,
            filter_on=True,
            sort='both'
        )
        dg.add_tablecol(
            DateTime('Last Updated'),
            orm.Widget.updatedts,
            filter_on=True,
            sort='both'
        )
        return dg

class WidgetCrudDeletePerm(WidgetCrud):

    def init(self):
        WidgetCrud.init(self)
        self.delete_protect = True
        self.delete_require_any = 'widget-delete'

@asview('/')
def home_page():
    return user.get_messages()
    