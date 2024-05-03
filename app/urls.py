from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", UserInfoAPIView.as_view(), name="user-info"),
    path("tasks/", TaskAPIView.as_view(), name="user-tasks"),
    path('<int:pk>/tasks_detail/', TaskDetailAPIView.as_view(), name='task_detail_api'),
    path('<int:pk>/tasks_detail_modif/', TaskDetailModifiactionAPIView.as_view(), name='task_detail_api_modif'),
    ]