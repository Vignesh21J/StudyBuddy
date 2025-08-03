from django.urls import path
from . import views

urlpatterns = [

    path('',views.home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),

    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<uuid:reset_id>/', views.ResetPassword, name='reset-password'),


    path('room/<int:pk>',views.room, name='room'),

    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),


    path('profile/<int:pk>/', views.user_profile, name="user-profile"),



    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<int:pk>', views.update_room , name="update-room"),
    path('delete-room/<int:pk>', views.delete_room , name="delete-room"),
    

    path('update-user/', views.update_user, name="update-user"),

    path('topics/', views.topics_page, name="topics"),
]
