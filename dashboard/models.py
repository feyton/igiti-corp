from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class NurseryManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=False, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.user.get_full_name(), self.location)


class Species(models.Model):
    scientific_name = models.CharField(
        blank=False, unique=True, max_length=255)
    seeds_kg = models.IntegerField(blank=True)


class Nursery(models.Model):
    # Choices

    # DATABASE

    manager = models.ForeignKey(NurseryManager, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    species = models.ManyToManyField(Species)


class SowingBed(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    size = models.CharField(max_length=255, blank=True, null=True)
    specie = models.ManyToManyField(Species)
    sowing_date = models.DateTimeField(auto_now=False, blank=True, null=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    action = models.CharField(max_length=255, blank=False, null=False)
    date_completed = models.DateTimeField(
        blank=True, null=True, auto_now_add=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    def complete_url(self):
        return reverse('dashboard:complete_task', kwargs={'pk': self.id})


class Workers(models.Model):
    # CHOICES
    # DATABASE
    account_number = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=255, )
    job = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.full_name

    def pay_url(self):
        return reverse('dashboard:pay_worker', kwargs={'pk': self.id})

    def delete_url(self):
        return reverse('dashboard:remove-worker', kwargs={'pk': self.id})
