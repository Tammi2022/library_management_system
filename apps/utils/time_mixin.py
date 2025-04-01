from django.db import models


class TimeMixin(models.Model):
    """ Add creation and update times to a model. """
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True