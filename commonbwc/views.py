from blazeweb.views import View


class BadRequestError(View):
    def default(self):
        self.status_code = 400
        self.render_template()


class AuthError(View):
    def default(self):
        self.status_code = 401
        self.render_template()


class Forbidden(View):
    def default(self):
        self.status_code = 403
        self.render_template()


class NotFoundError(View):
    def default(self):
        self.status_code = 404
        self.render_template()


class SystemError(View):
    def default(self):
        self.status_code = 500
        self.render_template()
