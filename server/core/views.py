from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.base import TemplateView


class AppView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            raise Http404('App build missing')
