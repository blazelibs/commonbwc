from plugstack.auth.model.actions import permission_update

def action_30_perms():
    permission_update(None, name=u'widget-delete', _ignore_unique_exception=True)
