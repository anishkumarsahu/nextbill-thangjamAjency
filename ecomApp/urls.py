from django.conf.urls import url
from .views import *

urlpatterns = [
    # Executive
    url(r'^home/$', home, name='home'),
    url(r'^browse_products/$', browse_products, name='browse_products'),

    # admin
    url(r'^sales_executive/$', sales_executive, name='sales_executive'),
    url(r'^ExecutiveUserListJson/$', ExecutiveUserListJson.as_view(), name='ExecutiveUserListJson'),

    url(r'^api/post_User_executive/$', post_User_executive, name='post_User_executive'),
    url(r'^api/delete_executive/$', delete_executive, name='delete_executive'),
    url(r'^api/get_executive_detail/$', get_executive_detail, name='get_executive_detail'),
    url(r'^api/Edit_executive/$', Edit_executive, name='Edit_executive'),

    # product images
    url(r'^product_images/$', product_images, name='product_images'),
    url(r'^ProductListForImageJson/$', ProductListForImageJson.as_view(), name='ProductListForImageJson'),
    url(r'^add_product_image_api/$', add_product_image_api, name='add_product_image_api'),
    url(r'^product_image_list_api/$', product_image_list_api, name='product_image_list_api'),
    url(r'^delete_product_image_api/$', delete_product_image_api, name='delete_product_image_api'),


    url(r'^get_customer_ledger_detail/$', get_customer_ledger_detail, name='get_customer_ledger_detail'),
    url(r'^product_list_api/(?P<Page>[0-9]+)/$', product_list_api, name='product_list_api'),
    url(r'^get_product_detail_for_cart_api/$', get_product_detail_for_cart_api, name='get_product_detail_for_cart_api'),


    url(r'^add_booking_from_ecom/$', add_booking_from_ecom, name='add_booking_from_ecom'),
    url(r'^BookingEcomListByUserJson/$', BookingEcomListByUserJson.as_view(), name='BookingEcomListByUserJson'),
    url(r'^BookingEcomListByAdminJson/$', BookingEcomListByAdminJson.as_view(), name='BookingEcomListByAdminJson'),
    url(r'^booking_list_ecom/$', booking_list_ecom, name='booking_list_ecom'),
    url(r'^ecom_booking_list_admin/$', ecom_booking_list_admin, name='ecom_booking_list_admin'),
    url(r'^EcomBookingSale/(?P<id>[0-9]+)/$', EcomBookingSale, name='EcomBookingSale'),

]