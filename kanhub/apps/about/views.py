__all__ = ()
from django.http import HttpResponse


def main(request):
    return HttpResponse("О проекте", 200)
