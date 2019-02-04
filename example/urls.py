from django.urls import re_path

from .apis import TripView

app_name = 'example_taxi'

urlpatterns = [
    re_path(r'^$', TripView.as_view({'get': 'list'}), name='trip_list'),
    re_path(r'^(?P<trip_nk>\w{32})/$', TripView.as_view(
        {'get': 'retrieve'}), name='trip_detail'),
]
