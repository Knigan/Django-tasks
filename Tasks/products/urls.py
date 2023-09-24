from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('', views.statistics, name="Statistics"),
    path("<int:user_id>/lessons/", views.full_lessons_list, name="List of all this user's lessons"),
    path("<int:user_id>/<int:product_id>/lessons/", views.lessons_list, name="List of this user's lessons contained in this product"),
]