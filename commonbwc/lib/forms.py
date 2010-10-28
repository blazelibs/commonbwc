
from blazeform.form import Form as BlazeForm
from blazeform.util import NotGiven
from blazeutils.strings import case_cw2dash
from blazeweb.globals import rg, user
from blazeweb.routing import current_url
from blazeweb.utils import registry_has_object, werkzeug_multi_dict_conv

class Form(BlazeForm):
    note_prefix = '- '
    error_prefix = None
    req_note_level = 'section'
    req_note = None

    def __init__(self, name=None, auto_init=True, **kwargs):
        if name is None:
            name = case_cw2dash(self.__class__.__name__)
        if registry_has_object(rg):
            curl = current_url(strip_host=True)
        else:
            curl = ''
        action = kwargs.pop('action', curl)
        kwargs.setdefault('class_', 'generated')
        BlazeForm.__init__(self, name, action=action, **kwargs)
        self._request_submitted = False
        if auto_init:
            self.init()

    def assign_from_request(self, req):
        to_submit = werkzeug_multi_dict_conv(req.form)
        to_submit.update(req.files.to_dict())
        self.set_submitted(to_submit)

    def is_submitted(self):
        # don't want to repeat the assignment and is_submitted might be used
        # more than once
        if not self._request_submitted and not self._static:
            if registry_has_object(rg):
                self.assign_from_request(rg.request)
            self._request_submitted = True
        return BlazeForm.is_submitted(self)

    def assign_user_errors(self):
        # set the form error messages first
        for msg in self._errors:
            user.add_message('error', msg)
        # set element error messages
        for el in self.submittable_els:
            for msg in el.errors:
                user.add_message('error', '%s: %s' % (el.label, msg))

    def render(self, **kwargs):
        if self.note_prefix:
            kwargs.setdefault('note_prefix', self.note_prefix)
        if self.error_prefix:
            kwargs.setdefault('error_prefix', self.error_prefix)
        if self.req_note_level:
            kwargs.setdefault('req_note_level', self.req_note_level)
        if self.req_note:
            kwargs.setdefault('req_note', self.req_note)
        return BlazeForm.render(self, **kwargs)
