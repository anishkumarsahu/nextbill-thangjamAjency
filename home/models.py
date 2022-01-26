from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class PrinterSetting(models.Model):
    size = models.CharField(max_length=100, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name_plural = 'a) Printer Setting'


class CompanyProfile(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    gst = models.CharField(max_length=200, blank=True, null=True, default='')
    city = models.CharField(max_length=200, blank=True, null=True, default='')
    zip = models.CharField(max_length=200, blank=True, null=True, default='')
    state = models.CharField(max_length=200, blank=True, null=True, default='')
    phone = models.CharField(max_length=200, blank=True, null=True, default='')
    address = models.TextField(blank=True, null=True, default='')
    email = models.CharField(max_length=200, blank=True, null=True, default='')
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'b) Company Profile'


class BankDetails(models.Model):
    accHolderName = models.CharField(max_length=200, blank=True, null=True, default='')
    bankName = models.CharField(max_length=200, blank=True, null=True, default='')
    accNo = models.CharField(max_length=200, blank=True, null=True, default='')
    branch = models.CharField(max_length=200, blank=True, null=True, default='')
    accountType = models.CharField(max_length=200, blank=True, null=True, default='')
    ifsc = models.CharField(max_length=200, blank=True, null=True, default='')
    bankAddress = models.CharField(max_length=200, blank=True, null=True, default='')
    companyID = models.ForeignKey(CompanyProfile)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.accHolderName

    class Meta:
        verbose_name_plural = 'c) Bank Details'


class Invoice(models.Model):
    invoiceSeries = models.CharField(max_length=100)
    invoiceMaxCount = models.IntegerField(default=1000)
    companyID = models.ForeignKey(CompanyProfile, blank=True, null=True)
    invoiceStartWith = models.IntegerField(default=1)
    invoiceType = models.CharField(max_length=100,blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.invoiceSeries

    class Meta:
        verbose_name_plural = 'd) Invoice'


class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    gst = models.CharField(max_length=200, blank=True, null=True, default='')
    state = models.CharField(max_length=200, blank=True, null=True, default='')
    phone = models.CharField(max_length=200, blank=True, null=True, default='')
    address = models.TextField(blank=True, null=True, default='')
    email = models.CharField(max_length=200, blank=True, null=True, default='')
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'e) Customers List'


class Supplier(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    gst = models.CharField(max_length=200, blank=True, null=True, default='')
    state = models.CharField(max_length=200, blank=True, null=True, default='')
    phone = models.CharField(max_length=200, blank=True, null=True, default='')
    address = models.TextField(blank=True, null=True, default='')
    email = models.CharField(max_length=200, blank=True, null=True, default='')
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'f) Supplier List'


class Hsn(models.Model):
    hsn = models.CharField(max_length=100, blank=True, null=True, default='')
    tax = models.FloatField(default=0.0)
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.hsn

    class Meta:
        verbose_name_plural = 'g) HSN List'


class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    hsnID = models.ForeignKey(Hsn, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True, default='N/A')
    price = models.FloatField(default=0.0)
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'h) Category List'


class WareHouse(models.Model):
    wareHouseName = models.CharField(max_length=200, blank=True, null=True, default='')
    wareHouseAddress = models.CharField(max_length=100, blank=True, null=True, default='')
    datetime = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.wareHouseName

    class Meta:
        verbose_name_plural = 'i) Ware House List'


class Unit(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'j) Unit List'


class Product(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    brand = models.CharField(max_length=100, blank=True, null=True, default='')
    categoryID = models.ForeignKey(Category, blank=True, null=True)
    mrp = models.FloatField(default=0.0)
    cost = models.FloatField(default=0.0)
    spWithoutGst = models.FloatField(default=0.0)
    spWithGst = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    discountPc = models.FloatField(default=0.0)
    barcode = models.CharField(max_length=100, blank=True, null=True, default='')
    status = models.CharField(max_length=100, blank=True, null=True, default='')
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    company_ID = models.ForeignKey(CompanyProfile, blank=True, null=True)
    wareHouse_ID = models.ForeignKey(WareHouse, blank=True, null=True)
    unitID = models.ForeignKey(Unit, blank=True, null=True)
    warningStockLimit = models.IntegerField(default=0)
    productType = models.CharField(max_length=100, blank=True, null=True, default='')
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'k) Product List'


class ProductBatch(models.Model):
    productID = models.ForeignKey(Product, blank=True, null=True)
    batchNumber = models.CharField(max_length=200, default='N/A')
    quantity = models.FloatField(default=0.0)
    rate = models.FloatField(default=0.0)
    mrp = models.FloatField(default=0.0)
    mDate = models.DateField(blank=True, null=True)
    eDate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    additionalDetail = models.CharField(max_length=500, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.batchNumber

    class Meta:
        verbose_name_plural = 't) Product Batch List'

class Expense(models.Model):
    expenseType = models.CharField(max_length=200, default='N/A')
    description = models.CharField(max_length=500, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    expenseDate = models.DateField(blank=True, null=True)
    companyID = models.ForeignKey(CompanyProfile, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.expenseType

    class Meta:
        verbose_name_plural = 'l) Expense List'


class CompanyUser(models.Model):
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
    company_ID = models.ForeignKey(CompanyProfile)
    user_ID = models.ForeignKey(User, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'm) Company User List'


class Purchase(models.Model):
    supplierID = models.ForeignKey(Supplier, blank=True, null=True)
    supplierName = models.CharField(max_length=200, blank=True, null=True)
    supplierGst = models.CharField(max_length=200, blank=True, null=True)
    supplierPhone = models.CharField(max_length=200, blank=True, null=True)
    supplierEmail = models.CharField(max_length=200, blank=True, null=True)
    supplierAddress = models.CharField(max_length=500, blank=True, null=True)
    supplierState = models.CharField(max_length=200, blank=True, null=True)
    purchaseType = models.CharField(max_length=200, blank=True, null=True)
    paymentType = models.CharField(max_length=200, blank=True, null=True)
    creditDays = models.IntegerField(default=0)
    invoiceNumber = models.CharField(max_length=200, blank=True, null=True)
    invoiceDate = models.DateField(blank=True, null=True)
    taxable = models.FloatField(default=0.0)
    gst = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    status = models.BooleanField(default=True)
    paidDate = models.DateField(blank=True, null=True)
    chequeDetail = models.CharField(max_length=500, blank=True, null=True)
    companyID = models.ForeignKey(CompanyProfile, blank=True, null=True)
    addedBy = models.ForeignKey(User, blank=True, null=True)
    deliveryNote = models.CharField(max_length=500, blank=True, null=True)
    supplierReference = models.CharField(max_length=500, blank=True, null=True)
    buyersOrderNumber = models.CharField(max_length=500, blank=True, null=True)
    dispatchDocumentNumber = models.CharField(max_length=500, blank=True, null=True)
    dispatchThrough = models.CharField(max_length=500, blank=True, null=True)
    otherReference = models.CharField(max_length=500, blank=True, null=True)
    dispatchNoteDate = models.CharField(max_length=500, blank=True, null=True)
    destination = models.CharField(max_length=500, blank=True, null=True)
    otherCharges = models.FloatField(default=0.0)
    roundOff = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.supplierName

    class Meta:
        verbose_name_plural = 'n) Purchase List'


class PurchaseProduct(models.Model):
    purchaseID = models.ForeignKey(Purchase, blank=True, null=True)
    productID = models.ForeignKey(Product, blank=True, null=True)
    productName = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    hsn = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=200, blank=True, null=True)
    rate = models.FloatField(default=0.0)
    gst = models.FloatField(default=0.0)
    netRate = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.productName


class Sales(models.Model):
    customerID = models.ForeignKey(Customer, blank=True, null=True)
    customerName = models.CharField(max_length=200, blank=True, null=True)
    customerGst = models.CharField(max_length=200, blank=True, null=True)
    customerPhone = models.CharField(max_length=200, blank=True, null=True)
    customerEmail = models.CharField(max_length=200, blank=True, null=True)
    customerAddress = models.CharField(max_length=500, blank=True, null=True)
    customerState = models.CharField(max_length=200, blank=True, null=True)
    salesType = models.CharField(max_length=200, blank=True, null=True)
    paymentType = models.CharField(max_length=200, blank=True, null=True)
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

    def __str__(self):
        return self.customerName

    class Meta:
        verbose_name_plural = 'o) Sales List'


class SalesProduct(models.Model):
    salesID = models.ForeignKey(Sales, blank=True, null=True)
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

    def __str__(self):
        return self.productName


class UserPrinterSetting(models.Model):
    printerID = models.ForeignKey(PrinterSetting, default=1)
    userID = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'p) User Printer Setting List'


# class SalesReturn(models.Model):
#     salesID = models.ForeignKey(Sales, blank=True, null=True)
#     quantity = models.IntegerField(default=0)
#     return_amount = models.FloatField(default=0.0)
#     datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
#     lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)


class PaymentHistory(models.Model):
    salesID = models.ForeignKey(Sales, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    addedBy = models.ForeignKey(User, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Q) Payment History List'


class SalesLater(models.Model):
    customerID = models.ForeignKey(Customer, blank=True, null=True)
    customerName = models.CharField(max_length=200, blank=True, null=True)
    customerGst = models.CharField(max_length=200, blank=True, null=True)
    customerPhone = models.CharField(max_length=200, blank=True, null=True)
    customerEmail = models.CharField(max_length=200, blank=True, null=True)
    customerAddress = models.CharField(max_length=500, blank=True, null=True)
    customerState = models.CharField(max_length=200, blank=True, null=True)
    salesType = models.CharField(max_length=200, blank=True, null=True)
    paymentType = models.CharField(max_length=200, blank=True, null=True)
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

    def __str__(self):
        return self.customerName

    class Meta:
        verbose_name_plural = 'R) Booking List'


class SalesLaterProduct(models.Model):
    salesID = models.ForeignKey(SalesLater, blank=True, null=True)
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

    def __str__(self):
        return self.productName


class Referrer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    balance = models.FloatField(default=0.0)
    commission = models.FloatField(default=0.0)
    phone = models.CharField(max_length=200, blank=True, null=True, default='')
    address = models.TextField(blank=True, null=True, default='')
    email = models.CharField(max_length=200, blank=True, null=True, default='')
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R) Referrer List'


class ReferrerTransaction(models.Model):
    referrerID = models.ForeignKey(Referrer, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    transactionType = models.CharField(max_length=100, blank=True, null=True)
    addedBy = models.ForeignKey(User, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    transactionDate = models.DateField(blank=True, null=True)
    isDeleted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.referrerID.name

    class Meta:
        verbose_name_plural = 'S) Referrer Transaction'


class SalesReturn(models.Model):
    salesID =  models.ForeignKey(Sales, blank=True, null=True)
    addedBy = models.ForeignKey(User, blank=True, null=True)
    totalAmount = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = 'T) Sales Return'


class SalesReturnProduct(models.Model):
    salesReturnID = models.ForeignKey(SalesReturn, blank=True, null=True)
    productID = models.ForeignKey(SalesProduct, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    rate = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    lastUpdatedOn = models.DateTimeField(auto_now_add=False, auto_now=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.productID.productName

    class Meta:
        verbose_name_plural = 'T) Sales Return Products'