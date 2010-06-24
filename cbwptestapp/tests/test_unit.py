from blazeweb.globals import ag
from blazeweb.testing import inrequest
from blazeweb.views import View

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
