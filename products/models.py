from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='subcategories', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name