from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'categories'


class Subcategory(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'subcategories'


class DonationRequest(models.Model):
    first_name = models.CharField(max_length=120, blank=True, help_text='First name (or nickname)')
    last_name = models.CharField(max_length=120, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    notes = models.TextField(max_length=120, blank=True)

    def __str__(self):
        return str(self.subcategory)
