from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('', views.index, name="index"),
    path("lessons/user=<int:user_id>", views.full_lessons_list, name="List of all this user's lessons"),
    path("lessons/user=<int:user_id>/product=<int:product_id>", views.lessons_list, name="List of this user's lessons contained in this product"),
    path("statistics", views.statistics, name="Statistics")
]