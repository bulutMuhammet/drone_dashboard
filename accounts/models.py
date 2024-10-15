from django.contrib.auth.models import User
from django.db import models
User._meta.get_field('email')._unique = True


class Team(models.Model):
    name = models.CharField(max_length=50)
    is_assembler = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()
