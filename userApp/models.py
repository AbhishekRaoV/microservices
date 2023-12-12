from django.db import models

# Create your models here.
class KeycloakUser(models.Model):
    id=models.CharField(max_length=100,primary_key=True)
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    enabled=models.BooleanField()
    username=models.CharField(max_length=100)
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    attributes = models.JSONField()

    def __str__(self):
        return self.id+self.createdTimestamp+self.username+self.firstName+self.lastName+self.email+self.password+self.attributes
