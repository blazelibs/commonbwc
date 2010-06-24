from blazeweb.globals import ag
from blazeweb.testing import TestApp
from nose.tools import eq_

from commonbwp.lib.testing import has_message

class TestForm1(object):
    @classmethod
    def setup_class(cls):
        cls.ta = TestApp(ag.wsgi_test_app)

    def test_form_get(self):
        r = self.ta.get('/ft1')
        d = r.pyq
        eq_(d('form:first').attr('id'), 'name-form', r)
        eq_(d('#name-form-email').attr('value'), 'foo@example.com', r)

    def test_form_post(self):
        r = self.ta.get('/ft1')
        r.form['name'] = 'Fred'
        r = r.form.submit('submit')
        assert 'Hello Fred' == r.body, r

    def test_form_cancel(self):
        r = self.ta.get('/ft1')
        r = r.form.submit('cancel')
        assert 'cancelled' == r.body, r

    def test_form_invalid(self):
        r = self.ta.get('/ft1')
        r = r.form.submit('submit')
        assert 'invalid' == r.body, r

    def test_exception_handling(self):
        r = self.ta.get('/ft1')
        r.form['name'] = 'Fred'
        r.form['email'] = ''
        r = r.form.submit('submit')
        assert 'invalid' == r.body, r

class TestForm2(object):
    @classmethod
    def setup_class(cls):
        cls.ta = TestApp(ag.wsgi_test_app)

    def test_form_post(self):
        r = self.ta.get('/ft2')
        r.form['name'] = 'Fred'
        r.form['email'] = 'e'
        r = r.form.submit('submit')
        assert has_message(r.pyq, 'notice', 'Hello Fred')

    def test_form_cancel(self):
        r = self.ta.get('/ft2/url')
        r = r.form.submit('cancel')
        assert r.pyq('p a').attr.href == '/somewhere', r

        r = self.ta.get('/ft2/endpoint')
        r = r.form.submit('cancel')
        assert r.pyq('p a').attr.href == '/ft1', r

        r = self.ta.get('/ft2')
        r = r.form.submit('cancel')
        assert r.pyq('p a').attr.href == '/ft2', r

    def test_form_invalid(self):
        r = self.ta.get('/ft2')
        r = r.form.submit('submit')
        d = r.pyq
        assert d('#name-form-name-fw p.error').text() == '- field is required', r

    def test_exception_handling(self):
        r = self.ta.get('/ft2')
        r.form['name'] = 'Fred'
        r.form['email'] = ''
        r = r.form.submit('submit')
        assert has_message(r.pyq, 'error', 'Email: email is empty')
