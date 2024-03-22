from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ["username",  "email", "bio"]



class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "fullname",  "bio", "phone"]

# class ProfileProjectAdmin(admin.ModelAdmin):
#     list_display = ["user", "name",  "email", "status"]

# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ["profile",  "location", "website"]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(ProfileProject, ProfileProjectAdmin)
# admin.site.register(Organization,  OrganizationAdmin)
# admin.site.register(Teacher)
# admin.site.register(Student)