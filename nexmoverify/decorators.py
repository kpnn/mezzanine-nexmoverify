from functools import wraps

from django.core.urlresolvers import reverse
from django.utils.decorators import available_attrs

from mezzanine.conf import settings

def phone_requred(function, add_phone_url=None):
    def user_phone(user):
        obj = UserPhone.get_by_user(user)
        if obj:
            return obj.phone
        return None

    @wraps(function, assigned=available_attrs(function))
    def _wrapped(request, *args, **kwargs):
        from django.contrib.auth.views import redirect_to_login
        if not request.user.is_authenticated():
            return redirect_to_login(next=request.path)
        phone = request.session.get('user_phone') or user_phone(request.user)
        if not phone:
            redirect_to = add_phone_url or reverse('add_phone') or settings.ADD_PHONE_URL
            return redirect_to_login(request.path, redirect_to, 'next')

        request.session['user_phone'] = phone
        return function(request, *args, **kwargs)

    return _wrapped
