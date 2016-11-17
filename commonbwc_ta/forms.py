from commonbwc.lib.forms import Form


class NameForm(Form):
    def init(self):
        self.add_text('name', 'Name', required=True)
        el = self.add_text('email', 'Email')
        el.add_handler('email is empty')
        self.add_submit('submit')
        self.add_cancel('cancel')
