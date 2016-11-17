from blazeweb.globals import ag
from blazeweb.testing import TestApp
from nose.tools import eq_

from commonbwc.lib.testing import has_message


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
        assert b'Hello Fred' == r.body, r

    def test_form_cancel(self):
        r = self.ta.get('/ft1')
        r = r.form.submit('cancel')
        assert b'cancelled' == r.body, r

    def test_form_invalid(self):
        r = self.ta.get('/ft1')
        r = r.form.submit('submit')
        assert b'invalid' == r.body, r

    def test_exception_handling(self):
        r = self.ta.get('/ft1')
        r.form['name'] = 'Fred'
        r.form['email'] = ''
        r = r.form.submit('submit')
        assert b'invalid' == r.body, r


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
        assert d('#name-form-name-fw p.error').text() == 'field is required', r

    def test_exception_handling(self):
        r = self.ta.get('/ft2')
        r.form['name'] = 'Fred'
        r.form['email'] = ''
        r = r.form.submit('submit')
        assert has_message(r.pyq, 'error', 'Email: email is empty')


class TestErrorCodes(object):

    @classmethod
    def setup_class(cls):
        cls.ta = TestApp(ag.wsgi_test_app)

    def test_400(self):
        r = self.ta.get('/ectest/400', status=400)
        assert '<h1>Bad Request Error Encountered</h1>' in r

    def test_401(self):
        r = self.ta.get('/ectest/401', status=401)
        assert '<h1>Authorization Error Encountered</h1>' in r

    def test_403(self):
        r = self.ta.get('/ectest/403', status=403)
        assert '<h1>Forbidden Error Encountered</h1>' in r

    def test_404(self):
        r = self.ta.get('/ectest/404', status=404)
        assert '<h1>404 Not Found Error Encountered</h1>' in r

    def test_500(self):
        r = self.ta.get('/ectest/500', status=500)
        assert '<h1>Application Error Encountered</h1>' in r
