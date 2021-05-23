from django.contrib import admin
from .models import Category,SubCategory,Poll,PollOption,PollResult,TargetedIndustry,PointingTo,PollBranching
from django.urls import path
from django import forms
from django.contrib import messages
import csv,io
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.shortcuts import render,redirect
from django.db import connection,transaction

admin.site.site_header = "Pollobe"
admin.site.site_title = "Welecome to Pollobe"
admin.site.index_title = "Welecome to Pollobe"

# Register your models here.

class InLinePollOptions(admin.TabularInline):
    model = PollOption

class InLinePollBranching(admin.TabularInline):
    model = PollBranching
    fk_name = 'Poll'
    max_num=1

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','Title','Description','IsActive']
    list_filter = ['IsActive',]
    search_fields = ['Title']


class TargetedIndustryAdmin(admin.ModelAdmin):
    list_display = ['id','Title','Description','IsActive']
    list_filter = ['IsActive',]
    search_fields = ['Title']

    
class PointingToAdmin(admin.ModelAdmin):
    list_display = ['id','Title','Description','IsActive']
    list_filter = ['IsActive',]
    search_fields = ['Title']

class SubCategoryAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"
    list_display = ['id','Title','Description','IsActive']
    list_filter = ['IsActive',]
    search_fields = ['Title']
    actions = ["export_as_csv"]
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/',self.import_csv),
            path('download-csv/',self.download_csv),
            path('download-listdata/',self.download_listdata,)
        ]
        return my_urls + urls

    def download_listdata(self, request):
        cursor = connection.cursor()
        #'Keywords','Description','slug','IsActive'
        cursor.execute("SELECT a.id as 'Category_id',a.Title as 'CategoryTitle',a.IsActive as 'Category_IsActive',b.id as 'SubCategory_id',b.Title as 'SubCategory_Title',b.Keywords,b.Description,b.slug,b.IsActive as 'SubCategory_IsActive' FROM  pollsrestapiapp_subcategory b left join pollsrestapiapp_category a on (b.category_id=a.id)")
        row = cursor.fetchall()
        dictalldata = []
        for items in row:
            datalist = {
                "Category_id": items[0],
                "CategoryTitle": items[1],
                "Category_IsActive": items[2],
                "SubCategory_id": items[3],
                "SubCategory_Title": items[4],
                "Keywords": items[5],
                "Description": items[6],
                "slug": items[7],     
                "SubCategory_IsActive": items[8],       
                }
            dictalldata.append(datalist)
        cursor.close()
        #print(dictalldata)
        qs = super(SubCategoryAdmin, self).get_queryset(request)
        print(self.model._meta)
        meta = self.model._meta
        #field_names = [field.name for field in meta.fields]
        field_names = ['Category_id','Category_Title','Category_IsActive','SubCategory_id','SubCategory_Title','Keywords','Description','slug','SubCategory_IsActive']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=subcategoryalldata.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        column = ['Category_id','CategoryTitle','Category_IsActive','SubCategory_id','SubCategory_Title','Keywords','Description','slug','SubCategory_IsActive']
        for obj in dictalldata:
            #print(obj)    
            writer.writerow(obj.get(field,None) for field in column)
            #row1 = writer.writerow([obj.get(field,None) for field in column])
            #break

        return response

    # def export_as_csv(self, request, queryset):
    #     meta = self.model._meta
    #     field_names = [field.name for field in meta.fields]
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename=product.csv'.format(meta)
    #     writer = csv.writer(response)
    #     writer.writerow(field_names)
    #     for obj in queryset:
    #         row = writer.writerow([getattr(obj, field) for field in field_names])
    #     return response
    #     export_as_csv.short_description = "Export Selected"
        
    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('import-csv/',self.import_csv),
    #         path('download-csv/',self.download_csv,)
    #         ]
    #     return my_urls + urls

    def download_csv(self, request):
        qs = super(SubCategoryAdmin, self).get_queryset(request)
        #print(self.model._meta)
        meta = self.model._meta
        #field_names = [field.name for field in meta.fields]
        field_names = ['Category_id','id','Title','Keywords','Description','slug','IsActive']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=subcategory.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        column = ['Category_id','id','Title','Keywords','Description','slug','IsActive']
        for obj in qs:
            #print(obj)
            row = writer.writerow([getattr(obj, field) for field in column])
            break

        return response

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, 'Please Upload CSV file')
                #return redirect("..")
            else:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                reader = csv.reader(csv_file)
                print(reader)
                counter=0
                for column in csv.reader(io_string, delimiter=','):
                    counter = counter + 1
                    try:
                        categorydata = Category.objects.select_related().get(id=column[0])
                    except ObjectDoesNotExist:
                        categorydata = None
                    try:
                        SubCategoryCheck = SubCategory.objects.select_related().get(id=column[1])
                    except ObjectDoesNotExist:
                        SubCategoryCheck = None
                    
                    if categorydata is not None:
                        if SubCategoryCheck is not None:
                            subcategoryupdate = SubCategory.objects.get(pk=column[1])
                            if not SubCategory.objects.filter(pk=column[1]).filter(Category=column[0]).exists():
                                subcategoryupdate.Category = categorydata
                            subcategoryupdate.Title = column[2]
                            subcategoryupdate.Keywords = column[3]
                            subcategoryupdate.Description = column[4]
                            subcategoryupdate.slug = column[5]
                            subcategoryupdate.IsActive = column[6]
                            subcategoryupdate.save()
                        else:
                            subcategoryadd = SubCategory.objects.create(
                                Category=categorydata,
                                Title= column[2],
                                Keywords= column[3],
                                Description= column[4],
                                slug= column[5],
                                IsActive= column[6]
                            )
                            #print("Hi" + column[0])
                            #subcategoryadd.Category.add(column[0])
                            subcategoryadd.save()                            
                    else:
                        if categorydata is None:
                            messages.error(request,"Category id " + str(column[0]) + " is invalid on line no. " + str(counter))
                self.message_user(request, "Your csv file has been imported")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
            )

class Polls(admin.ModelAdmin):
    inlines = [InLinePollOptions,InLinePollBranching]
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
admin.site.register(TargetedIndustry,TargetedIndustryAdmin)
admin.site.register(PointingTo,PointingToAdmin)
admin.site.register(Poll,Polls)
admin.site.register(PollResult,PollResultAdmin)
