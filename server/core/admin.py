from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm
)
from django.utils.translation import ugettext_lazy as _
from rules.contrib.admin import ObjectPermissionsModelAdmin

from core.models import RelatedOrgPermissionModel, User


class RelatedOrgPermissionModelAdmin(ObjectPermissionsModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.for_org_user(request.org, request.user)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        # Restrict related permission model choices
        if formfield and hasattr(formfield, 'queryset'):
            Model = formfield.queryset.model

            if issubclass(Model, RelatedOrgPermissionModel):
                formfield.queryset = Model.objects.for_org_user(
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
            obj.org = request.user.org

        super().save_model(request, obj, form, change)


class UserAdmin(UserAdminBase):
    # add_form_template = 'admin/auth/user/add_form.html'
    # change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('display_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
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


admin.site.register(User, UserAdmin)
