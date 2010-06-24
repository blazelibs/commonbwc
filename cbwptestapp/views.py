from blazeweb.globals import user
from blazeweb.views import View
from commonbwp.lib.views import FormMixin

from cbwptestapp.forms import NameForm

class FormTest1(View, FormMixin):
    def setup_view(self):
        self.form_init(NameForm)

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
        self.form_init(NameForm)
        if cancel_type == 'url':
            self.cancel_url = '/somewhere'
        elif cancel_type == 'endpoint':
            self.cancel_endpoint = 'FormTest1'

    def form_on_valid(self):
        if not self.form.els.email.value:
            raise ValueError('email is empty')
        user.add_message('notice', 'Hello %s' % self.form.els.name.value)
