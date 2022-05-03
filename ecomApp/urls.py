from django.conf.urls import url
from .views import *

urlpatterns = [
    # pages
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


    ]