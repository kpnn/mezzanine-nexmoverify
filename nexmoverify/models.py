from django.db import models
from django.contrib.auth.models import User

class UserPhone(models.Model):
    """
    """

    user = models.ForeignKey(User)
    phone = models.CharField(max_length=20, unique=True)
    verification_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u' '.join((self.user.username, self.phone))

    @classmethod
    def get_by_phone(cls, phone):
        return cls.objects.filter(phone=phone).first()

    @classmethod
    def get_by_user(cls, user):
        return cls.objects.filter(user=user).first()

