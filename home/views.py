from django.core import management
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.template import loader
from django.template.defaultfilters import register
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from datetime import datetime, timedelta

from activation.models import Validity
from activation.views import is_activated
from home.numberToWord import num2words
from .models import *

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape


@register.filter('has_group')
def has_group(user, group_name):
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False


@register.simple_tag()
def multiply(qty, price, dis ,*args, ** kwargs):
    t = round(price - price * (dis / 100.0),2)
    return round(qty * t,2)

# ----------------- html Views--------------------------
# ----------------- html Views--------------------------
def print_invoice(request, *args, **kwargs):
    query = request.GET.get('q')

    sale = Sales.objects.get(pk=int(query))
    saleProductMain = SalesProduct.objects.filter(salesID=int(query))
    saleProduct =[]
    for a in saleProductMain:
        n_rate = (a.netRate / (1 + (a.gst/100)))
        t_gst = (n_rate * (a.gst/100.0))* a.quantity
        cA = round(t_gst/2, 2)
        sA = round(t_gst/2, 2)
        tA = round((a.total + cA + sA), 2)
        prod_dic ={
            'hsn':a.hsn,
            'name':a.productName,
            'quantity':str(a.quantity) +' '+ a.unit ,
            'rate':a.rate,
            'disc': a.disc,
            'tax':a.gst,
            'taxableAmount':round(a.total,2),
            'cgst':a.gst/2,
            'cgstAmount':cA,
            'sgst':a.gst/2,
            'sgstAmount':sA,
            'total':tA

        }
        saleProduct.append(prod_dic)




    context = {
        'query': query,
        'sale': sale,
        'saleProduct': saleProduct,
        'left': 12 - saleProductMain.count(),
        'loo': str().zfill(10 - saleProductMain.count()-1),
        'IGST': round(sale.gst / 2,2),
        'CGST': round(sale.gst / 2,2),
        'TotalInWords': num2words(int(sale.grandTotal))


    }
    return render(request, 'home/invoice.html', context)

def print_invoicea5(request, *args, **kwargs):
    query = request.GET.get('q')

    sale = Sales.objects.get(pk=int(query))
    saleProductMain = SalesProduct.objects.filter(salesID=int(query))
    saleProduct = []
    for a in saleProductMain:
        n_rate = (a.netRate / (1 + (a.gst/100)))
        t_gst = (n_rate * (a.gst/100.0))* a.quantity
        cA = round(t_gst/2, 2)
        sA = round(t_gst/2, 2)
        tA = round((a.total + cA + sA), 2)
        prod_dic = {
            'hsn': a.hsn,
            'name': a.productName,
            'quantity': str(a.quantity) + ' ' + a.unit,
            'rate': a.rate,
            'disc': a.disc,
            'tax': a.gst,
            'taxableAmount': round(a.total, 2),
            'cgst': a.gst / 2,
            'cgstAmount': cA,
            'sgst': a.gst / 2,
            'sgstAmount': sA,
            'total': tA

        }
        saleProduct.append(prod_dic)

    context = {
        'query': query,
        'sale': sale,
        'saleProduct': saleProduct,
        'left': 12 - saleProductMain.count(),
        'loo': str().zfill(10 - saleProductMain.count() - 1),
        'IGST': round(sale.gst / 2, 2),
        'CGST': round(sale.gst / 2, 2),
        'TotalInWords': num2words(int(sale.grandTotal))

    }
    return render(request, 'home/Printinvoicea5.html', context)



def print_bill(request, *args, **kwargs):
    query = request.GET.get('q')

    sale = Sales.objects.get(pk=int(query))
    saleProduct = SalesProduct.objects.filter(salesID=int(query))

    context = {
        'query': query,
        'sale': sale,
        'saleProduct': saleProduct,
        'left': 13 - saleProduct.count(),
        'loo': str().zfill(12 - saleProduct.count() - 1),
        'IGST': round(sale.gst / 2, 2),
        'CGST': round(sale.gst / 2, 2),
        'TotalInWords': num2words(int(sale.grandTotal))

    }
    return render(request, 'home/billPrint.html', context)


def print_billA5(request, *args, **kwargs):
    query = request.GET.get('q')

    sale = Sales.objects.get(pk=int(query))
    saleProduct = SalesProduct.objects.filter(salesID=int(query))

    context = {
        'query': query,
        'sale': sale,
        'saleProduct': saleProduct,
        'left': 11 - saleProduct.count(),
        'loo': str().zfill(11 - saleProduct.count()-1),
        'IGST': round(sale.gst / 2,2),
        'CGST': round(sale.gst / 2,2),
        'TotalInWords': num2words(int(sale.grandTotal))


    }
    return render(request, 'home/billPrintA5.html', context)

def print_bill_thermal(request, *args, **kwargs):
    query = request.GET.get('q')

    sale = Sales.objects.get(pk=int(query))
    saleProduct = SalesProduct.objects.filter(salesID=int(query))

    context = {
        'query': query,
        'sale': sale,
        'saleProduct': saleProduct,
    }
    return render(request, 'home/thermalBillPrint.html', context)


def homepage(request):
    if request.user.is_authenticated:
        try:
            val = Validity.objects.last()
            message = "Your License is Valid till {}".format(val.expiryDate.strftime('%d-%m-%Y'))
        except:
            message = "You are using a trial version."

        context = {
            'message': message
        }

        return render(request, 'home/main.html', context)
    else:
        return redirect('/loginPage/')


def index(request):
    return render(request, 'home/index.html')


@is_activated()
def sales(request):
    if request.user.is_authenticated:
        # if request.groups.filter(name='Staff').is_authenticated:

        if 'Admin' in request.user.groups.values_list('name', flat=True):
            company = CompanyProfile.objects.filter(isDeleted__exact=False)
        else:
            user = CompanyUser.objects.get(user_ID_id=request.user.pk)
            company = CompanyProfile.objects.filter(pk=user.company_ID_id, isDeleted__exact=False)

        context = {
            'company': company,
        }

        return render(request, 'home/sales.html', context)
    else:
        return redirect('homeApp:loginPage')


@is_activated()
def puchase(request):
    if request.user.is_authenticated:

        if 'Admin' in request.user.groups.values_list('name', flat=True):
            company = CompanyProfile.objects.filter(isDeleted__exact=False)
        else:
            user = CompanyUser.objects.get(user_ID_id=request.user.pk)
            company = CompanyProfile.objects.filter(pk=user.company_ID_id, isDeleted__exact=False)

        context = {

            'company': company,
        }
        return render(request, 'home/purchase.html', context)
    else:
        return redirect('homeApp:loginPage')


@is_activated()
def product(request):
    if request.user.is_authenticated:
        return render(request, 'home/product.html')
    else:
        return redirect('homeApp:loginPage')


@is_activated()
def hsn_and_category(request):
    if request.user.is_authenticated:
        return render(request, 'home/hsn&category.html')
    else:
        return redirect('homeApp:loginPage')


@is_activated()
def salesReport(request):
    return render(request, 'home/salesReport.html')


@is_activated()
def bookingList(request):
    return render(request, 'home/bookingList.html')

@is_activated()
def purchaseReport(request):
    return render(request, 'home/purchaseReport.html')


@is_activated()
def contact(request):
    return render(request, 'home/contact.html')

@is_activated()
def referrer(request):
    return render(request, 'home/referrer.html')

@is_activated()
def generalSetting(request):
    printers = PrinterSetting.objects.filter(isDeleted__exact=False).order_by('size')
    try:
        u_p = UserPrinterSetting.objects.get(userID_id=request.user.pk)
        p = u_p.printerID_id
    except:
        p = 1
    context = {
        'printers': printers,
        'myPrinter': p
    }

    return render(request, 'home/generalsetting.html', context)


@is_activated()
def settings(request):
    # if request.user.is_authenticated:
    users_in_group = Group.objects.get(name="Admin").user_set.all()
    if request.user in users_in_group:
        # if request.user.is_authenticated:
        companyList = CompanyProfile.objects.all()

        context = {
            'details': companyList
        }
        return render(request, 'home/settings.html', context)
    else:
        return redirect('homeApp:loginPage')


@is_activated()
def manage_invoice(request):
    if 'Admin' in request.user.groups.values_list('name', flat=True):
        company = CompanyProfile.objects.filter(isDeleted__exact=False)
    else:
        user = CompanyUser.objects.get(user_ID_id=request.user.pk)
        company = CompanyProfile.objects.filter(pk=user.company_ID_id, isDeleted__exact=False)

    context = {

        'company': company,
    }
    return render(request, 'home/manageInvoice.html', context)


@is_activated()
def expense(request):
    if 'Admin' in request.user.groups.values_list('name', flat=True):
        company = CompanyProfile.objects.filter(isDeleted__exact=False)
    else:
        user = CompanyUser.objects.get(user_ID_id=request.user.pk)
        company = CompanyProfile.objects.filter(pk=user.company_ID_id, isDeleted__exact=False)

    context = {

        'company': company,
    }
    return render(request, 'home/expense.html', context)


@is_activated()
def manageUser(request):
    return render(request, 'home/ManageUser.html')


@is_activated()
def wareHouseList(request):
    return render(request, 'home/wareHouse.html')


def loginPage(request):
    if not request.user.is_authenticated:
        return render(request, 'home/log.html')
    else:
        return redirect('/')


@is_activated()
def dashboard(request):
    if request.user.is_authenticated:
        # purchase
        purchases = Purchase.objects.filter(datetime__contains=datetime.today().date(),
                                            isDeleted__exact=False).aggregate(Sum('total'))
        if purchases['total__sum'] is None:
            p = 0
        else:
            p = purchases['total__sum']

        # sales
        sales = Sales.objects.filter(datetime__contains=datetime.today().date(), isDeleted__exact=False).aggregate(
            Sum('grandTotal'))
        if sales['grandTotal__sum'] is None:
            s = 0
        else:
            s = sales['grandTotal__sum']

        # expenses
        expenses = Expense.objects.filter(datetime__contains=datetime.today().date(), isDeleted__exact=False).aggregate(
            Sum('amount'))
        if expenses['amount__sum'] is None:
            e = 0
        else:
            e = expenses['amount__sum']
        # new customer
        new_customer = Customer.objects.filter(datetime__contains=datetime.today().date(),
                                               isDeleted__exact=False).count()

        # total Sales Count
        sales_count = Sales.objects.filter(isDeleted__exact=False).count()
        purchase_count = Purchase.objects.filter(isDeleted__exact=False).count()
        customer_count = Customer.objects.filter(isDeleted__exact=False).count()
        supplier_count = Supplier.objects.filter(isDeleted__exact=False).count()

        context = {
            'purchases': p,
            'sales': s,
            'expenses': e,
            'new_customer': new_customer,
            'sales_count': sales_count,
            'purchase_count': purchase_count,
            'customer_count': customer_count,
            'supplier_count': supplier_count,
        }

        return render(request, 'home/dahboard.html', context)
    else:
        return redirect('/')


@is_activated()
def report(request):
    if 'Admin' in request.user.groups.values_list('name', flat=True):
        company = CompanyProfile.objects.filter(isDeleted__exact=False)
    else:
        user = CompanyUser.objects.get(user_ID_id=request.user.pk)
        company = CompanyProfile.objects.filter(pk=user.company_ID_id, isDeleted__exact=False)

    context = {
        'company': company,
    }
    return render(request, 'home/report.html', context)


@is_activated()
def customer_ledger(request, id=None):
    instance = get_object_or_404(Customer, pk=id)
    sale = Sales.objects.filter(customerID_id=instance.pk, isDeleted__exact=False, salesType__icontains='Normal')
    paid = 0.0
    total = 0.0
    for s in sale:
        paid = paid + s.paidAgainstBill
        total = total + s.grandTotal
    sale_j = Sales.objects.filter(customerID_id=instance.pk, isDeleted__exact=False, salesType__icontains='jet')
    paid_j = 0.0
    total_j = 0.0
    for s_j in sale_j:
        paid_j = paid_j + s_j.paidAgainstBill
        total_j = total_j + s_j.grandTotal
    context = {
        'instance': instance,
        'due': total - paid,
        'paid': paid,
        'total': total,
        'due_j': total_j - paid_j,
        'paid_j': paid_j,
        'total_j': total_j,
    }

    return render(request, 'home/customerLedger.html', context)


@is_activated()
def supplier_ledger(request, id=None):
    instance = get_object_or_404(Supplier, pk=id)
    pur = Purchase.objects.filter(supplierID_id=instance.pk, isDeleted__exact=False)
    due = 0.0
    paid = 0.0
    total = 0.0
    for s in pur:
        if s.status == False:
            due = due + s.total
            total = total + s.total
        else:
            paid = paid + s.total
            total = total + s.total

    context = {
        'instance': instance,
        'due': due,
        'paid': paid,
        'total': total,
    }

    return render(request, 'home/supplierLedger.html', context)


@is_activated()
def referrer_ledger(request, id=None):
    instance = get_object_or_404(Referrer, pk=id)
    ref = ReferrerTransaction.objects.filter(referrerID_id=instance.pk, isDeleted__exact=False, transactionType__icontains='Credit')
    total = 0.0
    for s in ref:
        total = total + s.amount
    refD = ReferrerTransaction.objects.filter(referrerID_id=instance.pk, isDeleted__exact=False, transactionType__icontains='Debit')
    total_j = 0.0
    for s_j in refD:
        total_j = total_j + s_j.amount
    context = {
        'instance': instance,
        'totalCredit': total,
        'totalDebit': total_j,
    }

    return render(request, 'home/referrerLedger.html', context)


# --------------------api-------------------------------


def post_customer(request):
    if request.method == 'POST':
        cname = request.POST.get("cname")
        cemail = request.POST.get("cemail")
        caddress = request.POST.get("caddress")
        cgst = request.POST.get("cgst")
        cstate = request.POST.get("cstate")
        cphone = request.POST.get("cphone")

        cus = Customer()
        cus.name = cname
        cus.email = cemail
        cus.address = caddress
        cus.gst = cgst
        cus.state = cstate
        cus.phone = cphone
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


def get_customer_list(request):
    data = []
    q = request.GET.get('q')
    for cus in Customer.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(gst__icontains=q),
                                       isDeleted__exact=False).order_by('name'):
        data_dic = {
            'ID': cus.pk,
            'Name': '#{}|'.format(cus.pk) + cus.name.upper(),
            'Address': cus.address,
            'Gst': cus.gst,

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_customer_detail(request, id=None):
    instance = get_object_or_404(Customer, pk=id)
    data = {
        'ID': instance.pk,
        'Name': instance.name,
        'Email': instance.email,
        'Address': instance.address,
        'Gst': instance.gst,
        'Phone': instance.phone,
        'State': instance.state

    }
    return JsonResponse({'data': data}, safe=False)


def get_customer_detail_by_name(request):
    q = request.GET.get('q')

    try:
        instance = Customer.objects.get(pk=int(q), isDeleted__exact=False)
        try:
            lastSale = Sales.objects.filter(customerID_id=instance.pk).order_by('-datetime').first()
            saleID = lastSale.pk
        except:
            saleID = 'N/A'

        data = {
            'ID': instance.pk,
            'Name': instance.name,
            'Email': instance.email,
            'Address': instance.address,
            'Gst': instance.gst,
            'Phone': instance.phone,
            'State': instance.state,
            'SaleID': saleID

        }
    except:
        data = {
            'ID': '',
            'Name': '',
            'Email': '',
            'Address': '',
            'Gst': '',
            'Phone': '',
            'State': '',
            'SaleID': 'N/A'

        }

    return JsonResponse({'data': data}, safe=False)


def edit_customer(request):
    if request.method == 'POST':
        idC = request.POST.get("idC")
        cname = request.POST.get("cname")
        cemail = request.POST.get("cemail")
        caddress = request.POST.get("caddress")
        cgst = request.POST.get("cgst")
        cstate = request.POST.get("cstate")
        cphone = request.POST.get("cphone")

        cus = Customer.objects.get(pk=int(idC))
        cus.name = cname
        cus.email = cemail
        cus.address = caddress
        cus.gst = cgst
        cus.state = cstate
        cus.phone = cphone
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_customer(request):
    if request.method == 'POST':
        idC = request.POST.get("userID")

        cus = Customer.objects.get(pk=int(idC))
        cus.isDeleted = True
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


def post_supplier(request):
    if request.method == 'POST':
        sname = request.POST.get("sname")
        semail = request.POST.get("semail")
        saddress = request.POST.get("saddress")
        sgst = request.POST.get("sgst")
        sstate = request.POST.get("sstate")
        sphone = request.POST.get("sphone")

        sup = Supplier()
        sup.name = sname
        sup.email = semail
        sup.address = saddress
        sup.gst = sgst
        sup.state = sstate
        sup.phone = sphone
        sup.save()
        return JsonResponse({'message': 'success'}, safe=False)


def get_supplier_list(request):
    data = []
    q = request.GET.get('q')
    for sup in Supplier.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(gst__icontains=q),
                                       isDeleted__exact=False).order_by('name'):
        data_dic = {
            'ID': sup.pk,
            'Name': sup.name,
            'Address': sup.address,
            'Gst': sup.gst,

        }
        data.append(data_dic)

    return JsonResponse({'data': data}, safe=False)


def get_supplier_detail(request, id=None):
    instance = get_object_or_404(Supplier, pk=id)
    data = {
        'ID': instance.pk,
        'Name': instance.name,
        'Email': instance.email,
        'Address': instance.address,
        'Gst': instance.gst,
        'Phone': instance.phone,
        'State': instance.state

    }
    return JsonResponse({'data': data}, safe=False)


def get_supplier_detail_by_name(request):
    q = request.GET.get('q')

    try:
        instance = Supplier.objects.get(pk=int(q), isDeleted__exact=False)
        data = {
            'ID': instance.pk,
            'Name': instance.name,
            'Email': instance.email,
            'Address': instance.address,
            'Gst': instance.gst,
            'Phone': instance.phone,
            'State': instance.state

        }
    except:
        data = {
            'ID': '',
            'Name': '',
            'Email': '',
            'Address': '',
            'Gst': '',
            'Phone': '',
            'State': '',

        }

    return JsonResponse({'data': data}, safe=False)


def edit_supplier(request):
    if request.method == 'POST':
        idC = request.POST.get("idC")
        cname = request.POST.get("cname")
        cemail = request.POST.get("cemail")
        caddress = request.POST.get("caddress")
        cgst = request.POST.get("cgst")
        cstate = request.POST.get("cstate")
        cphone = request.POST.get("cphone")

        cus = Supplier.objects.get(pk=int(idC))
        cus.name = cname
        cus.email = cemail
        cus.address = caddress
        cus.gst = cgst
        cus.state = cstate
        cus.phone = cphone
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_supplier(request):
    if request.method == 'POST':
        idC = request.POST.get("userID")

        cus = Supplier.objects.get(pk=int(idC))
        cus.isDeleted = True
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


# hsn
@csrf_exempt
def post_hsn(request):
    if request.method == 'POST':
        hsn = request.POST.get("hsn")
        tax = request.POST.get("tax")
        try:
            Hsn.objects.get(hsn__iexact=hsn, isDeleted__exact=False)
            return JsonResponse({'message': 'HSN Already Exist'}, safe=False)
        except:
            h = Hsn()
            h.hsn = hsn
            h.tax = tax
            h.save()
            return JsonResponse({'message': 'success'}, safe=False)


def get_hsn_list(request):
    data = []
    q = request.GET.get('q')

    for h in Hsn.objects.filter(hsn__icontains=q, isDeleted__exact=False).order_by('-id'):
        data_dic = {
            'ID': h.pk,
            'Hsn': h.hsn,
            'Tax': h.tax,

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_hsn_detail(request, id=None):
    instance = get_object_or_404(Hsn, pk=id)
    data = {
        'ID': instance.pk,
        'HSN': instance.hsn,
        'Tax': instance.tax,

    }
    return JsonResponse({'data': data}, safe=False)


def edit_hsn(request):
    if request.method == 'POST':
        hsnID = request.POST.get("hsnID")
        hsn = request.POST.get("hsn")
        tax = request.POST.get("tax")

        hsnCount = Hsn.objects.filter(hsn__iexact=hsn, isDeleted__exact=False).exclude(pk=int(hsnID)).count()

        if hsnCount == 0:
            h = Hsn.objects.get(pk=int(hsnID), isDeleted__exact=False)
            h.hsn = hsn
            h.tax = tax
            h.save()

            return JsonResponse({'message': 'success'}, safe=False)
        else:
            return JsonResponse({'message': 'Already Exist'}, safe=False)


@csrf_exempt
def delete_hsn(request):
    if request.method == 'POST':
        idC = request.POST.get("ID")

        cus = Hsn.objects.get(pk=int(idC))
        cus.isDeleted = True
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


# category

def post_category(request):
    if request.method == 'POST':
        hsn = request.POST.get("hsn")
        category = request.POST.get("category")
        brand = request.POST.get("brand")
        price = request.POST.get("price")

        try:
            Category.objects.get(name__iexact=category, brand__iexact=brand, isDeleted__exact=False)
            return JsonResponse({'message': 'Category Already Exist'}, safe=False)
        except:

            try:

                hsnID = Hsn.objects.get(hsn__iexact=hsn)
                c = Category()
                c.name = category
                c.hsnID_id = hsnID.pk
                c.brand = brand
                c.price = float(price)
                c.save()
                return JsonResponse({'message': 'success'}, safe=False)

            except:

                return JsonResponse({'message': 'Invalid HSN Code.'}, safe=False)


def get_category_list(request):
    data = []
    q = request.GET.get('q')
    for c in Category.objects.filter(name__icontains=q, isDeleted__exact=False).order_by('-name'):
        data_dic = {
            'ID': c.pk,
            'Hsn': c.hsnID.hsn,
            'Category': c.name,
            'GST': c.hsnID.tax,

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_category_by_name(request):
    q = request.GET.get('q')
    tax = 0.0
    try:
        c = Category.objects.get(name__iexact=q, isDeleted__exact=False)
        tax = c.hsnID.tax
    except:
        tax = 0.0

    return JsonResponse({'data': tax}, safe=False)


def get_category_detail(request, id=None):
    instance = get_object_or_404(Category, pk=id)
    data = {
        'ID': instance.pk,
        'HSN': instance.hsnID.hsn,
        'CategoryName': instance.name,
        'Brand': instance.brand,
        'Price': instance.price,
        'GST': instance.hsnID.tax,

    }
    return JsonResponse({'data': data}, safe=False)


def edit_category(request):
    if request.method == 'POST':
        categoryID = request.POST.get("categoryID")
        hsn = request.POST.get("hsn")
        category = request.POST.get("Category")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        catCount = Category.objects.filter(name__iexact=category, brand__iexact=brand, isDeleted__exact=False).exclude(
            pk=int(categoryID)).count()

        if catCount == 0:
            try:
                hsnID = Hsn.objects.get(hsn__exact=hsn)
                c = Category.objects.get(pk=int(categoryID))
                c.name = category
                c.brand = brand
                c.price = float(price)
                c.hsnID_id = hsnID.pk
                c.save()
                return JsonResponse({'message': 'success'}, safe=False)

            except:

                return JsonResponse({'message': 'Invalid HSN Code.'}, safe=False)
        else:
            return JsonResponse({'message': 'Already Exist'}, safe=False)


@csrf_exempt
def delete_category(request):
    if request.method == 'POST':
        idC = request.POST.get("ID")

        cus = Category.objects.get(pk=int(idC))
        cus.isDeleted = True
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


# product

def post_product(request):
    if request.method == 'POST':
        pType = request.POST.get("pType")
        productName = request.POST.get("productName")
        brand = request.POST.get("brand")
        category = request.POST.get("category")
        mrp = request.POST.get("mrp")
        cost = request.POST.get("cost")
        sp = request.POST.get("sp")
        net = request.POST.get("net")
        stock = request.POST.get("stock")
        company = request.POST.get("company")
        wareHouse = request.POST.get("wareHouse")
        discount = request.POST.get("discount")
        barCode = request.POST.get("barCode")
        status = request.POST.get("status")
        unit = request.POST.get("unit")
        stockWarning = request.POST.get("stockWarning")

        p = Product()
        p.productType = pType
        p.name = productName
        p.brand = brand

        p.categoryID_id = int(category)
        p.mrp = mrp
        p.cost = cost
        p.spWithoutGst = sp
        p.spWithGst = net
        p.stock = stock
        p.warningStockLimit = stockWarning

        p.company_ID_id = int(company)
        p.wareHouse_ID_id = int(wareHouse)
        p.discountPc = discount
        p.barcode = barCode
        p.status = status
        p.unitID_id = int(unit)
        p.save()
        return JsonResponse({'message': 'success'}, safe=False)

        # except:
        #     return JsonResponse({'message': 'error'}, safe=False)


def get_product_list(request):
    data = []
    q = request.GET.get('q')
    r = request.GET.get('type')
    company = request.GET.get('company')
    if 'Admin' in request.user.groups.values_list('name', flat=True):
        instance = Product.objects.filter(Q(name__icontains=q) | Q(categoryID__name__icontains=q),

                                          isDeleted__exact=False,
                                          company_ID_id=int(company), productType__iexact=r).order_by('name')
    else:
        user = CompanyUser.objects.get(user_ID_id=request.user.pk)
        instance = Product.objects.filter(Q(name__icontains=q) | Q(categoryID__name__icontains=q),

                                          isDeleted__exact=False,
                                          company_ID_id=int(company), productType__iexact=r)

    for c in instance:
        data_dic = {
            'ID': c.pk,
            'ProductName': '{}({})'.format(c.name, c.categoryID.name, ),
            'Brand': '{} ({} ({}))'.format(c.brand, c.stock, c.unitID.name),
            'Company': 'Company Name:{} at WareHouse: {}'.format(c.company_ID.name, c.wareHouse_ID.wareHouseName)

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_product_detail_by_name(request):
    q = request.GET.get('q')
    pType = request.GET.get('pType')
    try:
        if 'Admin' in request.user.groups.values_list('name', flat=True):
            instance = Product.objects.get(pk__iexact=q, isDeleted__exact=False, productType__iexact=pType)
        else:
            user = CompanyUser.objects.get(user_ID_id=request.user.pk)
            instance = Product.objects.get(pk__iexact=q, isDeleted__exact=False,
                                           company_ID=user.company_ID_id, productType__iexact=pType)

        data = {
            'ID': instance.pk,
            'ProductName': instance.name,
            'Category': instance.categoryID.name,
            'Price': instance.cost,
            'Gst': instance.categoryID.hsnID.tax,
            'Hsn': instance.categoryID.hsnID.hsn,
            'Mrp': instance.mrp,
            'Stock': instance.stock,
            'ActualUnit': instance.unitID.name,
            'Sp': instance.spWithoutGst,
            'Net': instance.spWithGst,
            'BarCode':instance.barcode

        }
    except:
        data = {
            'ID': '',
            'ProductName': '',
            'Category': '',
            'Price': '',
            'Gst': '',
            'Hsn': '',
            'Mrp': '',
            'Stock': '',
            'ActualUnit': '',
            'Sp': '',
            'Net': '',
            'BarCode': '',

        }

    return JsonResponse({'data': data}, safe=False)



def get_product_detail_by_barcode(request):
    q = request.GET.get('q')
    pType = request.GET.get('pType')
    try:
        if 'Admin' in request.user.groups.values_list('name', flat=True):
            instance = Product.objects.get(barcode__iexact=q, isDeleted__exact=False, productType__iexact=pType)
        else:
            user = CompanyUser.objects.get(user_ID_id=request.user.pk)
            instance = Product.objects.get(barcode__iexact=q, isDeleted__exact=False,
                                           company_ID=user.company_ID_id, productType__iexact=pType)

        data = {
            'ID': instance.pk,
            'ProductName': instance.name,
            'Category': instance.categoryID.name,
            'Price': instance.cost,
            'Gst': instance.categoryID.hsnID.tax,
            'Hsn': instance.categoryID.hsnID.hsn,
            'Mrp': instance.mrp,
            'Stock': instance.stock,
            'ActualUnit': instance.unitID.name,
            'Sp': instance.spWithoutGst,
            'Net': instance.spWithGst,
            'BarCode':instance.barcode

        }
    except:
        data = {
            'ID': '',
            'ProductName': '',
            'Category': '',
            'Price': '',
            'Gst': '',
            'Hsn': '',
            'Mrp': '',
            'Stock': '',
            'ActualUnit': '',
            'Sp': '',
            'Net': '',
            'BarCode': '',

        }

    return JsonResponse({'data': data}, safe=False)




def get_product_detail(request, id=None):
    try:
        instance = get_object_or_404(Product, pk=id)
        data = {
            'ID': instance.pk,
            'Brand': instance.brand,
            'Category': instance.categoryID.name,
            'CatID': instance.categoryID.id,
            'Mrp': instance.mrp,
            'Cost': instance.cost,
            'Sp': instance.spWithoutGst,
            'Net': instance.spWithGst,
            'Stock': instance.stock,
            'Discount': instance.discountPc,
            'Barcode': instance.barcode,
            'Status': instance.status,
            'Company': instance.company_ID_id,
            'Warehouse': instance.wareHouse_ID_id,
            'Unit': instance.unitID_id,
            'ActualUnit': instance.unitID.name,
            'ProductType': instance.productType,
            'ProductName': instance.name,
            'Tax': instance.categoryID.hsnID.tax,
            'StockWarning': instance.warningStockLimit,

        }
        return JsonResponse({'data': data}, safe=False)
    except:
        data = {
            'ID': '',
            'Brand': '',
            'Category': '',
            'CatID': 'N/A',
            'Mrp': 0.0,
            'Cost': 0.0,
            'Sp': 0.0,
            'Net': 0.0,
            'Stock': 0,
            'Discount': 0.0,
            'Barcode': '',
            'Status': '',
            'Company': '',
            'Warehouse': '',
            'Unit': '',
            'ActualUnit': '',
            'ProductType': '',
            'ProductName': '',
            'Tax': '0',
            'StockWarning': 0

        }
        return JsonResponse({'data': data}, safe=False)


def edit_product(request):
    if request.method == 'POST':
        pID = request.POST.get("pID")
        pType = request.POST.get("pType")
        productName = request.POST.get("productName")
        brand = request.POST.get("brand")
        category = request.POST.get("category")
        mrp = request.POST.get("mrp")
        cost = request.POST.get("cost")
        sp = request.POST.get("sp")
        net = request.POST.get("net")
        stock = request.POST.get("stock")
        company = request.POST.get("company")
        wareHouse = request.POST.get("wareHouse")
        discount = request.POST.get("discount")
        barCode = request.POST.get("barCode")
        status = request.POST.get("status")
        unit = request.POST.get("unit")
        stockWarning = request.POST.get("stockWarning")

        p = Product.objects.get(pk=int(pID))
        p.productType = pType
        p.name = productName
        p.brand = brand

        p.categoryID_id = int(category)
        p.mrp = mrp
        p.cost = cost
        p.spWithoutGst = sp
        p.spWithGst = net
        p.stock = stock
        p.warningStockLimit = stockWarning

        p.company_ID_id = int(company)
        p.wareHouse_ID_id = int(wareHouse)
        p.discountPc = discount
        p.barcode = barCode
        p.status = status
        p.unitID_id = int(unit)
        p.save()
        return JsonResponse({'message': 'success'}, safe=False)

        # except:
        #     return JsonResponse({'message': 'error'}, safe=False)


@csrf_exempt
def delete_product(request):
    if request.method == 'POST':
        idC = request.POST.get("ID")

        cus = Product.objects.get(pk=int(idC))
        cus.isDeleted = True
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


def get_running_down_out_of_stock_product_list(request):
    pType = request.GET.get('pType')
    companyID = request.GET.get('companyID')

    if 'Admin' in request.user.groups.values_list('name', flat=True):
        instance = Product.objects.filter(productType__iexact=pType, isDeleted__exact=False,
                                          stock__lt=F('warningStockLimit'), company_ID_id=int(companyID)).order_by(
            'stock')
    else:
        user = CompanyUser.objects.get(user_ID_id=request.user.pk)
        instance = Product.objects.filter(productType__iexact=pType, isDeleted__exact=False,

                                          company_ID_id=int(companyID), stock__lt=F('warningStockLimit')).order_by(
            'stock')
    p_list = []
    for p in instance:
        data = {
            'ID': p.pk,
            'ProductName': p.name + ' ({})'.format(p.brand),
            'Stock': str(p.stock) + ' ({})'.format(p.unitID.name),

        }

        p_list.append(data)
    return JsonResponse({'data': p_list}, safe=False)


def get_last_selling_price_of_the_product_by_customer(request):
    pID = request.GET.get('pID')
    cID = request.GET.get('cID')

    try:
        lastSale = SalesProduct.objects.filter(salesID__customerID_id=int(cID), productID_id=int(pID)).order_by(
            '-id').first()
        return JsonResponse({'data': "#LSP(₹ {})".format(lastSale.rate)}, safe=False)
    except:
        return JsonResponse({'data': "#LSP(₹ N/A)"}, safe=False)


def get_bank_detail(request, id=None):
    company = get_object_or_404(CompanyProfile, id=id)
    instance = BankDetails.objects.get(companyID_id=company.pk)
    # getCetogory = Category.objects.get(pk=int(instance.categoryID))
    # hsn = Hsn.objects.get(pk=int(getCetogory.hsnID))
    data = {
        'ID': instance.pk,
        'AccHolder': instance.accHolderName,
        'AccNumber': instance.accNo,
        'Branch': instance.branch,
        'AccType': instance.accountType,
        'ifscCode': instance.ifsc,
        'HolderAddress': instance.bankAddress,

    }
    return JsonResponse({'data': data}, safe=False)


def get_Company_detail(request, id=None):
    company = get_object_or_404(CompanyProfile, id=id)
    instance = BankDetails.objects.get(companyID_id=company.pk)

    data = {
        'ID': company.pk,
        'EditCompanyName': company.name,
        'EditGstNo': company.gst,
        'EditCompanyPhone': company.phone,
        'EditCompanyEmail': company.email,
        'EditCompanyAddress': company.address,
        'EditZip': company.zip,
        'EditState': company.state,
        'EditCity': company.city,
        'EditAccountHolderName': instance.accHolderName,
        'EditBankName': instance.bankName,
        'EditBranch': instance.branch,
        'EditAccount_type': instance.accountType,
        'EditAccountNo': instance.accNo,
        'EDitIfsc': instance.ifsc,
        'EditBankAddress': instance.bankAddress,

    }
    return JsonResponse({'data': data}, safe=False)


# ------------------------ Datatables api------------------------


class CustomerListJson(BaseDatatableView):
    order_columns = ['name', 'gst', 'phone', ]

    def get_initial_queryset(self):

        return Customer.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(gst__icontains=search) | Q(phone__icontains=search)).order_by('-name')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<a href="/contact/customer_ledger/{}/" style="font-size:10px;"  class="ui circular facebook icon button violet">
                 <i class="scroll icon"></i>
               </a>
               
               <button style="font-size:10px;" onclick = "GetCustomerDetail('{}')" class="ui circular facebook icon button green">
                 <i class="pen icon"></i>
               </button>
        
               <button style="font-size:10px;" onclick ="delCustomer('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                 <i class="trash alternate icon"></i>
               </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<a href="/contact/customer_ledger/{}/" style="font-size:10px;"  class="ui circular facebook icon button violet">
                 <i class="scroll icon"></i>
               </a>
               
              '''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.gst),
                escape(item.phone),
                action,

            ])
        return json_data


class SupplierListJson(BaseDatatableView):
    order_columns = ['name', 'gst', 'phone', ]

    def get_initial_queryset(self):

        return Supplier.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(gst__icontains=search) | Q(phone__icontains=search)).order_by('-name')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''
                <a href="/contact/supplier_ledger/{}/" style="font-size:10px;" class="ui circular facebook icon button violet">
                 <i class="scroll icon"></i>
               </a>
                
                <button style="font-size:10px;" onclick = "GetSupplierDetail('{}')" class="ui circular facebook icon button green">
                                 <i class="pen icon"></i>
                               </button>
    
                               <button style="font-size:10px;" onclick ="delSupplier('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                                 <i class="trash alternate icon"></i>
                               </button>'''.format(item.pk, item.pk, item.pk)
            else:
                action = '''
                <a href="/contact/supplier_ledger/{}/" style="font-size:10px;" class="ui circular facebook icon button violet">
                 <i class="scroll icon"></i>
               </a>
                
                '''.format(item.pk, item.pk, item.pk)
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.gst),
                escape(item.phone),
                action,

            ])
        return json_data


class HsnListJson(BaseDatatableView):
    order_columns = ['hsn', 'tax', ]

    def get_initial_queryset(self):

        return Hsn.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(hsn__icontains=search) | Q(tax__icontains=search)).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<button style="font-size:10px;" onclick = "GetHSNDetail('{}')" class="ui circular facebook icon button green">
                                                 <i class="pen icon"></i>
                                               </button>
    
                                               <button style="font-size:10px;" onclick ="delHSN('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                                                 <i class="trash alternate icon"></i>
                                               </button></td>'''.format(item.pk, item.pk)
            else:
                action = '<button class="mini ui button">Denied</button>'
            json_data.append([
                escape(item.hsn),  # escape HTML for security reasons
                escape(item.tax),
                action

            ])
        return json_data


class CategoryListJson(BaseDatatableView):
    order_columns = ['name', 'brand', 'price', 'hsnID', ]

    def get_initial_queryset(self):

        return Category.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(hsnID__hsn__icontains=search) | Q(brand__icontains=search) | Q(price__icontains=search) | Q(
                    hsnID__tax__icontains=search) | Q(name__icontains=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<button style="font-size:10px;" onclick = "GetCategoryDetail('{}')" class="ui circular facebook icon button green">
                <i class="pen icon"></i>
              </button>

              <button style="font-size:10px;" onclick ="delCategory('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                <i class="trash alternate icon"></i>
              </button></td>'''.format(item.pk, item.pk)
            else:
                action = '<button class="mini ui button">Denied</button>'
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.brand),  # escape HTML for security reasons
                escape(item.price),  # escape HTML for security reasons
                escape(item.hsnID.hsn),
                action

            ])
        return json_data


# done
class ProductListJson(BaseDatatableView):
    order_columns = ['name', 'brand', 'categoryID', 'mrp',
                     'cost', 'spWithoutGst', 'spWithGst', 'stock', 'warningStockLimit', 'unitID', 'company_ID',
                     'wareHouse_ID'
                     'discountPc', 'barcode',
                     'status', 'productType'
                     ]

    def get_initial_queryset(self):
        if 'Admin' in self.request.user.groups.values_list('name', flat=True):

            return Product.objects.filter(wareHouse_ID__isDeleted__exact=False, company_ID__isDeleted__exact=False,
                                          isDeleted__exact=False)
        else:
            user = CompanyUser.objects.get(user_ID_id=self.request.user.pk)
            return Product.objects.filter(wareHouse_ID__isDeleted__exact=False, company_ID__isDeleted__exact=False,
                                          isDeleted__exact=False, company_ID_id=user.company_ID_id,
                                          productType__iexact='Normal')

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(brand__icontains=search)
                | Q(categoryID__name__icontains=search) | Q(mrp__icontains=search)
                | Q(cost__icontains=search) | Q(spWithoutGst__icontains=search)
                | Q(spWithGst__icontains=search) | Q(stock__icontains=search)
                | Q(company_ID__name__icontains=search) | Q(wareHouse_ID__wareHouseName__icontains=search)
                | Q(discountPc__icontains=search) | Q(barcode__icontains=search)
                | Q(status__icontains=search) | Q(productType__icontains=search) | Q(unitID__name__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.company_ID is None:
                company = 'N/A'
            else:
                company = item.company_ID.name
            if item.wareHouse_ID is None:
                wareHouse = 'N/A'
            else:
                wareHouse = item.wareHouse_ID.wareHouseName

            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''
                <button data-content="Manage Batch" style="font-size:10px;" onclick = "openProductBatch('{}')" class="ui circular server icon button blue">
                                               <i class="server icon"></i>
                                             </button>
                
                <button style="font-size:10px;" onclick = "GetProductDetail('{}')" class="ui circular facebook icon button green">
                                               <i class="pen icon"></i>
                                             </button>

                                             <button style="font-size:10px;" onclick ="delProduct('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                                               <i class="trash alternate icon"></i>
                                             </button></td>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '<button class="mini ui button">Denied</button>'

            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.brand),
                escape(item.categoryID.name),
                escape(item.mrp),
                escape(item.cost),
                escape(item.spWithoutGst),
                escape(item.spWithGst),
                escape(item.stock),
                escape(item.warningStockLimit),
                escape(item.unitID.name),
                company,
                wareHouse,
                escape(item.discountPc),
                escape(item.barcode),
                escape(item.status),
                escape(item.productType),
                action,

            ])
        return json_data


class CompanyListJson(BaseDatatableView):
    order_columns = ['name', 'gst', 'city', 'zip',
                     'state', 'phone', 'address', 'email',
                     ]

    def get_initial_queryset(self):

        return CompanyProfile.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(gst__icontains=search)
                | Q(city__icontains=search) | Q(zip__icontains=search)
                | Q(state__icontains=search) | Q(phone__icontains=search)
                | Q(address__icontains=search) | Q(email__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.gst),
                escape(item.city),
                escape(item.zip),
                escape(item.state),
                escape(item.phone),
                escape(item.address),
                escape(item.email),
                '''<button style="font-size:10px;" onclick = "GetCompanyDetails('{}')" class="ui circular facebook icon button green">
  <i class="pen icon"></i>
</button>
<button style="font-size:10px;" onclick = "GetBankDetails('{}')" class="ui circular facebook icon button teal" style="margin-left: 3px">
  <i class="bars icon"></i>
</button>
<button style="font-size:10px;" onclick ="delCompany('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
  <i class="trash alternate icon"></i>
</button></td>'''.format(item.pk, item.pk,
                         item.pk),

            ])
        return json_data


class UserListJson(BaseDatatableView):
    order_columns = ['name', 'username', 'userPassword', 'phone', 'address', 'city',
                     'zip', 'state', 'email', 'company_ID','target'
                     ]

    def get_initial_queryset(self):

        return CompanyUser.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(username__icontains=search) | Q(userPassword__icontains=search) | Q(name__icontains=search) | Q(
                    phone__icontains=search)
                | Q(address__icontains=search) | Q(city__icontains=search)
                | Q(zip__icontains=search) | Q(state__icontains=search)| Q(target__icontains=search)
                | Q(email__icontains=search) | Q(company_ID__name__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.username),  # escape HTML for security reasons
                escape(item.userPassword),  # escape HTML for security reasons
                escape(item.phone),
                escape(item.address),
                escape(item.city),
                escape(item.zip),
                escape(item.state),
                escape(item.email),
                escape(item.company_ID.name),
                escape(item.target),
                '''<button style="font-size:10px;" onclick = "GetUserDetails('{}')" class="ui circular facebook icon button green">
  <i class="pen icon"></i>
</button>
<button style="font-size:10px;" onclick ="delUser('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
  <i class="trash alternate icon"></i>
</button></td>'''.format(item.pk, item.pk,
                         item.pk),

            ])
        return json_data


class WareHouseListJson(BaseDatatableView):
    order_columns = ['wareHouseName', 'wareHouseAddress', 'datetime']

    def get_initial_queryset(self):

        return WareHouse.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(wareHouseName__icontains=search) | Q(wareHouseAddress__icontains=search)
                | Q(datetime__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                escape(item.wareHouseName),  # escape HTML for security reasons
                escape(item.wareHouseAddress),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                '''<button style="font-size:10px;" onclick = "GetWareDetails('{}')" class="ui circular facebook icon button green">
  <i class="pen icon"></i>
</button>
<button style="font-size:10px;" onclick ="delWareHouse('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
  <i class="trash alternate icon"></i>
</button></td>'''.format(item.pk, item.pk,
                         item.pk),

            ])
        return json_data


# ---------END OF API LIST-------- #


# def get_category_detail(request, id=None):
#     instance = get_object_or_404(Category, pk=id)
#     hsn = Hsn.objects.get(hsn__exact=instance.hsn)
#
#     data = {
#         'ID': instance.pk,
#         'tax': hsn.tax,
#         'categoryName': instance.name,
#
#     }
#     return JsonResponse({'data': data}, safe=False)




@csrf_exempt
def add_sales(request):
    if request.method == 'POST':
        personalDiscount = request.POST.get("personalDiscount")
        customerID = request.POST.get("customerID")
        name = request.POST.get("name")
        gst = request.POST.get("gst")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        state = request.POST.get("state")
        pType = request.POST.get("pType")
        payment = request.POST.get("payment")
        cDays = request.POST.get("cDays")
        invoiceNumber = request.POST.get("invoiceNumber")
        pDate = request.POST.get("pDate")
        datas = request.POST.get("datas")
        subTotal = request.POST.get("subTotal")
        taxable = request.POST.get("taxable")
        totalFinal = request.POST.get("totalFinal")
        roundOff = request.POST.get("roundOff")
        taxableGST = request.POST.get("taxableGST")
        bill_disc = request.POST.get("bill_disc")
        GrandTotal = request.POST.get("GrandTotal")
        otherCharges = request.POST.get("otherCharges")
        chequeDetail = request.POST.get("chequeDetail")
        deliveryNote = request.POST.get("deliveryNote")
        supplierReference = request.POST.get("supplierReference")
        orderNumber = request.POST.get("orderNumber")
        dispatchNumber = request.POST.get("dispatchNumber")
        dispatchThrough = request.POST.get("dispatchThrough")
        otherReference = request.POST.get("otherReference")
        dispatchNoteDate = request.POST.get("dispatchNoteDate")
        destination = request.POST.get("destination")
        company = request.POST.get("company")
        paid = request.POST.get("paid")
        dueOrReturn = request.POST.get("dueOrReturn")
        invoiceSeriesID = request.POST.get("invoiceSeriesID")
        defaultInvoiceSeries = request.POST.get("defaultInvoiceSeries")
        paidAgainstBill = request.POST.get("paidAgainstBill")
        referrerID = request.POST.get("referrerID")

        status = True
        paidDate = datetime.today().date()
        if payment == 'Credit':

            status = False
            paidDate = None
        else:
            cDays = 0



        if customerID == 'NaN':
            cus = Customer()
            cus.name = name
            cus.gst = gst
            cus.phone = phone
            cus.address = address
            cus.state = state
            cus.email = email
            cus.save()
            sale = Sales()
            sale.customerID_id = cus.pk
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.personalDiscount = float(personalDiscount)

            sale.save()
            if referrerID != 'NaN':
                referral = Referrer.objects.get(pk=int(referrerID))
                com = ReferrerTransaction()
                com.addedBy_id = request.user.pk
                com.transactionType = 'Credit'
                com.amount = (referral.commission / 100.0) * float(subTotal)
                com.transactionDate = datetime.today().date()
                com.referrerID_id = int(referrerID)
                com.remark = "For a sale with amount Rs. {} and bill no. {}".format(str(subTotal), str(sale.pk))
                com.save()
                referral.balance = round(referral.balance + com.amount,2)
                referral.save()


            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]

                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock - int(item_details[4]))
                pro.save()
                p.save()
                if item_details[11] == 'Default':
                    try:
                        bat = ProductBatch.objects.filter(productID_id=int(item_details[0])).first()
                        ori_batch_stock = bat.quantity
                        bat.quantity = (ori_batch_stock - int(item_details[4]))
                        bat.save()
                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass
                else:
                    try:
                        bat = ProductBatch.objects.get(productID_id=int(item_details[0]), pk=int(item_details[11]))
                        ori_batch_stock = bat.quantity
                        bat.quantity = (ori_batch_stock - int(item_details[4]))
                        bat.save()
                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass



            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)
        else:

            sale = Sales()
            sale.customerID_id = int(customerID)
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.personalDiscount = float(personalDiscount)

            sale.save()
            if referrerID != 'NaN':
                referral = Referrer.objects.get(pk=int(referrerID))
                com = ReferrerTransaction()
                com.addedBy_id = request.user.pk
                com.transactionType = 'Credit'
                com.amount = (referral.commission / 100.0) * float(subTotal)
                com.transactionDate = datetime.today().date()
                com.referrerID_id = int(referrerID)
                com.remark = "For a sale with amount Rs. {} and bill no. {}".format(str(subTotal), str(sale.pk))
                com.save()
                referral.balance = round(referral.balance + com.amount,2)
                referral.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]
                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock - int(item_details[4]))
                pro.save()

                p.save()

                if item_details[11] == 'Default':
                    try:
                        bat = ProductBatch.objects.filter(productID_id=int(item_details[0])).first()
                        ori_batch_stock = bat.quantity
                        bat.quantity = (ori_batch_stock - int(item_details[4]))
                        bat.save()
                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass
                else:
                    try:
                        bat = ProductBatch.objects.get(productID_id=int(item_details[0]), pk = int(item_details[11]))
                        ori_batch_stock = bat.quantity
                        bat.quantity = (ori_batch_stock - int(item_details[4]))
                        bat.save()
                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)


class SalesListByProductJson(BaseDatatableView):
    order_columns = ['productName', 'productID.brand', 'salesID.invoiceDate', 'salesID.invoiceNumber',
                     'salesID.customerName', 'salesID.customerGst', 'quantity', 'rate', 'total', 'salesID.salesType',
                     'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return SalesProduct.objects.filter(salesID__isDeleted__exact=False,
                                               salesID__invoiceDate__gte=startDate.date(),
                                               salesID__invoiceDate__lte=endDate.date() + timedelta(days=1))
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return SalesProduct.objects.filter(salesID__isDeleted__exact=False,
                                               salesID__companyID_id=user.company_ID_id,
                                               salesID__invoiceDate__gte=startDate.date(),
                                               salesID__invoiceDate__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(salesID__customerName__icontains=search) | Q(salesID__customerGst__icontains=search)
                | Q(salesID__invoiceDate__icontains=search) | Q(salesID__invoiceNumber__icontains=search)
                | Q(salesID__salesType__icontains=search)
                | Q(productName__icontains=search) | Q(productID__brand__icontains=search) | Q(
                    quantity__icontains=search) | Q(rate__icontains=search) | Q(total__icontains=search) | Q(
                    salesID__companyID__name__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.salesID.customerGst is None:
                customerGst = 'N/A'
            else:
                customerGst = item.salesID.customerGst
            if item.salesID.invoiceNumber is None:
                invoiceNumber = 'N/A'
            else:
                invoiceNumber = item.salesID.invoiceNumber
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):

                action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>
'''.format(item.salesID.pk),
            else:
                action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                                               <i class="receipt icon"></i>
                                             </button>'''.format(item.salesID.pk),

            json_data.append([
                escape(item.productName),  # escape HTML for security reasons
                escape(item.productID.brand),  # escape HTML for security reasons
                escape(item.salesID.invoiceDate),
                invoiceNumber,
                escape(item.salesID.customerName),
                escape(customerGst),
                escape(item.quantity),
                escape(item.rate),
                escape(item.total),
                escape(item.salesID.salesType),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action

                #                      < button
                #     style = "font-size:10px;"
                #     onclick = "GetSaleDetail('{}')"
                #
                #     class ="ui circular facebook icon button green" >
                #
                #     < i
                #
                #     class ="pen icon" > < / i >
                # < / button >
            ])
        return json_data


class SalesListJson(BaseDatatableView):
    order_columns = ['customerName', 'customerGst', 'invoiceDate', 'id', 'invoiceNumber',
                     'grandTotal', 'paidAgainstBill', 'dueOrReturnAmount', 'paymentType', 'companyID', 'salesType',
                     'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return Sales.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
                                        invoiceDate__lte=endDate.date() + timedelta(days=1))
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return Sales.objects.filter(isDeleted__exact=False, companyID_id=user.company_ID_id,
                                        invoiceDate__gte=startDate.date(),
                                        invoiceDate__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(customerName__icontains=search) | Q(customerGst__icontains=search) | Q(id__icontains=search)
                | Q(invoiceDate__icontains=search) | Q(invoiceNumber__icontains=search)
                | Q(salesType__icontains=search)
                | Q(grandTotal__icontains=search) | Q(paymentType__icontains=search) | Q(
                    creditDays__icontains=search) | Q(status__icontains=search) | Q(companyID__name__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.customerGst is None:
                customerGst = 'N/A'
            else:
                customerGst = item.customerGst
            if item.invoiceNumber is None:
                invoiceNumber = 'N/A'
            else:
                invoiceNumber = item.invoiceNumber
            # if item.status == True:
            #     status = '''<a class="ui green label">Paid</a>'''
            # else:
            #     status = '''<a class="ui red label">Due</a>'''

            if 'Admin' in self.request.user.groups.values_list('name', flat=True):

                action = '''<button style="font-size:10px;" onclick = "TakePayment('{}')" class="ui circular  icon button blue">
                               <i class="hand holding usd icon"></i>
                             </button><button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>



                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                                               <i class="receipt icon"></i>
                                             </button>'''.format(item.pk, item.pk, item.pk),

            json_data.append([
                escape(item.customerName),  # escape HTML for security reasons
                customerGst,
                escape(item.invoiceDate),
                str(item.pk).zfill(5),
                invoiceNumber,
                escape(item.grandTotal),
                escape(item.paidAgainstBill),
                escape(item.grandTotal - item.paidAgainstBill),
                escape(item.paymentType),
                escape(item.companyID.name),
                escape(item.salesType),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action

                #                      < button
                #     style = "font-size:10px;"
                #     onclick = "GetSaleDetail('{}')"
                #
                #     class ="ui circular facebook icon button green" >
                #
                #     < i
                #
                #     class ="pen icon" > < / i >
                # < / button >
            ])
        return json_data


class SalesListByCustomerJson(BaseDatatableView):
    order_columns = ['id', 'invoiceDate', 'id', 'invoiceNumber',
                     'grandTotal', 'paidAgainstBill', 'paymentType', 'companyID', 'salesType', 'datetime', ]

    def get_initial_queryset(self):
        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return Sales.objects.filter(isDeleted__exact=False, customerID_id=self.request.GET.get('ID'))
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return Sales.objects.filter(isDeleted__exact=False, companyID_id=user.company_ID_id,
                                        customerID_id=self.request.GET.get('ID'))

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(status__icontains=search)
                | Q(invoiceDate__icontains=search) | Q(invoiceNumber__icontains=search) | Q(id__icontains=search)
                | Q(salesType__icontains=search)
                | Q(grandTotal__icontains=search) | Q(paymentType__icontains=search) | Q(creditDays__icontains=search)
                | Q(companyID__name__icontains=search)
            )

        return qs

    def prepare_results(self, qs):
        json_data = []
        i = 1
        for item in qs:
            if item.invoiceNumber is None:
                invoiceNumber = 'N/A'
            else:
                invoiceNumber = item.invoiceNumber

            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>



                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(i),  # escape HTML for security reasons
                escape(item.invoiceDate),
                str(item.pk).zfill(5),
                invoiceNumber,
                escape(item.grandTotal),
                escape(item.paidAgainstBill),
                escape(item.paymentType),
                escape(item.companyID.name),
                escape(item.salesType),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action,

            ])
            i = i + 1
        return json_data


def get_sales_detail(request, id=None):
    instance = get_object_or_404(Sales, pk=id)
    basic = {
        'Name': instance.customerName,
        'Gst': instance.customerGst,
        'Phone': instance.customerPhone,
        'Address': instance.customerAddress,
        'Email': instance.customerEmail,
        'State': instance.customerState,
        'PaymentType': instance.paymentType,
        'Invoice': instance.invoiceNumber,
        'InvoiceDate': instance.invoiceDate,
        'Taxable': instance.taxable,
        'SubTotal': instance.subTotal,
        'Discount': instance.billDisc,
        'GrandTotal': instance.grandTotal,
        'RoundOff': instance.roundOff,
        'TotalFinal': instance.totalFinal,
        'BillGst': instance.gst,
        'CreditDays': instance.creditDays,
        'chequeDetail': instance.chequeDetail,
        'deliveryNote': instance.deliveryNote,
        'SupplierReference': instance.supplierReference,
        'BuyersOrderNumber': instance.buyersOrderNumber,
        'DispatchDocumentNumber': instance.dispatchDocumentNumber,
        'DispatchThrough': instance.dispatchThrough,
        'OtherReference': instance.otherReference,
        'DispatchNoteDate': instance.dispatchNoteDate,
        'Destination': instance.destination,
        'OtherCharges': instance.otherCharges,
        'PaidAmount': instance.paidAmount,
        'DueOrReturnAmount': instance.dueOrReturnAmount,
        'PaidAgainstBill': instance.paidAgainstBill,
        'AddedBy': instance.addedBy.username,
        'PersonalDiscount': instance.personalDiscount,
        'BillNumber': str(instance.pk).zfill(5),
        'BillType': instance.salesType,
    }
    items = SalesProduct.objects.filter(salesID_id=instance.pk)
    item_list = []
    for i in items:
        item_dic = {
            'ItemID': i.pk,
            'ItemProductName': i.productName,
            'ItemCategory': i.category,
            'ItemHsn': i.hsn,
            'ItemQuantity': i.quantity,
            'ItemUnit': i.unit,
            'ItemRate': i.rate,
            'ItemGst': i.gst,
            'ItemDisc': i.disc,
            'ItemnetRate': i.netRate,
            'ItemTotal': i.total,

        }
        item_list.append(item_dic)

    data = {
        'Basic': basic,
        'Items': item_list

    }
    return JsonResponse({'data': data}, safe=False)


def get_sales_detail_for_invoice(request, id=None):
    instance = get_object_or_404(Sales, pk=id)
    basic = {
        'CompanyName': instance.companyID.name,
        'CompanyGst': instance.companyID.gst,
        'CompanyPhone': instance.companyID.phone,
        'CompanyAddress': instance.companyID.address,
        'CompanyEmail': instance.companyID.email,
        'CompanyState': instance.companyID.state,
        'CustomerName': instance.customerName.capitalize(),
        'CustomerID': instance.customerID_id,
        'CustomerGst': instance.customerGst,
        'CustomerPhone': instance.customerPhone,
        'CustomerAddress': instance.customerAddress,
        'CustomerEmail': instance.customerEmail,
        'CustomerState': instance.customerState,
        'Invoice': instance.invoiceNumber,
        'InvoiceDate': instance.invoiceDate,
        'DeliveryNote': instance.deliveryNote,
        'SupplierReference': instance.supplierReference,
        'BuyersOrderNumber': instance.buyersOrderNumber,
        'DispatchDocumentNumber': instance.dispatchDocumentNumber,
        'DispatchThrough': instance.dispatchThrough,
        'OtherReference': instance.otherReference,
        'DispatchNoteDate': instance.dispatchNoteDate,
        'Destination': instance.destination,
        'PaymentType': instance.paymentType,
        'Taxable': instance.taxable,
        'SubTotal': instance.subTotal,
        'Discount': instance.billDisc,
        'GrandTotal': instance.grandTotal,
        'RoundOff': instance.roundOff,
        'TotalFinal': instance.totalFinal,
        'BillGst': instance.gst,
        'OtherCharges': instance.otherCharges,
        'BillNumber': str(instance.pk).zfill(6),

    }
    items = SalesProduct.objects.filter(salesID_id=instance.pk)
    item_list = []

    item_serial = []
    item_product = []
    item_hsn = []
    item_gst = []
    item_quantity = []
    item_rate = []
    item_unit = []
    item_item_total = []
    item_gst_amount = []
    count = 1
    for i in items:
        item_dic = {
            'ItemID': i.pk,
            'ItemProductName': i.productName,
            'ItemCategory': i.category,
            'ItemHsn': i.hsn,
            'ItemQuantity': i.quantity,
            'ItemRate': i.rate,
            'ItemGst': i.gst,
            'ItemDisc': i.disc,
            'ItemnetRate': i.netRate,
            'ItemTotal': i.total,

        }
        item_list.append(item_dic)
        item_serial.append(count)
        item_product.append(i.productName)
        item_hsn.append(i.productID.categoryID.hsnID.hsn)
        item_gst.append(i.gst)
        item_quantity.append(i.quantity)
        item_rate.append(i.rate)
        item_unit.append(i.unit)
        item_gst_amount.append((i.quantity * i.rate) * (i.gst / 100))
        val = (i.rate * i.quantity) - ((instance.billDisc / 100) * i.rate * i.quantity)
        item_item_total.append(val)
        count = count + 1

    data = {
        'Basic': basic,
        'Items': item_list,
        'serial': item_serial,
        'product': item_product,
        'hsn': item_hsn,
        'gst': item_gst,
        'quantity': item_quantity,
        'rate': item_rate,
        'unit': item_unit,
        'item_total': item_item_total,
        'IGST': instance.gst / 2,
        'CGST': instance.gst / 2,
        'TotalInWords': num2words(int(instance.totalFinal)),
        'item_gst_amount': item_gst_amount,
        'item_gst_amountInWords': num2words(int(instance.gst)),

    }
    return JsonResponse({'data': data}, safe=False)


@csrf_exempt
def delete_sales(request):
    if request.method == 'POST':
        id = request.POST.get("ID")
        sale = Sales.objects.get(pk=int(id))
        sale.isDeleted = True
        sale.save()
        sales_products = SalesProduct.objects.filter(salesID_id=int(id))
        for pro in sales_products:
            product = Product.objects.get(pk=pro.productID_id)
            product.stock = product.stock + pro.quantity
            product.save()

        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def take_sale_payment(request):
    if request.method == 'POST':
        id = request.POST.get("ID")
        Amount = request.POST.get("Amount")
        sale = Sales.objects.get(pk=int(id))
        sale.paidAgainstBill = (sale.paidAgainstBill + float(Amount))
        sale.save()
        pay = PaymentHistory()
        pay.salesID_id = int(id)
        pay.amount = float(Amount)
        pay.addedBy_id = request.user.pk
        pay.save()


        return JsonResponse({'message': 'success'}, safe=False)

def post_company(request):
    if request.method == 'POST':
        companyName = request.POST.get("companyName")
        gstNo = request.POST.get("gstNo")
        companyPhone = request.POST.get("companyPhone")
        companyEmail = request.POST.get("companyEmail")
        companyAddress = request.POST.get("companyAddress")
        zip = request.POST.get("zip")
        city = request.POST.get("city")
        state = request.POST.get("state")
        accountHolderName = request.POST.get("accountHolderName")
        bankName = request.POST.get("bankName")
        branch = request.POST.get("branch")
        account_type = request.POST.get("account_type")
        accountNo = request.POST.get("accountNo")
        ifsc = request.POST.get("ifsc")
        bankAddress = request.POST.get("bankAddress")

        company = CompanyProfile()

        company.name = companyName
        company.gst = gstNo
        company.city = city
        company.zip = zip
        company.state = state
        company.phone = companyPhone
        company.address = companyAddress
        company.email = companyEmail
        company.save()

        bank = BankDetails()
        bank.companyID_id = company.pk
        bank.accHolderName = accountHolderName
        bank.bankName = bankName
        bank.accNo = accountNo
        bank.branch = branch
        bank.accountType = account_type
        bank.ifsc = ifsc
        bank.bankAddress = bankAddress
        bank.save()

        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_company(request):
    if request.method == 'POST':
        # try:
        id = request.POST.get("companyID")
        company = CompanyProfile.objects.get(pk=int(id))
        company.isDeleted = True
        company.save()

        return JsonResponse({'message': 'success'}, safe=False)
        # except:
        #     return JsonResponse({'message': 'error'}, safe=False)


# For EDit

def Edit_company(request):
    if request.method == 'POST':
        ID = request.POST.get("companyID")
        companyName = request.POST.get("companyName")
        gstNo = request.POST.get("gstNo")
        companyPhone = request.POST.get("companyPhone")
        companyEmail = request.POST.get("companyEmail")
        companyAddress = request.POST.get("companyAddress")
        zip = request.POST.get("zip")
        city = request.POST.get("city")
        state = request.POST.get("state")

        accountHolderName = request.POST.get("accountHolderName")
        bankName = request.POST.get("bankName")
        branch = request.POST.get("branch")
        account_type = request.POST.get("account_type")
        accountNo = request.POST.get("accountNo")
        ifsc = request.POST.get("ifsc")
        bankAddress = request.POST.get("bankAddress")

        edit_company = CompanyProfile.objects.get(pk=int(ID))
        # company = CompanyProfile()


        edit_company.name = companyName
        edit_company.gst = gstNo
        edit_company.city = city
        edit_company.zip = zip
        edit_company.state = state
        edit_company.phone = companyPhone
        edit_company.address = companyAddress
        edit_company.email = companyEmail
        edit_company.save()

        edit_bank = BankDetails.objects.get(companyID_id=int(ID))
        # bank = BankDetails()
        edit_bank.companyID_id = edit_company.pk
        edit_bank.accHolderName = accountHolderName
        edit_bank.bankName = bankName
        edit_bank.accNo = accountNo
        edit_bank.branch = branch
        edit_bank.accountType = account_type
        edit_bank.ifsc = ifsc
        edit_bank.bankAddress = bankAddress
        edit_bank.save()

        return JsonResponse({'message': 'success'}, safe=False)


def get_company_list(request):
    data = []
    for c in CompanyProfile.objects.filter(isDeleted__exact=False).order_by('name'):
        data_dic = {
            'ID': c.pk,
            'CompanyName': c.name,
        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


# For User

def post_User(request):
    if request.method == 'POST':
        CompanyUserName = request.POST.get("CompanyUserName")
        UserCompany = request.POST.get("UserCompany")
        UserPhoneNo = request.POST.get("UserPhoneNo")
        UserEmail = request.POST.get("UserEmail")
        UserAddress = request.POST.get("UserAddress")
        UserZip = request.POST.get("UserZip")
        UserState = request.POST.get("UserState")
        UserCity = request.POST.get("UserCity")
        UserPwd = request.POST.get("UserPwd")
        Target = request.POST.get("Target")

        user = CompanyUser()

        user.name = CompanyUserName
        user.company_ID_id = int(UserCompany)
        user.phone = UserPhoneNo
        user.email = UserEmail
        user.address = UserAddress
        user.zip = UserZip
        user.state = UserState
        user.city = UserCity
        user.userPassword = UserPwd
        user.target = float(Target)

        username = 'USER' + get_random_string(length=2, allowed_chars='1234567890')
        while User.objects.filter(username__exact=username).count() > 0:
            username = 'USER' + get_random_string(length=2, allowed_chars='1234567890')
        else:
            new_user = User()
            new_user.username = username
            new_user.set_password(UserPwd)

            new_user.save()
            user.username = username
            user.user_ID_id = new_user.pk

            user.save()

            try:
                g = Group.objects.get(name='Staff')
                g.user_set.add(new_user.pk)
                g.save()

            except:
                g = Group()
                g.name = "Staff"
                g.save()
                g.user_set.add(new_user.pk)
                g.save()

            myPrint = UserPrinterSetting()
            myPrint.userID_id = new_user.pk
            myPrint.save()

            return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        try:
            id = request.POST.get("userID")
            company = CompanyUser.objects.get(pk=int(id))
            company.isDeleted = True
            company.save()

            return JsonResponse({'message': 'success'}, safe=False)
        except:
            return JsonResponse({'message': 'error'}, safe=False)


def get_User_detail(request, id=None):
    C_User = get_object_or_404(CompanyUser, id=id)
    # instance = BankDetails.objects.get(companyID_id=company.pk)

    data = {
        'ID': C_User.pk,
        'UserName': C_User.name,
        'UserPhone': C_User.phone,
        'UserAddress': C_User.address,
        'UserCity': C_User.city,
        'UserZip': C_User.zip,
        'UserState': C_User.state,
        'UserEmail': C_User.email,
        'UserCompany': C_User.company_ID.id,
        'Target': C_User.target,

    }
    return JsonResponse({'data': data}, safe=False)


def Edit_user(request):
    if request.method == 'POST':
        ID = request.POST.get("UserID")
        EditCompanyUserName = request.POST.get("EditCompanyUserName")
        EditUserCompany = request.POST.get("EditUserCompany")
        EditUserPhoneNo = request.POST.get("EditUserPhoneNo")
        EditUserEmail = request.POST.get("EditUserEmail")
        EditUserAddress = request.POST.get("EditUserAddress")
        EditUserZip = request.POST.get("EditUserZip")
        EditUserState = request.POST.get("EditUserState")
        EditUserCity = request.POST.get("EditUserCity")
        EditUserTarget = request.POST.get("EditUserTarget")

        edit_user = CompanyUser.objects.get(pk=int(ID))

        edit_user.name = EditCompanyUserName
        edit_user.company_ID_id = int(EditUserCompany)
        edit_user.phone = EditUserPhoneNo
        edit_user.email = EditUserEmail
        edit_user.address = EditUserAddress
        edit_user.zip = EditUserZip
        edit_user.state = EditUserState
        edit_user.city = EditUserCity
        edit_user.target = float(EditUserTarget)
        edit_user.save()

        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def postLogin(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'success'}, safe=False)


        else:
            return JsonResponse({'message': 'fail'}, safe=False)
    else:
        return JsonResponse({'message': 'fail'}, safe=False)


def user_logout(request):
    logout(request)
    return redirect("homeApp:loginPage")


# For WareHouse
def add_warehouse(request):
    if request.method == 'POST':
        WareHouseName = request.POST.get("WareHouseName")
        WareHouseAddress = request.POST.get("WareHouseAddress")

        ware_house = WareHouse()

        ware_house.wareHouseName = WareHouseName
        ware_house.wareHouseAddress = WareHouseAddress

        ware_house.save()

        return JsonResponse({'message': 'success'}, safe=False)


def GetWareHouseList(request):
    data = []
    for c in WareHouse.objects.filter(isDeleted__exact=False).order_by('wareHouseName'):
        data_dic = {
            'ID': c.pk,
            'WareHouseName': c.wareHouseName,

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_warehouse_detail(request, id=None):
    instance = get_object_or_404(WareHouse, pk=id)
    data = {
        'WareID': instance.pk,
        'WareHouseName': instance.wareHouseName,
        'WareHouseAddress': instance.wareHouseAddress,

    }
    return JsonResponse({'data': data}, safe=False)


def edit_warehouse(request):
    if request.method == 'POST':
        WareID = request.POST.get("WareID")
        WareHouseName = request.POST.get("WareHouseName")
        WareHouseAddress = request.POST.get("WareHouseAddress")

        ware_house = WareHouse.objects.get(pk=int(WareID))

        ware_house.wareHouseName = WareHouseName
        ware_house.wareHouseAddress = WareHouseAddress

        ware_house.save()

        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_wareHouse(request):
    if request.method == 'POST':
        # try:
        id = request.POST.get("WareHouseID")
        wareHouse = WareHouse.objects.get(pk=int(id))
        wareHouse.isDeleted = True
        wareHouse.save()

        return JsonResponse({'message': 'success'}, safe=False)
        # except:
        #     return JsonResponse({'message': 'error'}, safe=False)


# ------------------------units-----------------
class UnitsListJson(BaseDatatableView):
    order_columns = ['name', 'datetime']

    def get_initial_queryset(self):

        return Unit.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(datetime__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                '''<button style="font-size:10px;" onclick = "GetUnitDetails('{}')" class="ui circular facebook icon button green">
  <i class="pen icon"></i>
</button>
<button style="font-size:10px;" onclick ="delUnit('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
  <i class="trash alternate icon"></i>
</button></td>'''.format(item.pk, item.pk,
                         item.pk),

            ])
        return json_data


def add_unit(request):
    if request.method == 'POST':
        unitName = request.POST.get("unitName")

        u = Unit()
        u.name = unitName
        u.save()

        return JsonResponse({'message': 'success'}, safe=False)


def get_unit_list(request):
    data = []
    for c in Unit.objects.filter(isDeleted__exact=False).order_by('name'):
        data_dic = {
            'ID': c.pk,
            'Name': c.name,

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_unit_detail(request, id=None):
    instance = get_object_or_404(Unit, pk=id)
    data = {
        'uniID': instance.pk,
        'UnitName': instance.name,

    }
    return JsonResponse({'data': data}, safe=False)


def edit_unit(request):
    if request.method == 'POST':
        uniID = request.POST.get("uniID")
        unitName = request.POST.get("unitName")

        u = Unit.objects.get(pk=int(uniID))

        u.name = unitName

        u.save()

        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_unit(request):
    if request.method == 'POST':
        # try:
        id = request.POST.get("UnitID")
        u = Unit.objects.get(pk=int(id))
        u.isDeleted = True
        u.save()

        return JsonResponse({'message': 'success'}, safe=False)


# purchase

@csrf_exempt
def add_purchase(request):
    if request.method == 'POST':
        supplierID = request.POST.get("supplierID")
        name = request.POST.get("name")
        gst = request.POST.get("gst")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        state = request.POST.get("state")
        pType = request.POST.get("pType")
        payment = request.POST.get("payment")
        cDays = request.POST.get("cDays")
        invoiceNumber = request.POST.get("invoiceNumber")
        pDate = request.POST.get("pDate")
        GrandTaxable = request.POST.get("GrandTaxable")
        GrandGst = request.POST.get("GrandGst")
        GrandTotal = request.POST.get("GrandTotal")
        datas = request.POST.get("datas")
        chequeDetail = request.POST.get("chequeDetail")
        company = request.POST.get("company")
        roundOff = request.POST.get("roundOff")
        deliveryNote = request.POST.get("deliveryNote")
        supplierReference = request.POST.get("supplierReference")
        orderNumber = request.POST.get("orderNumber")
        dispatchNumber = request.POST.get("dispatchNumber")
        dispatchThrough = request.POST.get("dispatchThrough")
        otherReference = request.POST.get("otherReference")
        dispatchNoteDate = request.POST.get("dispatchNoteDate")
        destination = request.POST.get("destination")
        otherCharges = request.POST.get("otherCharges")
        supplier = Supplier.objects.filter(name__iexact=name, phone__iexact=phone)
        status = True
        paidDate = datetime.today().date()
        if payment == 'Credit':

            status = False
            paidDate = None
        else:
            cDays = 0

        if supplierID == 'NaN':
            sup = Supplier()
            sup.name = name
            sup.gst = gst
            sup.phone = phone
            sup.address = address
            sup.state = state
            sup.email = email
            sup.save()
            pur = Purchase()
            pur.supplierID_id = sup.pk
            pur.supplierName = name
            pur.supplierGst = gst
            pur.supplierEmail = email
            pur.supplierPhone = phone
            pur.supplierAddress = address
            pur.supplierState = state
            pur.purchaseType = pType
            pur.paymentType = payment
            pur.creditDays = int(cDays)
            pur.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            pur.invoiceNumber = invoiceNumber
            pur.total = float(GrandTotal)
            pur.gst = float(GrandGst)
            pur.taxable = float(GrandTaxable)
            pur.status = status
            pur.paidDate = paidDate
            pur.companyID_id = int(company)
            pur.chequeDetail = chequeDetail
            pur.addedBy_id = request.user.pk
            pur.roundOff = float(roundOff)
            pur.deliveryNote = deliveryNote
            pur.supplierReference = supplierReference
            pur.buyersOrderNumber = orderNumber
            pur.dispatchDocumentNumber = dispatchNumber
            pur.dispatchThrough = dispatchThrough
            pur.otherReference = otherReference
            if dispatchNoteDate == '':
                pur.dispatchNoteDate = None
            else:
                pur.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            pur.destination = destination
            pur.otherCharges = float(otherCharges)
            pur.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = PurchaseProduct()
                p.purchaseID_id = pur.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.unit = item_details[9]
                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock + int(item_details[4]))
                pro.save()
                p.save()

        else:

            pur = Purchase()
            pur.supplierID_id = int(supplierID)
            pur.supplierName = name
            pur.supplierGst = gst
            pur.supplierEmail = email
            pur.supplierPhone = phone
            pur.supplierAddress = address
            pur.supplierState = state
            pur.purchaseType = pType
            pur.paymentType = payment
            pur.creditDays = int(cDays)
            pur.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            pur.invoiceNumber = invoiceNumber
            pur.total = float(GrandTotal)
            pur.gst = float(GrandGst)
            pur.taxable = float(GrandTaxable)
            pur.status = status
            pur.paidDate = paidDate
            pur.companyID_id = int(company)
            pur.chequeDetail = chequeDetail
            pur.addedBy_id = request.user.pk
            pur.roundOff = float(roundOff)
            pur.deliveryNote = deliveryNote
            pur.supplierReference = supplierReference
            pur.buyersOrderNumber = orderNumber
            pur.dispatchDocumentNumber = dispatchNumber
            pur.dispatchThrough = dispatchThrough
            pur.otherReference = otherReference
            if dispatchNoteDate == '':
                pur.dispatchNoteDate = None
            else:
                pur.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            pur.destination = destination
            pur.otherCharges = float(otherCharges)
            pur.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = PurchaseProduct()
                p.purchaseID_id = pur.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.unit = item_details[9]
                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock + int(item_details[4]))
                pro.save()
                p.save()
        return JsonResponse({'message': 'success'}, safe=False)


class PurchaseListJson(BaseDatatableView):
    order_columns = ['supplierName', 'supplierGst', 'invoiceDate', 'invoiceNumber',
                     'total', 'paymentType', 'companyID', 'purchaseType', 'status', 'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')
        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return Purchase.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
                                           invoiceDate__lte=endDate.date() + timedelta(days=1))
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return Purchase.objects.filter(isDeleted__exact=False, companyID_id=user.company_ID_id,
                                           invoiceDate__gte=startDate.date(),
                                           invoiceDate__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(supplierName__icontains=search) | Q(supplierGst__icontains=search)
                | Q(invoiceDate__icontains=search) | Q(invoiceNumber__icontains=search) | Q(
                    purchaseType__icontains=search)
                | Q(total__icontains=search) | Q(paymentType__icontains=search) | Q(creditDays__icontains=search)
                | Q(status__icontains=search) | Q(companyID__name__icontains=search)
            )

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.supplierGst is None:
                supplierGst = 'N/A'
            else:
                supplierGst = item.supplierGst
            if item.invoiceNumber is None:
                invoiceNumber = 'N/A'
            else:
                invoiceNumber = item.invoiceNumber

            if item.status == True:
                status = '''<a class="ui green label">Paid</a>'''
            else:
                status = '''<a class="ui red label">Due</a>'''
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<button style="font-size:10px;" onclick = "GetPurchaseDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>
                   

                             <button style="font-size:10px;" onclick ="delPurchase('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<button style="font-size:10px;" onclick = "GetPurchaseDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>
                   '''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(item.supplierName),  # escape HTML for security reasons
                supplierGst,
                escape(item.invoiceDate),
                invoiceNumber,
                escape(item.total),
                escape(item.paymentType),
                escape(item.companyID.name),
                escape(item.purchaseType),
                status,
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action,

                #                      < button
                #     style = "font-size:10px;"
                #     onclick = "GetProductDetail('{}')"
                #
                #     class ="ui circular facebook icon button green" >
                #
                #     < i
                #
                #     class ="pen icon" > < / i >
                # < / button >
            ])
        return json_data


class PurchaseListBySupplierJson(BaseDatatableView):
    order_columns = ['id', 'invoiceDate', 'invoiceNumber',
                     'total', 'paymentType', 'companyID', 'status', 'purchaseType', ]

    def get_initial_queryset(self):
        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return Purchase.objects.filter(isDeleted__exact=False, supplierID_id=self.request.GET.get('ID'))
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return Purchase.objects.filter(isDeleted__exact=False, companyID_id=user.company_ID_id,
                                           supplierID_id=self.request.GET.get('ID'))

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(status__icontains=search)
                | Q(invoiceDate__icontains=search) | Q(invoiceNumber__icontains=search)
                | Q(purchaseType__icontains=search)
                | Q(total__icontains=search) | Q(paymentType__icontains=search)
                | Q(creditDays__icontains=search) | Q(companyID__name__icontains=search)
            )

        return qs

    def prepare_results(self, qs):
        json_data = []
        i = 1
        for item in qs:
            if item.status == True:
                status = '''<a class="ui green label">Paid</a>'''
            else:
                status = '''<a class="ui red label">Due</a>'''

            if item.invoiceNumber is None:
                invoiceNumber = 'N/A'
            else:
                invoiceNumber = item.invoiceNumber
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<button style="font-size:10px;" onclick = "GetPurchaseDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>



                             <button style="font-size:10px;" onclick ="delPurchase('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<button style="font-size:10px;" onclick = "GetPurchaseDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(i),  # escape HTML for security reasons
                escape(item.invoiceDate),
                invoiceNumber,
                escape(item.total),
                escape(item.paymentType),
                escape(item.companyID.name),
                status,
                escape(item.purchaseType),
                action,

                #                      < button
                #     style = "font-size:10px;"
                #     onclick = "GetSaleDetail('{}')"
                #
                #     class ="ui circular facebook icon button green" >
                #
                #     < i
                #
                #     class ="pen icon" > < / i >
                # < / button >
            ])
            i = i + 1
        return json_data


def get_purchase_detail(request, id=None):
    instance = get_object_or_404(Purchase, pk=id)
    basic = {
        'Name': instance.supplierName,
        'Gst': instance.supplierGst,
        'Phone': instance.supplierPhone,
        'Address': instance.supplierAddress,
        'Email': instance.supplierEmail,
        'State': instance.supplierState,
        'PaymentType': instance.paymentType,
        'Invoice': instance.invoiceNumber,
        'InvoiceDate': instance.invoiceDate,
        'Taxable': instance.taxable,
        'GrandTotal': instance.total,
        'BillGst': instance.gst,
        'CreditDays': instance.creditDays,
        'chequeDetail': instance.chequeDetail,
        'deliveryNote': instance.deliveryNote,
        'SupplierReference': instance.supplierReference,
        'BuyersOrderNumber': instance.buyersOrderNumber,
        'DispatchDocumentNumber': instance.dispatchDocumentNumber,
        'DispatchThrough': instance.dispatchThrough,
        'OtherReference': instance.otherReference,
        'DispatchNoteDate': instance.dispatchNoteDate,
        'Destination': instance.destination,
        'OtherCharges': instance.otherCharges,
        'AddedBy': instance.addedBy.username,
    }
    items = PurchaseProduct.objects.filter(purchaseID_id=instance.pk)
    item_list = []
    for i in items:
        item_dic = {
            'ItemID': i.pk,
            'ItemProductName': i.productName,
            'ItemCategory': i.category,
            'ItemHsn': i.hsn,
            'ItemQuantity': i.quantity,
            'Unit': i.unit,
            'ItemRate': i.rate,
            'ItemGst': i.gst,
            'ItemnetRate': i.netRate,
            'ItemTotal': i.total,

        }
        item_list.append(item_dic)

    data = {
        'Basic': basic,
        'Items': item_list

    }
    return JsonResponse({'data': data}, safe=False)


@csrf_exempt
def delete_purchase(request):
    if request.method == 'POST':
        id = request.POST.get("ID")
        sale = Purchase.objects.get(pk=int(id))
        sale.isDeleted = True
        sale.save()
        sales_products = PurchaseProduct.objects.filter(purchaseID_id=int(id))
        for pro in sales_products:
            product = Product.objects.get(pk=pro.productID_id)
            product.stock = product.stock - pro.quantity
            product.save()
        return JsonResponse({'message': 'success'}, safe=False)


# expense

def add_expense(request):
    if request.method == 'POST':
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        expenseType = request.POST.get("expenseType")
        company = request.POST.get("company")

        ex = Expense()
        ex.expenseType = expenseType
        ex.description = description
        ex.companyID_id = int(company)
        ex.amount = float(amount)
        ex.expenseDate = datetime.strptime(date, '%d/%m/%Y')
        ex.save()

        return JsonResponse({'message': 'success'}, safe=False)

class ExpenseListJson(BaseDatatableView):
    order_columns = ['expenseType', 'description', 'amount', 'companyID', 'expenseDate', 'datetime','action']

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        return Expense.objects.filter(isDeleted__exact=False, expenseDate__gte=startDate.date(),
                                      expenseDate__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(expenseType__icontains=search) | Q(description__icontains=search) | Q(amount__icontains=search) | Q(
                    expenseDate__icontains=search) | Q(datetime__icontains=search) | Q(
                    companyID__name__icontains=search)
            )

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<button style="font-size:10px;" onclick ="delExpense('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                                                 <i class="trash alternate icon"></i>
                                               </button></td>'''.format(item.pk)
            else:
                action = '<button class="mini ui button">Denied</button>'
            json_data.append([
                escape(item.expenseType),  # escape HTML for security reasons
                escape(item.description),  # escape HTML for security reasons
                escape(item.amount),  # escape HTML for security reasons
                escape(item.companyID.name),  # escape HTML for security reasons
                escape(item.expenseDate),  # escape HTML for security reasons
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action,
            ])
        return json_data

@csrf_exempt
def delete_expense(request):
    if request.method == 'POST':
        idC = request.POST.get("ID")
        cus = Expense.objects.get(pk=int(idC))
        cus.delete()
        return JsonResponse({'message': 'success'}, safe=False)

def change_password(request):
    if request.method == 'POST':

        oldPassword = request.POST.get('oldPassword')
        password = request.POST.get('newPassword')
        try:
            data = CompanyUser.objects.get(user_ID_id=request.user.pk, userPassword=oldPassword)
            data.userPassword = password
            data.save()
            user = User.objects.get(pk=request.user.pk)
            user.set_password(password)
            user.save()
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'success'}, safe=False)
            else:
                return JsonResponse({'message': 'error'}, safe=False)



        except:
            return JsonResponse({'message': 'Invalid old password. Please try again.'}, safe=False)


def get_user_printer(request):
    myPrinter = get_object_or_404(UserPrinterSetting, userID_id=request.user.pk)

    data = {
        'PrinterID': myPrinter.printerID_id

    }

    return JsonResponse({'data': data}, safe=False)


@csrf_exempt
def change_user_printer_setting(request):
    if request.method == 'POST':
        printerID = request.POST.get("printerID")
        p = UserPrinterSetting.objects.get(userID_id=request.user.pk)
        p.printerID_id = int(printerID)
        p.save()
        return JsonResponse({'message': 'success'}, safe=False)


# invoice

def add_invoice(request):
    if request.method == 'POST':
        invoiceSeries = request.POST.get("invoiceSeries")
        invoiceLimit = request.POST.get("invoiceLimit")
        startWith = request.POST.get("startWith")
        company = request.POST.get("company")
        invoiceFor = request.POST.get("invoiceFor")
        try:
            inv = Invoice.objects.get(invoiceSeries__iexact=invoiceSeries, companyID_id=int(company))
            return JsonResponse({'message': 'Invoice series already exist. Please try again.'}, safe=False)
        except:
            try:
                inv = Invoice()
                inv.invoiceSeries = invoiceSeries
                inv.invoiceMaxCount = int(invoiceLimit)
                inv.companyID_id = int(company)
                inv.invoiceStartWith = int(startWith)
                inv.invoiceType = invoiceFor
                inv.save()

                return JsonResponse({'message': 'success'}, safe=False)

            except:
                return JsonResponse({'message': 'error'}, safe=False)


class InvoiceListJson(BaseDatatableView):
    order_columns = ['companyID', 'invoiceType', 'invoiceSeries', 'invoiceMaxCount', 'invoiceStartWith', 'datetime']

    def get_initial_queryset(self):

        return Invoice.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(invoiceSeries__icontains=search) | Q(invoiceMaxCount__icontains=search) | Q(
                    invoiceStartWith__icontains=search)
                | Q(invoiceType__icontains=search) | Q(datetime__icontains=search) | Q(companyID__name__icontains=search)
            )

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                escape(item.companyID.name),  # escape HTML for security reasons
                escape(item.invoiceType),  # escape HTML for security reasons
                escape(item.invoiceSeries),  # escape HTML for security reasons
                escape(item.invoiceMaxCount),  # escape HTML for security reasons
                escape(item.invoiceStartWith),  # escape HTML for security reasons
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
            ])
        return json_data


def get_invoice_series_by_company(request):
    companyID = request.GET.get('companyID')
    invoice = request.GET.get('invoiceType')
    inv = Invoice.objects.filter(isDeleted__exact=False, companyID_id=int(companyID),
                                 isCompleted__exact=False,invoiceType__exact = invoice).order_by('-id')
    inv_list = []
    for i in inv:
        inv_dic = {
            'ID': i.pk,
            'Series': i.invoiceSeries
        }

        inv_list.append(inv_dic)

    return JsonResponse({'data': inv_list}, safe=False)


def get_new_sale_invoice_number(request):
    invoiceSeriesID = request.GET.get('invoiceSeriesID')
    try:
        lastSale = Sales.objects.filter(invoiceSeriesID_id=int(invoiceSeriesID)).last()

        NewInvoiceNumber = str(lastSale.invoiceActualNumber + 1).zfill(
            len(str(lastSale.invoiceSeriesID.invoiceMaxCount)))

        return JsonResponse({'Invoice': NewInvoiceNumber}, safe=False)

    except:
        inv = Invoice.objects.get(pk=int(invoiceSeriesID))
        NewInvoiceNumber = str(inv.invoiceStartWith).zfill(len(str(inv.invoiceMaxCount)))

        return JsonResponse({'Invoice': NewInvoiceNumber}, safe=False)


import sys
import xlsxwriter


def download_backup(request):
    response = HttpResponse(content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename="NextBillBackUp-{}.json"'.format(datetime.today())
    stdout_orig = sys.stdout
    sys.stdout = response
    management.call_command('dumpdata')
    sys.stdout = stdout_orig
    response.write(sys.stdout)
    return response


def download_expense_report(request):
    companyID = request.GET.get('companyID')
    eType = request.GET.get('eType')
    sDate = request.GET.get('startDate')
    eDate = request.GET.get('endDate')
    startDate = datetime.strptime(sDate, '%d/%m/%Y')
    endDate = datetime.strptime(eDate, '%d/%m/%Y')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ExpenseReport({}--{}).xlsx"'.format(sDate, eDate)
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    ex = Expense.objects.filter(isDeleted__exact=False, expenseDate__gte=startDate.date(),
                                expenseDate__lte=endDate.date() + timedelta(days=1), expenseType=eType,
                                companyID_id=int(companyID))

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Serial No.', bold)
    worksheet.write('B1', 'Type', bold)
    worksheet.write('C1', 'Date', bold)
    worksheet.write('D1', 'Amount', bold)
    worksheet.write('E1', 'Description', bold)
    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    total = 0.0

    # Iterate over the data and write it out row by row.
    for item in ex:
        worksheet.write(row, col, row)
        worksheet.write(row, col + 1, item.expenseType)
        worksheet.write(row, col + 2, str(item.expenseDate))
        worksheet.write(row, col + 3, item.amount)
        worksheet.write(row, col + 4, item.description)
        row += 1
        total = total + item.amount

    # Write a total using a formula.
    worksheet.write(row, 2, 'Total', bold)
    worksheet.write(row, 3, total)

    workbook.close()
    # response.write(workbook)
    return response


def download_purchase_report(request):
    companyID = request.GET.get('companyID')
    eType = request.GET.get('eType')
    sDate = request.GET.get('startDate')
    eDate = request.GET.get('endDate')
    startDate = datetime.strptime(sDate, '%d/%m/%Y')
    endDate = datetime.strptime(eDate, '%d/%m/%Y')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="PurchaseReport({}--{}).xlsx"'.format(sDate, eDate)
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    pur = Purchase.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
                                  invoiceDate__lte=endDate.date() + timedelta(days=1), purchaseType=eType,
                                  companyID_id=int(companyID))

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Serial No.', bold)
    worksheet.write('B1', 'Date', bold)
    worksheet.write('C1', 'Party Name', bold)
    worksheet.write('D1', 'GSTIN No.', bold)
    worksheet.write('E1', 'Invoice No.', bold)
    worksheet.write('F1', 'Tax Value', bold)
    worksheet.write('G1', 'Tax Rate', bold)
    worksheet.write('H1', 'Tax Amount', bold)
    worksheet.write('I1', 'CGST', bold)
    worksheet.write('J1', 'SGST', bold)
    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    total = 0.0

    merge_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })

    # Iterate over the data and write it out row by row.
    pCount = 1
    total_tax_val = 0.0
    total_tax_amount = 0.0
    total_cgst = 0.0
    total_sgst = 0.0

    for item in pur:
        rowCount = 0
        gsts = set({})
        for p in PurchaseProduct.objects.filter(purchaseID_id=item.pk, isDeleted__exact=False):
            gsts.add(p.gst)
        for g in gsts:

            taxVal = 0.0
            taxAmount = 0.0

            for po in PurchaseProduct.objects.filter(purchaseID_id=item.pk, isDeleted__exact=False, gst__exact=g):
                taxVal = taxVal + po.total
                taxAmount = taxAmount + (po.total * (g / 100.0))
                rowCount = rowCount + 1

            worksheet.write(row, col + 5, taxVal)
            worksheet.write(row, col + 6, g)
            worksheet.write(row, col + 7, taxAmount)
            worksheet.write(row, col + 8, taxAmount / 2.0)
            worksheet.write(row, col + 9, taxAmount / 2.0)
            row += 1
            total_tax_val = total_tax_val + taxVal
            total_tax_amount = total_tax_amount + taxAmount
            total_cgst = total_cgst + (taxAmount / 2.0)
            total_sgst = total_sgst + (taxAmount / 2.0)
        if row != (row + 2 - rowCount):
            worksheet.merge_range('A{}:A{}'.format(str(row), str(row + 2 - rowCount)), pCount, merge_format)
            worksheet.merge_range('B{}:B{}'.format(str(row), str(row + 2 - rowCount)), str(item.invoiceDate),
                                  merge_format)
            worksheet.merge_range('C{}:C{}'.format(str(row), str(row + 2 - rowCount)), str(item.supplierName),
                                  merge_format)
            worksheet.merge_range('D{}:D{}'.format(str(row), str(row + 2 - rowCount)), str(item.supplierGst),
                                  merge_format)
            worksheet.merge_range('E{}:E{}'.format(str(row), str(row + 2 - rowCount)), str(item.invoiceNumber),
                                  merge_format)
        else:
            worksheet.write(row - 1, 0, pCount, merge_format)
            worksheet.write(row - 1, 1, str(item.invoiceDate), merge_format)
            worksheet.write(row - 1, 2, str(item.supplierName), merge_format)
            worksheet.write(row - 1, 3, str(item.supplierGst), merge_format)
            worksheet.write(row - 1, 4, str(item.invoiceNumber), merge_format)

        rowCount = 1

        pCount = pCount + 1
    worksheet.write(row + 1, 5, total_tax_val, bold)
    worksheet.write(row + 1, 7, total_tax_amount, bold)
    worksheet.write(row + 1, 8, total_cgst, bold)
    worksheet.write(row + 1, 9, total_sgst, bold)

    workbook.close()
    return response


def download_sales_report(request):
    companyID = request.GET.get('companyID')
    eType = request.GET.get('eType')
    sDate = request.GET.get('startDate')
    eDate = request.GET.get('endDate')
    startDate = datetime.strptime(sDate, '%d/%m/%Y')
    endDate = datetime.strptime(eDate, '%d/%m/%Y')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="SalesReport({}--{}).xlsx"'.format(sDate, eDate)
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    pur = Sales.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
                               invoiceDate__lte=endDate.date() + timedelta(days=1), salesType=eType,
                               companyID_id=int(companyID))

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Serial No.', bold)
    worksheet.write('B1', 'Date', bold)
    worksheet.write('C1', 'Customer Name', bold)
    worksheet.write('D1', 'GSTIN No.', bold)
    worksheet.write('E1', 'Invoice No.', bold)
    worksheet.write('F1', 'Tax Value', bold)
    worksheet.write('G1', 'Tax Rate', bold)
    worksheet.write('H1', 'Tax Amount', bold)
    worksheet.write('I1', 'CGST', bold)
    worksheet.write('J1', 'SGST', bold)
    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    total = 0.0

    merge_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })

    # Iterate over the data and write it out row by row.
    pCount = 1
    total_tax_val = 0.0
    total_tax_amount = 0.0
    total_cgst = 0.0
    total_sgst = 0.0

    for item in pur:
        rowCount = 0
        gsts = set({})
        for p in SalesProduct.objects.filter(salesID_id=item.pk, isDeleted__exact=False):
            gsts.add(p.gst)
        for g in gsts:

            taxVal = 0.0
            taxAmount = 0.0

            for po in SalesProduct.objects.filter(salesID_id=item.pk, isDeleted__exact=False, gst__exact=g):
                taxVal = taxVal + po.total
                taxAmount = taxAmount + (po.total * (g / 100.0))
                rowCount = rowCount + 1

            worksheet.write(row, col + 5, taxVal)
            worksheet.write(row, col + 6, g)
            worksheet.write(row, col + 7, taxAmount)
            worksheet.write(row, col + 8, taxAmount / 2.0)
            worksheet.write(row, col + 9, taxAmount / 2.0)
            row += 1
            total_tax_val = total_tax_val + taxVal
            total_tax_amount = total_tax_amount + taxAmount
            total_cgst = total_cgst + (taxAmount / 2.0)
            total_sgst = total_sgst + (taxAmount / 2.0)
        if row != (row + 1 - rowCount):
            worksheet.merge_range('A{}:A{}'.format(str(row), str(row + 1 - rowCount)), pCount, merge_format)
            worksheet.merge_range('B{}:B{}'.format(str(row), str(row + 1 - rowCount)), str(item.invoiceDate),
                                  merge_format)
            worksheet.merge_range('C{}:C{}'.format(str(row), str(row + 1 - rowCount)), str(item.customerName),
                                  merge_format)
            worksheet.merge_range('D{}:D{}'.format(str(row), str(row + 1 - rowCount)), str(item.customerGst),
                                  merge_format)
            worksheet.merge_range('E{}:E{}'.format(str(row), str(row + 1 - rowCount)), str(item.invoiceNumber),
                                  merge_format)
        else:
            worksheet.write(row - 1, 0, pCount, merge_format)
            worksheet.write(row - 1, 1, str(item.invoiceDate), merge_format)
            worksheet.write(row - 1, 2, str(item.customerName), merge_format)
            worksheet.write(row - 1, 3, str(item.customerGst), merge_format)
            worksheet.write(row - 1, 4, str(item.invoiceNumber), merge_format)

        rowCount = 1

        pCount = pCount + 1
    worksheet.write(row + 1, 5, total_tax_val, bold)
    worksheet.write(row + 1, 7, total_tax_amount, bold)
    worksheet.write(row + 1, 8, total_cgst, bold)
    worksheet.write(row + 1, 9, total_sgst, bold)

    workbook.close()
    return response


@csrf_exempt
def add_booking(request):
    if request.method == 'POST':
        personalDiscount = request.POST.get("personalDiscount")

        customerID = request.POST.get("customerID")
        name = request.POST.get("name")
        gst = request.POST.get("gst")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        state = request.POST.get("state")
        pType = request.POST.get("pType")
        payment = request.POST.get("payment")
        cDays = request.POST.get("cDays")
        invoiceNumber = request.POST.get("invoiceNumber")
        pDate = request.POST.get("pDate")
        datas = request.POST.get("datas")
        subTotal = request.POST.get("subTotal")
        taxable = request.POST.get("taxable")
        totalFinal = request.POST.get("totalFinal")
        roundOff = request.POST.get("roundOff")
        taxableGST = request.POST.get("taxableGST")
        bill_disc = request.POST.get("bill_disc")
        GrandTotal = request.POST.get("GrandTotal")
        otherCharges = request.POST.get("otherCharges")
        chequeDetail = request.POST.get("chequeDetail")
        deliveryNote = request.POST.get("deliveryNote")
        supplierReference = request.POST.get("supplierReference")
        orderNumber = request.POST.get("orderNumber")
        dispatchNumber = request.POST.get("dispatchNumber")
        dispatchThrough = request.POST.get("dispatchThrough")
        otherReference = request.POST.get("otherReference")
        dispatchNoteDate = request.POST.get("dispatchNoteDate")
        destination = request.POST.get("destination")
        company = request.POST.get("company")
        paid = request.POST.get("paid")
        dueOrReturn = request.POST.get("dueOrReturn")
        invoiceSeriesID = request.POST.get("invoiceSeriesID")
        defaultInvoiceSeries = request.POST.get("defaultInvoiceSeries")
        paidAgainstBill = request.POST.get("paidAgainstBill")

        status = True
        paidDate = datetime.today().date()
        if payment == 'Credit':

            status = False
            paidDate = None
        else:
            cDays = 0

        if customerID == 'NaN':
            cus = Customer()
            cus.name = name
            cus.gst = gst
            cus.phone = phone
            cus.address = address
            cus.state = state
            cus.email = email
            cus.save()
            sale = SalesLater()
            sale.customerID_id = cus.pk
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.personalDiscount = float(personalDiscount)

            sale.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesLaterProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]
                p.save()
                if item_details[11] == 'Default':
                    try:
                        bat = ProductBatch.objects.filter(productID_id=int(item_details[0])).first()
                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass
                else:
                    try:
                        bat = ProductBatch.objects.get(productID_id=int(item_details[0]), pk=int(item_details[11]))

                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)
        else:

            sale = SalesLater()
            sale.customerID_id = int(customerID)
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.personalDiscount = float(personalDiscount)

            sale.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesLaterProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]
                if item_details[11] == 'Default':
                    try:
                        bat = ProductBatch.objects.filter(productID_id=int(item_details[0])).first()
                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass
                else:
                    try:
                        bat = ProductBatch.objects.get(productID_id=int(item_details[0]), pk=int(item_details[11]))

                        p.batchID_id = bat.pk
                        p.save()
                    except:
                        pass

                p.save()
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)


class BookingListJson(BaseDatatableView):
    order_columns = ['customerName', 'customerGst', 'invoiceDate', 'invoiceNumber',
                     'grandTotal', 'paidAgainstBill', 'dueOrReturnAmount', 'paymentType', 'companyID', 'salesType',
                     'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return SalesLater.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
                                        invoiceDate__lte=endDate.date() + timedelta(days=1))
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return SalesLater.objects.filter(isDeleted__exact=False, companyID_id=user.company_ID_id,
                                        invoiceDate__gte=startDate.date(),
                                        invoiceDate__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(customerName__icontains=search) | Q(customerGst__icontains=search)
                | Q(invoiceDate__icontains=search) | Q(invoiceNumber__icontains=search)
                | Q(salesType__icontains=search)
                | Q(grandTotal__icontains=search) | Q(paymentType__icontains=search) | Q(
                    creditDays__icontains=search) | Q(status__icontains=search) | Q(companyID__name__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.customerGst is None:
                customerGst = 'N/A'
            else:
                customerGst = item.customerGst
            if item.invoiceNumber is None:
                invoiceNumber = 'N/A'
            else:
                invoiceNumber = item.invoiceNumber
            # if item.status == True:
            #     status = '''<a class="ui green label">Paid</a>'''
            # else:
            #     status = '''<a class="ui red label">Due</a>'''

            if 'Admin' in self.request.user.groups.values_list('name', flat=True):

                action = '''<a style="font-size:10px;" href="/BookingSale/{}" class="ui circular  icon button green">
                               <i class="clipboard check icon"></i>
                             </a>



                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<a style="font-size:10px;" href="/BookingSale/{}" class="ui circular  icon button green">
                               <i class="clipboard check icon"></i>
                             </a>



                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(item.customerName),  # escape HTML for security reasons
                customerGst,
                escape(item.invoiceDate),
                invoiceNumber,
                escape(item.grandTotal),
                escape(item.paidAgainstBill),
                escape(item.grandTotal - item.paidAgainstBill),
                escape(item.paymentType),
                escape(item.companyID.name),
                escape(item.salesType),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action

                #                      < button
                #     style = "font-size:10px;"
                #     onclick = "GetSaleDetail('{}')"
                #
                #     class ="ui circular facebook icon button green" >
                #
                #     < i
                #
                #     class ="pen icon" > < / i >
                # < / button >
            ])
        return json_data

@csrf_exempt
def delete_booking(request):
    if request.method == 'POST':
        id = request.POST.get("ID")
        sale = SalesLater.objects.get(pk=int(id))
        sale.isDeleted = True
        sale.save()
        # sales_products = SalesLaterProduct.objects.filter(salesID_id=int(id))
        # for pro in sales_products:
        #     product = Product.objects.get(pk=pro.productID_id)
        #     product.stock = product.stock + pro.quantity
        #     product.save()

        return JsonResponse({'message': 'success'}, safe=False)


def BookingSale(request, id=None):
    if request.user.is_authenticated:
        instance = get_object_or_404(SalesLater, pk=id)
        pro = SalesLaterProduct.objects.filter(salesID_id = instance.pk)


        # if request.groups.filter(name='Staff').is_authenticated:

        if 'Admin' in request.user.groups.values_list('name', flat=True):
            company = CompanyProfile.objects.filter(isDeleted__exact=False)
        else:
            user = CompanyUser.objects.get(user_ID_id=request.user.pk)
            company = CompanyProfile.objects.filter(pk=user.company_ID_id, isDeleted__exact=False)

        context = {
            'sale': instance,
            'Products': pro,
            'company': company,
        }

        return render(request, 'home/BookingSale.html', context)
    else:
        return redirect('homeApp:loginPage')


@csrf_exempt
def update_booking(request):
    if request.method == 'POST':
        bookingID = request.POST.get("bookingID")
        customerID = request.POST.get("customerID")
        name = request.POST.get("name")
        gst = request.POST.get("gst")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        state = request.POST.get("state")
        pType = request.POST.get("pType")
        payment = request.POST.get("payment")
        cDays = request.POST.get("cDays")
        invoiceNumber = request.POST.get("invoiceNumber")
        pDate = request.POST.get("pDate")
        datas = request.POST.get("datas")
        subTotal = request.POST.get("subTotal")
        taxable = request.POST.get("taxable")
        totalFinal = request.POST.get("totalFinal")
        roundOff = request.POST.get("roundOff")
        taxableGST = request.POST.get("taxableGST")
        bill_disc = request.POST.get("bill_disc")
        GrandTotal = request.POST.get("GrandTotal")
        otherCharges = request.POST.get("otherCharges")
        chequeDetail = request.POST.get("chequeDetail")
        deliveryNote = request.POST.get("deliveryNote")
        supplierReference = request.POST.get("supplierReference")
        orderNumber = request.POST.get("orderNumber")
        dispatchNumber = request.POST.get("dispatchNumber")
        dispatchThrough = request.POST.get("dispatchThrough")
        otherReference = request.POST.get("otherReference")
        dispatchNoteDate = request.POST.get("dispatchNoteDate")
        destination = request.POST.get("destination")
        company = request.POST.get("company")
        paid = request.POST.get("paid")
        dueOrReturn = request.POST.get("dueOrReturn")
        invoiceSeriesID = request.POST.get("invoiceSeriesID")
        defaultInvoiceSeries = request.POST.get("defaultInvoiceSeries")
        paidAgainstBill = request.POST.get("paidAgainstBill")

        status = True
        paidDate = datetime.today().date()
        if payment == 'Credit':

            status = False
            paidDate = None
        else:
            cDays = 0

        if customerID == 'NaN':
            cus = Customer()
            cus.name = name
            cus.gst = gst
            cus.phone = phone
            cus.address = address
            cus.state = state
            cus.email = email
            cus.save()
            sale = SalesLater.objects.get(pk = int(bookingID))
            sale.customerID_id = cus.pk
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)

            sale.save()

            splited_receive_item = datas.split("@")

            old_pro = SalesLaterProduct.objects.filter(salesID_id = int(bookingID))
            old_pro.delete()
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesLaterProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]

                # pro = Product.objects.get(pk=int(int(item_details[0])))
                # ori_stock = pro.stock
                # pro.stock = (ori_stock - int(item_details[4]))
                # pro.save()
                p.save()
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)
        else:

            sale = SalesLater.objects.get(pk=int(bookingID))
            sale.customerID_id = int(customerID)
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.save()

            splited_receive_item = datas.split("@")
            old_pro = SalesLaterProduct.objects.filter(salesID_id=int(bookingID))
            old_pro.delete()
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesLaterProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]
                # pro = Product.objects.get(pk=int(int(item_details[0])))
                # ori_stock = pro.stock
                # pro.stock = (ori_stock - int(item_details[4]))
                # pro.save()

                p.save()
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)


@csrf_exempt
def add_sales_from_booking(request):
    if request.method == 'POST':
        personalDiscount = request.POST.get("personalDiscount")
        bookingID = request.POST.get("bookingID")
        customerID = request.POST.get("customerID")
        name = request.POST.get("name")
        gst = request.POST.get("gst")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        state = request.POST.get("state")
        pType = request.POST.get("pType")
        payment = request.POST.get("payment")
        cDays = request.POST.get("cDays")
        invoiceNumber = request.POST.get("invoiceNumber")
        pDate = request.POST.get("pDate")
        datas = request.POST.get("datas")
        subTotal = request.POST.get("subTotal")
        taxable = request.POST.get("taxable")
        totalFinal = request.POST.get("totalFinal")
        roundOff = request.POST.get("roundOff")
        taxableGST = request.POST.get("taxableGST")
        bill_disc = request.POST.get("bill_disc")
        GrandTotal = request.POST.get("GrandTotal")
        otherCharges = request.POST.get("otherCharges")
        chequeDetail = request.POST.get("chequeDetail")
        deliveryNote = request.POST.get("deliveryNote")
        supplierReference = request.POST.get("supplierReference")
        orderNumber = request.POST.get("orderNumber")
        dispatchNumber = request.POST.get("dispatchNumber")
        dispatchThrough = request.POST.get("dispatchThrough")
        otherReference = request.POST.get("otherReference")
        dispatchNoteDate = request.POST.get("dispatchNoteDate")
        destination = request.POST.get("destination")
        company = request.POST.get("company")
        paid = request.POST.get("paid")
        dueOrReturn = request.POST.get("dueOrReturn")
        invoiceSeriesID = request.POST.get("invoiceSeriesID")
        defaultInvoiceSeries = request.POST.get("defaultInvoiceSeries")
        paidAgainstBill = request.POST.get("paidAgainstBill")
        referrerID = request.POST.get("referrerID")

        status = True
        paidDate = datetime.today().date()
        if payment == 'Credit':

            status = False
            paidDate = None
        else:
            cDays = 0

        if customerID == 'NaN':
            cus = Customer()
            cus.name = name
            cus.gst = gst
            cus.phone = phone
            cus.address = address
            cus.state = state
            cus.email = email
            cus.save()
            sale = Sales()
            sale.customerID_id = cus.pk
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.personalDiscount = float(personalDiscount)

            sale.save()
            if referrerID != 'NaN':
                referral = Referrer.objects.get(pk=int(referrerID))
                com = ReferrerTransaction()
                com.addedBy_id = request.user.pk
                com.transactionType = 'Credit'
                com.amount = (referral.commission / 100.0) * float(subTotal)
                com.transactionDate = datetime.today().date()
                com.referrerID_id = int(referrerID)
                com.remark = "For a sale with amount Rs. {} and bill no. {}".format(str(subTotal), str(sale.pk))
                com.save()
                referral.balance = round(referral.balance + com.amount,2)
                referral.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]

                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock - int(item_details[4]))
                pro.save()
                p.save()
            book = SalesLater.objects.get(pk = int(bookingID))
            book.isDeleted = True
            book.save()
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)
        else:

            sale = Sales()
            sale.customerID_id = int(customerID)
            sale.customerName = name
            sale.customerGst = gst
            sale.customerEmail = email
            sale.customerPhone = phone
            sale.customerAddress = address
            sale.customerState = state
            sale.salesType = pType
            sale.paymentType = payment
            sale.creditDays = int(cDays)
            sale.invoiceDate = datetime.strptime(pDate, '%d/%m/%Y')
            if defaultInvoiceSeries != 'N/A':

                sale.invoiceNumber = defaultInvoiceSeries + invoiceNumber
                sale.invoiceSeriesID_id = int(invoiceSeriesID)
                sale.invoiceActualNumber = int(invoiceNumber)
            else:
                sale.invoiceNumber = invoiceNumber
            sale.subTotal = float(subTotal)
            sale.taxable = float(taxable)
            sale.totalFinal = float(totalFinal)
            sale.billDisc = float(bill_disc)
            sale.gst = float(taxableGST)
            sale.roundOff = float(roundOff)
            sale.grandTotal = float(GrandTotal)
            sale.status = status
            sale.paidDate = paidDate
            sale.chequeDetail = chequeDetail
            sale.deliveryNote = deliveryNote
            sale.supplierReference = supplierReference
            sale.buyersOrderNumber = orderNumber
            sale.dispatchDocumentNumber = dispatchNumber
            sale.dispatchThrough = dispatchThrough
            sale.otherReference = otherReference
            if dispatchNoteDate == '':
                sale.dispatchNoteDate = None
            else:
                sale.dispatchNoteDate = datetime.strptime(dispatchNoteDate, '%d/%m/%Y')
            sale.destination = destination
            sale.otherCharges = float(otherCharges)
            sale.companyID_id = int(company)
            sale.addedBy_id = request.user.pk
            sale.paidAmount = float(paid)
            sale.dueOrReturnAmount = float(dueOrReturn)
            sale.paidAgainstBill = float(paidAgainstBill)
            sale.personalDiscount = float(personalDiscount)

            sale.save()
            if referrerID != 'NaN':
                referral = Referrer.objects.get(pk=int(referrerID))
                com = ReferrerTransaction()
                com.addedBy_id = request.user.pk
                com.transactionType = 'Credit'
                com.amount = (referral.commission / 100.0) * float(subTotal)
                com.transactionDate = datetime.today().date()
                com.referrerID_id = int(referrerID)
                com.remark = "For a sale with amount Rs. {} and bill no. {}".format(str(subTotal), str(sale.pk))
                com.save()
                referral.balance = round(referral.balance + com.amount,2)
                referral.save()

            splited_receive_item = datas.split("@")
            for item in splited_receive_item[:-1]:
                item_details = item.split('|')

                p = SalesProduct()
                p.salesID_id = sale.pk
                p.productID_id = int(item_details[0])
                p.productName = item_details[1]
                p.category = item_details[2]
                p.hsn = item_details[3]
                p.quantity = int(item_details[4])
                p.rate = float(item_details[5])
                p.gst = float(item_details[6])
                p.netRate = float(item_details[7])
                p.total = float(item_details[8])
                p.disc = float(item_details[9])
                p.unit = item_details[10]
                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock - int(item_details[4]))
                pro.save()

                p.save()
            book = SalesLater.objects.get(pk=int(bookingID))
            book.isDeleted = True
            book.save()
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)

# referrer

class ReferrerListJson(BaseDatatableView):
    order_columns = ['name', 'balance','commission', 'phone', ]

    def get_initial_queryset(self):

        return Referrer.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(balance__icontains=search) | Q(phone__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''<a href="/referrer/referrer_ledger/{}/" style="font-size:10px;"  class="ui circular facebook icon button violet">
                 <i class="scroll icon"></i>
               </a>

               <button style="font-size:10px;" onclick = "GetCustomerDetail('{}')" class="ui circular facebook icon button green">
                 <i class="pen icon"></i>
               </button>

               <button style="font-size:10px;" onclick ="delCustomer('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                 <i class="trash alternate icon"></i>
               </button>
               <button style="font-size:10px;" onclick = "TakePayment('{}')" class="ui circular  icon button blue">
                               <i class="hand holding usd icon"></i>
                             </button>
               '''.format(item.pk, item.pk, item.pk, item.pk),
            else:
                action = '''<a href="/contact/customer_ledger/{}/" style="font-size:10px;"  class="ui circular facebook icon button violet">
                 <i class="scroll icon"></i>
               </a>

              '''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(item.name),  # escape HTML for security reasons
                escape(item.balance),
                escape(item.commission),
                escape(item.phone),
                action,

            ])
        return json_data


def post_referrer(request):
    if request.method == 'POST':
        cname = request.POST.get("cname")
        cemail = request.POST.get("cemail")
        caddress = request.POST.get("caddress")
        bal = request.POST.get("bal")
        com = request.POST.get("com")
        cphone = request.POST.get("cphone")

        cus = Referrer()
        cus.name = cname
        cus.email = cemail
        cus.address = caddress
        cus.balance = float(bal)
        cus.commission = float(com)
        cus.phone = cphone
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


def get_referrer_list(request):
    data = []
    q = request.GET.get('q')
    for cus in Referrer.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q) ,
                                       isDeleted__exact=False).order_by('name'):
        data_dic = {
            'ID': cus.pk,
            'Name': '#{}|'.format(cus.pk) + cus.name.upper(),
            'Address': cus.address,
            'Commission': str(cus.commission) + '%',

        }
        data.append(data_dic)
    return JsonResponse({'data': data}, safe=False)


def get_referrer_detail(request, id=None):
    instance = get_object_or_404(Referrer, pk=id)
    data = {
        'ID': instance.pk,
        'Name': instance.name,
        'Email': instance.email,
        'Address': instance.address,
        'Balance': instance.balance,
        'Commission': instance.commission,
        'Phone': instance.phone,

    }
    return JsonResponse({'data': data}, safe=False)


def get_referrer_detail_by_name(request):
    q = request.GET.get('q')

    try:
        instance = Referrer.objects.get(pk=int(q), isDeleted__exact=False)

        data = {
            'ID': instance.pk,
            'Name': instance.name,
            'Email': instance.email,
            'Address': instance.address,
            'Commission': instance.commission,
            'Phone': instance.phone,

        }
    except:
        data = {
            'ID': '',
            'Name': '',
            'Email': '',
            'Address': '',
            'Commission': '',
            'Phone': '',

        }

    return JsonResponse({'data': data}, safe=False)


def edit_referrer(request):
    if request.method == 'POST':
        idC = request.POST.get("idC")
        cname = request.POST.get("cname")
        cemail = request.POST.get("cemail")
        caddress = request.POST.get("caddress")
        bal = request.POST.get("bal")
        com = request.POST.get("com")
        cphone = request.POST.get("cphone")

        cus = Referrer.objects.get(pk=int(idC))
        cus.name = cname
        cus.email = cemail
        cus.address = caddress
        cus.balance = float(bal)
        cus.commission  = float(com)
        cus.phone = cphone
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def delete_referrer(request):
    if request.method == 'POST':
        idC = request.POST.get("userID")

        cus = Referrer.objects.get(pk=int(idC))
        cus.isDeleted = True
        cus.save()
        return JsonResponse({'message': 'success'}, safe=False)


@csrf_exempt
def take_referrer_payment(request):
    if request.method == 'POST':
        id = request.POST.get("ID")
        Amount = request.POST.get("Amount")
        tType = request.POST.get("tType")
        tdate = request.POST.get("tdate")
        remark = request.POST.get("remark")
        ref = Referrer.objects.get(pk=int(id))
        if tType == 'Credit':
            ref.balance = (ref.balance + float(Amount))
        if tType =='Debit':
            ref.balance = (ref.balance - float(Amount))

        ref.save()
        pay = ReferrerTransaction()
        pay.transactionType = tType
        pay.amount = float(Amount)
        pay.remark = remark
        pay.referrerID_id = int(id)
        pay.transactionDate = datetime.strptime(tdate, '%d/%m/%Y')
        pay.addedBy_id = request.user.pk
        pay.save()
        return JsonResponse({'message': 'success'}, safe=False)


class TransactionListByReferrerJson(BaseDatatableView):
    order_columns = ['id', 'transactionDate', 'amount',
                     'transactionType', 'remark', 'datetime' ]

    def get_initial_queryset(self):
        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return ReferrerTransaction.objects.filter(isDeleted__exact=False, referrerID_id=self.request.GET.get('ID'))
        else:
            return ReferrerTransaction.objects.filter(isDeleted__exact=False,
                                                      referrerID_id=self.request.GET.get('ID'))

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(referrerID__name__icontains=search)
                | Q(amount__icontains=search) | Q(transactionType__icontains=search)
                | Q(remark__icontains=search)
                | Q(transactionDate__icontains=search)
            )

        return qs

    def prepare_results(self, qs):
        json_data = []
        i = 1
        for item in qs:
            if item.transactionType == 'Credit':
                trans = '<span class="ui green label">Credit</span>'
            else:
                trans = '<span class="ui red label">Debit</span>'

            # if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            #     action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
            #                    <i class="receipt icon"></i>
            #                  </button>
            #
            #
            #
            #                  <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
            #                    <i class="trash alternate icon"></i>
            #                  </button>'''.format(item.pk, item.pk, item.pk),
            # else:
            #     action = '''<button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
            #                    <i class="receipt icon"></i>
            #                  </button>'''.format(item.pk, item.pk, item.pk),
            json_data.append([
                escape(i),  # escape HTML for security reasons
                escape(item.transactionDate),
                escape(item.amount),
                trans,
                escape(item.remark),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
            ])
            i = i + 1
        return json_data

def error_404(request, exception):
        data = {}
        return render(request, 'home/error/404.html', data)


def error_500(request, exception):
    data = {}
    return render(request, 'home/error/500.html', data)


def daily_report(request):
    mode = ['Cash','Card','Credit','Cheque']
    cash_sale_total = 0.0
    card_sale_total = 0.0
    credit_sale_total = 0.0
    cheque_sale_total = 0.0
    sales_user =CompanyUser.objects.all().order_by('name')
    expense = Expense.objects.filter(expenseDate__exact=datetime.today().date())
    total_expense = 0.0
    for e in expense:
        total_expense += e.amount
    user_data =[]
    for user in sales_user:
        cash_sale_user = 0.0
        card_sale_user = 0.0
        credit_sale_user = 0.0
        cheque_sale_user = 0.0
        for c in mode:
            today_sales = Sales.objects.filter(paymentType__iexact=c,addedBy_id=user.user_ID_id, invoiceDate__exact=datetime.today().date())
            for s in today_sales:
                if c == 'Cash':
                    cash_sale_user += s.grandTotal
                    cash_sale_total += s.grandTotal
                if c == 'Card':
                    card_sale_user += s.grandTotal
                    card_sale_total += s.grandTotal
                if c == 'Credit':
                    credit_sale_user += s.grandTotal
                    credit_sale_total += s.grandTotal
                if c == 'Cheque':
                    cheque_sale_user += s.grandTotal
                    cheque_sale_total += s.grandTotal


        data = {
            'name':user.name,
            'target': user.target,
            'cash':cash_sale_user,
            'card':card_sale_user,
            'credit':credit_sale_user,
            'cheque':cheque_sale_user,
            'total':cash_sale_user+card_sale_user+credit_sale_user+cheque_sale_user
        }
        user_data.append(data)


    cash_sale_user = 0.0
    card_sale_user = 0.0
    credit_sale_user = 0.0
    cheque_sale_user = 0.0
    for c in mode:
        today_sales = Sales.objects.filter(paymentType__iexact=c,addedBy__username='Admin', invoiceDate__exact=datetime.today().date())
        for s in today_sales:
            if c == 'Cash':
                cash_sale_user += s.grandTotal
                cash_sale_total += s.grandTotal
            if c == 'Card':
                card_sale_user += s.grandTotal
                card_sale_total += s.grandTotal
            if c == 'Credit':
                credit_sale_user += s.grandTotal
                credit_sale_total += s.grandTotal
            if c == 'Cheque':
                cheque_sale_user += s.grandTotal
                cheque_sale_total += s.grandTotal
    admin_data = {
        'name': "Admin",
        'target': "N/A",
        'cash': cash_sale_user,
        'card': card_sale_user,
        'credit': credit_sale_user,
        'cheque': cheque_sale_user,
        'total': cash_sale_user + card_sale_user + credit_sale_user + cheque_sale_user
    }

    context = {
        'date':datetime.today().date(),
        'admin_data':admin_data,
        'users':user_data,
        'cash_sale_total':cash_sale_total,
        'card_sale_total':card_sale_total,
        'credit_sale_total':credit_sale_total,
        'cheque_sale_total':cheque_sale_total,
        'sale_total':cash_sale_total+card_sale_total+credit_sale_total+cheque_sale_total,
        'total_expense':total_expense,
        'cash_in_hand':cash_sale_total-total_expense
    }


    return render(request, 'home/dailyReport.html',context)

# Product Batch

class ProductBatchListJson(BaseDatatableView):
    order_columns = ['batchNumber', 'quantity', 'rate', 'mrp',
                     'mDate', 'eDate', 'location', 'additionalDetail', 'datetime'
                     ]

    def get_initial_queryset(self):
        batchProductID = self.request.GET.get('batchProductID')
        if batchProductID != '':
            return ProductBatch.objects.filter(isDeleted__exact=False,productID_id=int(batchProductID))
        else:
            return ProductBatch.objects.filter(isDeleted__exact=True)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(batchNumber__icontains=search) | Q(mDate__icontains=search)
                | Q(eDate__icontains=search) | Q(location__icontains=search)
                | Q(additionalDetail__icontains=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''
                <button style="font-size:10px;" onclick = "GetProductBatchDetail('{}')" class="ui circular facebook icon button green">
                                               <i class="pen icon"></i>
                                             </button>

                                             <button style="font-size:10px;" onclick ="delProductBatch('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                                               <i class="trash alternate icon"></i>
                                             </button></td>'''.format(item.pk, item.pk),
            else:
                action = '<button class="mini ui button">Denied</button>'

            json_data.append([
                escape(item.batchNumber),  # escape HTML for security reasons
                escape(item.quantity),
                escape(item.rate),
                escape(item.mrp),
                escape(item.mDate),
                escape(item.eDate),
                escape(item.location),
                escape(item.additionalDetail),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action,
                item.id
                ,

            ])
        return json_data


def post_product_batch_detail(request):
    if request.method == 'POST':
        try:
            batchProductID = request.POST.get("batchProductID")
            batchNumber = request.POST.get("batchNumber")
            batchQuantity = request.POST.get("batchQuantity")
            batchRate = request.POST.get("batchRate")
            batchMrp = request.POST.get("batchMrp")
            manufactureBatch = request.POST.get("manufactureBatch")
            expiryBatch = request.POST.get("expiryBatch")
            locationBatch = request.POST.get("locationBatch")
            additionBatch = request.POST.get("additionBatch")

            p = Product.objects.get(pk = int(batchProductID))
            b = ProductBatch()
            b.productID_id = int(batchProductID)
            b.batchNumber = batchNumber
            b.quantity = float(batchQuantity)
            b.rate = float(batchRate)
            b.mrp = float(batchMrp)
            b.additionalDetail = additionBatch
            b.location = locationBatch
            b.mDate = datetime.strptime(manufactureBatch, '%d/%m/%Y')
            b.eDate = datetime.strptime(expiryBatch, '%d/%m/%Y')
            p.stock = p.stock + float(batchQuantity)
            b.save()
            p.save()
            return JsonResponse({'message': 'success'}, safe=False)

        except:
            return JsonResponse({'message': 'error'}, safe=False)


def get_product_batch_detail(request, id=None):
    instance = get_object_or_404(ProductBatch, pk=id)
    data = {
        'ID': instance.pk,
        'ProductID': instance.productID.pk,
        'BatchNumber': instance.batchNumber,
        'Quantity': instance.quantity,
        'Mrp': instance.mrp,
        'Rate': instance.rate,
        'MDate': instance.mDate.strftime('%d/%m/%Y'),
        'EDate': instance.eDate.strftime('%d/%m/%Y'),
        'Location': instance.location,
        'AdditionalDetail': instance.additionalDetail,


    }
    return JsonResponse({'data': data}, safe=False)


def edit_product_batch_detail(request):
    if request.method == 'POST':
        try:
            batchID = request.POST.get("batchID")
            batchProductID = request.POST.get("batchProductID")
            batchNumber = request.POST.get("batchNumber")
            batchQuantity = request.POST.get("batchQuantity")
            batchRate = request.POST.get("batchRate")
            batchMrp = request.POST.get("batchMrp")
            manufactureBatch = request.POST.get("manufactureBatch")
            expiryBatch = request.POST.get("expiryBatch")
            locationBatch = request.POST.get("locationBatch")
            additionBatch = request.POST.get("additionBatch")

            p = Product.objects.get(pk = int(batchProductID))
            b = ProductBatch.objects.get(pk=int(batchID))
            p.stock = p.stock - float(b.quantity) + float(batchQuantity)
            b.productID_id = int(batchProductID)
            b.batchNumber = batchNumber
            b.quantity = float(batchQuantity)
            b.rate = float(batchRate)
            b.mrp = float(batchMrp)
            b.additionalDetail = additionBatch
            b.location = locationBatch
            b.mDate = datetime.strptime(manufactureBatch, '%d/%m/%Y')
            b.eDate = datetime.strptime(expiryBatch, '%d/%m/%Y')
            b.save()
            p.save()
            return JsonResponse({'message': 'success'}, safe=False)

        except:
            return JsonResponse({'message': 'error'}, safe=False)


@csrf_exempt
def delete_product_batch(request):
    if request.method == 'POST':
        idC = request.POST.get("ID")

        b = ProductBatch.objects.get(pk=int(idC))
        p = Product.objects.get(pk=b.productID_id)
        p.stock = p.stock - b.quantity
        b.isDeleted = True
        p.save()
        b.save()
        return JsonResponse({'message': 'success'}, safe=False)



def download_product_sales_report(request):
    companyID = request.GET.get('companyID')
    eType = request.GET.get('eType')
    sDate = request.GET.get('startDate')
    eDate = request.GET.get('endDate')
    startDate = datetime.strptime(sDate, '%d/%m/%Y')
    endDate = datetime.strptime(eDate, '%d/%m/%Y')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ProductSalesReport({}--{}).xlsx"'.format(sDate, eDate)
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    ex = SalesProduct.objects.filter(isDeleted__exact=False, salesID__invoiceDate__gte=startDate.date(),
                                salesID__invoiceDate__lte=endDate.date() + timedelta(days=1)).order_by('productID_id')

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Serial No.', bold)
    worksheet.write('B1', 'Product Name.', bold)
    worksheet.write('C1', 'BarCode', bold)
    worksheet.write('D1', 'Quantity', bold)
    # worksheet.write('D1', 'Amount', bold)
    # worksheet.write('E1', 'Description', bold)
    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    total = 0.0
    p_list = []
    for p in ex:
        p_list.append(p.productID.pk)

    # Iterate over the data and write it out row by row.
    for item in tuple(set(p_list)):
        p_name = Product.objects.get(pk = int(item))
        p_sale_count = SalesProduct.objects.filter(productID_id=int(item),salesID__invoiceDate__gte=startDate.date(),
                                salesID__invoiceDate__lte=endDate.date() + timedelta(days=1)).aggregate(Sum('quantity'))
        worksheet.write(row, col, row)
        worksheet.write(row, col + 1, p_name.name)
        worksheet.write(row, col + 2,p_name.barcode)
        worksheet.write(row, col + 3, str(p_sale_count['quantity__sum']))
        # worksheet.write(row, col + 4, item.description)
        row += 1
        # total = total + item.amount

    # Write a total using a formula.
    # worksheet.write(row, 2, 'Total', bold)
    # worksheet.write(row, 3, total)

    workbook.close()
    # response.write(workbook)
    return response