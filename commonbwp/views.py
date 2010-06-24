from pysmvt.utils import redirect
from pysmvt.views import SecureView

class FormMixin(object):

    def form_assign(self, formcls):
        self.form = self.formcls()
        self.assign_form_defaults()

    def post(self, *args, **kwargs):
        self.form_submission()
        self.default(*args, **kwargs)

    def assign_form_defaults(self):
        pass

    def form_submission(self):
        if self.form.is_cancel():
            self.form_on_cancel()
        if self.form.is_valid():
            try:
                self.form_on_valid()
                return
            except Exception, e:
                # if the form can't handle the exception, re-raise it
                if not self.form.handle_exception(e):
                    raise
                self.form_handled_exception()
        elif not self.form.is_submitted():
            # form was not submitted, nothing left to do
            return

        self.form_invalid()

    def form_on_valid(self):
        raise NotImplementedError('form_on_valid() must be defined in the main View')

    def form_on_invalid(self):
        self.form.assign_user_errors()

    def form_handled_exception(self):
        self.form.assign_user_errors()

    def form_on_cancel(self):
        redirect(self.get_cancel_url())

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        return url_for(self.cancel_endpoint)

    def default(self, *args, **kwargs):
        self.assign('form', self.form)
