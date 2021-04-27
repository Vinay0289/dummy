from django.contrib import admin
from .models import Category,SubCategory,Poll,PollOption,PollResult
admin.site.site_header = "Pollobe"
admin.site.site_title = "Welecome to Pollobe"
admin.site.index_title = "Welecome to Pollobe"

# Register your models here.

class InLinePollOptions(admin.TabularInline):
    model = PollOption


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','Title','Description','IsActive']
    list_filter = ['IsActive',]
    search_fields = ['Title']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','Title','Description','IsActive']
    list_filter = ['IsActive',]
    search_fields = ['Title']

class Polls(admin.ModelAdmin):
    inlines = [InLinePollOptions]
    list_display = ['id','Category','SubCategory','title','description','slug','isMultipleType','isActive','createdDate','modifiedDate'] 
    list_display_links = ['id']
    list_editable = ['isActive']

    def get_queryset(self,request):
        queryset = super(Polls,self).get_queryset(request)
        queryset = queryset.order_by('-createdDate','id')
        return queryset

class PollResultAdmin(admin.ModelAdmin):
    list_display = ['id','poll','polloptions','user','otherDescription']



admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Poll,Polls)
admin.site.register(PollResult,PollResultAdmin)
