from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from users import views

routers = DefaultRouter()
routers.register("users", views.UserView)

urlpatterns = [
    # JWT urls to obtain token for active user
    path('jwt/create/', jwt_views.TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', jwt_views.TokenVerifyView.as_view(), name='jwt_verify'),
    
    # URL to register, update, delete user
    path('', include(routers.urls))
]
