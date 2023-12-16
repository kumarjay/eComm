from django.db import models
from base.models import BaseModel

# Create your models here.

class BannerImage(BaseModel):
    banner_name = models.CharField(max_length=100, null=True, blank=True)
    banner_image = models.ImageField(upload_to='banner')

    def __str__(self) -> str:
        return str(self.banner_name)
