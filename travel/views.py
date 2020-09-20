from django.shortcuts import render
from .models import Package, PackageImage
from django.views import View, generic


class HomeView(generic.ListView):
    model = Package
    template_name = 'package/index.html'
    context_object_name = 'package_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

    def get_queryset(self):
        qs = Package.objects.prefetch_related('images').all()
        return qs


def contact(request):
    return render(request, "contact.html")
