from django.urls import path
from . import views
from .dash_apps.finished_apps import covid, ecom_test

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    path('auth_user/', views.auth_user, name="authuser"),
    path('logout/', views.logout, name='logout'),
    path('table/', views.table, name='table'),
    path('table/upload/', views.table_upload, name='table_upload'),
    path('table/show/', views.show_table, name="show_table"),

    path('plotly/', views.plotly, name="plotly"),
    path('show/plotly/', views.plotly_chart, name="plotly chart"),
    path('show/plotly2/', views.plotly_chart, name="plotly chart"),

    path('email/verification/<str:time_stamp>', views.confirmation, name='reset'),
    # path('email/verification/<str:time_stamp>', views.confirmation, name='reset'),

    path('email/', views.reset, name='reset'),
    path('email/post/', views.resetpassword, name="emailpost"),
    path('reset/password/form/', views.resetpasswrodform, name="resetform"),
    path('reset/password/<int:user_id>', views.password, name="password"),

    # profile page url
    path('profile/logout', views.logout, name='logout'),
    path('profile/change-password-page', views.send_change_password_page, name='change-password'),
    path('profile/change-password', views.change_password_after_login),
    path('profile/file-delete/<str:azure_file_name>', views.file_delete, name="file-delete"),
    path('profile/view-profile-picture', views.get_profile_picture, name="profile-picture"),
    path('profile/view-file/<str:azure_file_name>', views.view_user_file, name="file-view"),
    path('profile/download-file/<str:azure_file_name>', views.download_file, name="file-download"),
    # path('profile/view-profile-picture/<int"user_id>', views.get_profile_picture, name="profile-picture"),

    # change profile picture
    path('profile/upload-new-profile-picture/<int:user_id>', views.upload_new_profile_picture, name="profile-picture"),

    path('covid/', views.covid, name='custome'),
    path('vis/', views.vis, name='visualization')
]
