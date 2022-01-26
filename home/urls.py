from django.conf.urls import url
from .views import *

urlpatterns = [
    # pages
    url(r'^$', homepage, name='homepage'),
    url(r'^print/$', print_invoice, name='print'),
    url(r'^print_invoicea5/$', print_invoicea5, name='print_invoicea5'),
    url(r'^printBill/$', print_bill, name='print_bill'),
    url(r'^print_billA5/$', print_billA5, name='print_billA5'),
    url(r'^print_bill_thermal/$', print_bill_thermal, name='print_bill_thermal'),
    url(r'^index/$', index, name='index'),
    url(r'^sales/$', sales, name='sales'),
    url(r'^purchase/$', puchase, name='puchase'),
    url(r'^product/$', product, name='product'),
    url(r'^hsnCategory/$', hsn_and_category, name='hsn'),
    url(r'^create_return/$', create_return, name='create_return'),
    url(r'^salesReport/$', salesReport, name='salesReport'),
    url(r'^returnReport/$', returnReport, name='returnReport'),
    url(r'^bookingList/$', bookingList, name='bookingList'),
    url(r'^purchaseReport/$', purchaseReport, name='purchaseReport'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^referrer/$', referrer, name='referrer'),
    url(r'^generalSetting/$', generalSetting, name='generalSetting'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^manage_invoice/$', manage_invoice, name='manage_invoice'),
    url(r'^expense/$', expense, name='expense'),
    url(r'^manageUser/$', manageUser, name='manageUser'),
    url(r'^WareHouse/$', wareHouseList, name='WareHouse'),
    url(r'^loginPage/$', loginPage, name='loginPage'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^report/$', report, name='report'),
    url(r'^contact/customer_ledger/(?P<id>[0-9]+)/$', customer_ledger, name='customer_ledger'),
    url(r'^contact/supplier_ledger/(?P<id>[0-9]+)/$', supplier_ledger, name='supplier_ledger'),
    url(r'^referrer/referrer_ledger/(?P<id>[0-9]+)/$', referrer_ledger, name='referrer_ledger'),

    # customer
    url(r'^CustomerListJson/$', CustomerListJson.as_view(), name='CustomerListJson'),

    url(r'^api/PostCustomerDetail/$', post_customer, name='post_customer'),
    url(r'^api/GetCustomerList/$', get_customer_list, name='get_customer_list'),
    url(r'^api/GetCustomerDetail/(?P<id>[0-9]+)/$', get_customer_detail, name='get_customer_detail'),
    url(r'^api/GetCustomerDetailByName/$', get_customer_detail_by_name, name='get_customer_detail_by_name'),

    url(r'^api/EditCustomerDetail/$', edit_customer, name='edit_customer'),
    url(r'^api/DeleteCustomerDetail/$', delete_customer, name='delete_customer'),

    # supplier
    url(r'^SupplierListJson/$', SupplierListJson.as_view(), name='SupplierListJson'),

    url(r'^api/PostSupplierDetail/$', post_supplier, name='post_supplier'),
    url(r'^api/GetSupplierList/$', get_supplier_list, name='get_supplier_list'),
    url(r'^api/GetSupplierDetail/(?P<id>[0-9]+)/$', get_supplier_detail, name='get_supplier_detail'),
    url(r'^api/GetSupplierDetailByName/$', get_supplier_detail_by_name, name='get_supplier_detail_by_name'),
    url(r'^api/EditSupplierDetail/$', edit_supplier, name='edit_supplier'),
    url(r'^api/DeleteSupplierDetail/$', delete_supplier, name='delete_supplier'),

    # HSN
    url(r'^HsnListJson/$', HsnListJson.as_view(), name='HsnListJson'),

    url(r'^api/PostHsnDetail/$', post_hsn, name='post_hsn'),
    url(r'^api/GetHsnList/$', get_hsn_list, name='get_hsn_list'),
    url(r'^api/GetHSNDetail/(?P<id>[0-9]+)/$', get_hsn_detail, name='get_hsn_detail'),
    url(r'^api/EditHSNDetail/$', edit_hsn, name='edit_hsn'),
    url(r'^api/DeleteHSNDetail/$', delete_hsn, name='delete_hsn'),

    # Category
    url(r'^CategoryListJson/$', CategoryListJson.as_view(), name='CategoryListJson'),

    url(r'^api/PostCategoryDetail/$', post_category, name='post_category'),
    url(r'^api/GetCategoryList/$', get_category_list, name='get_category_list'),
    url(r'^api/get_category_by_name/$', get_category_by_name, name='get_category_by_name'),
    url(r'^api/GetCategoryDetail/(?P<id>[0-9]+)/$', get_category_detail, name='get_category_detail'),
    url(r'^api/EditCategoryDetail/$', edit_category, name='edit_category'),
    url(r'^api/DeleteCategoryDetail/$', delete_category, name='delete_category'),

    # product
    url(r'^ProductListJson/$', ProductListJson.as_view(), name='ProductListJson'),

    url(r'^api/PostProductDetail/$', post_product, name='post_product'),
    url(r'^api/EditProductDetail/$', edit_product, name='edit_product'),
    url(r'^api/GetProductList/$', get_product_list, name='get_product_list'),
    url(r'^api/GetProductDetailByName/$', get_product_detail_by_name, name='get_product_detail_by_name'),
    url(r'^api/get_product_detail_by_barcode/$', get_product_detail_by_barcode, name='get_product_detail_by_barcode'),
    url(r'^api/GetProductDetail/(?P<id>[0-9]+)/$', get_product_detail, name='get_product_detail'),
    url(r'^api/DeleteProductDetail/$', delete_product, name='delete_product'),
    url(r'^api/get_running_down_out_of_stock_product_list/$', get_running_down_out_of_stock_product_list,
        name='get_running_down_out_of_stock_product_list'),
    url(r'^api/get_last_selling_price_of_the_product_by_customer/$', get_last_selling_price_of_the_product_by_customer,
        name='get_last_selling_price_of_the_product_by_customer'),

    # Company
    url(r'^CompanyListJson/$', CompanyListJson.as_view(), name='CompanyListJson'),
    url(r'^api/PostCompanyDetail/$', post_company, name='post_company'),
    url(r'^api/delete_company/$', delete_company, name='delete_company'),
    url(r'^api/EditCompanyDetail/$', Edit_company, name='Edit_company'),
    url(r'^api/GetCompanyList/$', get_company_list, name='get_company_list'),
    url(r'^api/get_bank_detail/(?P<id>[0-9]+)/$', get_bank_detail, name='get_bank_detail'),
    url(r'^api/get_Company_detail/(?P<id>[0-9]+)/$', get_Company_detail, name='get_Company_detail'),

    # User
    url(r'^UserListJson/$', UserListJson.as_view(), name='UserListJson'),

    url(r'^api/PostUserDetail/$', post_User, name='post_User'),
    url(r'^api/delete_user/$', delete_user, name='delete_user'),
    url(r'^api/get_User_detail/(?P<id>[0-9]+)/$', get_User_detail, name='get_User_detail'),
    url(r'^api/EditUserDetail/$', Edit_user, name='Edit_user'),

    # warehouse
    url(r'^WareHouseListJson/$', WareHouseListJson.as_view(), name='WareHouseListJson'),
    url(r'^api/add_warehouse/$', add_warehouse, name='add_warehouse'),
    url(r'^api/GetWareHouseList/$', GetWareHouseList, name='GetWareHouseList'),
    url(r'^api/GetWareHouseDetail/(?P<id>[0-9]+)/$', get_warehouse_detail, name='get_warehouse_detail'),
    url(r'^api/EditWareHouseDetail/$', edit_warehouse, name='edit_warehouse'),
    url(r'^api/delete_wareHouse/$', delete_wareHouse, name='delete_wareHouse'),

    # unit
    url(r'^UnitsListJson/$', UnitsListJson.as_view(), name='UnitsListJson'),
    url(r'^api/add_unit/$', add_unit, name='add_unit'),

    url(r'^api/get_unit_list/$', get_unit_list, name='get_unit_list'),
    url(r'^api/GetUnitDetail/(?P<id>[0-9]+)/$', get_unit_detail, name='get_unit_detail'),
    url(r'^api/EditUnitDetail/$', edit_unit, name='edit_unit'),

    url(r'^api/delete_unit/$', delete_unit, name='delete_unit'),

    # Sales
    url(r'^SalesListByProductJson/$', SalesListByProductJson.as_view(), name='SalesListByProductJson'),
    url(r'^SalesListJson/$', SalesListJson.as_view(), name='SalesListJson'),
    url(r'^ReturnListJson/$', ReturnListJson.as_view(), name='ReturnListJson'),
    url(r'^SalesListByCustomerJson/$', SalesListByCustomerJson.as_view(), name='SalesListByCustomerJson'),
    url(r'^api/AddNewSalesDetail/$', add_sales, name='add_sales'),
    url(r'^api/add_return_sales/$', add_return_sales, name='add_return_sales'),
    url(r'^api/get_sales_detail/(?P<id>[0-9]+)/$', get_sales_detail, name='get_sales_detail'),
    url(r'^api/get_return_detail/(?P<id>[0-9]+)/$', get_return_detail, name='get_return_detail'),
    url(r'^api/get_sales_detail_by_invoice_number/$', get_sales_detail_by_invoice_number, name='get_sales_detail_by_invoice_number'),
    url(r'^api/get_sales_detail_for_invoice/(?P<id>[0-9]+)/$', get_sales_detail_for_invoice,
        name='get_sales_detail_for_invoice'),
    url(r'^api/delete_sales/$', delete_sales, name='delete_sales'),
    url(r'^api/delete_return/$', delete_return, name='delete_return'),
    url(r'^api/take_sale_payment/$', take_sale_payment, name='take_sale_payment'),

    # Purchase
    url(r'^PurchaseListJson/$', PurchaseListJson.as_view(), name='PurchaseListJson'),
    url(r'^PurchaseListBySupplierJson/$', PurchaseListBySupplierJson.as_view(), name='PurchaseListBySupplierJson'),

    url(r'^api/AddNewPurchaseDetail/$', add_purchase, name='add_purchase'),
    url(r'^api/get_purchase_detail/(?P<id>[0-9]+)/$', get_purchase_detail, name='get_purchase_detail'),
    url(r'^api/delete_purchase/$', delete_purchase, name='delete_purchase'),

    # expense
    url(r'^api/AddNewExpense/$', add_expense, name='add_expense'),
    url(r'^ExpenseListJson/$', ExpenseListJson.as_view(), name='ExpenseListJson'),
    url(r'^api/delete_expense/$', delete_expense, name='delete_expense'),

    # login
    url(r'^postLogin/$', postLogin, name='UserLogin'),

    # change password
    url(r'^change_password/$', change_password, name='change_password'),
    url(r'^get_user_printer/$', get_user_printer, name='get_user_printer'),
    url(r'^api/change_user_printer_setting/$', change_user_printer_setting, name='change_user_printer_setting'),

    # invoice
    url(r'^api/AddNewInvoice/$', add_invoice, name='add_invoice'),
    url(r'^InvoiceListJson/$', InvoiceListJson.as_view(), name='InvoiceListJson'),
    url(r'^api/get_invoice_series_by_company/$', get_invoice_series_by_company, name='get_invoice_series_by_company'),
    url(r'^api/get_new_sale_invoice_number/$', get_new_sale_invoice_number, name='get_new_sale_invoice_number'),

    # back up
    url(r'^api/download_backup/$', download_backup, name='download_backup'),
    url(r'^api/download_expense_report/$', download_expense_report, name='download_expense_report'),
    url(r'^api/download_purchase_report/$', download_purchase_report, name='download_purchase_report'),
    url(r'^api/download_sales_report/$', download_sales_report, name='download_sales_report'),
    url(r'^api/download_product_sales_report/$', download_product_sales_report, name='download_product_sales_report'),

    #booking
    url(r'^api/add_booking/$', add_booking, name='add_booking'),
    url(r'^api/update_booking/$', update_booking, name='update_booking'),
    url(r'^BookingListJson/$', BookingListJson.as_view(), name='BookingListJson'),
    url(r'^api/delete_booking/$', delete_booking, name='delete_booking'),
    url(r'^BookingSale/(?P<id>[0-9]+)/$', BookingSale, name='BookingSale'),
    url(r'^api/add_sales_from_booking/$', add_sales_from_booking, name='add_sales_from_booking'),

    # Referrer
    url(r'^ReferrerListJson/$', ReferrerListJson.as_view(), name='ReferrerListJson'),
    url(r'^TransactionListByReferrerJson/$', TransactionListByReferrerJson.as_view(), name='TransactionListByReferrerJson'),

    url(r'^api/PostReferrerDetail/$', post_referrer, name='post_referrer'),
    url(r'^api/get_referrer_list/$', get_referrer_list, name='get_referrer_list'),
    url(r'^api/GetReferrerDetail/(?P<id>[0-9]+)/$', get_referrer_detail, name='get_referrer_detail'),
    url(r'^api/get_referrer_detail_by_name/$', get_referrer_detail_by_name, name='get_referrer_detail_by_name'),

    url(r'^api/EditReferrerDetail/$', edit_referrer, name='edit_referrer'),
    url(r'^api/DeleteReferrerDetail/$', delete_referrer, name='delete_referrer'),
    url(r'^api/take_referrer_payment/$', take_referrer_payment, name='take_referrer_payment'),


    #daily report
    url(r'^daily_report/$', daily_report, name='daily_report'),

    #Product Batch Detail
    url(r'^ProductBatchListJson/$', ProductBatchListJson.as_view(), name='ProductBatchListJson'),
    url(r'^api/post_product_batch_detail/$', post_product_batch_detail, name='post_product_batch_detail'),
    url(r'^api/get_product_batch_detail/(?P<id>[0-9]+)/$', get_product_batch_detail, name='get_product_batch_detail'),
    url(r'^api/edit_product_batch_detail/$', edit_product_batch_detail, name='edit_product_batch_detail'),
    url(r'^api/delete_product_batch/$', delete_product_batch, name='delete_product_batch'),

]
