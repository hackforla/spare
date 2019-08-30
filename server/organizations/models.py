from django.db import models
from enumfields import Enum, EnumIntegerField

from core.models import AddressModel


class OrgUserRole(Enum):
    ADMIN = 1
    READ_ONLY = 2


class OrgUser(models.Model):
    role = EnumIntegerField(OrgUserRole, default=OrgUserRole.READ_ONLY)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    org = models.ForeignKey('Org', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'org')

    def __str__(self):
        return '{} ({})'.format(str(self.user), str(self.org))


class Org(AddressModel):
    name = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(
        'core.User', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='owned_orgs')
    users = models.ManyToManyField(
        'core.User',
        through=OrgUser,
        related_name='orgs'
    )
    ein = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'organization'
        verbose_name_plural = 'organizations'
