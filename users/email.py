from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from users import utils


class ActivationEmail(BaseEmailMessage):
    '''
    Send an account activation email to the registered user
    '''
    template_name = "email/activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        url = "/activate/{uid}/{token}/"
        user = context.get("user")
        context['uid'] = utils.encode_url_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context['url'] = url.format(**context)
        return context


class ConfrimationEmail(BaseEmailMessage):
    '''
    Send confirmation email after user account is activated
    '''
    template_name = 'email/confirmation.html'
