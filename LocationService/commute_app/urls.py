from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # need the '/' before $ to properly route call to generics.ListCreateAPIView
    url(r'^commute', views.CommuteInfoList.as_view()),

    # supports /jobPost/{jobPostId}
    url(r'^commute/(?P<commuteInfoId>.+)$', views.CommuteInfoDetail.as_view()),
    url(r'^commute/bulkSave$', views.CommuteInfoBulkSave.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)