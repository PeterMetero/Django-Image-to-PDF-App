from django.db import models

class ConversionLog(models.Model):
    filename = models.CharField(max_length=255)
    image_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.image_count} images)"