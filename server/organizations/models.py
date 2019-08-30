from django.db import models
from enumfields import Enum, EnumIntegerField
from rules.contrib.models import RulesModel

from core.models import AddressModel


class OrgUserRoleType(Enum):
    ADMIN = 1
    READ_ONLY = 2


class OrgUserRole(RulesModel):
    type = EnumIntegerField(OrgUserRoleType, default=OrgUserRoleType.READ_ONLY)
    user = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        related_name='org_roles'
    )
    org = models.ForeignKey(
        'Org',
        on_delete=models.CASCADE,
        related_name='user_roles',
    )

    class Meta:
        unique_together = ('user', 'org')

    def __str__(self):
        return '{} ({})'.format(str(self.user), str(self.org))


class Org(AddressModel, RulesModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=False, blank=True)
    users = models.ManyToManyField(
        'core.User',
        through=OrgUserRole,
        related_name='orgs'
    )
    ein = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'organization'
        verbose_name_plural = 'organizations'
