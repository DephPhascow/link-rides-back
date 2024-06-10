from django.db import models

class TmpCustomManager(models.Manager):
    def get_by_name(self, name):
        return self.filter(name=name)