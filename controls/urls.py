from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    path('controls_homepage/', views.ahomepage, name="ahomepage"),
    path('add_product/', views.adproduct_view, name='aproduct'),
    path('admin_control/', views.acontrol_view, name='acontrol'),
    path('customers/', views.customers_view, name='customers'),
    path('admin_products/', views.aproducts_view, name='products'),
    path('messages/', views.messages_view, name='messages'),
    path('customer_form/', views.cform_view, name='cform'),
    path('admin_form/', views.aform_view, name='aform'),
    path('newsletter/', views.news_view, name='news'),
    path('orders/', views.order_view, name='order'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('customer/add/', views.add_customer, name='add_customer'),
    path('customer/update/<int:user_id>/', views.update_customer, name='update_customer'),
    path('customer/delete/<int:user_id>/', views.delete_customer, name='delete_customer'),
    path('admin/add/', views.add_admin, name='add_admin'),
    path('admin/update/<int:user_id>/', views.update_admin, name='update_admin'),
    path('admin/delete/<int:user_id>/', views.delete_admin, name='delete_admin'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('update-blog/<int:blog_id>/', views.update_blog, name='update_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('add_news/', views.newsletter, name='add_newsletter'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]