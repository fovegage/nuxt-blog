# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from operation.models import UserFav


@receiver(post_save, sender=UserFav)
def user_add_fav(sender, instance=None, created=False, **kwargs):
    if created:
        good = instance.good
        good.fav_num += 1
        good.save()
