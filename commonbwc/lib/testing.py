from blazeutils.strings import normalizews


def has_message(d, sev, message, container_id='user-messages'):
    for li in d('#%s ul li' % container_id):
        li = d.__class__(li)
        sev_wrapper = li.find('.sev-%s' % sev)
        if not sev_wrapper:
            continue
        if sev_wrapper.text() != sev:
            continue
        if normalizews(li.text()) == '%s: %s' % (sev, message):
            return True


def user_messages(d, container_id='user-messages'):
    messages = []
    for li in d('#%s ul li' % container_id):
        li = d.__class__(li)
        sev_wrapper = li.find('strong')
        messages.append((sev_wrapper.text(), li.text()))
    return messages
