from datetime import datetime
from deadline.models import Deadline
from django.utils.functional import curry
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import ObjectDoesNotExist

def redirect(request, *args, **kwargs):
    expiration = kwargs.get('expiration', None)
    template_file = 'deadline/%s_expired.html' % expiration.code_name
    return render_to_response(template_file, 
                              {'expiry': expiration.expiry,
                               'descr' : expiration.descr},
                              context_instance = RequestContext(request))

def deadline_expired(code_name):
    def wrapped(func, *args, **kwargs):
        try:
            expiration = Deadline.objects.get(code_name = code_name)
        except ObjectDoesNotExist:
            return func
        if not datetime.now() > expiration.expiry:
            return func
        return curry(redirect, expiration = expiration)
    return wrapped
