from django.contrib import admin
from travel.models import Division, City, Location, Package, PackageImage, PackageSchedule, PackageExtra, PackageVideo, Booking, Clientfeedback

# Register your models here.


class CityInline(admin.StackedInline):
    model = City
    extra = 0


# class LocationInline(admin.StackedInline):
#     model = Location
#     extra = 0


class DivisionAdmin(admin.ModelAdmin):
    inlines = [CityInline]
    list_display = ['name']
    search_fields = ('name',)
    list_per_page = 20


admin.site.register(Division, DivisionAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'place']
    search_fields = ('city', 'place',)
    list_per_page = 20


admin.site.register(Location, LocationAdmin)


class PackageImageInline(admin.StackedInline):
    model = PackageImage
    extra = 0
    max_num = 5


class PackageScheduleInline(admin.StackedInline):
    model = PackageSchedule
    extra = 0


class PackageExtraInline(admin.StackedInline):
    model = PackageExtra
    extra = 0


class PackageVideoInline(admin.StackedInline):
    model = PackageVideo
    extra = 0


class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageImageInline, PackageScheduleInline,
               PackageExtraInline, PackageVideoInline]
    list_display = ['title', 'location', 'price',
                    'start_date', 'end_date', 'total_day']
    search_fields = ('title', 'location__city',
                     'location__area', 'location__division')
    list_filter = ['location__division']
    list_per_page = 20
    exclude = ['slug']


admin.site.register(Package, PackageAdmin)


class PackageImageAdmin(admin.ModelAdmin):
    list_display = ['package', 'image', 'image_tag']
    list_filter = ['package__location__division']
    readonly_fields = ['image_tag']
    search_fields = ('package__title', 'package__location__city',
                     'package__location__area')
    list_per_page = 20


admin.site.register(PackageImage, PackageImageAdmin)


class PackageScheduleAdmin(admin.ModelAdmin):
    list_display = ['package', 'title']
    list_filter = ['package__location__division']
    search_fields = ('package__title', 'package__location__city',
                     'package__location__area')
    list_per_page = 20


admin.site.register(PackageSchedule, PackageScheduleAdmin)


class PackageExtraAdmin(admin.ModelAdmin):
    list_display = ['package', 'name', 'avialable']
    list_filter = ['package__location__division', 'avialable']
    search_fields = ('package__title', 'package__location__city',
                     'package__location__area', 'name')
    list_per_page = 20


admin.site.register(PackageExtra, PackageExtraAdmin)


class PackageVideoAdmin(admin.ModelAdmin):
    list_display = ['package', 'link']
    list_filter = ['package__location__division']
    search_fields = ('package__title', 'package__location__city',
                     'package__location__area', 'link')
    list_per_page = 20


admin.site.register(PackageVideo, PackageVideoAdmin)


admin.site.register(Booking)
admin.site.register(Clientfeedback)
