============================
Welcome to mezzanine-nexmoverify
============================



Use Nexmo Verify in your Mezzanine websites.

Features:
 * Enables you to verify your users phone number 
 * Password reset (users can use their phone number to log in and reset password).
 * Ability to restrict access to some actions/parts of your web site using @phone_required decorator in a similar fashion as @login_required is used (only users with verified phone number will have access, so it can stop people making fake accounts, stop spamming...).


Installation
------------

1. Download or clone this repo and call ``$ python setup.py install``

2. Install Mezzanine 3.1.10

    ``$ pip install mezzanine``

3. Create mezzanine project or use in your existing mezzanine project:
    
    ``$ mezzanine-project mezzanine_project_name``

4. Add to INSTALLED_APPS in your ``<mezzanine_project_name>/settings.py``:

   ``'bootstrap3',``
   
   ``'mezzanine.accounts',``
   
   ``'django.contrib.formtools',``
   
   ``'nexmoverify',`` 

5.  Add to urlpatterns in your ``<mezzanine_project_name>/urls.py``:

   ``("^", include("nexmoverify.urls")),``

6. Copy ``templates`` folder (it only contains one file: 'user_panel.html') into your mezzanine_project_name folder:

   So your mezzanine_project_name folder should contain:
   ``/templates/accounts/includes/user_panel.html``
   
   Full path should be:
   ``<mezzanine_project_name>/templates/accounts/includes/user_panel.html``

7. Run:

    ``$ cd mezzanine_project_name``
    
    ``$ python manage.py createdb --noinput``
    
    ``$ python manage.py runserver``

You should be able to browse to http://127.0.0.1:8000/admin/ and log in using the default account (username: admin, password: default)

8. Go to Admin Settings and add your:
    
    ``Nexmo API KEY``, ``Nexmo API SECRET`` and ``Nexmo Brand``
    


Examples
----------------

    Using the @phone_required decorator
    
  .. code:: Python

    from django.http import HttpResponse
    from nexmoverify.decorators import phone_requred

    @phone_requred
    def secret(request):
        return HttpResponse('Wow you verified your phone number!')

 
 
 Visit http://127.0.0.1:8000/test/secret to see it in action.
 
    .. code:: Python

    Using Nexmo Verify API Directly

    >>> from nexmoverify.nexmo_verify import NexmoVerify, NexmoException
    >>> api = NexmoVerify(api_key='',
                         api_secret='',
                         brand='mybrand')
    >>> print api.verify('phone', country='')
    ....
    >>> print api.check('request_id', 'code') 



Requirements
------------

- Python 2.6, 2.7, 3.2+
- Django 1.6, 1.7
- Mezzanine 3.1.10


Bugs and requests
-----------------

If you have found a bug please use the issue tracker on GitHub.

https://github.com/kpnn/mezzanine-nexmoverify/issues


License
-------

You can use this under BSD.


