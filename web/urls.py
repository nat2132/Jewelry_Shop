from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.homepage_view, name="homepage"),
    path('homepage/', views.homepage_view, name="homepage"),
    path('shop/', views.shop_view, name='shop'),
    path('blog/', views.blog_view, name='blog'),
    path('sproduct/<int:product_id>/', views.sproduct_view, name='sproduct'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('about/', views.about_view, name='about'),
    path('save-message/', views.save_message, name='save_message'),
    path('process_order/',views.process_order, name='process_order' )
]
