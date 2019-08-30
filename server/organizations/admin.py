from django.contrib import admin
from rules.contrib.admin import (
    ObjectPermissionsModelAdmin, ObjectPermissionsTabularInline
)

from core.admin import RelatedOrgPermissionModelAdmin
from core.models import User
from organizations.models import Org, OrgUserRole


class OrgUserRoleInline(ObjectPermissionsTabularInline):
    model = OrgUserRole
    extra = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        user = request.user
        org = request.org

        # Superusers always have access to all fields
        if user.is_superuser:
            return formfield

        # Restrict related permission model choices
        if formfield and hasattr(formfield, 'queryset'):
            Model = formfield.queryset.model

            # If user has no associated org for user or org, return nothing
            if Model in (User, Org) and not org:
                formfield.queryset = Model.objects.none()

            # If user model, filter those related to user's org
            elif Model == User:
                formfield.queryset = User.objects.all().for_org_user(
                    org, user
                )

            # If org model, only show user's org
            elif Model == Org:
                formfield.queryset = Org.objects.filter(pk=org.pk)

        return formfield


class OrgAdmin(RelatedOrgPermissionModelAdmin):
    def get_queryset(self, request):
        # Target base class permission class for super call
        queryset = super(ObjectPermissionsModelAdmin, self).get_queryset(request)

        user = request.user
        org = request.org

        if user.is_superuser:
            queryset = queryset
        elif request.org:
            queryset = queryset.filter(pk=org.pk)
        else:
            queryset = queryset.none()

        return queryset

    inlines = [
        OrgUserRoleInline
    ]


admin.site.register(Org, OrgAdmin)
