import calendar
from django.core import management
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.template import loader
from django.template.defaultfilters import register
from django.utils.crypto import get_random_string
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from datetime import datetime, timedelta

from activation.models import Validity
from activation.views import is_activated, is_ecom_activated
from home.numberToWord import num2words
from home.views import check_group

from .models import *
from home.models import *
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape


@check_group('Admin')
@is_ecom_activated()
def sales_executive(request):
    return render(request, 'ecomApp/userEcom.html')

@check_group('Admin')
@is_ecom_activated()
def ecom_booking_list_admin(request):
    return render(request, 'ecomApp/ecomBookingListAdmin.html')


@check_group('Executive')
@is_ecom_activated()
def browse_products(request):
    product = request.GET.get('product')
    if product == '' or product == None:
        product = ''
    context = {
        "product":product
    }
    return render(request, 'ecomApp/productList.html', context)

@check_group('Executive')
@is_ecom_activated()
def home(request):
    customers = Customer.objects.filter(isDeleted__exact=False).order_by('name')
    context = {
        'customers':customers
    }
    return render(request, 'ecomApp/executiveHome.html', context)



class ExecutiveUserListJson(BaseDatatableView):
    order_columns = ['name', 'username', 'userPassword', 'phone', 'address', 'city',
                     'zip', 'state', 'email', 'isActive', 'target'
                     ]

    def get_initial_queryset(self):

        return ExecutiveUser.objects.filter(isDeleted__exact=False)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(username__icontains=search) | Q(userPassword__icontains=search) | Q(name__icontains=search) | Q(
                    phone__icontains=search)
                | Q(address__icontains=search) | Q(city__icontains=search)
                | Q(zip__icontains=search) | Q(state__icontains=search) | Q(target__icontains=search)
                | Q(email__icontains=search) | Q(isActive__icontains=search)
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
                escape(item.isActive),
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


# For User
@transaction.atomic
def post_User_executive(request):
    if request.method == 'POST':
        CompanyUserName = request.POST.get("CompanyUserName")
        UserPhoneNo = request.POST.get("UserPhoneNo")
        UserEmail = request.POST.get("UserEmail")
        UserAddress = request.POST.get("UserAddress")
        UserZip = request.POST.get("UserZip")
        UserState = request.POST.get("UserState")
        UserCity = request.POST.get("UserCity")
        UserPwd = request.POST.get("UserPwd")
        Target = request.POST.get("Target")

        user = ExecutiveUser()

        user.name = CompanyUserName
        user.phone = UserPhoneNo
        user.email = UserEmail
        user.address = UserAddress
        user.zip = UserZip
        user.state = UserState
        user.city = UserCity
        user.userPassword = UserPwd
        user.target = float(Target)

        username = 'EUSER' + get_random_string(length=5, allowed_chars='1234567890')
        while User.objects.filter(username__exact=username).count() > 0:
            username = 'EUSER' + get_random_string(length=5, allowed_chars='1234567890')
        else:
            new_user = User()
            new_user.username = username
            new_user.set_password(UserPwd)

            new_user.save()
            user.username = username
            user.user_ID_id = new_user.pk

            user.save()

            try:
                g = Group.objects.get(name='Executive')
                g.user_set.add(new_user.pk)
                g.save()

            except:
                g = Group()
                g.name = "Executive"
                g.save()
                g.user_set.add(new_user.pk)
                g.save()

            return JsonResponse({'message': 'success'}, safe=False)


@transaction.atomic
@csrf_exempt
def delete_executive(request):
    if request.method == 'POST':
        try:
            id = request.POST.get("userID")
            company = ExecutiveUser.objects.get(pk=int(id))
            company.isDeleted = True
            company.save()

            return JsonResponse({'message': 'success'}, safe=False)
        except:
            return JsonResponse({'message': 'error'}, safe=False)


def get_executive_detail(request):
    id = request.GET.get('id')
    C_User = get_object_or_404(ExecutiveUser, id=id)
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
        'IsActive': str(C_User.isActive).capitalize(),
        'Target': C_User.target,

    }
    return JsonResponse({'data': data}, safe=False)


@transaction.atomic
def Edit_executive(request):
    if request.method == 'POST':
        ID = request.POST.get("UserID")
        EditCompanyUserName = request.POST.get("EditCompanyUserName")
        EditUserPhoneNo = request.POST.get("EditUserPhoneNo")
        EditUserEmail = request.POST.get("EditUserEmail")
        EditUserAddress = request.POST.get("EditUserAddress")
        EditUserZip = request.POST.get("EditUserZip")
        EditUserState = request.POST.get("EditUserState")
        EditUserCity = request.POST.get("EditUserCity")
        EditUserTarget = request.POST.get("EditUserTarget")
        isActive = request.POST.get("isActive")
        edit_user = ExecutiveUser.objects.get(pk=int(ID))

        edit_user.name = EditCompanyUserName
        edit_user.phone = EditUserPhoneNo
        edit_user.email = EditUserEmail
        edit_user.address = EditUserAddress
        edit_user.zip = EditUserZip
        edit_user.state = EditUserState
        edit_user.city = EditUserCity
        edit_user.target = float(EditUserTarget)
        user = User.objects.get(pk=edit_user.user_ID_id)
        if isActive == 'True':

            edit_user.isActive = True
            user.is_active = True
        else:
            edit_user.isActive = False
            user.is_active = False
        edit_user.save()
        user.save()

        return JsonResponse({'message': 'success'}, safe=False)


@check_group('Admin')
@is_ecom_activated()
def product_images(request):
    return render(request, 'ecomApp/productImages.html')



@check_group('Executive')
@is_ecom_activated()
def booking_list_ecom(request):
    return render(request, 'ecomApp/ecomBookingListUser.html')



# done
class ProductListForImageJson(BaseDatatableView):
    order_columns = ['name', 'brand', 'categoryID', 'mrp','cost', 'spWithoutGst', 'spWithGst','barcode']

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
                | Q(spWithGst__icontains=search)
            ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            images = '<button class="mini ui red button">No Image Added</button>'
            img = ProductImage.objects.filter(productID_id=item.pk, isDeleted__exact=False)
            if img.count() < 1:
                images = '<button class="mini ui red button">No Image Added</button>'
            else:
                images =''
                for i in img:
                    images += '<img class="ui avatar image" src="{}">'.format(i.productImage.thumbnail.url)

            if 'Admin' in self.request.user.groups.values_list('name', flat=True):
                action = '''
                    <button style="font-size:10px;" onclick = "GetProductImageDetail('{}')" class="ui circular facebook icon button green">
                                               <i class="image icon"></i>
                                             </button>

                        '''.format(item.pk),
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
                images,
                action,

            ])
        return json_data


@transaction.atomic
@csrf_exempt
def add_product_image_api(request):
    if request.method == 'POST':
        try:
            productID = request.POST.get("productID")
            imageUpload = request.FILES["imageUpload"]

            pro = ProductImage()
            pro.productID_id = int(productID)
            pro.productImage = imageUpload
            pro.save()
            return JsonResponse({'message': 'success'}, safe=False)
        except:
            return JsonResponse({'message': 'error'}, safe=False)

@csrf_exempt
def product_image_list_api(request):
    productID = request.POST.get("productID")
    pro = ProductImage.objects.filter(productID_id=int(productID), isDeleted__exact=False)
    pro_list = []
    for p in pro:
        pro_dic ={
            'ImageID': p.id,
            'Image':p.productImage.medium.url
        }
        pro_list.append(pro_dic)



    return JsonResponse({'message': 'success', 'data':pro_list}, safe=False)



@csrf_exempt
def delete_product_image_api(request):
    if request.method == 'POST':
        idC = request.POST.get("ID")

        cus = ProductImage.objects.get(pk=int(idC))
        cus.delete()
        return JsonResponse({'message': 'success'}, safe=False)



@csrf_exempt
def get_customer_ledger_detail(request):
    try:
        q = request.GET.get('q')
        id = str(q).split('|')
        instance = Customer.objects.get(pk=int(id[1]), isDeleted__exact=False)
        all_sales = Sales.objects.filter(isDeleted__exact=False, customerID_id=instance.pk)
        pay = TakePayment.objects.filter(customerID_id=instance.pk)

        paid = 0.0
        total = 0.0
        for s in all_sales:
            paid = paid + s.paidAgainstBill
            total = total + s.grandTotal

        for p in pay:
            paid = paid + p.amount
        due = total - paid

        return JsonResponse({'message': 'success', 'total':total, 'paid':paid , 'due':due, 'name':instance.name.capitalize(), 'address':instance.address, 'id':instance.pk }, safe=False)
    except:
        return JsonResponse({'message': 'error'}, safe=False)

def product_list_api(request, *args,**kwargs):

    try:

        # print
        searchProduct = request.GET.get('searchProduct')
        if searchProduct != '' :
            products = Product.objects.filter(Q(name__icontains=searchProduct) | Q(categoryID__brand__icontains=searchProduct) | Q(categoryID__name__icontains=searchProduct),isDeleted__exact=False).order_by('name')
        else:
            products = Product.objects.filter(isDeleted__exact=False).order_by('name')

        Index = kwargs['Page']
        paginator = Paginator(products, 8)
        try:
            products = paginator.page(Index)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = []

        product_list = []

        for product in products:
            # try:
            #     Wish = Wishlist.objects.get(customerID__userID_id=request.user.pk, isDeleted__exact=False,
            #                                 productID_id=product.pk)
            #     myWish = 'Y'
            # except:
            #     myWish = 'N'
            image = ProductImage.objects.filter(productID_id=product.pk, isDeleted__exact=False)
            if image.count() > 0:
                oriImage = image[0].productImage.medium.url
            else:
                oriImage = 'https://icons.iconarchive.com/icons/graphicloads/100-flat/256/shopping-icon.png'

            if product.stock > 0:
                stock = '<span style="color:green;font-weight:bold" class="date">/- {} {} Available </span>'.format(product.stock, product.unitID.name)
            else:
                stock = '<span style="color:red;" class="date">Out Of Stock </span>'
            product_dic = {
                'Name': str(product.name).capitalize(),
                'ID': product.pk,
                'OriImageURL': oriImage,
                'Category': product.categoryID.name +'/' + product.categoryID.brand,
                'Mrp': product.mrp,
                'IsAvailable': stock
            }
            product_list.append(product_dic)
        return JsonResponse({'message': 'success', 'data': product_list})
    except:
        return JsonResponse({'message': 'error'})


def get_product_detail_for_cart_api(request):
    try:
        ID = request.GET.get('ID')
        product = Product.objects.get(pk = int(ID))
        order_pro = BookingProductList.objects.filter(productID_id=product.pk, salesID__isSold__exact=False, isDeleted__exact=False)
        o_c = 0.0
        for p in order_pro:
            o_c = o_c + p.quantity

        if product.stock > 0:
            stock = '<span style="color:green;font-weight:bold" class="date">{} {} Available </span>'.format(
                product.stock, product.unitID.name)
        else:
            stock = '<span style="color:red;" class="date">Out Of Stock </span>'
        data = {
            'Name': str(product.name).capitalize(),
            'ID': product.pk,
            'Category': product.categoryID.name + '/ ' + product.categoryID.brand,
            'Mrp': product.mrp,
            'IsAvailable': stock,
            'Unit': product.unitID.name,
            'BookingCount':o_c
        }
        return JsonResponse({'message': 'success', 'data': data})
    except:
        return JsonResponse({'message': 'error'})

@csrf_exempt
@transaction.atomic
def add_booking_from_ecom(request):
    if request.method == 'POST':

        cus = request.POST.get("cus")
        cusID = request.POST.get("cusID")
        # pDate = request.POST.get("pDate")
        datas = request.POST.get("datas")
        grandTotal = request.POST.get("grandTotal")
        deliveryDate = request.POST.get("deliveryDate")

        # paidDate = datetime.today().date()


        sale = BookingEcom()
        sale.customerID_id = int(cusID)
        sale.customerName = cus

        sale.expectedDeliveryDate = datetime.strptime(deliveryDate, '%d/%m/%Y')

        sale.grandTotal = float(grandTotal)

        sale.companyID_id = 1
        sale.addedBy_id = request.user.pk
        euser = ExecutiveUser.objects.get(user_ID=request.user.pk)
        sale.addedByUser = euser.name


        sale.save()

        splited_receive_item = datas.split("@")
        for item in splited_receive_item[:-1]:
            item_details = item.split('|')
            pro = Product.objects.get(pk = int(item_details[0]))

            p = BookingProductList()
            p.salesID_id = sale.pk
            p.productID_id = int(item_details[0])
            p.productName = item_details[1]
            p.category = pro.categoryID.name
            p.hsn = pro.categoryID.hsnID.hsn
            p.gst = pro.categoryID.hsnID.tax
            p.unit = pro.unitID.name
            p.quantity = int(item_details[3])
            p.netRate = float(item_details[2])
            p.total = float(item_details[4])
            p.margin = 1.0
            try:
                bat = ProductBatch.objects.filter(productID_id=int(item_details[0])).first()
                p.batchID_id = bat.pk
            except:
                pass
            p.save()

        return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)



class BookingEcomListByUserJson(BaseDatatableView):
    order_columns = ['customerName', 'expectedDeliveryDate',  'grandTotal', 'isSold', 'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        # if 'Admin' in self.request.user.groups.values_list('name', flat=True):
        #     return SalesLater.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
        #                                      invoiceDate__lte=endDate.date() + timedelta(days=1))
        # else:
        return BookingEcom.objects.filter(isDeleted__exact=False, addedBy_id = self.request.user.pk,
                                             datetime__gte=startDate.date(),
                                            datetime__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(customerName__icontains=search) |  Q(isSold__icontains=search)
                | Q(grandTotal__icontains=search) ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            action = '''
                <a style="font-size:10px;" data-tooltip="Booking Detail" position="bottom left"  data-inverted="" 
                 data-variation="tiny"  onclick = "GetBookingDetail('{}')" class="ui circular  icon button pink">
                          <i class="clipboard outline icon"></i>
                         </a>
            '''.format(item.pk)
            # action = '''
            #              <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
            #                <i class="trash alternate icon"></i>
            #              </button>'''.format(item.pk, item.pk, item.pk)
            if item.isSold == True:
                sold = '<button class="ui tiny active green button" type="button" >  Yes </button>'
                action = action + '''
                <a style="font-size:10px;" data-tooltip="Invoice" position="bottom left"  data-inverted="" 
                 data-variation="tiny"  onclick = "GetSaleDetail('{}')" class="ui circular  icon button teal">
                           <i class="file invoice icon"></i>
                         </a>
                '''.format(item.confirmBookID)
            else:
                sold = '<button class="ui tiny active red button" type="button" >  No </button>'
            json_data.append([
                escape(item.customerName),  # escape HTML for security reasons
                escape(item.expectedDeliveryDate),
                escape(item.grandTotal),
                sold,
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action
            ])
        return json_data


class BookingEcomListByAdminJson(BaseDatatableView):
    order_columns = ['customerName', 'expectedDeliveryDate',  'grandTotal','isSold','addedByUser', 'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
        #     return SalesLater.objects.filter(isDeleted__exact=False, invoiceDate__gte=startDate.date(),
        #                                      invoiceDate__lte=endDate.date() + timedelta(days=1))
        # else:
            return BookingEcom.objects.filter(isDeleted__exact=False,
                                                 datetime__gte=startDate.date(),
                                                datetime__lte=endDate.date() + timedelta(days=1))

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(customerName__icontains=search) |Q(addedByUser__icontains=search) | Q(grandTotal__icontains=search) ).order_by('-id')

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if 'Admin' in self.request.user.groups.values_list('name', flat=True):

                action = '''<a style="font-size:10px;" href="/ecom/EcomBookingSale/{}" class="ui circular  icon button green">
                               <i class="clipboard check icon"></i>
                             </a>



                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            else:
                action = '''<a style="font-size:10px;" href="/ecom/EcomBookingSale/{}" class="ui circular  icon button green">
                               <i class="clipboard check icon"></i>
                             </a>



                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button>'''.format(item.pk, item.pk, item.pk),
            if item.isSold == True:
                sold = '<button class="ui tiny active green button" type="button" >  Yes </button>'
            else:
                sold = '<button class="ui tiny active red button" type="button" >  No </button>'
            json_data.append([
                escape(item.customerName),  # escape HTML for security reasons
                escape(item.expectedDeliveryDate),
                escape(item.grandTotal),
                sold,
                escape(item.addedByUser),
                escape(item.datetime.strftime('%d-%m-%Y %I:%M %p')),
                action
            ])
        return json_data

@is_ecom_activated()
@check_group('Admin')
def EcomBookingSale(request, id=None):
    if request.user.is_authenticated:
        instance = get_object_or_404(BookingEcom, pk=id)
        pro = BookingProductList.objects.filter(salesID_id=instance.pk)

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

        return render(request, 'ecomApp/ecomBookingSale.html', context)
    else:
        return redirect('homeApp:loginPage')

@csrf_exempt
@transaction.atomic
def add_sales_from_booking_ecom(request):
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
            sale.saleFrom = "ByEcom"

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
                referral.balance = round(referral.balance + com.amount, 2)
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
                p.margin = float(item_details[12])

                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock - int(item_details[4]))
                pro.save()
                p.save()
            book = BookingEcom.objects.get(pk=int(bookingID))
            # book.isDeleted = True
            book.isSold = True
            book.confirmBookID = sale.pk
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
            sale.saleFrom = "ByEcom"
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
                referral.balance = round(referral.balance + com.amount, 2)
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
                p.margin = float(item_details[12])
                pro = Product.objects.get(pk=int(int(item_details[0])))
                ori_stock = pro.stock
                pro.stock = (ori_stock - int(item_details[4]))
                pro.save()

                p.save()
            book = BookingEcom.objects.get(pk=int(bookingID))
            # book.isDeleted = True
            book.isSold = True
            book.confirmBookID = sale.pk
            book.save()
            return JsonResponse({'message': 'success', 'saleID': sale.pk}, safe=False)

@check_group('Admin')
@is_ecom_activated()
def ecom_salesReport(request):
    return render(request, 'ecomApp/salesReportEcom.html')


class EcomSalesListJson(BaseDatatableView):
    order_columns = ['customerName', 'customerGst', 'invoiceDate', 'id', 'invoiceNumber',
                     'grandTotal', 'paidAgainstBill', 'dueOrReturnAmount', 'paymentType', 'saleFrom', 'salesType',
                     'datetime', ]

    def get_initial_queryset(self):
        sDate = self.request.GET.get('startDate')
        eDate = self.request.GET.get('endDate')
        startDate = datetime.strptime(sDate, '%d/%m/%Y')
        endDate = datetime.strptime(eDate, '%d/%m/%Y')

        if 'Admin' in self.request.user.groups.values_list('name', flat=True):
            return Sales.objects.filter( isDeleted__exact=False, invoiceDate__range=(startDate.date(), endDate.date()), saleFrom__exact='ByEcom')
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return Sales.objects.filter(isDeleted__exact=False, companyID_id=user.company_ID_id,
                                        invoiceDate__range=(startDate.date(), endDate.date()), saleFrom__exact='ByEcom')

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(customerName__icontains=search) | Q(customerGst__icontains=search) | Q(id__icontains=search)
                | Q(invoiceDate__icontains=search) | Q(invoiceNumber__icontains=search)
                | Q(salesType__icontains=search)| Q(saleFrom__icontains=search)
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

                action = '''<span style="display:flex;"><button style="font-size:10px;" onclick = "TakePayment('{}')" class="ui circular  icon button blue">
                               <i class="hand holding usd icon"></i>
                             </button><button style="font-size:10px;" onclick = "GetSaleDetail('{}')" class="ui circular  icon button green">
                               <i class="receipt icon"></i>
                             </button>
                        <a style="font-size:10px;" href="/ecom/edit_sale_ecom/{}/" class="ui circular yellow icon button" style="margin-left: 3px">
                              <i class="pen icon"></i>
                             </a>


                             <button style="font-size:10px;" onclick ="delSale('{}')" class="ui circular youtube icon button" style="margin-left: 3px">
                               <i class="trash alternate icon"></i>
                             </button></span>'''.format(item.pk, item.pk, item.pk, item.pk),
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
                escape(item.saleFrom),
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



class SalesListByProductEcomJson(BaseDatatableView):
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
                                               salesID__invoiceDate__lte=endDate.date(), salesID__saleFrom__exact='ByEcom')
        else:
            user = CompanyUser.objects.get(user_ID=self.request.user.pk)
            return SalesProduct.objects.filter(salesID__isDeleted__exact=False,
                                               salesID__companyID_id=user.company_ID_id,
                                               salesID__invoiceDate__gte=startDate.date(),
                                               salesID__invoiceDate__lte=endDate.date(), salesID__saleFrom__exact='ByEcom')

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

@check_group('Admin')
@is_ecom_activated()
def edit_sale_ecom(request, id=None):
    if request.user.is_authenticated:
        instance = get_object_or_404(Sales, pk=id)
        pro = SalesProduct.objects.filter(salesID_id=instance.pk)

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

        return render(request, 'ecomApp/EditSaleEcom.html', context)
    else:
        return redirect('homeApp:loginPage')



def get_ecom_booking_detail(request, id=None):
    instance = get_object_or_404(BookingEcom, pk=id)
    basic = {
        'Name': instance.customerName,
        'EDate': instance.expectedDeliveryDate,
        'GTotal': instance.grandTotal,

    }
    items = BookingProductList.objects.filter(salesID_id=instance.pk)
    item_list = []
    for i in items:
        item_dic = {
            'ItemID': i.pk,
            'ItemProductName': i.productName,
            'MRP': i.netRate,
            'Quantity': i.quantity,
            'ItemTotal': i.total,

        }
        item_list.append(item_dic)

    data = {
        'Basic': basic,
        'Items': item_list

    }
    return JsonResponse({'data': data}, safe=False)

