# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.manager import BaseManager
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rules.contrib.models import RulesModel, RulesModelBase

zipcode_validator = RegexValidator(
    message='Invalid zip code format (must be 5 or 9 digits)',
    code='invalid_zipcode',
)


class RelatedOrgQuerySet(models.QuerySet):
    def get_visibility_filter(self, user):
        raise NotImplementedError

    def for_org_user(self, org, user):
        if user.is_superuser:
            return self.all()

        elif not org:
            return self.none()

        else:
            return self.filter(**self.model.get_visibility_filter_params(org))


class RelatedOrgManager(BaseManager.from_queryset(RelatedOrgQuerySet)):
    pass


class RelatedOrgPermissionModel(RulesModel):
    # To bypass, set to 'None'
    org_lookup = 'org'

    def get_related_org(self):
        # If already has related org, just return org
        if hasattr(self, 'org'):
            return getattr(self, 'org')

        # Otherwise, subclass must define behavior
        raise NotImplementedError('Subclass must define related orgs')

    @classmethod
    def get_visibility_filter_params(cls, org):
        # If using default lookup, query by default
        lookup = cls.org_lookup

        if lookup:
            return {
                cls.org_lookup: org
            }

        # Otherwise, sublcass must define behavior
        raise NotImplementedError('Subclass must define visibility filter params')

    objects = RelatedOrgManager()

    class Meta(RulesModelBase):
        abstract = True


class AddressModel(models.Model):
    street_address_1 = models.CharField(max_length=150)
    street_address_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=50, default='Los Angeles')
    state = models.CharField(max_length=2, default='CA')
    zipcode = models.CharField(max_length=10, validators=[zipcode_validator], default='90042')
    phone = PhoneNumberField(blank=True)
    website = models.URLField(max_length=100, blank=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    display_name = models.CharField(
        _('display name'),
        help_text="Name to be displayed to others on the app",
        blank=False,
        max_length=50,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = UserManager()

    REQUIRED_FIELDS = ['display_name']

    @property
    def org(self):
        from organizations.models import Org

        # Return first related org (either owner or staff)
        return Org.objects.filter(
            Q(users=self) | Q(owner=self)).first()

    # Possible solution (if this is too slow):
    # @cached_property
    @property
    def is_org_user(self):
        return bool(self.org)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name
