import datetime
import hashlib

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Trip(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )

    nk = models.CharField(max_length=32, unique=True, db_index=True)  # natural kay
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pick_up_address = models.CharField(max_length=255)
    drop_off_address = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUSES, default=REQUESTED)

    def __str__(self):
        return self.nk

    def get_absolute_url(self):
        return reverse('trip:trip_detail', kwargs={'trip_nk': self.nk})

    def save(self, **kwargs):
        if not self.nk:
            now = datetime.datetime.now()
            secure_hash = hashlib.md5()
            secure_hash.update(
                f'{now}:{self.pick_up_address}:{self.drop_off_address}'.encode(
                    'utf-8'))
            self.nk = secure_hash.hexdigest()
        super().save(**kwargs)