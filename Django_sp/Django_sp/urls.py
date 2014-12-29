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


	# test 
	#-------------------------------------------------------------------------------------------------------------------------
	url(r'^test/photo/upload/', 'sp_app.views.test_photo_upload'),
	url(r'^test/photo/download/1/', 'sp_app.views.test_photo_download_1'),
	url(r'^test/photo/download/s/', 'sp_app.views.test_photo_download_s'),
	url(r'^test/photo/download/2/', 'sp_app.views.test_photo_download_2'),
	url(r'^test/photo/open/t/', 'sp_app.views.test_photo_open_t'),
	url(r'^test/photo/open/c/', 'sp_app.views.test_photo_open_c'),


	# product & coupon
	#-------------------------------------------------------------------------------------------------------------------------
	url(r'^request/coupon/all/', 'sp_app.views.request_coupon_all'),
	url(r'^response/coupon/all/', 'sp_app.views.request_coupon_all'),

	url(r'^request/coupon/daily/', 'sp_app.views.request_coupon_daily'),
	url(r'^request/coupon/greens/', 'sp_app.views.request_coupon_greens'),
	url(r'^request/coupon/fish/', 'sp_app.views.request_coupon_fish'),
	url(r'^request/coupon/rice/', 'sp_app.views.request_coupon_rice'),
	url(r'^request/coupon/meat/', 'sp_app.views.request_coupon_meat'),
	url(r'^request/coupon/egg/', 'sp_app.views.request_coupon_egg'),
	url(r'^request/coupon/ham/', 'sp_app.views.request_coupon_ham'),
	url(r'^request/coupon/side/', 'sp_app.views.request_coupon_side'),
	url(r'^request/coupon/water/', 'sp_app.views.request_coupon_water'),
	url(r'^request/coupon/instant/', 'sp_app.views.request_coupon_instant'),
	url(r'^request/coupon/ice/', 'sp_app.views.request_coupon_ice'),
	url(r'^request/coupon/bakery/', 'sp_app.views.request_coupon_bakery'),
	url(r'^request/coupon/snack/', 'sp_app.views.request_coupon_snack'),

    url(r'^request/make/daily/', 'sp_app.views.request_make_daily'),
    url(r'^request/make/greens/', 'sp_app.views.request_make_greens'),
    url(r'^request/make/fish/', 'sp_app.views.request_make_fish'),
    url(r'^request/make/rice/', 'sp_app.views.request_make_rice'),
    url(r'^request/make/meat/', 'sp_app.views.request_make_meat'),
    url(r'^request/make/egg/', 'sp_app.views.request_make_egg'),
    url(r'^request/make/ham/', 'sp_app.views.request_make_ham'),
    url(r'^request/make/side/', 'sp_app.views.request_make_side'),
    url(r'^request/make/water/', 'sp_app.views.request_make_water'),
    url(r'^request/make/instant/', 'sp_app.views.request_make_instant'),
    url(r'^request/make/ice/', 'sp_app.views.request_make_ice'),
    url(r'^request/make/bakery/', 'sp_app.views.request_make_bakery'),
    url(r'^request/make/snack/', 'sp_app.views.request_make_snack'),

	url(r'^request/inactive/coupon/', 'sp_app.views.request_inactive_coupon'),
	url(r'^response/inactive/coupon/', 'sp_app.views.response_inactive_coupon'),
	url(r'^request/active/coupon/', 'sp_app.views.request_active_coupon'),
	url(r'^response/active/coupon/', 'sp_app.views.response_active_coupon'),
	url(r'^request/reservation/coupon/', 'sp_app.views.request_reservation_coupon'),
	url(r'^response/reservation/coupon/', 'sp_app.views.response_reservation_coupon'),
	url(r'^request/used/coupon/', 'sp_app.views.request_used_coupon'),
	url(r'^response/used/coupon/', 'sp_app.views.response_used_coupon'),


	# seller
	#-------------------------------------------------------------------------------------------------------------------------
	url(r'^join/page/s/', 'sp_app.views.join_page_s'),
	url(r'^login/page/s/', 'sp_app.views.login_page_s'),

	url(r'^request/join/seller/', 'sp_app.views.request_join_seller'),
	url(r'^response/join/seller/', 'sp_app.views.response_join_seller'),
	url(r'^request/login/seller/', 'sp_app.views.request_login_seller'),
	url(r'^response/login/seller/', 'sp_app.views.response_login_seller'),
	

	# buyer 
	#-------------------------------------------------------------------------------------------------------------------------
	url(r'^join/page/b/', 'sp_app.views.join_page_b'),
	url(r'^login/page/b/', 'sp_app.views.login_page_b'),
	url(r'^request/join/buyer/', 'sp_app.views.request_join_buyer'),
	url(r'^response/join/buyer/', 'sp_app.views.response_join_buyer'),
	url(r'^request/login/buyer/', 'sp_app.views.request_login_buyer'),
	url(r'^response/login/buyer/', 'sp_app.views.response_login_buyer'),

)
