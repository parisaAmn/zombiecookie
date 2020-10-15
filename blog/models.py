from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(User):
    # username = models.CharField(max_length = 150)
    # password = models.CharField(max_length = 150)
    # email = models.EmailField()
    cookieval = models.UUIDField(primary_key=False, default=uuid.uuid4 , unique=True)

    def __str__(self):
        return self.username + ' / ' + str(self.email) +' / '+ str(self.cookieval)
