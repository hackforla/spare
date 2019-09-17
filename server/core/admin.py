from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm
)
from django.utils.translation import ugettext_lazy as _
from rules.contrib.admin import ObjectPermissionsModelAdmin

from core.models import RelatedOrgPermissionModel, User


class AccessLevel:
    SUPERUSER = 'superuser'
    RESTRICTED = 'restricted'


class RelatedOrgPermissionModelAdmin(ObjectPermissionsModelAdmin):
    list_display_choices = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.for_org_user(request.org, request.user)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        # Restrict related permission model choices
        if formfield and hasattr(formfield, 'queryset'):
            Model = formfield.queryset.model

            if issubclass(Model, RelatedOrgPermissionModel):
                formfield.queryset = Model.objects.all().for_org_user(
                    request.org, request.user
                )

        return formfield

    def get_exclude(self, request, obj):
        excluded = super().get_exclude(request, obj) or []

        # If not a superuser, remove org choice from select
        if not request.user.is_superuser:
            excluded.append('org')

        # If excluded is empty list, return None (to be
        # consistent with Django)
        return excluded or None

    def save_model(self, request, obj, form, change):
        # If not a superuser, force to default org
        if not request.user.is_superuser:
            try:
                obj.org = request.user.org
            except AttributeError:
                pass

        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        # If not explicitly set, return default list display
        if not self.list_display_choices:
            return super().get_list_display(request)

        if request.user.is_superuser:
            return self.list_display_choices[AccessLevel.SUPERUSER]
        else:
            return self.list_display_choices[AccessLevel.RESTRICTED]


class UserAdmin(RelatedOrgPermissionModelAdmin, UserAdminBase):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'display_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'display_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    _add_fieldset_choices = {
        AccessLevel.SUPERUSER: (
            (None, {
                'classes': ('wide',),
                'fields': ('display_name', 'email', 'password1', 'password2')
            }),
        ),
        AccessLevel.RESTRICTED: (
            (None, {
                'classes': ('wide',),
                'fields': ('display_name', 'email', 'password1', 'password2')
            }),
        ),
    }

    _fieldset_choices = {
        AccessLevel.SUPERUSER: (
            (None, {'fields': ('display_name', 'email', 'password')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                           'groups', 'user_permissions')}),
            (_('Important dates'), {'fields': ('last_login',)}),
        ),
        AccessLevel.RESTRICTED: (
            (None, {'fields': ('display_name', 'email', 'password')}),
            (_('Permissions'), {'fields': ('is_active',)}),
        )
    }

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            fieldset_choices = self._add_fieldset_choices
        else:
            fieldset_choices = self._fieldset_choices

        if request.user.is_superuser:
            return fieldset_choices[AccessLevel.SUPERUSER]
        else:
            return fieldset_choices[AccessLevel.RESTRICTED]

    @property
    def inlines(self):
        # Avoid circular imports (otherwise would need to move
        # OrgUserRoleInline to this file, but it seems better to keep
        # in organizations app).
        from organizations.admin import OrgUserRoleInline

        return [
            OrgUserRoleInline
        ]

    def get_inline_instances(self, request, obj=None):
        # Avoid circular imports (otherwise would need to move
        # OrgUserRoleInline to this file, but it seems better to keep
        # in organizations app).
        from organizations.admin import OrgUserRoleInline

        inline_instances = []
        inline_class = OrgUserRoleInline

        inline = inline_class(self.model, self.admin_site)
        inline.max_num = 1

        if request:
            inline.max_num = 1

            # Not sure if this is needed (from ModelAdmin.get_inline_instances)
            if not (inline.has_add_permission(request) or
                    inline.has_change_permission(request, obj) or
                    inline.has_delete_permission(request, obj)):
                return []

            if not inline.has_add_permission(request):
                inline.max_num = 0

        inline_instances.append(inline)

        return inline_instances


admin.site.register(User, UserAdmin)
