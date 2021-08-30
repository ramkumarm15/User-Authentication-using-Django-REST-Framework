from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode



def encode_url_uid(pk):
    '''
    It converts a user id to binary term by using base64_encoding
    '''
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_url_uid(pk):
    ''' 
    It decodes the binary term of user id to user id by using base64_decoding
    '''
    return force_str(urlsafe_base64_decode(pk))
