from django.contrib.auth.models import User
from django.db import models
from stdimage import StdImageField
# Create your models here.
from home.models import *


class ExecutiveUser(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    zip = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    userPassword = models.CharField(max_length=200, blank=True, null=True)
    target = models.FloatField(default=0.0)
    user_ID = models.ForeignKey(User, blank=True, null=True)
    isActive = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'a) Sales Executive User List'


class ProductImage(models.Model):
    productID = models.ForeignKey(Product, blank=True, null=True)
    productImage = StdImageField(upload_to='product/img', blank=True, variations={
        'large': (600, 400),
        'thumbnail': (50, 50, True),
        'medium': (300, 200),
    }, delete_orphans=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)


class BookingEcom(models.Model):
    customerID = models.ForeignKey(Customer, blank=True, null=True)
    customerName = models.CharField(max_length=200, blank=True, null=True)
    customerGst = models.CharField(max_length=200, blank=True, null=True)
    customerPhone = models.CharField(max_length=200, blank=True, null=True)
    customerEmail = models.CharField(max_length=200, blank=True, null=True)
    customerAddress = models.CharField(max_length=500, blank=True, null=True)
    customerState = models.CharField(max_length=200, blank=True, null=True)
    salesType = models.CharField(max_length=200, blank=True, null=True, default='Normal')
    paymentType = models.CharField(max_length=200, blank=True, null=True, default='Cash')
    creditDays = models.IntegerField(default=0)
    invoiceNumber = models.CharField(max_length=200, blank=True, null=True)
    invoiceDate = models.DateField(blank=True, null=True)
    subTotal = models.FloatField(default=0.0)
    taxable = models.FloatField(default=0.0)
    totalFinal = models.FloatField(default=0.0)
    billDisc = models.FloatField(default=0.0)
    gst = models.FloatField(default=0.0)
    grandTotal = models.FloatField(default=0.0)
    roundOff = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    paidDate = models.DateField(blank=True, null=True)
    chequeDetail = models.CharField(max_length=500, blank=True, null=True)
    deliveryNote = models.CharField(max_length=500, blank=True, null=True)
    supplierReference = models.CharField(max_length=500, blank=True, null=True)
    buyersOrderNumber = models.CharField(max_length=500, blank=True, null=True)
    dispatchDocumentNumber = models.CharField(max_length=500, blank=True, null=True)
    dispatchThrough = models.CharField(max_length=500, blank=True, null=True)
    otherReference = models.CharField(max_length=500, blank=True, null=True)
    dispatchNoteDate = models.CharField(max_length=500, blank=True, null=True)
    destination = models.CharField(max_length=500, blank=True, null=True)
    otherCharges = models.FloatField(default=0.0)
    companyID = models.ForeignKey(CompanyProfile, blank=True, null=True)
    addedBy = models.ForeignKey(User, blank=True, null=True)
    paidAmount = models.FloatField(default=0.0)
    dueOrReturnAmount = models.FloatField(default=0.0)
    invoiceSeriesID = models.ForeignKey(Invoice, blank=True, null=True)
    invoiceActualNumber = models.IntegerField(default=0)
    paidAgainstBill = models.FloatField(default=0.0)
    personalDiscount = models.FloatField(default=0.0)
    expectedDeliveryDate = models.DateField(blank=True, null=True)
    addedByUser = models.CharField(max_length=100, blank=True, null=True)
    isSold = models.BooleanField(default=False)
    confirmBookID = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.customerName

    class Meta:
        verbose_name_plural = 'c) Booking List'


class BookingProductList(models.Model):
    salesID = models.ForeignKey(BookingEcom, blank=True, null=True)
    productID = models.ForeignKey(Product, blank=True, null=True)
    productName = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    hsn = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=200, blank=True, null=True)
    rate = models.FloatField(default=0.0)
    gst = models.FloatField(default=0.0)
    disc = models.FloatField(default=0.0)
    netRate = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)
    batchID = models.ForeignKey(ProductBatch, blank=True, null=True)
    margin = models.FloatField(default=1.0)

    def __str__(self):
        return self.productName
