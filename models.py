from django.db import models

class city(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='cities' 
        ordering = ['-id']