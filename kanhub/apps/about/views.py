__all__ = ()
import django.shortcuts


def main(request):
    return django.shortcuts.render(request, "about/main.html")
