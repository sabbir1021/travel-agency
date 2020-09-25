from django.shortcuts import render , get_object_or_404 , redirect, HttpResponse
from .models import Package , Location , Clientfeedback
from django.views import View, generic
from django.db.models import Max, Min , Count , Sum
from .forms import BookingForm , FilterForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import json
from blog.models import Post

class HomeView(View):
    def get(self, request, *args, **kwargs):
        package_list = Package.objects.prefetch_related('images','extras').all().order_by('-id')[:6]
        special_package = Package.objects.prefetch_related('images','extras').filter(special=True)
        location_pak = Location.objects.all()
        blog_post = Post.objects.all()
        clients = Clientfeedback.objects.all().order_by('-id')[:5]
        
        form = FilterForm(request.GET)
        if form.is_valid():
            price = request.GET.get('price_range')
            date = request.GET.get('date') or None
            title = request.GET.get('title')
            city = request.GET.get('city')

            if date == None:
                if price == "500" or price == "1000" or price== "5000":
                    if city=='':
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(0,price), title__contains=title )
                    else:
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(0,price) ,location__city=city, title__contains=title )
                if price == "inf":
                    if city=='':
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(5000,100000),title__contains=title)
                    else:
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(5000,100000),title__contains=title, location__city=city)
                if price == '0':
                    if city=='':
                        package_list = Package.objects.prefetch_related('images','extras').filter(title__contains=title)
                    else:
                        package_list = Package.objects.prefetch_related('images','extras').filter(title__contains=title, location__city=city)
            else:
                if price == "500" or price == "1000" or price== "5000":
                    if city=='':
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(0,price), start_date=date,title__contains=title )
                    else:
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(0,price) ,location__city=city, start_date=date,title__contains=title )
                if price == "inf":
                    if city=='':
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(5000,100000),start_date=date,title__contains=title)
                    else:
                        package_list = Package.objects.prefetch_related('images','extras').filter(price__range=(5000,100000),start_date=date,title__contains=title, location__city=city)
                if price == '0':
                    if city=='':
                        package_list = Package.objects.prefetch_related('images','extras').filter(title__contains=title,start_date=date)
                    else:
                        package_list = Package.objects.prefetch_related('images','extras').filter(title__contains=title,start_date=date, location__city=city)
           
        context = {
            'homective':'active',
            'title':'home',
            'package_list': package_list,
            'special_package': special_package,
            'location_pak':location_pak,
            'blog_post' : blog_post,
            'clients' : clients,
            'form':form
        }
        return render(request, 'package/index.html', context)
    
    
# class HomeView(generic.ListView):
    # model = Package
    # template_name = 'package/index.html'
    # context_object_name = 'package_list'
    # paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Home'
    #     return context

    # def get_queryset(self):
    #     qs = Package.objects.prefetch_related('images','extras').all()
    #     return qs


class PackageView(generic.ListView):
    model = Package
    template_name = 'package/package.html'
    context_object_name = 'package_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Package All'
        context['packageactive'] = 'active'
        return context

    def get_queryset(self):
        qs = Package.objects.prefetch_related('images','extras').all()
        return qs
    


# class PackageDetailsView(View):
#     def get(self, request, *args, **kwargs):
#         package = get_object_or_404(Package, id=self.request.resolver_match.kwargs['id'])
#         form = BookingForm() 
#         context = {
#             'homective':'active',
#             'title':'Package details',
#             'package': package,  
#             'form':form
#         }
#         return render(request, 'package/package_details.html', context)
#     def post(self, request, *args, **kwargs):
#         package = get_object_or_404(Package, id=self.request.resolver_match.kwargs['id'])
#         form = BookingForm(request.POST or None)
#         if form.is_valid():
#             instance=form.save(commit=False)
#             instance.package=package
#             instance.save();
#         return redirect('travel:details',id=self.request.resolver_match.kwargs['id'])

class PackageDetailsView(generic.ListView):
    model = Package
    template_name = 'package/package_details.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Package details'
        context['packageactive'] = 'active'
        context['form'] = BookingForm(),
        context['Similar_Packages'] = Package.objects.all().exclude(id=self.request.resolver_match.kwargs['id'])
        return context

    def get_queryset(self):
        qs = get_object_or_404(Package, id=self.request.resolver_match.kwargs['id'])
        return qs
    def post(self, request, *args, **kwargs):
        package = get_object_or_404(Package, id=self.request.resolver_match.kwargs['id'])
        form = BookingForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.package=package
            instance.save(); 
        return redirect('travel:details',id=self.request.resolver_match.kwargs['id'])
        
    

class LocationView(generic.ListView):
    model = Package
    template_name = 'package/location.html'
    context_object_name = 'package_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Package All'
        context['packageactive'] = 'active'
        return context

    def get_queryset(self):
        qs = Package.objects.prefetch_related('images','extras').filter(location=self.request.resolver_match.kwargs['id'])
        return qs



@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        comments = request.POST.get('comments')
        message_full = f'Name : {name} \n Email : {email} \n Phone : {phone} \n Message : {comments}.'

        if name != '' and email != '' and phone != '' and comments != '':
            host = settings.EMAIL_HOST_USER
            send_mail(
                'travelstar Contact',
                message_full,
                email,
                [host],
                fail_silently=False,
            )
            return redirect('travel:contact')
            
        else:
            return HttpResponse(
                json.dumps('Please Input All The Fields'),
                content_type="application/json"
            )

class ContactsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Contact Us',
        }
        return render(request, 'contact.html', context)


class GalleryView(generic.ListView):
    model = Package
    template_name = 'gallery/gallery.html'
    context_object_name = 'package_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gallery'
        context['galleryactive'] = 'active'
        return context

    def get_queryset(self):
        qs = Package.objects.prefetch_related('images').all()
        return qs


