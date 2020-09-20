from django.shortcuts import render
from .models import Package , PackageImage
from django.views import View, generic


class HomeView(View):
    def get(self, request, *args, **kwargs):
        packages = Package.objects.prefetch_related('images').all()
        
        context = {
            'packages': packages,
            
        }
        return render(request, 'index.html', context)


def contact(request):
    return render(request , "contact.html")