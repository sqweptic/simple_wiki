from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class WikiPage(models.Model):
    validate_a_n_u = RegexValidator(r'[0-9a-z_]+$', 'Contain only numeric, lowcase alphabetical and underscore')
    
    public_date = models.DateTimeField(blank=True, default=timezone.now())
    text = models.TextField()
    title = models.CharField(max_length=100)
    url_title = models.CharField(max_length=125, validators=[validate_a_n_u,])
    url = models.CharField(max_length=100)