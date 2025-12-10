from django.contrib import admin
from .models import Events, Clubs, Services, Support, News, NewsImage, Zayvka

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [NewsImageInline]

class EventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']

    
class ClubsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


class SupportAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']

class ZayvkaAdmin(admin.ModelAdmin):
    list_display = ['initiative_name', 'status', 'created_at']

admin.site.register(News, NewsAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(Clubs, ClubsAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(Zayvka, ZayvkaAdmin)