#from librarymanagement.library.views import SearchPage

from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from library import views

urlpatterns = [
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('tenantclick', views.tenantclick_view),


    path('adminsignup', views.adminsignup_view),
    path('tenantsignup', views.tenantsignup_view),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html')),
    path('tenantlogin', LoginView.as_view(template_name='library/tenantlogin.html')),

    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin', views.afterlogin_view),
    
    path('myBooking',views.myBooking),
    path("bookProp",views.bookProp),
   # path("confirmation", views.confirmation, name="confirmation"),
    path('search',views.SearchPage),
    path('addProperty', views.addProperty_view),
    path('viewProperty', views.viewProperty_view),
    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.viewissuedbook_view),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),

    path('aboutus', views.aboutus_view),
    # path('contactus', views.contactus_view),
]