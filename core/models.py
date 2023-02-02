from .hash import Hasher
from django.db import models

class HashableModel(models.Model):
    class Meta:
        abstract = True

    @property
    def hash(self):
        return Hasher.from_model(self)

