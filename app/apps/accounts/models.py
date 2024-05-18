from django.db import models


class Account(models.Model):
    uuid = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
