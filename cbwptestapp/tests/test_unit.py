from StringIO import StringIO
from blazeweb.globals import ag
from blazeweb.testing import inrequest
from blazeweb.views import View
from blazeweb.wrappers import Request

from commonbwp.lib.forms import Form as CommonForm
from commonbwp.lib.views import FormMixin

class TestForms(object):

    @inrequest('/')
    def test_view(self):

        class FormTest(View):
            def default(self):
                return 'foo'

        ft = FormTest({}, 'formtest')
        r = ft.process()
        assert r.data == 'foo', r.data

#class TestForm(object):

    @classmethod
    def setup_class(cls):
        class TestForm(CommonForm):
            def init(self):
                self.add_text('name_first', 'First name', maxlength=30)
                self.add_file('txtfile', 'Text File')
        cls.Form = TestForm

    def test_with_no_request_object(self):
        f = self.Form()
        assert not f.is_submitted()

    @inrequest()
    def test_auto_form_submit(self):
        # setup the request, which will bind to the app's rg.request
        # which should result in the form values getting submitted
        Request.from_values(
            {
            'name_first': 'bob',
            'txtfile': (StringIO('my file contents'), 'test.txt'),
            'test-form-submit-flag': 'submitted'},
            bind_to_context=True
            )
        # test the form
        f = self.Form()
        assert f.is_submitted()
        assert f.is_valid()
        assert f.name_first.value == 'bob'
        assert f.txtfile.value.file_name == 'test.txt'
        assert f.txtfile.value.content_type == 'text/plain'
