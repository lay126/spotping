# _*_ coding: utf-8 _*_

from django import forms
from django.db import models
from django.conf import settings

from PIL import Image
from django.contrib.auth.models import User



'''
******************************
seller/buyer distint index is 
user_00000_photo_index

seller : 0
buyer  : 1
******************************

coupon active is,

0 	: inactive
1 	: active
2 	: reservation
******************************
'''


#----------------------------------------------------------------------------
class USER(models.Model):
	class Meta:
		verbose_name = u'USER'
		db_table = 'USER_DB'
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

class USER_SELLER(models.Model):
	class Meta:
		verbose_name = u'USER_SELLER'
		db_table = 'USER_SELLER_DB'
	user_seller_id = models.ForeignKey(User)
	user_seller_register_id = models.CharField(verbose_name=u'user_seller_register_id', null=False, max_length='200')
	user_seller_photo_index = models.IntegerField(verbose_name=u'user_seller_photo_index', null=False, default=0,)
	user_seller_market_name = models.CharField(verbose_name=u'user_seller_market_name',max_length='40', null=False,)
	user_seller_address = models.CharField(verbose_name=u'user_seller_address', max_length='200', null=False,)
	user_seller_latitude = models.FloatField(verbose_name=u'user_seller_latitude', null=False, default=0,)
	user_seller_longitude = models.FloatField(verbose_name=u'user_seller_longitude', null=False, default=0,)
	user_seller_phone = models.CharField(verbose_name=u'user_seller_phone', max_length='100', null=False,)

class USER_BUYER(models.Model):
	class Meta:
		verbose_name = u'USER_BUYER'
		db_table = 'USER_BUYER_DB'
	user_buyer_id = models.ForeignKey(User)
	user_buyer_register_id = models.CharField(verbose_name=u'user_buyer_register_id', null=False, max_length='200')
	user_buyer_photo_index = models.IntegerField(verbose_name=u'user_buyer_photo_index', null=False, default=0,)
	user_buyer_address = models.CharField(verbose_name=u'user_buyer_address', max_length='200', null=False,)
	user_buyer_phone = models.CharField(verbose_name=u'user_buyer_phone', max_length='100', null=False,)


#----------------------------------------------------------------------------
#모든 product
class PRODUCT(models.Model):
	class Meta:
		verbose_name = u'PRODUCT'
		db_table = 'PRODUCT_DB'
	product_index = models.AutoField(verbose_name=u'product_index', primary_key=True, unique=True, db_index=True,)
	product_photo_index = models.IntegerField(verbose_name=u'product_photo_index', null=False,)
	product_market_name = models.CharField(verbose_name=u'product_market_name', max_length='40',)
	product_name = models.CharField(verbose_name=u'product_name', max_length='40',)
	product_brand = models.CharField(verbose_name=u'product_brand', max_length='40',)
	product_unit = models.CharField(verbose_name=u'product_unit', max_length='20',)
	product_category_seller = models.IntegerField(verbose_name=u'product_category_seller', null=False, default=0)
	product_category_buyer = models.IntegerField(verbose_name=u'product_category_buyer', null=False, default=0)
	product_price = models.IntegerField(verbose_name=u'product_price', null=False, default=0,)
	# product_coupon_active = models.IntegerField(verbose_name=u'product_coupon_active', null=False, default=0,)
	product_coupon_times = models.IntegerField(verbose_name=u'product_coupon_times', null=False, default=0,)

# 유제품 
class COUPON_DAILY(models.Model):
	class Meta:
		verbose_name = u'COUPON_DAILY'
		db_table = 'COUPON_DAILY_DB'
	coupon_daily_index = models.AutoField(verbose_name=u'coupon_daily_index', primary_key=True, unique=True, db_index=True,)
	coupon_daily_product_index = models.IntegerField(verbose_name=u'coupon_daily_product_index', null=False,)
	coupon_daily_photo_index = models.IntegerField(verbose_name=u'coupon_daily_photo_index', null=False,)
	coupon_daily_market_name =  models.CharField(verbose_name=u'coupon_daily_market_name', max_length='20',)
	coupon_daily_name = models.CharField(verbose_name=u'coupon_daily_name', unique=True, max_length='40',)
	coupon_daily_brand = models.CharField(verbose_name=u'coupon_daily_brand', max_length='20',)
	coupon_daily_unit = models.CharField(verbose_name=u'coupon_daily_unit', max_length='20',)
	coupon_daily_price = models.IntegerField(verbose_name=u'coupon_daily_price', null=False, default=0,)
	coupon_daily_start = models.CharField(verbose_name=u'coupon_daily_start',  max_length='30',)
	coupon_daily_finish = models.CharField(verbose_name=u'coupon_daily_finish',  max_length='30',)
	coupon_daily_times = models.IntegerField(verbose_name=u'coupon_daily_times', default=0,)
	coupon_daily_detail = models.IntegerField(verbose_name=u'coupon_daily_detail', null=False, default=0,)
	coupon_daily_type = models.IntegerField(verbose_name=u'coupon_daily_type',null=False, default=0,)
	coupon_daily_active = models.IntegerField(verbose_name=u'coupon_daily_active', null=False, default=0,)
	coupon_daily_making = models.IntegerField(verbose_name=u'coupon_daily_making', null=False, default=0,)

# 야채 
class COUPON_GREENS(models.Model):
	class Meta:
		verbose_name = u'COUPON_GREENS'
		db_table = 'COUPON_GREENS_DB'
	coupon_greens_index = models.AutoField(verbose_name=u'coupon_greens_index', primary_key=True, unique=True, db_index=True,)
	coupon_greens_product_index = models.IntegerField(verbose_name=u'coupon_greens_product_index', null=False,)
	coupon_greens_photo_index = models.IntegerField(verbose_name=u'coupon_greens_photo_index', null=False,)
	coupon_greens_market_name =  models.CharField(verbose_name=u'coupon_greens_market_name', max_length='20',)
	coupon_greens_name = models.CharField(verbose_name=u'coupon_greens_name', max_length='40',)
	coupon_greens_brand = models.CharField(verbose_name=u'coupon_greens_brand', max_length='20',)
	coupon_greens_unit = models.CharField(verbose_name=u'coupon_greens_unit', max_length='20',)
	coupon_greens_area =  models.CharField(verbose_name=u'coupon_greens_area', max_length='20',)
	coupon_greens_price = models.IntegerField(verbose_name=u'coupon_greens_price', null=False, default=0,)
	coupon_greens_start = models.CharField(verbose_name=u'coupon_greens_start',  max_length='30',)
	coupon_greens_finish = models.CharField(verbose_name=u'coupon_greens_finish', max_length='30',)
	coupon_greens_times = models.IntegerField(verbose_name=u'coupon_greens_times', null=False, default=0,)
	coupon_greens_detail = models.IntegerField(verbose_name=u'coupon_greens_detail', null=False, default=0,)
	coupon_greens_type = models.IntegerField(verbose_name=u'coupon_greens_type',null=False, default=0,)
	coupon_greens_active = models.IntegerField(verbose_name=u'coupon_greens_active',null=False, default=0,)
	coupon_greens_making = models.IntegerField(verbose_name=u'coupon_greens_making', null=False, default=0,)
        
# 수산, 건어  
class COUPON_FISH(models.Model):
	class Meta:
		verbose_name = u'COUPON_FISH'
		db_table = 'COUPON_FISH_DB'
	coupon_fish_index = models.AutoField(verbose_name=u'coupon_fish_index', primary_key=True, unique=True, db_index=True,)
	coupon_fish_product_index = models.IntegerField(verbose_name=u'coupon_fish_product_index', null=False,)
	coupon_fish_photo_index = models.IntegerField(verbose_name=u'coupon_fish_photo_index', null=False,)
	coupon_fish_market_name =  models.CharField(verbose_name=u'coupon_fish_market_name', max_length='20',)
	coupon_fish_name = models.CharField(verbose_name=u'coupon_fish_name', max_length='40',)
	coupon_fish_brand = models.CharField(verbose_name=u'coupon_fish_brand', max_length='20',)
	coupon_fish_unit = models.CharField(verbose_name=u'coupon_fish_unit', max_length='20',)
	coupon_fish_area = models.CharField(verbose_name=u'coupon_fish_area', max_length='20',)
	coupon_fish_price = models.IntegerField(verbose_name=u'coupon_fish_price', null=False, default=0,)
	coupon_fish_start = models.CharField(verbose_name=u'coupon_fish_start',  max_length='30',)
	coupon_fish_finish = models.CharField(verbose_name=u'coupon_fish_finish', max_length='30',)
	coupon_fish_times = models.IntegerField(verbose_name=u'coupon_fish_times', null=False, default=0,)
	coupon_fish_detail = models.IntegerField(verbose_name=u'coupon_fish_detail', null=False, default=0,)
	coupon_fish_type = models.IntegerField(verbose_name=u'coupon_fish_type',null=False, default=0,)
	coupon_fish_active = models.IntegerField(verbose_name=u'coupon_fish_active',null=False, default=0,)
	coupon_fish_making = models.IntegerField(verbose_name=u'coupon_fish_making', null=False, default=0,)
        
# 쌀, 견과  
class COUPON_RICE(models.Model):
	class Meta:
		verbose_name = u'COUPON_RICE'
		db_table = 'COUPON_RICE_DB'
	coupon_rice_index = models.AutoField(verbose_name=u'coupon_rice_index', primary_key=True, unique=True, db_index=True,)
	coupon_rice_product_index = models.IntegerField(verbose_name=u'coupon_rice_product_index', null=False,)
	coupon_rice_photo_index = models.IntegerField(verbose_name=u'coupon_rice_photo_index', null=False,)
	coupon_rice_market_name =  models.CharField(verbose_name=u'coupon_rice_market_name', max_length='20',)
	coupon_rice_name = models.CharField(verbose_name=u'coupon_rice_name',  max_length='40',)
	coupon_rice_brand = models.CharField(verbose_name=u'coupon_rice_brand', max_length='20',)
	coupon_rice_unit = models.CharField(verbose_name=u'coupon_rice_unit', max_length='20',)
	coupon_rice_area = models.CharField(verbose_name=u'coupon_rice_area', max_length='20',)
	coupon_rice_price = models.IntegerField(verbose_name=u'coupon_rice_price', null=False, default=0,)
	coupon_rice_start = models.CharField(verbose_name=u'coupon_rice_start',  max_length='30',)
	coupon_rice_finish = models.CharField(verbose_name=u'coupon_rice_finish', max_length='30',)
	coupon_rice_times = models.IntegerField(verbose_name=u'coupon_rice_times', null=False, default=0,)
	coupon_rice_detail = models.IntegerField(verbose_name=u'coupon_rice_detail', null=False, default=0,)
	coupon_rice_type = models.IntegerField(verbose_name=u'coupon_rice_type',null=False, default=0,)
	coupon_rice_active = models.IntegerField(verbose_name=u'coupon_rice_active',null=False, default=0,)
	coupon_rice_making = models.IntegerField(verbose_name=u'coupon_rice_making', null=False, default=0,)
        
# 정육
class COUPON_MEAT(models.Model):
      	class Meta:
		verbose_name = u'COUPON_MEAT'
		db_table = 'COUPON_MEAT_DB'
	coupon_meat_index = models.AutoField(verbose_name=u'coupon_meat_index', primary_key=True, unique=True, db_index=True,)
	coupon_meat_product_index = models.IntegerField(verbose_name=u'coupon_meat_product_index', null=False,)
	coupon_meat_photo_index = models.IntegerField(verbose_name=u'coupon_meat_photo_index', null=False,)
	coupon_meat_market_name =  models.CharField(verbose_name=u'coupon_meat_market_name', max_length='20',)
	coupon_meat_name = models.CharField(verbose_name=u'coupon_meat_name', max_length='40',)
	coupon_meat_brand = models.CharField(verbose_name=u'coupon_meat_brand', max_length='20',)
	coupon_meat_unit = models.CharField(verbose_name=u'coupon_meat_unit', max_length='20',)
	coupon_meat_area = models.CharField(verbose_name=u'coupon_meat_area', max_length='20',)
	coupon_meat_price = models.IntegerField(verbose_name=u'coupon_meat_price', null=False, default=0,)
	coupon_meat_start = models.CharField(verbose_name=u'coupon_meat_start',  max_length='30',)
	coupon_meat_finish = models.CharField(verbose_name=u'coupon_meat_finish', max_length='30',)
	coupon_meat_times = models.IntegerField(verbose_name=u'coupon_meat_times', null=False, default=0,)
	coupon_meat_detail = models.IntegerField(verbose_name=u'coupon_meat_detail', null=False, default=0,)
	coupon_meat_type = models.IntegerField(verbose_name=u'coupon_meat_type',null=False, default=0,)
	coupon_meat_active = models.IntegerField(verbose_name=u'coupon_meat_active',null=False, default=0,)
	coupon_meat_making = models.IntegerField(verbose_name=u'coupon_meat_making', null=False, default=0,)
        
# 두부,콩나물,달걀
class COUPON_EGG(models.Model):
      	class Meta:
		verbose_name = u'COUPON_EGG'
		db_table = 'COUPON_EGG_DB'
	coupon_egg_index = models.AutoField(verbose_name=u'coupon_egg_index', primary_key=True, unique=True, db_index=True,)
	coupon_egg_product_index = models.IntegerField(verbose_name=u'coupon_egg_product_index', null=False,)
	coupon_egg_photo_index = models.IntegerField(verbose_name=u'coupon_egg_photo_index', null=False,)
	coupon_egg_market_name =  models.CharField(verbose_name=u'coupon_egg_market_name', max_length='20',)
	coupon_egg_name = models.CharField(verbose_name=u'coupon_egg_name', max_length='40',)
	coupon_egg_brand = models.CharField(verbose_name=u'coupon_egg_brand', max_length='20',)
	coupon_egg_unit = models.CharField(verbose_name=u'coupon_egg_unit', max_length='20',)
	coupon_egg_area = models.CharField(verbose_name=u'coupon_egg_area', max_length='20',)
	coupon_egg_price = models.IntegerField(verbose_name=u'coupon_egg_price', null=False, default=0,)
	coupon_egg_start = models.CharField(verbose_name=u'coupon_egg_start',  max_length='30',)
	coupon_egg_finish = models.CharField(verbose_name=u'coupon_egg_finish', max_length='30',)
	coupon_egg_times = models.IntegerField(verbose_name=u'coupon_egg_times', null=False, default=0,)
	coupon_egg_detail = models.IntegerField(verbose_name=u'coupon_egg_detail', null=False, default=0,)
	coupon_egg_type = models.IntegerField(verbose_name=u'coupon_egg_type',null=False, default=0,)
	coupon_egg_active = models.IntegerField(verbose_name=u'coupon_egg_active',null=False, default=0,)
	coupon_egg_making = models.IntegerField(verbose_name=u'coupon_egg_making', null=False, default=0,)
        
# 햄, 소시지, 어묵
class COUPON_HAM(models.Model):
      	class Meta:
		verbose_name = u'COUPON_HAM'
		db_table = 'COUPON_HAM_DB'
	coupon_ham_index = models.AutoField(verbose_name=u'coupon_ham_index', primary_key=True, unique=True, db_index=True,)
	coupon_ham_product_index = models.IntegerField(verbose_name=u'coupon_ham_product_index', null=False,)
	coupon_ham_photo_index = models.IntegerField(verbose_name=u'coupon_ham_photo_index', null=False,)
	coupon_ham_market_name =  models.CharField(verbose_name=u'coupon_ham_market_name', max_length='20',)
	coupon_ham_name = models.CharField(verbose_name=u'coupon_ham_name', unique=True, max_length='40',)
	coupon_ham_brand = models.CharField(verbose_name=u'coupon_ham_brand', max_length='20',)
	coupon_ham_unit = models.CharField(verbose_name=u'coupon_ham_unit', max_length='20',)
	coupon_ham_price = models.IntegerField(verbose_name=u'coupon_ham_price', null=False, default=0,)
	coupon_ham_start = models.CharField(verbose_name=u'coupon_ham_start',  max_length='30',)
	coupon_ham_finish = models.CharField(verbose_name=u'coupon_ham_finish', max_length='30',)
	coupon_ham_times = models.IntegerField(verbose_name=u'coupon_ham_times', null=False, default=0,)
	coupon_ham_detail = models.IntegerField(verbose_name=u'coupon_ham_detail', null=False, default=0,)
	coupon_ham_type = models.IntegerField(verbose_name=u'coupon_ham_type', null=False, default=0,)
	coupon_ham_active = models.IntegerField(verbose_name=u'coupon_ham_active', null=False, default=0,)
	coupon_ham_making = models.IntegerField(verbose_name=u'coupon_ham_making', null=False, default=0,)
        
# 김치, 반찬
class COUPON_SIDE(models.Model):
      	class Meta:
		verbose_name = u'COUPON_SIDE'
		db_table = 'COUPON_SIDE_DB'
	coupon_side_index = models.AutoField(verbose_name=u'coupon_side_index', primary_key=True, unique=True, db_index=True,)
	coupon_side_product_index = models.IntegerField(verbose_name=u'coupon_side_product_index', null=False,)
	coupon_side_photo_index = models.IntegerField(verbose_name=u'coupon_side_photo_index', null=False,)
	coupon_side_market_name =  models.CharField(verbose_name=u'coupon_side_market_name', max_length='20',)
	coupon_side_name = models.CharField(verbose_name=u'coupon_side_name', unique=True, max_length='40',)
	coupon_side_brand = models.CharField(verbose_name=u'coupon_side_brand', max_length='20',)
	coupon_side_unit = models.CharField(verbose_name=u'coupon_side_unit', max_length='20',)
	coupon_side_price = models.IntegerField(verbose_name=u'coupon_side_price', null=False, default=0,)
	coupon_side_start = models.CharField(verbose_name=u'coupon_side_start',  max_length='30',)
	coupon_side_finish = models.CharField(verbose_name=u'coupon_side_finish', max_length='30',)
	coupon_side_times = models.IntegerField(verbose_name=u'coupon_side_times', null=False, default=0,)
	coupon_side_detail = models.IntegerField(verbose_name=u'coupon_side_detail', null=False, default=0,)
	coupon_side_type = models.IntegerField(verbose_name=u'coupon_side_type',null=False, default=0,)
	coupon_side_active = models.IntegerField(verbose_name=u'coupon_side_active',null=False, default=0,)
	coupon_side_making = models.IntegerField(verbose_name=u'coupon_side_making', null=False, default=0,)
        
# 생수, 음료
class COUPON_WATER(models.Model):
      	class Meta:
		verbose_name = u'COUPON_WATER'
		db_table = 'COUPON_WATER_DB'
	coupon_water_index = models.AutoField(verbose_name=u'coupon_water_index', primary_key=True, unique=True, db_index=True,)
	coupon_water_product_index = models.IntegerField(verbose_name=u'coupon_water_product_index', null=False,)
	coupon_water_photo_index = models.IntegerField(verbose_name=u'coupon_water_photo_index', null=False,)
	coupon_water_market_name =  models.CharField(verbose_name=u'coupon_water_market_name', max_length='20',)
	coupon_water_name = models.CharField(verbose_name=u'coupon_water_name', unique=True, max_length='40',)
	coupon_water_brand = models.CharField(verbose_name=u'coupon_water_brand', max_length='20',)
	coupon_water_unit = models.CharField(verbose_name=u'coupon_water_unit', max_length='20',)
	coupon_water_price = models.IntegerField(verbose_name=u'coupon_water_price', null=False, default=0,)
	coupon_water_start = models.CharField(verbose_name=u'coupon_water_start',  max_length='30',)
	coupon_water_finish = models.CharField(verbose_name=u'coupon_water_finish', max_length='30',)
	coupon_water_times = models.IntegerField(verbose_name=u'coupon_water_times', null=False, default=0,)
	coupon_water_detail = models.IntegerField(verbose_name=u'coupon_water_detail', null=False, default=0,)
	coupon_water_type = models.IntegerField(verbose_name=u'coupon_water_type',null=False, default=0,)
	coupon_water_active = models.IntegerField(verbose_name=u'coupon_water_active',null=False, default=0,)
	coupon_water_making = models.IntegerField(verbose_name=u'coupon_water_making', null=False, default=0,)
        
# 라면, 통조림, 즉석식품
class COUPON_INSTANT(models.Model):
      	class Meta:
		verbose_name = u'COUPON_INSTANT'
		db_table = 'COUPON_INSTANT_DB'
	coupon_instant_index = models.AutoField(verbose_name=u'coupon_instant_index', primary_key=True, unique=True, db_index=True,)
	coupon_instant_product_index = models.IntegerField(verbose_name=u'coupon_instant_product_index', null=False,)
	coupon_instant_photo_index = models.IntegerField(verbose_name=u'coupon_instant_photo_index', null=False,)
	coupon_instant_market_name =  models.CharField(verbose_name=u'coupon_instant_market_name', max_length='20',)
	coupon_instant_name = models.CharField(verbose_name=u'coupon_instant_name', unique=True, max_length='40',)
	coupon_instant_brand = models.CharField(verbose_name=u'coupon_instant_brand', max_length='20',)
	coupon_instant_unit = models.CharField(verbose_name=u'coupon_instant_unit', max_length='20',)
	coupon_instant_price = models.IntegerField(verbose_name=u'coupon_instant_price', null=False, default=0,)
	coupon_instant_start = models.CharField(verbose_name=u'coupon_instant_start',  max_length='30',)
	coupon_instant_finish = models.CharField(verbose_name=u'coupon_instant_finish', max_length='30',)
	coupon_instant_times = models.IntegerField(verbose_name=u'coupon_instant_times', null=False, default=0,)
	coupon_instant_detail = models.IntegerField(verbose_name=u'coupon_instant_detail', null=False, default=0,)
	coupon_instant_type = models.IntegerField(verbose_name=u'coupon_instant_type',null=False, default=0,)
	coupon_instant_active = models.IntegerField(verbose_name=u'coupon_instant_active',null=False, default=0,)
	coupon_instant_making = models.IntegerField(verbose_name=u'coupon_instant_making', null=False, default=0,)
    	
# 냉동만두, 너겟, 빙과
class COUPON_ICE(models.Model):
      	class Meta:
		verbose_name = u'COUPON_ICE'
		db_table = 'COUPON_ICE_DB'
	coupon_ice_index = models.AutoField(verbose_name=u'coupon_ice_index', primary_key=True, unique=True, db_index=True,)
	coupon_ice_product_index = models.IntegerField(verbose_name=u'coupon_ice_product_index', null=False,)
	coupon_ice_photo_index = models.IntegerField(verbose_name=u'coupon_ice_photo_index', null=False,)
	coupon_ice_market_name =  models.CharField(verbose_name=u'coupon_ice_market_name', max_length='20',)
	coupon_ice_name = models.CharField(verbose_name=u'coupon_ice_name', unique=True, max_length='40',)
	coupon_ice_brand = models.CharField(verbose_name=u'coupon_ice_brand', max_length='20',)
	coupon_ice_unit = models.CharField(verbose_name=u'coupon_ice_unit', max_length='20',)
	coupon_ice_price = models.IntegerField(verbose_name=u'coupon_ice_price', null=False, default=0,)
	coupon_ice_start = models.CharField(verbose_name=u'coupon_ice_start',  max_length='30',)
	coupon_ice_finish = models.CharField(verbose_name=u'coupon_ice_finish', max_length='30',)
	coupon_ice_times = models.IntegerField(verbose_name=u'coupon_ice_times', null=False, default=0,)
	coupon_ice_detail = models.IntegerField(verbose_name=u'coupon_ice_detail', null=False, default=0,)
	coupon_ice_type = models.IntegerField(verbose_name=u'coupon_ice_type',null=False, default=0,)
	coupon_ice_active = models.IntegerField(verbose_name=u'coupon_ice_active',null=False, default=0,)
	coupon_ice_making = models.IntegerField(verbose_name=u'coupon_ice_m3aking', null=False, default=0,)
        
# 시리얼, 베이커리, 잼
class COUPON_BAKERY(models.Model):
      	class Meta:
		verbose_name = u'COUPON_BAKERY'
		db_table = 'COUPON_BAKERY_DB'
	coupon_bakery_index = models.AutoField(verbose_name=u'coupon_bakery_index', primary_key=True, unique=True, db_index=True,)
	coupon_bakery_product_index = models.IntegerField(verbose_name=u'coupon_bakery_product_index', null=False,)
	coupon_bakery_photo_index = models.IntegerField(verbose_name=u'coupon_bakery_photo_index', null=False,)
	coupon_bakery_market_name =  models.CharField(verbose_name=u'coupon_bakery_market_name', max_length='20',)
	coupon_bakery_name = models.CharField(verbose_name=u'coupon_bakery_name', unique=True, max_length='40',)
	coupon_bakery_brand = models.CharField(verbose_name=u'coupon_bakery_brand', max_length='20',)
	coupon_bakery_unit = models.CharField(verbose_name=u'coupon_bakery_unit', max_length='20',)
	coupon_bakery_price = models.IntegerField(verbose_name=u'coupon_bakery_price', null=False, default=0,)
	coupon_bakery_start = models.CharField(verbose_name=u'coupon_bakery_start',  max_length='30',)
	coupon_bakery_finish = models.CharField(verbose_name=u'coupon_bakery_finish', max_length='30',)
	coupon_bakery_times = models.IntegerField(verbose_name=u'coupon_bakery_times', null=False, default=0,)
	coupon_bakery_detail = models.IntegerField(verbose_name=u'coupon_bakery_detail', null=False, default=0,)
	coupon_bakery_type = models.IntegerField(verbose_name=u'coupon_bakery_type',null=False, default=0,)
	coupon_bakery_active = models.IntegerField(verbose_name=u'coupon_bakery_active',null=False, default=0,)
	coupon_bakery_making = models.IntegerField(verbose_name=u'coupon_bakery_making', null=False, default=0,)
    	
# 과자
class COUPON_SNACK(models.Model):
      	class Meta:
		verbose_name = u'COUPON_SNACK'
		db_table = 'COUPON_SNACK_DB'
	coupon_snack_index = models.AutoField(verbose_name=u'coupon_snack_index', primary_key=True, unique=True, db_index=True,)
	coupon_snack_product_index = models.IntegerField(verbose_name=u'coupon_snack_product_index', null=False,)
	coupon_snack_photo_index = models.IntegerField(verbose_name=u'coupon_snack_photo_index', null=False,)
	coupon_snack_market_name =  models.CharField(verbose_name=u'coupon_snack_market_name', max_length='20',)
	coupon_snack_name = models.CharField(verbose_name=u'coupon_snack_name', unique=True, max_length='40',)
	coupon_snack_brand = models.CharField(verbose_name=u'coupon_snack_brand', max_length='20',)
	coupon_snack_unit = models.CharField(verbose_name=u'coupon_snack_unit', max_length='20',)
	coupon_snack_price = models.IntegerField(verbose_name=u'coupon_snack_price', null=False, default=0,)
	coupon_snack_start = models.CharField(verbose_name=u'coupon_snack_start',  max_length='30',)
	coupon_snack_finish = models.CharField(verbose_name=u'coupon_snack_finish', max_length='30',)
	coupon_snack_times = models.IntegerField(verbose_name=u'coupon_snack_times', null=False, default=0,)
	coupon_snack_detail = models.IntegerField(verbose_name=u'coupon_snack_detail', null=False, default=0,)
	coupon_snack_type = models.IntegerField(verbose_name=u'coupon_snack_type',null=False, default=0,)
	coupon_snack_active = models.IntegerField(verbose_name=u'coupon_snack_active',null=False, default=0,)
	coupon_snack_making = models.IntegerField(verbose_name=u'coupon_snack_making', null=False, default=0,)
        

#-사용자 DB-----------------------------------------------------------------
class USER_FAVORITE_LIST(models.Model):
      	class Meta:
		verbose_name = u'USER_FAVORITE_LIST'
		db_table = 'USER_FAVORITE_LIST_DB'
		unique_together = ('user_favorite_list_userid', 'user_favorite_list_product_index',)
	user_favorite_list_index = models.AutoField(verbose_name=u'user_favorite_list_index', primary_key=True, unique=True, db_index=True,)
	user_favorite_list_userid = models.CharField(verbose_name=u'user_favorite_list_userid', max_length='20',)
	user_favorite_list_product_index = models.CharField(verbose_name=u'user_favorite_list_product_index', max_length='30',)
	user_favorite_list_product_name = models.CharField(verbose_name=u'user_favorite_list_product_name', max_length='30',)
	user_favorite_list_product_brand = models.CharField(verbose_name=u'user_favorite_list_product_brand', max_length='20',)
	user_favorite_list_product_unit = models.CharField(verbose_name=u'user_favorite_list_product_unit',max_length='20',)
	user_favorite_list_product_category = models.IntegerField(verbose_name=u'user_favorite_list_product_category', null=False, default=0,)

class USER_COUPON_USEDLIST(models.Model):
      	class Meta: 
		verbose_name = u'USER_COUPON_USEDLIST'
		db_table = 'USER_COUPON_USEDLIST_DB'
	user_coupon_usedlist_index = models.AutoField(verbose_name=u'user_coupon_usedlist_index', primary_key=True, unique=True, db_index=True,)
	user_coupon_usedlist_coupon_index = models.IntegerField(verbose_name=u'user_coupon_usedlist_coupon_index', db_index=True,)
	user_coupon_usedlist_userid = models.CharField(verbose_name=u'user_coupon_usedlist_userid', max_length='20',)
	user_coupon_usedlist_product_index = models.CharField(verbose_name=u'user_coupon_usedlist_product_index', max_length='30',)
	user_coupon_usedlist_product_name = models.CharField(verbose_name=u'user_coupon_usedlist_product_name', max_length='30',)
	user_coupon_usedlist_product_brand = models.CharField(verbose_name=u'user_coupon_usedlist_product_brand', max_length='20',)
	user_coupon_usedlist_product_unit = models.CharField(verbose_name=u'user_coupon_usedlist_product_unit',max_length='20',)
	user_coupon_usedlist_product_category = models.IntegerField(verbose_name=u'user_coupon_usedlist_product_category', null=False, default=0,)
	user_coupon_usedlist_type = models.IntegerField(verbose_name=u'user_coupon_usedlist_type',null=False, default=0,)
        

#----------------------------------------------------------------------------
class SP_PICTURE(models.Model):
	class Meta:
		verbose_name = u'SP_PICTURE'
		db_table = 'SP_PICTURE_DB'
	#db_index : indexing by computer
	sp_photo_index = models.AutoField(verbose_name=u'sp_photo_index', primary_key=True, unique=True, db_index=True,)
	sp_name = models.CharField(verbose_name=u'sp_name', max_length=100)
	sp_picture = models.ImageField(verbose_name=u'sp_picture', upload_to='sp_app/sp_pictures/sp_pictures/', blank=True, null=True)


class USER_PICTURE(models.Model):
	class Meta:
		verbose_name = u'USER_PICTURE'
		db_table = 'USER_PICTURE_DB'
	user_photo_index = models.IntegerField(verbose_name=u'user_photo_index', primary_key=True, unique=True, db_index=True,)
	user_name = models.CharField(verbose_name=u'user_name', max_length=100)
	user_picture = models.ImageField(verbose_name=u'user_picture', upload_to='sp_app/sp_pictures/user_picture/', blank=True, null=True)





