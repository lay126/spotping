# _*_ coding: utf-8 _*_

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sp_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^/', 'sp_app.views.'),

    url(r'^admin/', include(admin.site.urls)),


    # 테스트 
    #----------------------------------------------------------------------------
    url(r'^test/json/2/', 'sp_app.views.test_json_2'),
    url(r'^test/photo/upload', 'sp_app.views.test_photo_upload'),
    url(r'^test/photo/download/1/', 'sp_app.views.test_photo_download_1'),
    url(r'^test/photo/download/s/', 'sp_app.views.test_photo_download_s'),
    url(r'^test/photo/download/2/', 'sp_app.views.test_photo_download_2'),
    url(r'^test/photo/open', 'sp_app.views.test_photo_open'),


    # seller
    #----------------------------------------------------------------------------
    url(r'^join/page/', 'sp_app.views.join_page'),
    url(r'^login/page/', 'sp_app.views.login_page'),
    url(r'^request/join/seller/', 'sp_app.views.request_join_seller'),
    url(r'^response/join/seller/', 'sp_app.views.response_join_seller'),
    url(r'^request/login/seller/', 'sp_app.views.request_login_seller'),
    url(r'^response/login/seller/', 'sp_app.views.response_login_seller'),

    url(r'^request/allData/seller/', 'sp_app.views.request_allData_seller'),
    url(r'^response/allData/seller/', 'sp_app.views.response_allData_seller'),

    url(r'^request/active/coupon/', 'sp_app.views.request_active_coupon'),
    url(r'^response/active/coupon/', 'sp_app.views.response_active_coupon'),
    url(r'^request/reservation/coupon/', 'sp_app.views.request_reservation_coupon'),
    url(r'^response/reservation/coupon/', 'sp_app.views.response_reservation_coupon'),
    url(r'^request/inactive/coupon/', 'sp_app.views.request_inactive_coupon'),
    url(r'^response/inactive/coupon/', 'sp_app.views.response_inactive_coupon'),

	url(r'^request/stat/coupon/', 'sp_app.views.request_stat_coupon'),
	url(r'^response/stat/coupon/', 'sp_app.views.response_stat_coupon'),    


	# buyer 
	#----------------------------------------------------------------------------
	url(r'^request/join/buyer/', 'sp_app.views.request_join_buyer'),
    url(r'^response/join/buyer/', 'sp_app.views.response_join_buyer'),
	url(r'^request/login/buyer/', 'sp_app.views.request_login_buyer'),
    url(r'^response/login/buyer/', 'sp_app.views.response_login_buyer'),

)
