def get_email(user):
    '''
    It returns the email addresss of user
    '''
    email_field_name = get_email_field_name(user)
    return getattr(user, email_field_name, None)


def get_email_field_name(user):
    '''
    It returns a user email field name
    '''
    return user.get_email_field_name()
