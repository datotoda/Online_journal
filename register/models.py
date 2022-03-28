from django.db import models


class RegisterCode(models.Model):
    code = models.IntegerField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} RegisterCode object'

    class Meta:
        verbose_name = 'Register Code'
        verbose_name_plural = 'Register Codes'
