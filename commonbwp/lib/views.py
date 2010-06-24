from blazeweb.routing import url_for, current_url
from blazeweb.utils import redirect
from blazeweb.views import SecureView

class FormMixin(object):

    def form_init(self, formcls):
        self._cancel_url = None
        self.cancel_url = None
        self.cancel_endpoint = None
        self.form = formcls()
        self.form_assign_defaults()

    def post(self, *args, **kwargs):
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
            except Exception, e:
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

    def _get_cancel_url(self):
        if self._cancel_url:
            return self._cancel_url
        if self.cancel_endpoint:
            return url_for(self.cancel_endpoint)
        return current_url(strip_host=True)
    def _set_cancel_url(self, url):
        self._cancel_url = url
    cancel_url = property(_get_cancel_url, _set_cancel_url)

    def default(self):
        return self.form_default_action()

    def form_default_action(self):
        self.assign('form', self.form)
        self.render_template()
