from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} <{self.email}>"
