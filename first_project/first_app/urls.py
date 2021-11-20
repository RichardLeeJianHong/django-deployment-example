from django.urls import path
from first_app import views

# TEMPLATE TAGGING
app_name = 'first_app'

urlpatterns = [
    path('',views.index, name='index'),
    path('relative/',views.relative,name='relative'),
    path('other/',views.other,name='other')
]

