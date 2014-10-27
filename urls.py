from django.conf.urls import patterns, url
from hs_hydroprogram import views



urlpatterns = patterns('',
           url(r'^_internal/create-model-instance/$',views.create_model_instance),
           #url(r'^_internal/parse-metadata/$', views.parse_metadata),
           #url(r'^_internal/get-eula/$', views.get_eula),
           url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)