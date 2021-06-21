from django.contrib import admin
from .models import Property, StudentExtra #IssuedBook
from .models import booking
# Register your models here.


class PropertyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Property, PropertyAdmin)


class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)




admin.site.register(booking)



# class IssuedBookAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(IssuedBook, IssuedBookAdmin)
