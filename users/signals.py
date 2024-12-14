from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AccountBalance

@receiver(post_save, sender=CustomUser)
def create_account_balance(sender, instance, created, **kwargs):
    if created:
        account_balance = AccountBalance.objects.create(user=instance, balance=50)
        account_balance.save()
