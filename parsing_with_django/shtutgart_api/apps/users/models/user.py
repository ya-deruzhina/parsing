from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import BooleanField, CharField, DateTimeField, EmailField, SmallIntegerField
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class User(AbstractUser):
    manager = CustomUserManager()

    ADMIN = 'admin'
    USER = 'user'

    USER_ROLES_CHOICES = ((ADMIN, 'Admin'), (USER, 'User'))

    WAITING_FOR_ACTIVATION = 'wfa'
    ACTIVE = 'active'
    TERMINATED = 'terminated'
    BLOCKED = 'blocked'

    USER_STATUSES = [WAITING_FOR_ACTIVATION, ACTIVE, TERMINATED, BLOCKED]

    USER_STATUSES_DESCRIPTION = [_('Waiting for activation'), _('Active'), _('Terminated'), _('Blocked')]

    USER_STATUSES_CHOICES = tuple(zip(USER_STATUSES, USER_STATUSES_DESCRIPTION))

    email = EmailField(unique=True, null=True)
    first_name = CharField(max_length=255, blank=True, null=True)
    last_name = CharField(max_length=255, blank=True, null=True)
    status = CharField(
        max_length=255, choices=USER_STATUSES_CHOICES, default=ACTIVE
    )
    role = CharField(max_length=255, choices=USER_ROLES_CHOICES, default=USER)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted = BooleanField(default=False)
    last_request_at = DateTimeField(blank=False, null=False, default=now)
    last_login_attempt_at = DateTimeField(default=now)
    login_attempts_count = SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.id}. {self.username}'

    @property
    def app_role(self):
        """
        Returns the user's role in the app.
        """
        if self.is_superuser:
            return "super_admin"
        return self.role
