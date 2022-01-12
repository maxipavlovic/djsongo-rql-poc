from django.db import models


class RQLJsonToSQL(models.Model):
    json = models.JSONField()
