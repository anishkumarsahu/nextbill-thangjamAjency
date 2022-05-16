from django.contrib import admin
from.models import *
# Register your models here.

admin.site.register(ProductImage)

class BookingProductListAdmin(admin.TabularInline):
    model = BookingProductList
    extra = 0



class BookingEcomAdmin(admin.ModelAdmin):
    search_fields = ['customerName','customerGst','invoiceNumber']
    list_display = ['customerName','customerGst','invoiceNumber','invoiceDate','grandTotal','companyID','status', 'isDeleted', 'datetime', 'lastUpdatedOn']

    inlines = (BookingProductListAdmin,)
admin.site.register(BookingEcom, BookingEcomAdmin)
