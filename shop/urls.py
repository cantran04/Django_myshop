from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from . forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('', views.index, name='') ,
    path('about/', views.about, name='about') ,
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name='category') ,
    path('category-title/<val>', views.CategoryView.as_view(), name='category-title') ,
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail') ,
    path('profile/', views.ProfileView.as_view(), name='profile') ,
    path('address/', views.address, name='address') ,
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress') ,
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),

    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    # login authentication
    path('registration/',views.CustomerRegistetrationView.as_view(), name='customerregistration'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name = 'pages/login.html', authentication_form=LoginForm), name='login'),
    # path('accounts/login/',auth_views.LoginView.as_view(template_name="pages/login.html"), name="login"),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='pages/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='pages/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    

    path('pasword-reset/',auth_views.PasswordResetView.as_view(template_name = 'pages/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('pasword-reset/done',auth_views.PasswordResetDoneView.as_view(template_name = 'pages/password_reset_done.html'), name='password_reset_done'),
    path('pasword-reset-comfirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'pages/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('pasword-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'pages/password_reset_complete.html'), name='password_reset_complete'),

] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)