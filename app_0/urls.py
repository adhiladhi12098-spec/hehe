from django.urls import path

from.import views
urlpatterns=[
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('io/',views.index,name='io'),
    path('register/',views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('my-products/', views.my_products, name='my_products'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('update_cart/<int:id>/', views.update_cart, name='update_cart'),



]
