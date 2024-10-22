from django.urls import path

from .views import SignInView, CurrentUserView


urlpatterns = [
    path('users/sign_in/', SignInView.as_view()),
    path('users/current_user/', CurrentUserView.as_view()),
]
