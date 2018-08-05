from django.views.generic.base import TemplateView
from django.http import Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist


class AppView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            get_template(self.template_name)
            return super().dispatch(request, *args, **kwargs)
        except TemplateDoesNotExist:
            raise Http404('App build missing')
