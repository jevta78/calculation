from django.db import models
from django.conf import settings

class InputNumbers(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    list_num = models.IntegerField()

    def __str__(self):
        return str(self.list_num)

class Sums(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    calcSum = models.IntegerField()

    def __str__(self):
        return str(self.calcSumS)

class Sve(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    numbers = models.CharField(max_length=555)
    sums = models.CharField(max_length=555)

    def __str__(self):
        return str(self.numbers)+ " " +str(self.sums)