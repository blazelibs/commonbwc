from blazeweb.config import ComponentSettings


class Settings(ComponentSettings):

    def init(self):
        #######################################################################
        # ERROR DOCUMENTS
        #######################################################################
        self.app_settings.error_docs[400] = 'common:BadRequestError'
        self.app_settings.error_docs[401] = 'common:AuthError'
        self.app_settings.error_docs[403] = 'common:Forbidden'
        self.app_settings.error_docs[404] = 'common:NotFoundError'
        self.app_settings.error_docs[500] = 'common:SystemError'
