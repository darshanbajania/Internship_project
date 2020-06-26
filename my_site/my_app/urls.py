from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as auth_views

app_name="my_app"

urlpatterns = [
    path('', views.Profile_View, name='profile'),
    path('resume/', views.Upload_Resume_View, name='resume'),
    path('proposals/', views.Proposals_View, name='proposals'),
    path('update_profile/', views.Update_Profile_View, name='update_profile'),
    path('login/',views.Login_View, name = 'login_view'),
    path('register/', views.register_view, name='register_url'),
    path('password_reset/', views.password_Reset_View, name='password_reset'),
    path('logout/', LogoutView.as_view(next_page='my_app:login_view'),name="logout_url"),
    path('Proposal_admin/', views.Total_Proposal_View,name="proposal_admin"),
    path('admin_page/', views.Admin_view,name="admin_page"),
    path('admin_profile/', views.Admin_profile_view,name="admin_profile"),
    path('proposal/', views.Full_Proposal_view,name="full_proposal"),
    path('update_skills/', views.Update_Skill_view,name="update_skills"),
    # path('extracted_skills/', views.Extracted_Skills_view,name="extracted_skills"),
    path('proposals_admin/', views.Full_Proposal_Admin_view,name="full_proposal_admin"),
    path('admin_update_profile/', views.Admin_Update_Profile_view,name="admin_update_profile"),
    path(
        'password_change/done',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change_do.html'),
    name='password_change_done'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change_for.html',
        success_url='done'),
    name='password_change'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)