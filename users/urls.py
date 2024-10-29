from django.urls import path
from .views import login_view, logout_view, register_view, profile_view, member_list, add_member, download_csv_template, export_members_csv, edit_profile, get_user_activity

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('members/', member_list, name='member_list'),  
    path('add_member/', add_member, name='add_member'),
    path('download_csv_template/', download_csv_template, name='download_csv_template'),
    path('export_members_csv/', export_members_csv, name='export_members_csv'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('user_activity/', get_user_activity, name='get_user_activity'),
]