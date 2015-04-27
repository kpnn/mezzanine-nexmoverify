###from functools import wraps
import re

from django.shortcuts import render, redirect
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, HttpResponseRedirect

from django.utils.http import is_safe_url, int_to_base36

#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.decorators import available_attrs

from mezzanine.conf import settings
from mezzanine.utils.models import get_user_model

from nexmoverify.models import UserPhone
from nexmoverify.countries import COUNTRY_CODES
from nexmoverify.nexmo_verify import NexmoVerify, NexmoException
from nexmoverify.decorators import phone_requred


try:
    ## Django <=1.7
    from django.contrib.formtools.wizard.views import SessionWizardView
except:
    ## Django 1.8
    from formtools.wizard.views import SessionWizardView

def get_nexmoverify():
    settings.use_editable()
    return NexmoVerify(api_key=settings.NEXMO_API_KEY,
                       api_secret=settings.NEXMO_API_SECRET,
                       brand=settings.NEXMO_BRAND)


def normlize_phone(phone):
    return re.sub(r'([,.+()\s\-]+)', '', phone)



class BaseForm(forms.Form):

    def __init__(self, wizard, **kwargs):
        super(BaseForm, self).__init__(**kwargs)
        self.wizard = wizard


class PhoneVerifyForm(BaseForm):

    country_code = forms.CharField(max_length=2, label=_('Select country'),
                              widget=forms.Select(choices=COUNTRY_CODES))
    
    phone = forms.CharField(min_length=4, max_length=16,
                            validators=[RegexValidator(regex=r'^[\d]{4,}$', message=_('Enter a valid phone number [Digits only]')),],
                            label=_('Please enter your phone number'))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        country = self.cleaned_data.get('country_code')
        self.wizard.verify_phone(phone, country)
        return phone
        

class PhoneCheckForm(BaseForm):
    code = forms.CharField(max_length=6,
                           validators=[RegexValidator(regex=r'^[\d]{4,6}$', message=_('Enter a valid phone number [Digits only]')),],
                           label=_('Enter your PIN'))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        self.wizard.check_phone(code)
        return code


class PhoneVerifyWizard(SessionWizardView):

    template_name = 'nexmoverify/addphone.html'

    def __init__(self,  **kwargs):
        super(PhoneVerifyWizard, self).__init__(**kwargs)

    def get_form_kwargs(self, step=None):
        return {'wizard': self}

    def render_done(self, form, **kwargs):
        """
        This method gets called when all forms passed.
        We do not need to re-validate all steps so we simply call 'done'.
        """
        done_response = self.done([], **kwargs)
        self.storage.reset()
        return done_response
        
    def done(self, form_list, **kwargs):
        redirect_to = self.request.REQUEST.get('next', '')
        if not redirect_to or not is_safe_url(redirect_to,
                                              host=self.request.get_host()):
            redirect_to = '/'
        
        return redirect(redirect_to)
        
    def get_context_data(self, form, **kwargs):
        context = super(PhoneVerifyWizard, self).get_context_data(form,**kwargs)
        if self.steps.current == 'step_2':
            context['user_phone'] = self.get_user_phone()
        return context

    def get_user_phone(self):
        return self.storage.extra_data['phone']

    def verify_phone(self, phone, country_code):
        self.process_phone(phone)

        resp = self._send_verification_code(phone, country_code)
        self.storage.extra_data['phone'] = phone
        self.storage.extra_data['request_id'] = resp.get('request_id')
            
            

    def process_phone(self, phone):
        if UserPhone.get_by_phone(phone):
            raise forms.ValidationError(_("The phone number is already registered."))

    def _send_verification_code(self, phone, country_code):
        print 'phone', phone, country_code
        verify = get_nexmoverify()
        try:
            return verify.verify(phone, country=country_code)
        except NexmoException, e:
            raise forms.ValidationError(e[0])
        

    def _check_verification_code(self, request_id, code):
        print 'request_id', request_id, code
        verify = get_nexmoverify()
        try:
            return verify.check(request_id, code)
        except NexmoException, e:
            raise forms.ValidationError(e[0])

    def check_phone(self, code):
        old_code = self.storage.extra_data.get('code')
        if code != old_code:
            phone = self.get_user_phone()
            request_id = self.storage.extra_data.get('request_id')
            print request_id, code
            self.storage.extra_data['code'] = code

            resp = self._check_verification_code(request_id, code)
            self.process_verified_phone(phone, self.request)
 
            
            self.request.session['user_phone'] = phone


    def process_verified_phone(self, phone, request):
        print 'process_verified_phone', phone, request
        obj = UserPhone.get_by_user(request.user)
        if obj:
            obj.phone = phone
            obj.save()
        else:
            UserPhone.objects.create(user=request.user, phone=phone)

class PasswordResetWizard(PhoneVerifyWizard):

    template_name = 'nexmoverify/password_reset.html'

    def process_phone(self, phone):
        user = UserPhone.get_by_phone(phone)
        if not user:
            raise forms.ValidationError(_("Invalid phone number."))
        self.storage.extra_data['_user_id'] = user.user.id
            
            

    def process_verified_phone(self, phone, request):
        
        user = get_user_model().objects.get(
            pk=self.storage.extra_data.get('_user_id'))

        token = default_token_generator.make_token(user)
        user = authenticate(uidb36=int_to_base36(user.id),
                            token=token, is_active=True)

        auth_login(request, user)
        return redirect("profile_update")

    def done(self, form_list, **kwargs):
        return redirect("profile_update")

    

FORMS = [('step_1', PhoneVerifyForm),
         ('step_2', PhoneCheckForm)]

@login_required
def add_phone(request, **kwargs):
    return PhoneVerifyWizard.as_view(FORMS)(request, **kwargs)

def password_reset(request, **kwargs):
    return PasswordResetWizard.as_view(FORMS)(request, **kwargs)

#
# @phone_requred usage example
#
@phone_requred
def secret(request):
    return HttpResponse('Wow you verified your phone number!')

