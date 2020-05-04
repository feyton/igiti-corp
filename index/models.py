from django.db import models

class SignUp(models.Model):
    full_name   = models.CharField(max_length=50, null=True)
    email       = models.EmailField(null=False, unique=True)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return self.email


class ErrorReport(models.Model):
    email = models.EmailField(null=True, unique=False)
    message = models.TextField(blank=False, unique=False)
    time_stamp = models.TimeField(auto_now_add=True)
    sender_ip = models.GenericIPAddressField(unique=False)
    url = models.URLField(blank=True, null=True)
    spam = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)

