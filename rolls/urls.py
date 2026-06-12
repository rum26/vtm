from django.urls import path
from .views import (roll_list,
                    roll_detail,
                    add_history)

urlpatterns = [
    path("", roll_list,
         name="roll_list"),
    path("<int:roll_id>/", roll_detail,
        name="roll_detail"),
    path(
        "<int:roll_id>/add/", add_history,
        name="add_history")
]
