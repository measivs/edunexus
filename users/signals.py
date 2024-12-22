from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AccountBalance

@receiver(post_save, sender=CustomUser)
def create_account_balance(sender, instance, created, **kwargs):
    """
        Signal triggered upon user creation.

        Automatically creates an initial account balance for new users with a default value of 50 as a bonus.

        Args:
            sender: The model class (CustomUser).
            instance: The instance of the newly-created user.
            created: A boolean indicating whether the user was newly created.
    """
    if created:
        account_balance = AccountBalance.objects.create(user=instance, balance=50)
        account_balance.save()
