from django.db import models
import datetime
# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class Cinema(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='uploads/cinema/')
    location = models.CharField(max_length=60)
    phone = PhoneNumberField(null=False, blank=True, unique=False)
    email = models.EmailField(max_length = 254)

    @staticmethod
    def get_all_cinemas():
        return Cinema.objects.all()

    #def __str__(self):
    #    return self.name


class Hall(models.Model):
    name = models.CharField(max_length=60)
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Film(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Session(models.Model):
    date = models.DateField(default=datetime.datetime.today())
    time = models.TimeField(default=datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.film_id.name} - {self.hall_id} - {self.date} {self.time}"

    @staticmethod
    def get_all_sessions():
        return Session.objects.all()

    @staticmethod
    def get_all_session_by_date(date):
        if date:
            return Session.objects.filter(date=date)
        else:
            return Session.get_all_sessions()

