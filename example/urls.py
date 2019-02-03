from django.urls import re_path, path

from .apis import TripView

app_name = 'example_taxi'

urlpatterns = [
    re_path('', TripView.as_view({'get': 'list'}), name='trip_list'),
    # path('<str:trip_nk>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
    re_path(r'^(?P<trip_nk>\w{32})/$', TripView.as_view(
        {'get': 'retrieve'}), name='trip_detail'),
]
