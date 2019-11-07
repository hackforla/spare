from django import template
from django.http import HttpRequest

from suit import utils
from suit.templatetags.suit_menu import get_admin_site, Menu

register = template.Library()

django_version = utils.django_major_version()

simple_tag = register.simple_tag


@simple_tag(takes_context=True)
def get_menu(context, request):
    # Mostly duplicated from Django-Suit's `get_menu` tag (which
    # we're overriding in templates), only returns menu dynamically
    # based on user type.
    if not isinstance(request, HttpRequest):
        return None

    template_response = get_admin_site(request.current_app).index(request)

    try:
        app_list = template_response.context_data['app_list']
    except Exception:
        return

    return DynamicMenu(context, request, app_list).get_app_list()


class DynamicMenu(Menu):
    pass
    # def init_config(self):
    #     """
    #     Override default behavior and return menu dynamically based on user type.
    #     """
    #     super().init_config()

    #     if not self.request.user.is_authenticated:
    #         self.conf_menu = []

    #     elif self.request.user.is_superuser:

    #         self.conf_menu = [
    #             '-',
    #             {
    #                 'label': 'Scheduling',
    #                 'icon': 'icon-calendar',
    #                 'models': [
    #                     {
    #                         'model': 'donations.dropofftime',
    #                         'label': 'Dropoff Times',
    #                     },
    #                     {
    #                         'model': 'donations.manualdropoffdate',
    #                         'label': 'Manual Dropoff Date',
    #                     }
    #                 ]
    #             },
    #             {
    #                 'label': 'Locations',
    #                 'icon': 'icon-map-marker',
    #                 'models': ('donations.location', 'donations.neighborhood')
    #             },
    #             {
    #                 'app': 'donations',
    #                 'label': 'Donations',
    #                 'models': [
    #                     {
    #                         'model': 'donations.donationrequest',
    #                         'label': 'Requests',
    #                     },
    #                     {
    #                         'model': 'donations.donationfulfillment',
    #                         'label': 'Fulfillments',
    #                     }
    #                 ]
    #             },
    #             '-',
    #             {
    #                 'label': 'Users',
    #                 'icon': 'icon-user',
    #                 'models': (
    #                     'core.user',
    #                     'organizations.org')
    #             },
    #             {
    #                 'label': 'Settings',
    #                 'icon': 'icon-cog',
    #                 'models': [
    #                     {
    #                         'model': 'donations.category',
    #                         'label': 'Categories'
    #                     },
    #                     {
    #                         'model': 'donations.item',
    #                         'label': 'Items',
    #                     },
    #                 ]
    #             },
    #             '-',
    #             'sites',
    #             'donations',
    #         ]

    #     elif self.request.user.is_org_user:

    #         self.conf_menu = [
    #             '-',
    #             {
    #                 'label': 'Scheduling',
    #                 'icon': 'icon-calendar',
    #                 'models': [
    #                     {
    #                         'model': 'donations.dropofftime',
    #                         'label': 'Dropoff Times',
    #                     },
    #                     {
    #                         'model': 'donations.manualdropoffdate',
    #                         'label': 'Manual Dropoff Date',
    #                     }
    #                 ]
    #             },
    #             {
    #                 'label': 'Locations',
    #                 'icon': 'icon-map-marker',
    #                 'models': ('donations.location', 'donations.neighborhood')
    #             },
    #             {
    #                 'app': 'donations',
    #                 'label': 'Donations',
    #                 'models': [
    #                     {
    #                         'model': 'donations.donationrequest',
    #                         'label': 'Requests',
    #                     },
    #                     {
    #                         'model': 'donations.donationfulfillment',
    #                         'label': 'Fulfillments',
    #                     }
    #                 ]
    #             },
    #             '-',
    #             {
    #                 'label': 'Users',
    #                 'icon': 'icon-user',
    #                 'models': (
    #                     'core.user',
    #                     'organizations.org')
    #             },
    #             'donations',
    #         ]
