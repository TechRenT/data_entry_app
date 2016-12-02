from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.views import generic


class LogoutView(generic.RedirectView):
    url = reverse_lazy("homepage")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)