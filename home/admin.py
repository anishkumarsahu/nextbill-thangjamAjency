from django.contrib import admin

# Register your models here.
from .models import*


class PrinterSettingAdmin(admin.ModelAdmin):
    list_display = ['size', 'isDeleted', 'datetime', 'lastUpdatedOn']

admin.site.register(PrinterSetting, PrinterSettingAdmin)


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'gst', 'city','zip','city','state','phone','address', 'email', 'isDeleted', 'datetime', 'lastUpdatedOn']


admin.site.register(CompanyProfile, CompanyProfileAdmin)


class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['accHolderName', 'bankName', 'companyID','accNo','branch','accountType','ifsc', 'bankAddress', 'isDeleted']


admin.site.register(BankDetails, BankDetailsAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoiceSeries', 'invoiceMaxCount', 'companyID','invoiceStartWith','isCompleted', 'isDeleted', 'datetime', 'lastUpdatedOn']


admin.site.register(Invoice, InvoiceAdmin)


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'gst','phone','address', 'email']
    list_display = ['name', 'gst','phone','address', 'email', 'isDeleted', 'datetime', 'lastUpdatedOn']


admin.site.register(Customer, CustomerAdmin)


class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name', 'gst','phone','address', 'email']
    list_display = ['name', 'gst','phone','address', 'email', 'isDeleted', 'datetime', 'lastUpdatedOn']


admin.site.register(Supplier, SupplierAdmin)



class HsnAdmin(admin.ModelAdmin):
    search_fields = ['hsn', 'tax']
    list_display = ['hsn', 'tax','datetime', 'lastUpdatedOn']


admin.site.register(Hsn, HsnAdmin)



class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'brand']
    list_display = ['name', 'hsnID','brand','price','datetime', 'lastUpdatedOn']


admin.site.register(Category, CategoryAdmin)



class WareHouseAdmin(admin.ModelAdmin):
    search_fields = ['wareHouseName', 'wareHouseAddress']
    list_display = ['wareHouseName', 'wareHouseAddress', 'isDeleted','datetime']


admin.site.register(WareHouse, WareHouseAdmin)



class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'isDeleted','datetime','lastUpdatedOn']


admin.site.register(Unit, UnitAdmin)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name','brand','productType']
    list_display = ['name','brand','categoryID','cost','stock','unitID','productType','company_ID','wareHouse_ID','status', 'isDeleted','datetime','lastUpdatedOn']


admin.site.register(Product, ProductAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    search_fields = ['expenseType','description','amount']
    list_display = ['expenseType','description','amount','expenseDate','companyID', 'isDeleted','datetime','lastUpdatedOn']


admin.site.register(Expense, ExpenseAdmin)


class CompanyUserAdmin(admin.ModelAdmin):
    search_fields = ['name','phone','address']
    list_display = ['name','phone','address','username','userPassword','company_ID','user_ID', 'isDeleted']


admin.site.register(CompanyUser, CompanyUserAdmin)


class PurchaseProductListAdmin(admin.TabularInline):
    model = PurchaseProduct
    extra = 0



class PurchaseAdmin(admin.ModelAdmin):
    search_fields = ['supplierName','supplierGst','invoiceNumber']
    list_display = ['supplierName','supplierGst','invoiceNumber','invoiceDate','total','companyID','status', 'isDeleted', 'datetime', 'lastUpdatedOn']

    inlines = (PurchaseProductListAdmin,)
admin.site.register(Purchase, PurchaseAdmin)


class SalesProductListAdmin(admin.TabularInline):
    model = SalesProduct
    extra = 0



class SalesAdmin(admin.ModelAdmin):
    search_fields = ['customerName','customerGst','invoiceNumber']
    list_display = ['customerName','customerGst','invoiceNumber','invoiceDate','grandTotal','companyID','status', 'isDeleted', 'datetime', 'lastUpdatedOn']

    inlines = (SalesProductListAdmin,)
admin.site.register(Sales, SalesAdmin)


class UserPrinterSettingAdmin(admin.ModelAdmin):
    list_display = ['printerID','userID']

admin.site.register(UserPrinterSetting, UserPrinterSettingAdmin)



class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['salesID','amount','addedBy','datetime','lastUpdatedOn']

admin.site.register(PaymentHistory, PaymentHistoryAdmin)



class SalesLaterProductListAdmin(admin.TabularInline):
    model = SalesLaterProduct
    extra = 0



class SalesLaterAdmin(admin.ModelAdmin):
    search_fields = ['customerName','customerGst','invoiceNumber']
    list_display = ['customerName','customerGst','invoiceNumber','invoiceDate','grandTotal','companyID','status', 'isDeleted', 'datetime', 'lastUpdatedOn']

    inlines = (SalesLaterProductListAdmin,)
admin.site.register(SalesLater, SalesLaterAdmin)



class ReferrerAdmin(admin.ModelAdmin):
    list_display = ['name','balance','commission','phone','address','datetime','lastUpdatedOn']

admin.site.register(Referrer, ReferrerAdmin)

class ReferrerTransactionAdmin(admin.ModelAdmin):
    list_display = ['referrerID','amount','transactionType','addedBy','remark','transactionDate','datetime','lastUpdatedOn']

admin.site.register(ReferrerTransaction, ReferrerTransactionAdmin)