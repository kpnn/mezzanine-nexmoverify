"""
Default settings for the ``nexmoverify`` app. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="NEXMO_API_KEY",
    description=_("Nexmo api_key"),
    editable=True,
    default='',
)

register_setting(
    name="NEXMO_API_SECRET",
    description=_("Nexmo api_secret"),
    editable=True,
    default='',
)

register_setting(
    name="NEXMO_BRAND",
    description=_("Brand"),
    editable=True,
    default='MyBrand',
)
 
