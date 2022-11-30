from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect

from . import models


def view_link(request, short: str) -> HttpResponse:
    try:
        link = models.Link.objects.get(short__iexact=short)
        return HttpResponseRedirect(link.target)
    except ObjectDoesNotExist:
        raise Http404(f"Link {short} does not exist")
