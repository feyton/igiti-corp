from django.db import models

class SignUp(models.Model):
    full_name   = models.CharField(max_length=50, null=True)
    email       = models.EmailField(null=False, unique=True)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return self.email
