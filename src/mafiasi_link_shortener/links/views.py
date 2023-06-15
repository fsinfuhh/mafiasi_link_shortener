from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes

from . import models


@api_view(["GET"])
# no permissions required because we check for them depending on the link
@permission_classes([])
def view_link(request, short: str) -> HttpResponse:
    try:
        link = models.Link.objects.get(short__iexact=short)
        if link.login_required and not request.user.is_authenticated:
            return HttpResponseRedirect(f"/auth/openid/login?next={request.path}")
        return HttpResponseRedirect(link.target)
    except ObjectDoesNotExist:
        raise Http404(f"Link {short} does not exist")
