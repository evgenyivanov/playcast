from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'playcast.views.home'),

     url(r'^designer/(\d+)/', 'playcast.views.designer'),
     url(r'^designer/', 'playcast.views.designer'),
     url(r'^designer_body/', 'playcast.views.designer_body'),
     url(r'^designer_menu/', 'playcast.views.designer_menu'),
     url(r'^upload_image/', 'playcast.views.upload_image'),
     url(r'^images_list/(\d+)/', 'playcast.views.images_list'),
     url(r'^images_list/', 'playcast.views.images_list'),
     url(r'^select_image/', 'playcast.views.select_image'),
     url(r'^upload_music/', 'playcast.views.upload_music'),
     url(r'^music_list/', 'playcast.views.music_list'),
     url(r'^select_music/', 'playcast.views.select_music'),
     url(r'^save/', 'playcast.views.save'),
     url(r'^put/', 'playcast.views.put'),
     url(r'^playcast/(\d+)/', 'playcast.views.playcast'),
     url(r'^playcast_list/(\d+)/', 'playcast.views.playcast_list'),
     url(r'^playcast_list/', 'playcast.views.playcast_list'),
     url(r'^mylogin/', 'playcast.views.mylogin'),
     (r'^logout/$', 'django.contrib.auth.views.logout'),
     url(r'^deleteplaycast/(\d+)/', 'playcast.views.deleteplaycast'),
     url(r'^editeprofile/', 'playcast.views.editeprofile'),
     url(r'^author/(\d+)/', 'playcast.views.author'),
     url(r'^readers/(\d+)/', 'playcast.views.readers'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
