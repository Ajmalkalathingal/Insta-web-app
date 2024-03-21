from django.contrib import admin
from .models import Tag,Post,Follow,Stream,Like,Comments,Post_save


# Register your models here.

admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Like)
admin.site.register(Comments)
admin.site.register(Post_save)

@admin.register(Post)
class ProductModleAdmin(admin.ModelAdmin):
    list_display = ['id','caption'] 
