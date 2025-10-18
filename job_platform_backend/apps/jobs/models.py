
from django.db import models
from django.conf import settings

class Job(models.Model):
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=20, choices=[('fixed', 'Fixed'), ('hourly', 'Hourly')])
    budget_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='open', choices=[('open', 'Open'), ('filled', 'Filled'), ('closed', 'Closed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title