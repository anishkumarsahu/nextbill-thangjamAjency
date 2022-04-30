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

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape



@is_activated()
def sales_executive(request):
    return render(request, 'ecomApp/userEcom.html')



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
        'IsActive': C_User.isActive,
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

        edit_user = ExecutiveUser.objects.get(pk=int(ID))

        edit_user.name = EditCompanyUserName
        edit_user.phone = EditUserPhoneNo
        edit_user.email = EditUserEmail
        edit_user.address = EditUserAddress
        edit_user.zip = EditUserZip
        edit_user.state = EditUserState
        edit_user.city = EditUserCity
        edit_user.target = float(EditUserTarget)
        edit_user.save()

        return JsonResponse({'message': 'success'}, safe=False)

