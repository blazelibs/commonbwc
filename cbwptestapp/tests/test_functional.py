from blazeweb.globals import ag
from blazeweb.testing import TestApp
from nose.tools import eq_

from authbwp.lib.testing import login_client_with_permissions
from commonbwp.lib.testing import has_message
from plugstack.sqlalchemy import db
from cbwptestapp.model.orm import Widget

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

class TestCrud(object):
    @classmethod
    def setup_class(cls):
        cls.ta = TestApp(ag.wsgi_test_app)

    def create_widget(self, widget_type, color, quantity):
        w = Widget(widget_type=widget_type, color=color, quantity=quantity)
        db.sess.add(w)
        db.sess.commit()
        return w

    def test_add(self):
        r = self.ta.get('/widget/add/999999', status=400)
        
        r = self.ta.get('/widget/add')
        d = r.pyq
        eq_(d('form:first').attr('id'), 'widget-form', r)
        assert d('h2').text() == 'Add Widget'
        assert d('form#widget-form').attr.action == '/widget/add'
        assert d('span#widget-form-cancel a').attr.href == '/widget/manage'

        r.form['widget_type'] = 'Type A'
        r.form['color'] = 'silver'
        r = r.form.submit('submit', status=200)
        assert '/widget/add' in r.request.url
        
        r.form['quantity'] = '87'
        r = r.form.submit('submit', status=302)        
        assert '/widget/add' in r.request.url
        r = r.follow(status=200)
        assert '/widget/manage' in r.request.url

    def test_edit(self):
        r = self.ta.get('/widget/edit', status=404)
        r = self.ta.get('/widget/edit/999999', status=404)
    
        w_id = self.create_widget(u'edit_test_widget', u'black', 150).id
        r = self.ta.get('/widget/edit/%s'%w_id)
        d = r.pyq
        eq_(d('form:first').attr('id'), 'widget-form', r)
        assert d('form#widget-form').attr.action == '/widget/edit/%s'%w_id
        assert d('h2').text() == 'Edit Widget'
        assert d('input[name="widget_type"]').val() == 'edit_test_widget'
        assert d('input[name="color"]').val() == 'black'
        assert d('input[name="quantity"]').val() == '150'

        r.form['quantity'] = '75'
        r = r.form.submit('submit', status=302)
        assert '/widget/edit/%s'%w_id in r.request.url
        r = r.follow(status=200)
        assert '/widget/manage' in r.request.url

        w = Widget.get(w_id)
        assert w.quantity == 75
        
    def test_manage(self):
        r = self.ta.get('/widget/manage/999999', status=400)
        r = self.ta.post('/widget/manage', status=400)
        
        w_id = self.create_widget(u'manage_test_widget', u'black', 150).id
    
        r = self.ta.get('/widget/manage?filteron=type&filteronop=eq&filterfor=manage_test_widget')
        d = r.pyq
        assert d('form#widget-form').html() is None
        assert d('h2:eq(0)').text() == 'Manage Widgets'
        assert d('p a').eq(0).attr.href == '/widget/add'
        assert d('a[href="/widget/edit/%s"]'%w_id).html() is not None
        assert d('a[href="/widget/delete/%s"]'%w_id).html() is not None

    def test_delete(self):
        r = self.ta.get('/widget/delete', status=404)
        r = self.ta.get('/widget/delete/999999', status=404)
        
        w_id = self.create_widget(u'delete_test_widget', u'black', 150).id
        r = self.ta.post('/widget/delete/%s'%w_id, status=400)
        r = self.ta.get('/widget/delete/%s'%w_id, status=302)
        assert '/widget/delete/%s'%w_id in r.request.url
        
        r = r.follow(status=200)
        assert '/widget/manage' in r.request.url
    
        w = Widget.get(w_id)
        assert w is None

    def test_bad_action(self):
        r = self.ta.get('/widget/badaction', status=404)
        r = self.ta.get('/widget/badaction/999999', status=404)

    def test_delete_protect(self):
        w_id = self.create_widget(u'delete_protect_test_widget', u'black', 150).id

        r = self.ta.get('/widget-auth/manage?filteron=type&filteronop=eq&filterfor=delete_protect_test_widget')
        d = r.pyq
        assert d('a[href="/widget-auth/edit/%s"]'%w_id).html() is not None
        assert d('a[href="/widget-auth/delete/%s"]'%w_id).html() is None
        r = self.ta.get('/widget-auth/delete/%s'%w_id, status=403)

        login_client_with_permissions(self.ta, u'widget-delete')
        r = self.ta.get('/widget-auth/manage?filteron=type&filteronop=eq&filterfor=delete_protect_test_widget')
        d = r.pyq
        assert d('a[href="/widget-auth/edit/%s"]'%w_id).html() is not None
        assert d('a[href="/widget-auth/delete/%s"]'%w_id).html() is not None
        r = self.ta.get('/widget-auth/delete/%s'%w_id, status=302)        
        self.ta.get('/users/logout')

class TestFormErrors(object):
    @classmethod
    def setup_class(cls):
        cls.ta = TestApp(ag.wsgi_test_app)

    def test_required(self):
        r = self.ta.get('/widget/add')
        r.form['widget_type'] = 'Type A'
        r.form['color'] = 'silver'
        r = r.form.submit('submit', status=200)
        d = r.pyq
        assert 'Quantity: field is required' in d('div#user_messages li:eq(0)').html()

    def test_maxlength(self):
        r = self.ta.get('/widget/add')
        r.form['widget_type'] = ''.join(['a' for i in range(260)])
        r.form['color'] = 'silver'
        r.form['quantity'] = 125
        r = r.form.submit('submit', status=200)
        d = r.pyq
        assert 'Type: Enter a value not greater than 255 characters long' in d('div#user_messages li:eq(0)').html()
    