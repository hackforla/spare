from django import forms
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
    fieldset_choices = None
    list_display_choices = None
    add_fieldset_choice = None

    def _restrict_field_queryset(self, field, org, user, obj=None):
        """
        """
        if not hasattr(field, 'queryset') or not field.queryset.model:
            return

        Model = field.queryset.model

        # Allow overriding of queryset based on field name (i.e., get_somefield_queryset),
        # and if not defined will default to all instances of user-owned objects
        if issubclass(Model, RelatedOrgPermissionModel):
            method_name = "get_{}_queryset".format(Model._meta.model_name)
            queryset_method = getattr(self, method_name, None)

            if queryset_method:
                field.queryset = queryset_method(obj=obj)
            else:
                field.queryset = Model.objects.all().for_org_user(org, user)

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

    def get_form(self, request, obj=None, **kwargs):
        # NOTE: Reserved for overriding default behavior
        form = super().get_form(request, obj=obj, **kwargs)
        for name, field in form.base_fields.items():
            # NOTE: This updates field.queryset
            self._restrict_field_queryset(field, request.org, request.user, obj=obj)
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # NOTE: Reserved for overriding default behavior
        formfield = super().formfield_for_manytomany(db_field, request, **kwargs)

        return formfield

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        # NOTE: Reserved for overriding default behavior
        formfield = super().formfield_for_choice_field(db_field, request, **kwargs)

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

    def get_fieldsets(self, request, obj=None):
        # If creating a object, default to add choices (if defined), otherwise
        # default field choices
        if not obj:
            fieldset_choices = self.add_fieldset_choices or self.fieldset_choices
        else:
            fieldset_choices = self.fieldset_choices

        if request.user.is_superuser:
            return fieldset_choices[AccessLevel.SUPERUSER]
        else:
            return fieldset_choices[AccessLevel.RESTRICTED]


    def get_fieldsets(self, request, obj=None):
        # If not explicitly set, return default fieldsets
        if not self.fieldset_choices:
            return super().get_fieldsets(request, obj=obj)

        if request.user.is_superuser:
            return self.fieldset_choices[AccessLevel.SUPERUSER]
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

    add_fieldset_choices = {
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

    fieldset_choices = {
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
