from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name="my_app"

urlpatterns = [
    path('', views.Profile_View, name='profile'),
    path('resume/', views.Upload_Resume_View, name='resume'),
    path('proposals/', views.Proposals_View, name='proposals'),
    path('update_profile/', views.Update_Profile_View, name='update_profile'),
    path('loginv/',views.Login_View, name = 'login_view'),
    path('logoutv/',views.Logout_View, name = 'logout_view'),
    #path('login/', LoginView.as_view(), name='login_url'),
    path('register/', views.register_view, name='register_url'),
    #path('logout/', LogoutView.as_view(next_page='my_app:login_url'),name="logout_url"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)