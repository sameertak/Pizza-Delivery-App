from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', views.admin_login_view, name='adminloginpage'),
    path('adminauthenticate/', views.authenticate_admin),
    path('admin/adminhomepage/', views.admin_homepage_view, name='adminhomepage'),
    path('adminlogout/', views.log_out_admin),
    path('addpizza/', views.add_pizza),
    path('deletepizza/<int:pizzapk>/', views.delete_pizza),
    path('', views.homepage_view, name='homepage'),
    path('signupuser/', views.signup_user),
    path('loginuser/', views.user_login_view, name='userloginpage'),
    path('customer/welcome/',views.customer_welcome_view,name='customerpage'),
    path('customer/authenticate/', views.user_authenticate),
    path('userlogout/', views.user_logout),
    path('placeorder/', views.place_order),
    path('userorders/', views.user_orders),
    path('adminorders/', views.admin_orders, name='adminorder'),
    path('acceptorder/<int:orderpk>/', views.accept_order),
    path('declineorder/<int:orderpk>/', views.decline_order),
]

urlpatterns += staticfiles_urlpatterns()