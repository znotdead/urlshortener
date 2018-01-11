import random
import string

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class ShortURL(models.Model):
    '''
        Store correlation between short URL and long URL.
    '''
    code = models.CharField('URL short code', max_length=10, unique=True)
    long_url = models.URLField()

    @staticmethod
    def generate_code():
        ''' Generate random code of 2-11 length'''
        chars = string.ascii_letters + string.digits
        size = random.choice(range(2, 11))
        return ''.join(random.choice(chars) for x in range(size))

    def add_code(self):
        self.code = self.generate_code()


@receiver(pre_save, sender=ShortURL)
def add_code(sender, instance, **kwargs):
    if not instance.code:
        instance.add_code()
        while sender.objects.filter(code=instance.code).exists():
            instance.add_code()
