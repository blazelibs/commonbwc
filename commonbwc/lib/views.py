from blazeweb.globals import settings, user
from blazeweb.routing import url_for, current_url
from blazeweb.utils import redirect, abort
from blazeweb.views import SecureView
from formencode.validators import String
from webhelpers2.html import literal
from webhelpers2.html.tags import link_to
from werkzeug.utils import cached_property

try:
    from sqlalchemy.exc import IntegrityError
except ImportError:
    class IntegrityError(Exception):
        pass


class FormMixin(object):

    def form_init(self, formcls):
        self._cancel_url = None
        self.cancel_url = None
        self.cancel_endpoint = None
        self.form_assign(formcls)

    def form_assign(self, formcls):
        self.form = formcls()
        self.form_assign_defaults()

    def post(self):
        retval = self.form_submission()
        if retval is None:
            self.form_default_action()
        return retval

    def form_assign_defaults(self):
        pass

    def form_submission(self):
        if self.form.is_cancel():
            return self.form_on_cancel()
        if self.form.is_valid():
            try:
                return self.form_on_valid()
            except Exception as e:
                # if the form can't handle the exception, re-raise it
                if not self.form.handle_exception(e):
                    raise
        elif not self.form.is_submitted():
            # form was not submitted, nothing left to do
            return

        return self.form_on_invalid()

    def form_on_valid(self):
        raise NotImplementedError('form_on_valid() must be defined in the main View')

    def form_on_invalid(self):
        self.form.assign_user_errors()

    def form_on_cancel(self):
        redirect(self.cancel_url)

    @property
    def cancel_url(self):
        if self._cancel_url:
            return self._cancel_url
        if self.cancel_endpoint:
            return url_for(self.cancel_endpoint)
        return current_url(strip_host=True)

    @cancel_url.setter
    def cancel_url(self, url):
        self._cancel_url = url

    def default(self):
        return self.form_default_action()

    def form_default_action(self):
        self.assign('form', self.form)
        self.render_template()


class GridMixin(object):
    gridcls = None
    grid_sheet_name = None
    grid_endpoint = None

    def grid_apply_overrides(self):
        pass

    def grid_init(self):
        # gridcls can be a grid class, or another callable that returns a grid instance
        self.grid = grid = self.gridcls()

        # apply query string arguments first, so webgrid handles its own stuff
        grid.apply_qs_args()

        # separate method for allowing customization of filters. A lot of this can be done via
        #   default filters in webgrid itself, but sometimes a column's filter depends on another
        #   column, or something similar
        self.grid_apply_overrides()

        # if the request is for an XLS export, short-circuit the process here and return
        if grid.export_to == 'xls':
            grid.xls.as_response(sheet_name=self.grid_sheet_name)

        return grid

    def default(self):
        self.grid_init()
        self.assign('grid', self.grid)
        if self.grid_endpoint:
            self.render_endpoint(self.grid_endpoint)
        self.render_template()


class CrudMixin(FormMixin, GridMixin):
    # self.action may be referenced by these integers
    MANAGE = 1
    EDIT = 2
    DELETE = 3
    ADD = 4

    def init(self, objname, objnamepl, formcls, ormcls, gridcls=None):
        # the view supports datagridbwc for backwards compatibility, but if webgrid is passed or
        # set on the view, it will be used accordingly
        self.objname = objname
        self.objnamepl = objnamepl
        self.formcls = formcls
        self.form = None
        self.ormcls = ormcls
        self.gridcls = gridcls
        self.objinst = None
        self.form_auto_init = True

        # templating and endpoints
        self.extend_from = settings.template.admin
        if not gridcls:
            self.manage_template_endpoint = 'common:crud_manage.html'
        else:
            self.manage_template_endpoint = 'common:crud_manage_webgrid.html'
        self.addedit_template_endpoint = 'common:crud_addedit.html'
        self.delete_template_endpoint = 'common:crud_delete.html'

        # special auth for deletes?
        self.delete_protect = False
        self.delete_require_any = []
        self.delete_require_all = []

        # messages that will normally be ok, but could be overriden
        self.manage_title = 'Manage %(objnamepl)s'
        self.add_title = 'Add %(objname)s'
        self.edit_title = 'Edit %(objname)s'

        self.add_processor('session_key', String)

    @property
    def use_form(self):
        return self.action in (self.ADD, self.EDIT)

    def auth_post(self, action=None, objid=None, session_key=None):
        self.session_key = session_key
        if action == 'manage' or action is None:
            self.action = self.MANAGE
            if objid:
                abort(400)
        elif action == 'edit':
            self.action = self.EDIT
            if not objid:
                abort(404)  # objid was not given
        elif action == 'add':
            self.action = self.ADD
            if objid:
                abort(400)
        elif action == 'delete':
            self.action = self.DELETE
            if not objid:
                abort(404)
            if not self.delete_is_authorized:
                abort(403)
        else:
            abort(404)

        self.objid = objid
        if objid:
            self.objinst = self.ormcls.get(objid)
            if not self.objinst:
                abort(404)

        if self.use_form:
            self.form_init(self.formcls)

    @cached_property
    def delete_is_authorized(self):
        return not self.delete_protect or \
            self.auth_calculate_any_all(self.delete_require_any, self.delete_require_all)

    def form_init(self, formcls):
        FormMixin.form_init(self, formcls)
        self.cancel_url = url_for(self.endpoint, action='manage', session_key=self.session_key)

    def post(self):
        if not self.use_form:
            abort(400)
        FormMixin.post(self)

    def manage_action_links(self, row):
        idc = self.ormcls.__table__.c.id
        edit_link = link_to('(edit)', url_for(self.endpoint, action='edit', objid=row[idc]),
                            class_='edit_link', title='edit %s' % self.objname)
        if self.delete_is_authorized:
            return literal('%s%s') % \
                (link_to('(delete)', url_for(self.endpoint, action='delete', objid=row[idc]),
                         class_='delete_link', title='delete %s' % self.objname),
                 edit_link)
        else:
            return literal(edit_link)

    def manage_assign_vars(self):
        dg = self.manage_init_grid()
        if not self.gridcls:
            # pull the datagrid html right now.  This keeps Jinja from hiding
            # attribute errors in our code
            dg.html_table
            self.assign('datagrid', dg)
        else:
            self.assign('grid', dg)
        self.assign('pagetitle', self.manage_title % {'objnamepl': self.objnamepl})
        self.assign('endpoint', self.endpoint)
        self.assign('objectname', self.objname)
        self.assign('objectnamepl', self.objnamepl)
        self.assign('extend_from', self.extend_from)
        self.assign('session_key', self.session_key)

    def manage_init_grid(self):
        return self.grid_init()

    def form_assign(self, formcls):
        self.form = formcls(auto_init=self.form_auto_init)
        if self.form_auto_init:
            self.form_assign_defaults()

    def form_assign_defaults(self):
        if self.action == self.EDIT:
            self.form.set_defaults(self.objinst.to_dict())

    def form_assign_vars(self):
        self.assign('form', self.form)
        self.assign('extend_from', self.extend_from)
        if self.action == self.ADD:
            self.assign('form_action', 'add')
            pagetitle = self.add_title % {'objname': self.objname}
        else:
            self.assign('form_action', 'edit')
            pagetitle = self.edit_title % {'objname': self.objname}
        self.assign('pagetitle', pagetitle)

    def form_default_action(self):
        self.form_assign_vars()
        self.render_endpoint(self.addedit_template_endpoint)

    def form_on_valid(self):
        self.form_save_data()
        self.form_when_completed()

    def form_save_data(self):
        if self.action == self.ADD:
            self.form_resulting_entity = self.form_orm_add()
            user.add_message('notice', '%s added successfully' % self.objname)
        else:
            self.form_resulting_entity = self.form_orm_edit()
            user.add_message('notice', '%s edited successfully' % self.objname)

    def form_when_completed(self):
        redirect(url_for(self.endpoint, action='manage', session_key=self.session_key))

    def form_orm_add(self):
        return self.ormcls.add(**self.form.get_values())

    def form_orm_edit(self):
        return self.ormcls.edit(self.objid, **self.form.get_values())

    def default(self):
        if self.action == self.MANAGE:
            self.manage_assign_vars()
            self.render_endpoint(self.manage_template_endpoint)
        elif self.use_form:
            self.form_default_action()
        else:
            self.delete_record()

    def delete_record(self):
        try:
            if self.ormcls.delete(self.objid):
                user.add_message('notice', '%s deleted successfully' % self.objname)
            else:
                user.add_message('warning',
                                 'could not delete, the %s no longer existed' % self.objname)
        except IntegrityError:
            user.add_message('warning', 'could not delete, the %s is in use' % self.objname)

        self.delete_when_completed()

    def delete_when_completed(self):
        redirect(url_for(self.endpoint, action='manage', session_key=self.session_key))


class CrudBase(SecureView, CrudMixin):
    pass
