from django.contrib import admin
from . import models

admin.site.register(models.Categories)
admin.site.register(models.Tags)
admin.site.register(models.Discounts)
admin.site.register(models.Regions)
admin.site.register(models.Cities)
admin.site.register(models.Addresses)
admin.site.register(models.Comments)

class ProductImagesAdmin(admin.StackedInline):
    model = models.ProductImages

class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    class Meta:
        model = models.Products

admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.ProductImages)
admin.site.register(models.Orders)
admin.site.register(models.OrderListItems)
admin.site.register(models.Contacts)