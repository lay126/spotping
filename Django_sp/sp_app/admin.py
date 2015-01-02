# _*_ encoding: utf-8 _*_

from django.contrib import admin
from django import forms

from django.contrib.auth.models import User, UserManager
from django.contrib.auth.admin import UserAdmin

from sp_app.models import *


class USERInline(admin.StackedInline):
	model = USER
	can_delete = False
	verbose_name_plural = 'USER'

class UserAdmin(admin.ModelAdmin):
	inlines = (USERInline, )
	list_display = ('id', 'username', 'password', 'email',)

class USER_SELLERAdmin(admin.ModelAdmin):
	list_display = ('user_seller_id', 'user_seller_register_id', 'user_seller_photo_index', 'user_seller_market_name', 'user_seller_address', 'user_seller_phone',)

class USER_BUYERAdmin(admin.ModelAdmin):
	list_display = ('user_buyer_id', 'user_buyer_register_id' ,'user_buyer_photo_index', 'user_buyer_address', 'user_buyer_phone',)

class PRODUCTAdmin(admin.ModelAdmin):
	list_display = ('product_index','product_photo_index', 'product_market_name', 'product_name', 'product_brand', 'product_unit' ,'product_category_seller', 'product_category_buyer', 'product_price', 'product_coupon_times',)


#-product_list--------------------------------------------
class COUPON_DAILYAdmin(admin.ModelAdmin):
	list_display = ('coupon_daily_index', 'coupon_daily_product_index', 'coupon_daily_photo_index','coupon_daily_market_name','coupon_daily_name', 'coupon_daily_brand', 'coupon_daily_unit', 'coupon_daily_price','coupon_daily_start','coupon_daily_finish','coupon_daily_times','coupon_daily_type', 'coupon_daily_detail', 'coupon_daily_active', 'coupon_daily_making')

class COUPON_GREENSAdmin(admin.ModelAdmin):
	list_display = ('coupon_greens_index', 'coupon_greens_product_index', 'coupon_greens_photo_index','coupon_greens_market_name', 'coupon_greens_name', 'coupon_greens_brand', 'coupon_greens_unit', 'coupon_greens_area', 'coupon_greens_price','coupon_greens_start','coupon_greens_finish','coupon_greens_times','coupon_greens_type', 'coupon_greens_detail', 'coupon_greens_active', 'coupon_greens_making')

class COUPON_FISHAdmin(admin.ModelAdmin):
	list_display = ('coupon_fish_index', 'coupon_fish_product_index', 'coupon_fish_photo_index','coupon_fish_market_name', 'coupon_fish_name', 'coupon_fish_brand', 'coupon_fish_unit', 'coupon_fish_area', 'coupon_fish_price','coupon_fish_start','coupon_fish_finish','coupon_fish_times', 'coupon_fish_detail', 'coupon_fish_type', 'coupon_fish_active', 'coupon_fish_making')
	  
class COUPON_RICEAdmin(admin.ModelAdmin):
	list_display = ('coupon_rice_index', 'coupon_rice_product_index', 'coupon_rice_photo_index','coupon_rice_market_name','coupon_rice_name', 'coupon_rice_brand', 'coupon_rice_unit', 'coupon_rice_area', 'coupon_rice_price','coupon_rice_start','coupon_rice_finish','coupon_rice_times','coupon_rice_type', 'coupon_rice_detail', 'coupon_rice_active', 'coupon_rice_making')

class COUPON_MEATAdmin(admin.ModelAdmin):
	list_display = ('coupon_meat_index', 'coupon_meat_product_index', 'coupon_meat_photo_index', 'coupon_meat_market_name','coupon_meat_name', 'coupon_meat_brand', 'coupon_meat_unit', 'coupon_meat_area', 'coupon_meat_price','coupon_meat_start','coupon_meat_finish', 'coupon_meat_detail', 'coupon_meat_times','coupon_meat_type', 'coupon_meat_active', 'coupon_meat_making')

class COUPON_EGGAdmin(admin.ModelAdmin):
	list_display = ('coupon_egg_index', 'coupon_egg_product_index', 'coupon_egg_photo_index', 'coupon_egg_market_name','coupon_egg_name', 'coupon_egg_brand', 'coupon_egg_unit', 'coupon_egg_area', 'coupon_egg_price','coupon_egg_start','coupon_egg_finish','coupon_egg_times','coupon_egg_type', 'coupon_egg_detail', 'coupon_egg_active', 'coupon_egg_making')

class COUPON_HAMAdmin(admin.ModelAdmin):
	list_display = ('coupon_ham_index', 'coupon_ham_product_index', 'coupon_ham_photo_index', 'coupon_ham_market_name','coupon_ham_name', 'coupon_ham_brand', 'coupon_ham_unit', 'coupon_ham_price', 	'coupon_ham_start','coupon_ham_finish','coupon_ham_times','coupon_ham_type', 'coupon_ham_detail', 'coupon_ham_active', 'coupon_ham_making')

class COUPON_SIDEAdmin(admin.ModelAdmin):
	list_display = ('coupon_side_index', 'coupon_side_product_index', 'coupon_side_photo_index', 'coupon_side_market_name','coupon_side_name', 'coupon_side_brand', 'coupon_side_unit', 'coupon_side_price', 'coupon_side_start','coupon_side_finish','coupon_side_times', 'coupon_side_detail', 'coupon_side_type', 'coupon_side_active', 'coupon_side_making')

class COUPON_WATERAdmin(admin.ModelAdmin):
	list_display = ('coupon_water_index', 'coupon_water_product_index', 'coupon_water_photo_index', 'coupon_water_market_name','coupon_water_name', 'coupon_water_brand', 'coupon_water_unit', 'coupon_water_price', 'coupon_water_start','coupon_water_finish','coupon_water_times','coupon_water_type', 'coupon_water_detail', 'coupon_water_active', 'coupon_water_making')

class COUPON_INSTANTAdmin(admin.ModelAdmin):
	list_display = ('coupon_instant_index', 'coupon_instant_product_index', 'coupon_instant_photo_index','coupon_instant_market_name' ,'coupon_instant_name', 'coupon_instant_brand', 'coupon_instant_unit', 'coupon_instant_price', 'coupon_instant_start','coupon_instant_finish','coupon_instant_times','coupon_instant_type', 'coupon_instant_detail', 'coupon_instant_active', 'coupon_instant_making')

class COUPON_ICEAdmin(admin.ModelAdmin):
	list_display = ('coupon_ice_index', 'coupon_ice_product_index', 'coupon_ice_photo_index', 'coupon_ice_market_name','coupon_ice_name', 'coupon_ice_brand', 'coupon_ice_unit', 'coupon_ice_price', 'coupon_ice_start','coupon_ice_finish','coupon_ice_times','coupon_ice_type', 'coupon_ice_detail', 'coupon_ice_active', 'coupon_ice_making')

class COUPON_BAKERYAdmin(admin.ModelAdmin):
	list_display = ('coupon_bakery_index', 'coupon_bakery_product_index', 'coupon_bakery_photo_index', 'coupon_bakery_market_name','coupon_bakery_name', 'coupon_bakery_brand', 'coupon_bakery_unit', 'coupon_bakery_price', 'coupon_bakery_start','coupon_bakery_finish','coupon_bakery_times','coupon_bakery_type', 'coupon_bakery_detail', 'coupon_bakery_active', 'coupon_bakery_making')

class COUPON_SNACKAdmin(admin.ModelAdmin):
	list_display = ('coupon_snack_index', 'coupon_snack_product_index', 'coupon_snack_photo_index', 'coupon_snack_market_name','coupon_snack_name', 'coupon_snack_brand', 'coupon_snack_unit', 'coupon_snack_price', 'coupon_snack_start','coupon_snack_finish','coupon_snack_times', 'coupon_snack_detail', 'coupon_snack_type', 'coupon_snack_active', 'coupon_snack_making')


#-user_buyer-------------------------------------------
class USER_FAVORITE_LISTAdmin(admin.ModelAdmin):
	list_display = ('user_favorite_list_index', 'user_favorite_list_userid', 'user_favorite_list_product_index', 'user_favorite_list_product_name', 'user_favorite_list_product_brand', 'user_favorite_list_product_unit','user_favorite_list_product_category',)

class USER_COUPON_USEDLISTAdmin(admin.ModelAdmin):
	list_display = ('user_coupon_usedlist_index', 'user_coupon_usedlist_userid', 'user_coupon_usedlist_product_name', 'user_coupon_usedlist_product_brand', 'user_coupon_usedlist_product_unit','user_coupon_usedlist_product_category','user_coupon_usedlist_type',)
		

#-picture-------------------------------------------
class SP_PICTUREAdmin(admin.ModelAdmin):
	list_display = ('sp_photo_index', 'sp_name', 'sp_picture')

class USER_PICTUREAdmin(admin.ModelAdmin):
	list_display = ('user_photo_index', 'user_name', 'user_picture')




# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Un-register all
# admin.site.unregister(USER_SELLER)
# admin.site.unregister(USER_BUYER)
# admin.site.unregister(PRODUCT)
# admin.site.unregister(COUPON_DAILY)
# admin.site.unregister(COUPON_GREENS)
# admin.site.unregister(COUPON_FISH)
# admin.site.unregister(COUPON_RICE)
# admin.site.unregister(COUPON_MEAT)
# admin.site.unregister(COUPON_EGG)
# admin.site.unregister(COUPON_HAM)
# admin.site.unregister(COUPON_SIDE)
# admin.site.unregister(COUPON_WATER)
# admin.site.unregister(COUPON_INSTANT)
# admin.site.unregister(COUPON_ICE)
# admin.site.unregister(COUPON_BAKERY)
# admin.site.unregister(COUPON_SNACK)
# admin.site.unregister(USER_FAVORITE_LIST)
# admin.site.unregister(USER_COUPON_USEDLIST)
# admin.site.unregister(SP_PICTURE)
# admin.site.unregister(USER_PICTURE)

# Register your models here.
admin.site.register(USER_SELLER, USER_SELLERAdmin)
admin.site.register(USER_BUYER, USER_BUYERAdmin)
admin.site.register(PRODUCT, PRODUCTAdmin)
admin.site.register(COUPON_DAILY, COUPON_DAILYAdmin)
admin.site.register(COUPON_GREENS, COUPON_GREENSAdmin)
admin.site.register(COUPON_FISH, COUPON_FISHAdmin)
admin.site.register(COUPON_RICE, COUPON_RICEAdmin)
admin.site.register(COUPON_MEAT, COUPON_MEATAdmin)
admin.site.register(COUPON_EGG, COUPON_EGGAdmin)
admin.site.register(COUPON_HAM, COUPON_HAMAdmin)
admin.site.register(COUPON_SIDE, COUPON_SIDEAdmin)
admin.site.register(COUPON_WATER, COUPON_WATERAdmin)
admin.site.register(COUPON_INSTANT, COUPON_INSTANTAdmin)
admin.site.register(COUPON_ICE, COUPON_ICEAdmin)
admin.site.register(COUPON_BAKERY, COUPON_BAKERYAdmin)
admin.site.register(COUPON_SNACK, COUPON_SNACKAdmin)

admin.site.register(USER_FAVORITE_LIST, USER_FAVORITE_LISTAdmin)
admin.site.register(USER_COUPON_USEDLIST, USER_COUPON_USEDLISTAdmin)

admin.site.register(SP_PICTURE, SP_PICTUREAdmin)
admin.site.register(USER_PICTURE, USER_PICTUREAdmin)





