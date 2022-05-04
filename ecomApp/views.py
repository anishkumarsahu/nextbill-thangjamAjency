import calendar
from django.core import management
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
from activation.views import is_activated
from home.numberToWord import num2words
from .models import *
from home.models import *
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape



@is_activated()
def sales_executive(request):
    return render(request, 'ecomApp/userEcom.html')



@is_activated()
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



@is_activated()
def product_images(request):
    return render(request, 'ecomApp/productImages.html')


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
