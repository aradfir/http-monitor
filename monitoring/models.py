from django.db import models


# Create your models here.
class URL(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_threshold = models.IntegerField(default=10)
    error_count = models.IntegerField(default=0)
    owner = models.ForeignKey("auth.User", related_name="urls",
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class HeartBeat(models.Model):
    url = models.ForeignKey("URL", related_name="heartbeats", on_delete=models.CASCADE)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.status}"

    def to_dict(self):
        return {
            "url": self.url.url,
            "status": self.status,
            "time": self.created_at
        }
