# _*_ coding: utf-8 _*_
# samsung sGen Club 2014.winter spopting project : yoonmijae, leeayoung

import json
import base64

from django import forms
from django.shortcuts import *
from django.http import *
from django.core.context_processors import *
from django.forms.models import *
from django.template import *
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.core.files import File
from django.core.context_processors import *
from django.views.decorators.csrf import *

from django.contrib.auth import *
from django.contrib.auth.models import User, UserManager

from sp_app.models import *


def test_photo_open_t(request):
	page_title = 'test_photo_open_t'

	return render_to_response('imgForm_t.html')

def test_photo_open_c(request):
	page_title = 'test_photo_open_c'

	return render_to_response('imgForm_c.html')

# anroid -> server 
@csrf_exempt
def test_photo_upload(request):
	page_title = 'test_photo_upload'

	if request.method == 'POST':
		if 'file' in request.FILES:
			file = request.FILES['file']
			file_name_ = request.POST.get('file_name', 'False')
			file_day_ = request.POST.get('file_day', '00000')
			filename = file_name_ + '_' + file_day_

			try:
				pic_ = SP_PICTURE()
				# pic_.sp_photo_index = 1
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
			except:
				return HttpResponse(404)		
			pic_.save()


			# path = '/Users/ayoung/Documents/develope/Django_SP/Django_sp/sp_app/imges'
			# fp = open('%s/%s' % (path, filename+'.jpg') , 'wb')
			# for chunk in file.chunks():
			# 	fp.write(chunk)
			# fp.close()

			# use for android communication
			# response_data=[{"success": "1"}]
		# return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
	
			# use for test
			return HttpResponse('File Uploaded')

	return HttpResponse('Failed to Upload File')

# android <- server 
def test_photo_download_1(request):
	page_title = 'test_photo_download_1'

	# pic_ = SP_PICTURE.objects.filter(sp_name='sgenay_2014')

	# datas = []
	# for i in pic_:
	# 	data = model_to_dict(i)
	# 	datas.append(data)

	# json_data = json.dumps(datas)
	# return HttpResponse(json_data, content_type='image/jpg')

	# image_ = base64.decodestring(json.dumps(pic_))
	# return HttpResponse(image_, content_type='image/jpg')

	image_data_ = open("sp_app/sp_pictures/sp_pictures/mung_3.jpg", "rb").read()
	
	return HttpResponse(image_data_, mimetype="image/png")

# android <- server (photos)
def test_photo_download_s(request):
	page_title = 'test_photo_download_s'

	image_data_1 = open("sp_app/sp_pictures/sp_pictures/mung_2.jpg", "rb").read()
	image_data_2 = open("sp_app/sp_pictures/sp_pictures/mung_1.jpg", "rb").read()

	images = []
	images.append(image_data_2)
	images.append(image_data_1)

	return HttpResponse(images, mimetype="image/png")

# android <- server (base64)
def test_photo_download_2(request):
	page_title = 'test_photo_download_2'

	pic_1 = SP_PICTURE.objects.get(sp_name='mung_4')
	pic_2 = SP_PICTURE.objects.get(sp_name='mung_3')

	images = []
	images.append(pic_1.sp_picture)
	images.append(pic_2.sp_picture) 

	return HttpResponse(images, mimetype='image/png')


# seller join / login--------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def join_page_s(request):
	page_title = 'join_page_s'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('join_page_s.html', ctx)

@csrf_exempt
def request_join_seller(request):
	callback = request.GET.get('callback')
	page_title = 'request_join_seller'

	#id = username, firstname = name
	join_seller_id_ = request.POST.get('join_seller_id', False)
	join_seller_pwd_ = request.POST.get('join_seller_pwd', False)
	join_seller_name_ = request.POST.get('join_seller_name', False)
	join_seller_email_ = request.POST.get('join_seller_email', False)

	join_seller_photo_index_ = 0
	join_seller_market_name_ = request.POST.get('join_seller_market_name', False)
	join_seller_address_ = request.POST.get('join_seller_address', False)
	user_seller_latitude_ = request.POST.get('user_seller_latitude', False)
	user_seller_longitude_ = request.POST.get('user_seller_longitude', False)
	join_seller_phone_ = request.POST.get('join_seller_phone', False)

	join_seller_ = User.objects.create_user(join_seller_id_, join_seller_email_, join_seller_pwd_)
	join_seller_.first_name = join_seller_name_
	join_seller_.is_staff = False

	try:
		join_seller_.save()
		join_seller_info_ = USER_SELLER(user_seller_id=join_seller_, user_seller_photo_index=join_seller_photo_index_, user_seller_market_name=join_seller_market_name_, user_seller_address=join_seller_address_, user_seller_latitude=user_seller_latitude_, user_seller_longitude=user_seller_longitude_, user_seller_phone=join_seller_phone_)
		join_seller_info_.save()
	except:
		return HttpResponse('fail join')

	return HttpResponse('success join, %s' % join_seller_id_)


#-------------------------------------------------------------------------------------------------------------------------
def login_page_s(request):
	page_title = 'login_page_s'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('login_page_s.html', ctx)

@csrf_exempt
def request_login_seller(request):
	callback = request.GET.get('callback')
	page_title = 'request_login_seller'

	login_seller_id_ = request.POST.get('seller_id', False)
	login_seller_pwd_ = request.POST.get('seller_pwd', False)

	login_seller_ = authenticate(username=login_seller_id_, password=login_seller_pwd_)

	if login_seller_ is not None:
		if login_seller_.is_active:
			login(request, login_seller_)
		else:
			#disabled account
			return HttpResponse('disabled account')
	else:
		#invaild login
		return HttpResponse('invaild login %s, %s' %(login_seller_id_, login_seller_pwd_))

	#get userInfo
	user_seller_ = User.objects.get(username=login_seller_id_)
	user_seller_info_ = USER_SELLER.objects.get(user_seller_id=user_seller_)

	#make session
	request.session['sess_seller_id'] = user_seller_.username
	request.session['sess_seller_market_name'] = user_seller_info_.user_seller_market_name

	datas = []
	datas.append(user_seller_.id) 			#index
	datas.append(user_seller_.username) 	#id
	datas.append(user_seller_.first_name) 	#name
	datas.append(user_seller_.email)
	datas.append(user_seller_info_.user_seller_photo_index)
	datas.append(user_seller_info_.user_seller_market_name)
	datas.append(user_seller_info_.user_seller_address)
	datas.append(user_seller_info_.user_seller_phone)

	json_data = json.dumps(datas, ensure_ascii=False)
	return HttpResponse(json_data, content_type='application/json')


# controll coupon-----------------------------------------------------
# all coupon data---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_coupon_all(request):
	page_title = 'request_coupon_all'

	datas = []

	coupon_data_= COUPON_DAILY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_GREENS.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_FISH.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_RICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_MEAT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_EGG.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_HAM.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SIDE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_WATER.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_INSTANT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_ICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_BAKERY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SNACK.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# each coupon data---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_coupon_daily(request):
	page_title = 'request_coupon_daily'

	coupon_data_= COUPON_DAILY.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_greens(request):
	page_title = 'request_coupon_greens'

	coupon_data_= COUPON_GREENS.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_fish(request):
	page_title = 'request_coupon_fish'

	coupon_data_= COUPON_FISH.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_rice(request):
	page_title = 'request_coupon_rice'

	coupon_data_= COUPON_RICE.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_meat(request):
	page_title = 'request_coupon_meat'

	coupon_data_= COUPON_MEAT.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_egg(request):
	page_title = 'request_coupon_egg'

	coupon_data_= COUPON_EGG.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_ham(request):
	page_title = 'request_coupon_ham'

	coupon_data_= COUPON_HAM.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_side(request):
	page_title = 'request_coupon_side'

	coupon_data_= COUPON_SIDE.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_water(request):
	page_title = 'request_coupon_water'

	coupon_data_= COUPON_WATER.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_instant(request):
	page_title = 'request_coupon_instant'

	coupon_data_= COUPON_INSTANT.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_ice(request):
	page_title = 'request_coupon_ice'

	coupon_data_= COUPON_ICE.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_bakery(request):
	page_title = 'request_coupon_bakery'

	coupon_data_= COUPON_BAKERY.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_coupon_snack(request):
	page_title = 'request_coupon_snack'

	coupon_data_= COUPON_SNACK.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# make coupon-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_make_daily(request):
	page_title = 'request_make_daily'
	# /request/make/daily/?coupon_daily_product_index=0&coupon_daily_photo_index=1&coupon_daily_market_name=nabak&coupon_daily_name=milk&coupon_daily_brand=pul&coupon_daily_unit=0&coupon_daily_price=100&coupon_daily_start=0&coupon_daily_finish=0&coupon_daily_times=0&coupon_daily_detail=0&coupon_daily_type=0

	coupon_daily_product_index_ = request.POST.get('coupon_daily_product_index')
	# not change: 0 / change: 1
	coupon_daily_photo_index_ = request.POST.get('coupon_daily_photo_index')
	coupon_daily_market_name_ =  request.POST.get('coupon_daily_market_name')
	coupon_daily_name_ = request.POST.get('coupon_daily_name')
	coupon_daily_brand_ = request.POST.get('coupon_daily_brand')
	coupon_daily_unit_ = request.POST.get('coupon_daily_unit')
	coupon_daily_price_ = request.POST.get('coupon_daily_price')
	coupon_daily_start_ = request.POST.get('coupon_daily_start')
	coupon_daily_finish_ = request.POST.get('coupon_daily_finish')
	coupon_daily_times_ = request.POST.get('coupon_daily_times')
	coupon_daily_detail_ = request.POST.get('coupon_daily_detail')
	coupon_daily_type_ = request.POST.get('coupon_daily_type')

	# make coupon
	coupon_daily = COUPON_DAILY(coupon_daily_product_index = coupon_daily_product_index_, coupon_daily_photo_index = coupon_daily_photo_index_, coupon_daily_market_name = coupon_daily_market_name_, coupon_daily_name = coupon_daily_name_, coupon_daily_brand = coupon_daily_brand_, coupon_daily_unit = coupon_daily_unit_, coupon_daily_price = coupon_daily_price_, coupon_daily_start = coupon_daily_start_, coupon_daily_finish = coupon_daily_finish_, coupon_daily_times = coupon_daily_times_, coupon_daily_detail = coupon_daily_detail_, coupon_daily_type = coupon_daily_type_,)
	coupon_daily.save()

	coupon_ = COUPON_DAILY.objects.get(coupon_daily_name=coupon_daily_name_)
	coupon_daily_index_ = coupon_.coupon_daily_index

	# have to change photo
	if coupon_daily_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_daily' + '_' + str(coupon_daily_product_index_ )+ '_' + str(coupon_daily_index_) + '_' + coupon_daily_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_daily_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_daily_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_daily_product_index_)
		coupon_daily_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_daily_photo_index = coupon_daily_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_greens(request):
	page_title = 'request_make_greens'
	# /request/make/greens/?coupon_greens_product_index=0&coupon_greens_photo_index=1&coupon_greens_market_name=nabak&coupon_greens_name=milk&coupon_greens_brand=pul&coupon_greens_unit=0&coupon_greens_price=100&coupon_greens_start=0&coupon_greens_finish=0&coupon_greens_times=0&coupon_greens_detail=0&coupon_greens_type=0

	coupon_greens_product_index_ = request.POST.get('coupon_greens_product_index')
	# not change: 0 / change: 1
	coupon_greens_photo_index_ = request.POST.get('coupon_greens_photo_index')
	coupon_greens_market_name_ =  request.POST.get('coupon_greens_market_name')
	coupon_greens_name_ = request.POST.get('coupon_greens_name')
	coupon_greens_brand_ = request.POST.get('coupon_greens_brand')
	coupon_greens_unit_ = request.POST.get('coupon_greens_unit')
	coupon_greens_area_ =  request.POST.get('coupon_greens_area')
	coupon_greens_price_ = request.POST.get('coupon_greens_price')
	coupon_greens_start_ = request.POST.get('coupon_greens_start')
	coupon_greens_finish_ = request.POST.get('coupon_greens_finish')
	coupon_greens_times_ = request.POST.get('coupon_greens_times')
	coupon_greens_detail_ = request.POST.get('coupon_greens_detail')
	coupon_greens_type_ = request.POST.get('coupon_greens_type')

	# make coupon
	coupon_greens = COUPON_GREENS(coupon_greens_product_index = coupon_greens_product_index_, coupon_greens_photo_index = coupon_greens_photo_index_, coupon_greens_market_name = coupon_greens_market_name_, coupon_greens_name = coupon_greens_name_, coupon_greens_brand = coupon_greens_brand_, coupon_greens_unit = coupon_greens_unit_, coupon_greens_area=coupon_greens_area_, coupon_greens_price = coupon_greens_price_, coupon_greens_start = coupon_greens_start_, coupon_greens_finish = coupon_greens_finish_, coupon_greens_times = coupon_greens_times_, coupon_greens_detail = coupon_greens_detail_, coupon_greens_type = coupon_greens_type_,)
	coupon_greens.save()

	coupon_ = COUPON_GREENS.objects.get(coupon_greens_name=coupon_greens_name_)
	coupon_greens_index_ = coupon_.coupon_greens_index

	# have to change photo
	if coupon_greens_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_greens' + '_' + str(coupon_greens_product_index_ )+ '_' + str(coupon_greens_index_) + '_' + coupon_greens_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_greens_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_greens_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_greens_product_index_)
		coupon_greens_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_greens_photo_index = coupon_greens_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_fish(request):
	page_title = 'request_make_fish'
	# /request/make/fish/?coupon_fish_product_index=0&coupon_fish_photo_index=1&coupon_fish_market_name=nabak&coupon_fish_name=milk&coupon_fish_brand=pul&coupon_fish_unit=0&coupon_fish_price=100&coupon_fish_start=0&coupon_fish_finish=0&coupon_fish_times=0&coupon_fish_detail=0&coupon_fish_type=0

	coupon_fish_product_index_ = request.POST.get('coupon_fish_product_index')
	# not change: 0 / change: 1
	coupon_fish_photo_index_ = request.POST.get('coupon_fish_photo_index')
	coupon_fish_market_name_ =  request.POST.get('coupon_fish_market_name')
	coupon_fish_name_ = request.POST.get('coupon_fish_name')
	coupon_fish_brand_ = request.POST.get('coupon_fish_brand')
	coupon_fish_unit_ = request.POST.get('coupon_fish_unit')
	coupon_fish_area_ =  request.POST.get('coupon_fish_area')
	coupon_fish_price_ = request.POST.get('coupon_fish_price')
	coupon_fish_start_ = request.POST.get('coupon_fish_start')
	coupon_fish_finish_ = request.POST.get('coupon_fish_finish')
	coupon_fish_times_ = request.POST.get('coupon_fish_times')
	coupon_fish_type_ = request.POST.get('coupon_fish_type')

	# make coupon
	coupon_fish = COUPON_FISH(coupon_fish_product_index = coupon_fish_product_index_, coupon_fish_photo_index = coupon_fish_photo_index_, coupon_fish_market_name = coupon_fish_market_name_, coupon_fish_name = coupon_fish_name_, coupon_fish_brand = coupon_fish_brand_, coupon_fish_unit = coupon_fish_unit_, coupon_fish_area=coupon_fish_area_, coupon_fish_price = coupon_fish_price_, coupon_fish_start = coupon_fish_start_, coupon_fish_finish = coupon_fish_finish_, coupon_fish_times = coupon_fish_times_, coupon_fish_type = coupon_fish_type_,)
	coupon_fish.save()

	coupon_ = COUPON_FISH.objects.get(coupon_fish_name=coupon_fish_name_)
	coupon_fish_index_ = coupon_.coupon_fish_index

	# have to change photo
	if coupon_fish_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_fish' + '_' + str(coupon_fish_product_index_ )+ '_' + str(coupon_fish_index_) + '_' + coupon_fish_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_fish_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_fish_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_fish_product_index_)
		coupon_fish_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_fish_photo_index = coupon_fish_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_rice(request):
	page_title = 'request_make_rice'
	# /request/make/rice/?coupon_rice_product_index=0&coupon_rice_photo_index=1&coupon_rice_market_name=nabak&coupon_rice_name=milk&coupon_rice_brand=pul&coupon_rice_unit=0&coupon_rice_price=100&coupon_rice_start=0&coupon_rice_finish=0&coupon_rice_times=0&coupon_rice_detail=0&coupon_rice_type=0 

	coupon_rice_product_index_ = request.POST.get('coupon_rice_product_index')
	# not change: 0 / change: 1
	coupon_rice_photo_index_ = request.POST.get('coupon_rice_photo_index')
	coupon_rice_market_name_ =  request.POST.get('coupon_rice_market_name')
	coupon_rice_name_ = request.POST.get('coupon_rice_name')
	coupon_rice_brand_ = request.POST.get('coupon_rice_brand')
	coupon_rice_unit_ = request.POST.get('coupon_rice_unit')
	coupon_rice_area_ =  request.POST.get('coupon_rice_area')
	coupon_rice_price_ = request.POST.get('coupon_rice_price')
	coupon_rice_start_ = request.POST.get('coupon_rice_start')
	coupon_rice_finish_ = request.POST.get('coupon_rice_finish')
	coupon_rice_times_ = request.POST.get('coupon_rice_times')
	coupon_rice_detail_ = request.POST.get('coupon_rice_detail')
	coupon_rice_type_ = request.POST.get('coupon_rice_type')

	# make coupon
	coupon_rice = COUPON_RICE(coupon_rice_product_index = coupon_rice_product_index_, coupon_rice_photo_index = coupon_rice_photo_index_, coupon_rice_market_name = coupon_rice_market_name_, coupon_rice_name = coupon_rice_name_, coupon_rice_brand = coupon_rice_brand_, coupon_rice_unit = coupon_rice_unit_, coupon_rice_area=coupon_rice_area_, coupon_rice_price = coupon_rice_price_, coupon_rice_start = coupon_rice_start_, coupon_rice_finish = coupon_rice_finish_, coupon_rice_times = coupon_rice_times_, coupon_rice_detail = coupon_rice_detail_, coupon_rice_type = coupon_rice_type_,)
	coupon_rice.save()

	coupon_ = COUPON_RICE.objects.get(coupon_rice_name=coupon_rice_name_)
	coupon_rice_index_ = coupon_.coupon_rice_index

	# have to change photo
	if coupon_rice_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_rice' + '_' + str(coupon_rice_product_index_ )+ '_' + str(coupon_rice_index_) + '_' + coupon_rice_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_rice_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_rice_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_rice_product_index_)
		coupon_rice_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_rice_photo_index = coupon_rice_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_meat(request):
	page_title = 'request_make_meat'
	# /request/make/meat/?coupon_meat_product_index=0&coupon_meat_photo_index=1&coupon_meat_market_name=nabak&coupon_meat_name=milk&coupon_meat_brand=pul&coupon_meat_unit=0&coupon_meat_pmeat=100&coupon_meat_start=0&coupon_meat_finish=0&coupon_meat_times=0&coupon_meat_detail=0&coupon_meat_type=0

	coupon_meat_product_index_ = request.POST.get('coupon_meat_product_index')
	# not change: 0 / change: 1
	coupon_meat_photo_index_ = request.POST.get('coupon_meat_photo_index')
	coupon_meat_market_name_ =  request.POST.get('coupon_meat_market_name')
	coupon_meat_name_ = request.POST.get('coupon_meat_name')
	coupon_meat_brand_ = request.POST.get('coupon_meat_brand')
	coupon_meat_unit_ = request.POST.get('coupon_meat_unit')
	coupon_meat_area_ =  request.POST.get('coupon_meat_area')
	coupon_meat_price_ = request.POST.get('coupon_meat_price')
	coupon_meat_start_ = request.POST.get('coupon_meat_start')
	coupon_meat_finish_ = request.POST.get('coupon_meat_finish')
	coupon_meat_times_ = request.POST.get('coupon_meat_times')
	coupon_meat_type_ = request.POST.get('coupon_meat_type')

	# make coupon
	coupon_meat = COUPON_MEAT(coupon_meat_product_index = coupon_meat_product_index_, coupon_meat_photo_index = coupon_meat_photo_index_, coupon_meat_market_name = coupon_meat_market_name_, coupon_meat_name = coupon_meat_name_, coupon_meat_brand = coupon_meat_brand_, coupon_meat_unit = coupon_meat_unit_, coupon_meat_area=coupon_meat_area_, coupon_meat_price = coupon_meat_price_, coupon_meat_start = coupon_meat_start_, coupon_meat_finish = coupon_meat_finish_, coupon_meat_times = coupon_meat_times_, coupon_meat_type = coupon_meat_type_,)
	coupon_meat.save()

	coupon_ = COUPON_MEAT.objects.get(coupon_meat_name=coupon_meat_name_)
	coupon_meat_index_ = coupon_.coupon_meat_index

	# have to change photo
	if coupon_meat_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_meat' + '_' + str(coupon_meat_product_index_ )+ '_' + str(coupon_meat_index_) + '_' + coupon_meat_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_meat_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_meat_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_meat_product_index_)
		coupon_meat_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_meat_photo_index = coupon_meat_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_egg(request):
	page_title = 'request_make_egg'
	# /request/make/egg/?coupon_egg_product_index=0&coupon_egg_photo_index=1&coupon_egg_market_name=nabak&coupon_egg_name=milk&coupon_egg_brand=pul&coupon_egg_unit=0&coupon_egg_pegg=100&coupon_egg_start=0&coupon_egg_finish=0&coupon_egg_times=0&coupon_egg_detail=0&coupon_egg_type=0

	coupon_egg_product_index_ = request.POST.get('coupon_egg_product_index')
	# not change: 0 / change: 1
	coupon_egg_photo_index_ = request.POST.get('coupon_egg_photo_index')
	coupon_egg_market_name_ =  request.POST.get('coupon_egg_market_name')
	coupon_egg_name_ = request.POST.get('coupon_egg_name')
	coupon_egg_brand_ = request.POST.get('coupon_egg_brand')
	coupon_egg_unit_ = request.POST.get('coupon_egg_unit')
	coupon_egg_area_ =  request.POST.get('coupon_egg_area')
	coupon_egg_price_ = request.POST.get('coupon_egg_price_')
	coupon_egg_start_ = request.POST.get('coupon_egg_start')
	coupon_egg_finish_ = request.POST.get('coupon_egg_finish')
	coupon_egg_times_ = request.POST.get('coupon_egg_times')
	coupon_egg_detail_ = request.POST.get('coupon_egg_detail')
	coupon_egg_type_ = request.POST.get('coupon_egg_type')

	# make coupon
	coupon_egg = COUPON_EGG(coupon_egg_product_index = coupon_egg_product_index_, coupon_egg_photo_index = coupon_egg_photo_index_, coupon_egg_market_name = coupon_egg_market_name_, coupon_egg_name = coupon_egg_name_, coupon_egg_brand = coupon_egg_brand_, coupon_egg_unit = coupon_egg_unit_, coupon_egg_area=coupon_egg_area_, coupon_egg_price = coupon_egg_price_, coupon_egg_start = coupon_egg_start_, coupon_egg_finish = coupon_egg_finish_, coupon_egg_times = coupon_egg_times_, coupon_egg_detail = coupon_egg_detail_, coupon_egg_type = coupon_egg_type_,)
	coupon_egg.save()

	coupon_ = COUPON_EGG.objects.get(coupon_egg_name=coupon_egg_name_)
	coupon_egg_index_ = coupon_.coupon_egg_index

	# have to change photo
	if coupon_egg_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_egg' + '_' + str(coupon_egg_product_index_ )+ '_' + str(coupon_egg_index_) + '_' + coupon_egg_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_egg_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_egg_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_egg_product_index_)
		coupon_egg_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_egg_photo_index = coupon_egg_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_ham(request):
	page_title = 'request_make_ham'
	# /request/make/ham/?coupon_ham_product_index=0&coupon_ham_photo_index=1&coupon_ham_market_name=nabak&coupon_ham_name=milk&coupon_ham_brand=pul&coupon_ham_unit=0&coupon_ham_pham=100&coupon_ham_start=0&coupon_ham_finish=0&coupon_ham_times=0&coupon_ham_detail=0&coupon_ham_type=0

	coupon_ham_product_index_ = request.POST.get('coupon_ham_product_index')
	# not change: 0 / change: 1
	coupon_ham_photo_index_ = request.POST.get('coupon_ham_photo_index')
	coupon_ham_market_name_ =  request.POST.get('coupon_ham_market_name')
	coupon_ham_name_ = request.POST.get('coupon_ham_name')
	coupon_ham_brand_ = request.POST.get('coupon_ham_brand')
	coupon_ham_unit_ = request.POST.get('coupon_ham_unit')
	coupon_ham_price_ = request.POST.get('coupon_ham_price')
	coupon_ham_start_ = request.POST.get('coupon_ham_start')
	coupon_ham_finish_ = request.POST.get('coupon_ham_finish')
	coupon_ham_times_ = request.POST.get('coupon_ham_times')
	coupon_ham_detail_ = request.POST.get('coupon_ham_detail')
	coupon_ham_type_ = request.POST.get('coupon_ham_type')

	# make coupon
	coupon_ham = COUPON_HAM(coupon_ham_product_index = coupon_ham_product_index_, coupon_ham_photo_index = coupon_ham_photo_index_, coupon_ham_market_name = coupon_ham_market_name_, coupon_ham_name = coupon_ham_name_, coupon_ham_brand = coupon_ham_brand_, coupon_ham_unit = coupon_ham_unit_, coupon_ham_price = coupon_ham_price_, coupon_ham_start = coupon_ham_start_, coupon_ham_finish = coupon_ham_finish_, coupon_ham_times = coupon_ham_times_, coupon_ham_detail = coupon_ham_detail_, coupon_ham_type = coupon_ham_type_,)
	coupon_ham.save()

	coupon_ = COUPON_HAM.objects.get(coupon_ham_name=coupon_ham_name_)
	coupon_ham_index_ = coupon_.coupon_ham_index

	# have to change photo
	if coupon_ham_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_ham' + '_' + str(coupon_ham_product_index_ )+ '_' + str(coupon_ham_index_) + '_' + coupon_ham_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_ham_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_ham_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_ham_product_index_)
		coupon_ham_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_ham_photo_index = coupon_ham_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


	make_data_= COUPON_HAM.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_side(request):
	page_title = 'request_make_side'
	# /request/make/side/?coupon_side_product_index=0&coupon_side_photo_index=1&coupon_side_market_name=nabak&coupon_side_name=milk&coupon_side_brand=pul&coupon_side_unit=0&coupon_side_pside=100&coupon_side_start=0&coupon_side_finish=0&coupon_side_times=0&coupon_side_detail=0&coupon_side_type=0

	coupon_side_product_index_ = request.POST.get('coupon_side_product_index')
	# not change: 0 / change: 1
	coupon_side_photo_index_ = request.POST.get('coupon_side_photo_index')
	coupon_side_market_name_ =  request.POST.get('coupon_side_market_name')
	coupon_side_name_ = request.POST.get('coupon_side_name')
	coupon_side_brand_ = request.POST.get('coupon_side_brand')
	coupon_side_unit_ = request.POST.get('coupon_side_unit')
	coupon_side_price_ = request.POST.get('coupon_side_price')
	coupon_side_start_ = request.POST.get('coupon_side_start')
	coupon_side_finish_ = request.POST.get('coupon_side_finish')
	coupon_side_times_ = request.POST.get('coupon_side_times')
	coupon_side_type_ = request.POST.get('coupon_side_type')

	# make coupon
	coupon_side = COUPON_SIDE(coupon_side_product_index = coupon_side_product_index_, coupon_side_photo_index = coupon_side_photo_index_, coupon_side_market_name = coupon_side_market_name_, coupon_side_name = coupon_side_name_, coupon_side_brand = coupon_side_brand_, coupon_side_unit = coupon_side_unit_, coupon_side_price = coupon_side_price_, coupon_side_start = coupon_side_start_, coupon_side_finish = coupon_side_finish_, coupon_side_times = coupon_side_times_, coupon_side_type = coupon_side_type_,)
	coupon_side.save()

	coupon_ = COUPON_SIDE.objects.get(coupon_side_name=coupon_side_name_)
	coupon_side_index_ = coupon_.coupon_side_index

	# have to change photo
	if coupon_side_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_side' + '_' + str(coupon_side_product_index_ )+ '_' + str(coupon_side_index_) + '_' + coupon_side_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_side_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_side_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_side_product_index_)
		coupon_side_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_side_photo_index = coupon_side_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_water(request):
	page_title = 'request_make_water'
	# /request/make/water/?coupon_water_product_index=0&coupon_water_photo_index=1&coupon_water_market_name=nabak&coupon_water_name=milk&coupon_water_brand=pul&coupon_water_unit=0&coupon_water_pwater=100&coupon_water_start=0&coupon_water_finish=0&coupon_water_times=0&coupon_water_detail=0&coupon_water_type=0

	coupon_water_product_index_ = request.POST.get('coupon_water_product_index')
	# not change: 0 / change: 1
	coupon_water_photo_index_ = request.POST.get('coupon_water_photo_index')
	coupon_water_market_name_ =  request.POST.get('coupon_water_market_name')
	coupon_water_name_ = request.POST.get('coupon_water_name')
	coupon_water_brand_ = request.POST.get('coupon_water_brand')
	coupon_water_unit_ = request.POST.get('coupon_water_unit')
	coupon_water_price_ = request.POST.get('coupon_water_price')
	coupon_water_start_ = request.POST.get('coupon_water_start')
	coupon_water_finish_ = request.POST.get('coupon_water_finish')
	coupon_water_times_ = request.POST.get('coupon_water_times')
	coupon_water_detail_ = request.POST.get('coupon_water_detail')
	coupon_water_type_ = request.POST.get('coupon_water_type')

	# make coupon
	coupon_water = COUPON_WATER(coupon_water_product_index = coupon_water_product_index_, coupon_water_photo_index = coupon_water_photo_index_, coupon_water_market_name = coupon_water_market_name_, coupon_water_name = coupon_water_name_, coupon_water_brand = coupon_water_brand_, coupon_water_unit = coupon_water_unit_, coupon_water_price = coupon_water_price_, coupon_water_start = coupon_water_start_, coupon_water_finish = coupon_water_finish_, coupon_water_times = coupon_water_times_, coupon_water_detail = coupon_water_detail_, coupon_water_type = coupon_water_type_,)
	coupon_water.save()

	coupon_ = COUPON_WATER.objects.get(coupon_water_name=coupon_water_name_)
	coupon_water_index_ = coupon_.coupon_water_index

	# have to change photo
	if coupon_water_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_water' + '_' + str(coupon_water_product_index_ )+ '_' + str(coupon_water_index_) + '_' + coupon_water_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_water_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_water_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_water_product_index_)
		coupon_water_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_water_photo_index = coupon_water_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_instant(request):
	page_title = 'request_make_instant'
	# /request/make/instant/?coupon_instant_product_index=0&coupon_instant_photo_index=1&coupon_instant_market_name=nabak&coupon_instant_name=milk&coupon_instant_brand=pul&coupon_instant_unit=0&coupon_instant_pinstant=100&coupon_instant_start=0&coupon_instant_finish=0&coupon_instant_times=0&coupon_instant_detail=0&coupon_instant_type=0

	coupon_instant_product_index_ = request.POST.get('coupon_instant_product_index')
	# not change: 0 / change: 1
	coupon_instant_photo_index_ = request.POST.get('coupon_instant_photo_index')
	coupon_instant_market_name_ =  request.POST.get('coupon_instant_market_name')
	coupon_instant_name_ = request.POST.get('coupon_instant_name')
	coupon_instant_brand_ = request.POST.get('coupon_instant_brand')
	coupon_instant_unit_ = request.POST.get('coupon_instant_unit')
	coupon_instant_price_ = request.POST.get('coupon_instant_price')
	coupon_instant_start_ = request.POST.get('coupon_instant_start')
	coupon_instant_finish_ = request.POST.get('coupon_instant_finish')
	coupon_instant_times_ = request.POST.get('coupon_instant_times')
	coupon_instant_detail_ = request.POST.get('coupon_instant_detail')
	coupon_instant_type_ = request.POST.get('coupon_instant_type')

	# make coupon
	coupon_instant = COUPON_INSTANT(coupon_instant_product_index = coupon_instant_product_index_, coupon_instant_photo_index = coupon_instant_photo_index_, coupon_instant_market_name = coupon_instant_market_name_, coupon_instant_name = coupon_instant_name_, coupon_instant_brand = coupon_instant_brand_, coupon_instant_unit = coupon_instant_unit_, coupon_instant_price = coupon_instant_price_, coupon_instant_start = coupon_instant_start_, coupon_instant_finish = coupon_instant_finish_, coupon_instant_times = coupon_instant_times_, coupon_instant_detail = coupon_instant_detail_, coupon_instant_type = coupon_instant_type_,)
	coupon_instant.save()

	coupon_ = COUPON_INSTANT.objects.get(coupon_instant_name=coupon_instant_name_)
	coupon_instant_index_ = coupon_.coupon_instant_index

	# have to change photo
	if coupon_instant_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_instant' + '_' + str(coupon_instant_product_index_ )+ '_' + str(coupon_instant_index_) + '_' + coupon_instant_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_instant_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_instant_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_instant_product_index_)
		coupon_instant_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_instant_photo_index = coupon_instant_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_ice(request):
	page_title = 'request_make_ice'
	# /request/make/ice/?coupon_ice_product_index=0&coupon_ice_photo_index=1&coupon_ice_market_name=nabak&coupon_ice_name=milk&coupon_ice_brand=pul&coupon_ice_unit=0&coupon_ice_pice=100&coupon_ice_start=0&coupon_ice_finish=0&coupon_ice_times=0&coupon_ice_detail=0&coupon_ice_type=0

	coupon_ice_product_index_ = request.POST.get('coupon_ice_product_index')
	# not change: 0 / change: 1
	coupon_ice_photo_index_ = request.POST.get('coupon_ice_photo_index')
	coupon_ice_market_name_ =  request.POST.get('coupon_ice_market_name')
	coupon_ice_name_ = request.POST.get('coupon_ice_name')
	coupon_ice_brand_ = request.POST.get('coupon_ice_brand')
	coupon_ice_unit_ = request.POST.get('coupon_ice_unit')
	coupon_ice_price_ = request.POST.get('coupon_ice_price')
	coupon_ice_start_ = request.POST.get('coupon_ice_start')
	coupon_ice_finish_ = request.POST.get('coupon_ice_finish')
	coupon_ice_times_ = request.POST.get('coupon_ice_times')
	coupon_ice_detail_ = request.POST.get('coupon_ice_detail')
	coupon_ice_type_ = request.POST.get('coupon_ice_type')

	# make coupon
	coupon_ice = COUPON_ICE(coupon_ice_product_index = coupon_ice_product_index_, coupon_ice_photo_index = coupon_ice_photo_index_, coupon_ice_market_name = coupon_ice_market_name_, coupon_ice_name = coupon_ice_name_, coupon_ice_brand = coupon_ice_brand_, coupon_ice_unit = coupon_ice_unit_, coupon_ice_price = coupon_ice_price_, coupon_ice_start = coupon_ice_start_, coupon_ice_finish = coupon_ice_finish_, coupon_ice_times = coupon_ice_times_, coupon_ice_detail = coupon_ice_detail_, coupon_ice_type = coupon_ice_type_,)
	coupon_ice.save()

	coupon_ = COUPON_ICE.objects.get(coupon_ice_name=coupon_ice_name_)
	coupon_ice_index_ = coupon_.coupon_ice_index

	# have to change photo
	if coupon_ice_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_ice' + '_' + str(coupon_ice_product_index_ )+ '_' + str(coupon_ice_index_) + '_' + coupon_ice_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_ice_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_ice_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_ice_product_index_)
		coupon_ice_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_ice_photo_index = coupon_ice_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_bakery(request):
	page_title = 'request_make_bakery'
	# /request/make/bakery/?coupon_bakery_product_index=0&coupon_bakery_photo_index=1&coupon_bakery_market_name=nabak&coupon_bakery_name=milk&coupon_bakery_brand=pul&coupon_bakery_unit=0&coupon_bakery_pbakery=100&coupon_bakery_start=0&coupon_bakery_finish=0&coupon_bakery_times=0&coupon_bakery_detail=0&coupon_bakery_type=0

	coupon_bakery_product_index_ = request.POST.get('coupon_bakery_product_index')
	# not change: 0 / change: 1
	coupon_bakery_photo_index_ = request.POST.get('coupon_bakery_photo_index')
	coupon_bakery_market_name_ =  request.POST.get('coupon_bakery_market_name')
	coupon_bakery_name_ = request.POST.get('coupon_bakery_name')
	coupon_bakery_brand_ = request.POST.get('coupon_bakery_brand')
	coupon_bakery_unit_ = request.POST.get('coupon_bakery_unit')
	coupon_bakery_prbakery_ = request.POST.get('coupon_bakery_prbakery')
	coupon_bakery_start_ = request.POST.get('coupon_bakery_start')
	coupon_bakery_finish_ = request.POST.get('coupon_bakery_finish')
	coupon_bakery_times_ = request.POST.get('coupon_bakery_times')
	coupon_bakery_detail_ = request.POST.get('coupon_bakery_detail')
	coupon_bakery_type_ = request.POST.get('coupon_bakery_type')

	# make coupon
	coupon_bakery = COUPON_BAKERY(coupon_bakery_product_index = coupon_bakery_product_index_, coupon_bakery_photo_index = coupon_bakery_photo_index_, coupon_bakery_market_name = coupon_bakery_market_name_, coupon_bakery_name = coupon_bakery_name_, coupon_bakery_brand = coupon_bakery_brand_, coupon_bakery_unit = coupon_bakery_unit_, coupon_bakery_prbakery = coupon_bakery_prbakery_, coupon_bakery_start = coupon_bakery_start_, coupon_bakery_finish = coupon_bakery_finish_, coupon_bakery_times = coupon_bakery_times_, coupon_bakery_detail = coupon_bakery_detail_, coupon_bakery_type = coupon_bakery_type_,)
	coupon_bakery.save()

	coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_name=coupon_bakery_name_)
	coupon_bakery_index_ = coupon_.coupon_bakery_index

	# have to change photo
	if coupon_bakery_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_bakery' + '_' + str(coupon_bakery_product_index_ )+ '_' + str(coupon_bakery_index_) + '_' + coupon_bakery_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_bakery_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_bakery_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_bakery_product_index_)
		coupon_bakery_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_bakery_photo_index = coupon_bakery_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


def request_make_snack(request):
	page_title = 'request_make_snack'
	# /request/make/snack/?coupon_snack_product_index=0&coupon_snack_photo_index=1&coupon_snack_market_name=nabak&coupon_snack_name=milk&coupon_snack_brand=pul&coupon_snack_unit=0&coupon_snack_psnack=100&coupon_snack_start=0&coupon_snack_finish=0&coupon_snack_times=0&coupon_snack_detail=0&coupon_snack_type=0

	coupon_snack_product_index_ = request.POST.get('coupon_snack_product_index')
	# not change: 0 / change: 1
	coupon_snack_photo_index_ = request.POST.get('coupon_snack_photo_index')
	coupon_snack_market_name_ =  request.POST.get('coupon_snack_market_name')
	coupon_snack_name_ = request.POST.get('coupon_snack_name')
	coupon_snack_brand_ = request.POST.get('coupon_snack_brand')
	coupon_snack_unit_ = request.POST.get('coupon_snack_unit')
	coupon_snack_prsnack_ = request.POST.get('coupon_snack_prsnack')
	coupon_snack_start_ = request.POST.get('coupon_snack_start')
	coupon_snack_finish_ = request.POST.get('coupon_snack_finish')
	coupon_snack_times_ = request.POST.get('coupon_snack_times')
	coupon_snack_type_ = request.POST.get('coupon_snack_type')

	# make coupon
	coupon_snack = COUPON_SNACK(coupon_snack_product_index = coupon_snack_product_index_, coupon_snack_photo_index = coupon_snack_photo_index_, coupon_snack_market_name = coupon_snack_market_name_, coupon_snack_name = coupon_snack_name_, coupon_snack_brand = coupon_snack_brand_, coupon_snack_unit = coupon_snack_unit_, coupon_snack_prsnack = coupon_snack_prsnack_, coupon_snack_start = coupon_snack_start_, coupon_snack_finish = coupon_snack_finish_, coupon_snack_times = coupon_snack_times_, coupon_snack_type = coupon_snack_type_,)
	coupon_snack.save()

	coupon_ = COUPON_SNACK.objects.get(coupon_snack_name=coupon_snack_name_)
	coupon_snack_index_ = coupon_.coupon_snack_index

	# have to change photo
	if coupon_snack_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_snack' + '_' + str(coupon_snack_product_index_ )+ '_' + str(coupon_snack_index_) + '_' + coupon_snack_name_

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.jpg', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps(1)
					return HttpResponse(json_data, content_type='application/json')	
				pic_.save()

				# get make photo index
				pic_now = SP_PICTURE.objects.get(sp_name=filename)
				coupon_snack_photo_index_ = pic_now.sp_photo_index
	# dont have to change photo
	elif coupon_snack_photo_index_ == '0':
		# get default photo index
		product_ = PRODUCT.objects.get(product_index=coupon_snack_product_index_)
		coupon_snack_photo_index_ = product_.product_photo_index	

	# swich coupon photo index
	coupon_.coupon_snack_photo_index = coupon_snack_photo_index_
	coupon_.save()

	# code0 : success
	json_data = json.dumps(0)
	return HttpResponse(json_data, content_type='application/json')


# controll coupon-----------------------------------------------------
# get coupones by state-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_active_coupon(request):
	page_title = 'request_active_coupon'

	datas = []

	active_coupon_p_ = PRODUCT.objects.filter(product_coupon_active=1)
	for d in active_coupon_p_:
		data = model_to_dict(d)
		datas.append(data)

	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_d_ = COUPON_DAILY.objects.filter(coupon_daily_name=product_name_)
		for d_d in active_coupon_d_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_g_ = COUPON_GREENS.objects.filter(coupon_greens_name=product_name_)
		for d_d in active_coupon_g_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_f_ = COUPON_FISH.objects.filter(coupon_fish_name=product_name_)
		for d_d in active_coupon_f_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_r_ = COUPON_RICE.objects.filter(coupon_rice_name=product_name_)
		for d_d in active_coupon_r_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_m_ = COUPON_MEAT.objects.filter(coupon_meat_name=product_name_)
		for d_d in active_coupon_m_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_e_ = COUPON_EGG.objects.filter(coupon_egg_name=product_name_)
		for d_d in active_coupon_e_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_h_ = COUPON_HAM.objects.filter(coupon_ham_name=product_name_)
		for d_d in active_coupon_h_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_s_ = COUPON_SIDE.objects.filter(coupon_side_name=product_name_)
		for d_d in active_coupon_s_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_w_ = COUPON_WATER.objects.filter(coupon_water_name=product_name_)
		for d_d in active_coupon_w_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_i_ = COUPON_INSTANT.objects.filter(coupon_instant_name=product_name_)
		for d_d in active_coupon_i_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_ice_ = COUPON_ICE.objects.filter(coupon_ice_name=product_name_)
		for d_d in active_coupon_ice_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_b_ = COUPON_BAKERY.objects.filter(coupon_bakery_name=product_name_)
		for d_d in active_coupon_b_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_s_ = COUPON_SNACK.objects.filter(coupon_snack_name=product_name_)
		for d_d in active_coupon_s_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

#-------------------------------------------------------------------------------------------------------------------------
def request_reservation_coupon(request):
	page_title = 'request_reservation_coupon'

	datas = []

	active_coupon_p_ = PRODUCT.objects.filter(product_coupon_active=2)
	for d in active_coupon_p_:
		data = model_to_dict(d)
		datas.append(data)

	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_d_ = COUPON_DAILY.objects.filter(coupon_daily_name=product_name_)
		for d_d in active_coupon_d_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_g_ = COUPON_GREENS.objects.filter(coupon_greens_name=product_name_)
		for d_d in active_coupon_g_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_f_ = COUPON_FISH.objects.filter(coupon_fish_name=product_name_)
		for d_d in active_coupon_f_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_r_ = COUPON_RICE.objects.filter(coupon_rice_name=product_name_)
		for d_d in active_coupon_r_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_m_ = COUPON_MEAT.objects.filter(coupon_meat_name=product_name_)
		for d_d in active_coupon_m_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_e_ = COUPON_EGG.objects.filter(coupon_egg_name=product_name_)
		for d_d in active_coupon_e_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_h_ = COUPON_HAM.objects.filter(coupon_ham_name=product_name_)
		for d_d in active_coupon_h_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_s_ = COUPON_SIDE.objects.filter(coupon_side_name=product_name_)
		for d_d in active_coupon_s_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_w_ = COUPON_WATER.objects.filter(coupon_water_name=product_name_)
		for d_d in active_coupon_w_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_i_ = COUPON_INSTANT.objects.filter(coupon_instant_name=product_name_)
		for d_d in active_coupon_i_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_ice_ = COUPON_ICE.objects.filter(coupon_ice_name=product_name_)
		for d_d in active_coupon_ice_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_b_ = COUPON_BAKERY.objects.filter(coupon_bakery_name=product_name_)
		for d_d in active_coupon_b_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_s_ = COUPON_SNACK.objects.filter(coupon_snack_name=product_name_)
		for d_d in active_coupon_s_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

#-------------------------------------------------------------------------------------------------------------------------
def request_inactive_coupon(request):
	page_title = 'request_inactive_coupon'

	datas = []

	active_coupon_p_ = PRODUCT.objects.filter(product_coupon_active=0)
	for d in active_coupon_p_:
		data = model_to_dict(d)
		datas.append(data)

	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_d_ = COUPON_DAILY.objects.filter(coupon_daily_name=product_name_)
		for d_d in active_coupon_d_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_g_ = COUPON_GREENS.objects.filter(coupon_greens_name=product_name_)
		for d_d in active_coupon_g_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_f_ = COUPON_FISH.objects.filter(coupon_fish_name=product_name_)
		for d_d in active_coupon_f_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_r_ = COUPON_RICE.objects.filter(coupon_rice_name=product_name_)
		for d_d in active_coupon_r_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_m_ = COUPON_MEAT.objects.filter(coupon_meat_name=product_name_)
		for d_d in active_coupon_m_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_e_ = COUPON_EGG.objects.filter(coupon_egg_name=product_name_)
		for d_d in active_coupon_e_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_h_ = COUPON_HAM.objects.filter(coupon_ham_name=product_name_)
		for d_d in active_coupon_h_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_s_ = COUPON_SIDE.objects.filter(coupon_side_name=product_name_)
		for d_d in active_coupon_s_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_w_ = COUPON_WATER.objects.filter(coupon_water_name=product_name_)
		for d_d in active_coupon_w_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_i_ = COUPON_INSTANT.objects.filter(coupon_instant_name=product_name_)
		for d_d in active_coupon_i_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_ice_ = COUPON_ICE.objects.filter(coupon_ice_name=product_name_)
		for d_d in active_coupon_ice_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_b_ = COUPON_BAKERY.objects.filter(coupon_bakery_name=product_name_)
		for d_d in active_coupon_b_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)
	for d in active_coupon_p_:
		product_name_ = d.product_name
		active_coupon_s_ = COUPON_SNACK.objects.filter(coupon_snack_name=product_name_)
		for d_d in active_coupon_s_:
			data_d = model_to_dict(d_d)
			datas.append(data_d)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

#-------------------------------------------------------------------------------------------------------------------------
def request_delete_coupon(request):
	page_title = 'request_delete_coupon'

	delete_coupon_category_ = request.GET.get('delete_coupon_category')
	delete_coupon_index_ = request.GET.get('delete_coupon_index')

	if delete_coupon_category_ == '1':
		delete_coupon_category = 'daily'
		delete_coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=delete_coupon_index_)
		delete_coupon_.coupon_daily_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '2':
		delete_coupon_category = 'greens'
		delete_coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=delete_coupon_index_)
		delete_coupon_.coupon_greens_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '3':
		delete_coupon_category = 'fish'
		delete_coupon_ = COUPON_FISH.objects.get(coupon_fish_index=delete_coupon_index_)
		delete_coupon_.coupon_fish_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '4':
		delete_coupon_category = 'rice'
		delete_coupon_ = COUPON_RICE.objects.get(coupon_rice_index=delete_coupon_index_)
		delete_coupon_.coupon_rice_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '5':
		delete_coupon_category = 'meat'
		delete_coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=delete_coupon_index_)
		delete_coupon_.coupon_meat_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '6':
		delete_coupon_category = 'egg'
		delete_coupon_ = COUPON_EGG.objects.get(coupon_egg_index=delete_coupon_index_)
		delete_coupon_.coupon_egg_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '7':
		delete_coupon_category = 'ham'
		delete_coupon_ = COUPON_HAM.objects.get(coupon_ham_index=delete_coupon_index_)
		delete_coupon_.coupon_ham_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '8':
		delete_coupon_category = 'side'
		delete_coupon_ = COUPON_SIDE.objects.get(coupon_side_index=delete_coupon_index_)
		delete_coupon_.coupon_side_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '9':
		delete_coupon_category = 'water'
		delete_coupon_ = COUPON_WATER.objects.get(coupon_water_index=delete_coupon_index_)
		delete_coupon_.coupon_water_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '10':
		delete_coupon_category = 'instant'
		delete_coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=delete_coupon_index_)
		delete_coupon_.coupon_instant_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '11':
		delete_coupon_category = 'ice'
		delete_coupon_ = COUPON_ICE.objects.get(coupon_ice_index=delete_coupon_index_)
		delete_coupon_.coupon_ice_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '12':
		delete_coupon_category = 'bakery'
		delete_coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=delete_coupon_index_)
		delete_coupon_.coupon_bakery_active = 0
		delete_coupon_.delete()

	elif delete_coupon_category_ == '13':
		delete_coupon_category = 'snack'
		delete_coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=delete_coupon_index_)
		delete_coupon_.coupon_snack_active = 0
		delete_coupon_.delete()

	# give again coupon data
	datas = []

	coupon_data_= COUPON_DAILY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_GREENS.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_FISH.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_RICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_MEAT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_EGG.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_HAM.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SIDE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_WATER.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_INSTANT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_ICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_BAKERY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SNACK.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# chanage coupones state-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_inactive_change(request):
	page_title = 'request_inactive_change'

	inactive_coupon_category_ = request.GET.get('inactive_coupon_category')
	inactive_coupon_index_ = request.GET.get('inactive_coupon_index')

	if inactive_coupon_category_ == '1':
		inactive_coupon_category = 'daily'
		inactive_coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=inactive_coupon_index_)
		inactive_coupon_.coupon_daily_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '2':
		inactive_coupon_category = 'greens'
		inactive_coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=inactive_coupon_index_)
		inactive_coupon_.coupon_greens_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '3':
		inactive_coupon_category = 'fish'
		inactive_coupon_ = COUPON_FISH.objects.get(coupon_fish_index=inactive_coupon_index_)
		inactive_coupon_.coupon_fish_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '4':
		inactive_coupon_category = 'rice'
		inactive_coupon_ = COUPON_RICE.objects.get(coupon_rice_index=inactive_coupon_index_)
		inactive_coupon_.coupon_rice_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '5':
		inactive_coupon_category = 'meat'
		inactive_coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=inactive_coupon_index_)
		inactive_coupon_.coupon_meat_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '6':
		inactive_coupon_category = 'egg'
		inactive_coupon_ = COUPON_EGG.objects.get(coupon_egg_index=inactive_coupon_index_)
		inactive_coupon_.coupon_egg_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '7':
		inactive_coupon_category = 'ham'
		inactive_coupon_ = COUPON_HAM.objects.get(coupon_ham_index=inactive_coupon_index_)
		inactive_coupon_.coupon_ham_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '8':
		inactive_coupon_category = 'side'
		inactive_coupon_ = COUPON_SIDE.objects.get(coupon_side_index=inactive_coupon_index_)
		inactive_coupon_.coupon_side_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '9':
		inactive_coupon_category = 'water'
		inactive_coupon_ = COUPON_WATER.objects.get(coupon_water_index=inactive_coupon_index_)
		inactive_coupon_.coupon_water_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '10':
		inactive_coupon_category = 'instant'
		inactive_coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=inactive_coupon_index_)
		inactive_coupon_.coupon_instant_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '11':
		inactive_coupon_category = 'ice'
		inactive_coupon_ = COUPON_ICE.objects.get(coupon_ice_index=inactive_coupon_index_)
		inactive_coupon_.coupon_ice_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '12':
		inactive_coupon_category = 'bakery'
		inactive_coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=inactive_coupon_index_)
		inactive_coupon_.coupon_bakery_active = 0
		inactive_coupon_.save()

	elif inactive_coupon_category_ == '13':
		inactive_coupon_category = 'snack'
		inactive_coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=inactive_coupon_index_)
		inactive_coupon_.coupon_snack_active = 0
		inactive_coupon_.save()

	# give again coupon data
	datas = []

	coupon_data_= COUPON_DAILY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_GREENS.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_FISH.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_RICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_MEAT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_EGG.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_HAM.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SIDE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_WATER.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_INSTANT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_ICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_BAKERY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SNACK.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')
	
#-------------------------------------------------------------------------------------------------------------------------
def request_active_change(request):
	page_title = 'request_active_change'

	active_coupon_category_ = request.GET.get('active_coupon_category')
	active_coupon_index_ = request.GET.get('active_coupon_index')

	if active_coupon_category_ == '1':
		active_coupon_category = 'daily'
		active_coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=active_coupon_index_)
		active_coupon_.coupon_daily_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '2':
		active_coupon_category = 'greens'
		active_coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=active_coupon_index_)
		active_coupon_.coupon_greens_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '3':
		active_coupon_category = 'fish'
		active_coupon_ = COUPON_FISH.objects.get(coupon_fish_index=active_coupon_index_)
		active_coupon_.coupon_fish_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '4':
		active_coupon_category = 'rice'
		active_coupon_ = COUPON_RICE.objects.get(coupon_rice_index=active_coupon_index_)
		active_coupon_.coupon_rice_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '5':
		active_coupon_category = 'meat'
		active_coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=active_coupon_index_)
		active_coupon_.coupon_meat_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '6':
		active_coupon_category = 'egg'
		active_coupon_ = COUPON_EGG.objects.get(coupon_egg_index=active_coupon_index_)
		active_coupon_.coupon_egg_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '7':
		active_coupon_category = 'ham'
		active_coupon_ = COUPON_HAM.objects.get(coupon_ham_index=active_coupon_index_)
		active_coupon_.coupon_ham_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '8':
		active_coupon_category = 'side'
		active_coupon_ = COUPON_SIDE.objects.get(coupon_side_index=active_coupon_index_)
		active_coupon_.coupon_side_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '9':
		active_coupon_category = 'water'
		active_coupon_ = COUPON_WATER.objects.get(coupon_water_index=active_coupon_index_)
		active_coupon_.coupon_water_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '10':
		active_coupon_category = 'instant'
		active_coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=active_coupon_index_)
		active_coupon_.coupon_instant_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '11':
		active_coupon_category = 'ice'
		active_coupon_ = COUPON_ICE.objects.get(coupon_ice_index=active_coupon_index_)
		active_coupon_.coupon_ice_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '12':
		active_coupon_category = 'bakery'
		active_coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=active_coupon_index_)
		active_coupon_.coupon_bakery_active = 1
		active_coupon_.save()

	elif active_coupon_category_ == '13':
		active_coupon_category = 'snack'
		active_coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=active_coupon_index_)
		active_coupon_.coupon_snack_active = 1
		active_coupon_.save()

	# give again coupon data
	datas = []

	coupon_data_= COUPON_DAILY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_GREENS.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_FISH.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_RICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_MEAT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_EGG.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_HAM.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SIDE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_WATER.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_INSTANT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_ICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_BAKERY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SNACK.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

#-------------------------------------------------------------------------------------------------------------------------
def request_reservation_change(request):
	page_title = 'request_reservation_change'

	reservation_coupon_category_ = request.GET.get('reservation_coupon_category')
	reservation_coupon_index_ = request.GET.get('reservation_coupon_index')

	if reservation_coupon_category_ == '1':
		reservation_coupon_category = 'daily'
		reservation_coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=reservation_coupon_index_)
		reservation_coupon_.coupon_daily_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '2':
		reservation_coupon_category = 'greens'
		reservation_coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=reservation_coupon_index_)
		reservation_coupon_.coupon_greens_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '3':
		reservation_coupon_category = 'fish'
		reservation_coupon_ = COUPON_FISH.objects.get(coupon_fish_index=reservation_coupon_index_)
		reservation_coupon_.coupon_fish_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '4':
		reservation_coupon_category = 'rice'
		reservation_coupon_ = COUPON_RICE.objects.get(coupon_rice_index=reservation_coupon_index_)
		reservation_coupon_.coupon_rice_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '5':
		reservation_coupon_category = 'meat'
		reservation_coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=reservation_coupon_index_)
		reservation_coupon_.coupon_meat_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '6':
		reservation_coupon_category = 'egg'
		reservation_coupon_ = COUPON_EGG.objects.get(coupon_egg_index=reservation_coupon_index_)
		reservation_coupon_.coupon_egg_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '7':
		reservation_coupon_category = 'ham'
		reservation_coupon_ = COUPON_HAM.objects.get(coupon_ham_index=reservation_coupon_index_)
		reservation_coupon_.coupon_ham_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '8':
		reservation_coupon_category = 'side'
		reservation_coupon_ = COUPON_SIDE.objects.get(coupon_side_index=reservation_coupon_index_)
		reservation_coupon_.coupon_side_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '9':
		reservation_coupon_category = 'water'
		reservation_coupon_ = COUPON_WATER.objects.get(coupon_water_index=reservation_coupon_index_)
		reservation_coupon_.coupon_water_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '10':
		reservation_coupon_category = 'instant'
		reservation_coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=reservation_coupon_index_)
		reservation_coupon_.coupon_instant_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '11':
		reservation_coupon_category = 'ice'
		reservation_coupon_ = COUPON_ICE.objects.get(coupon_ice_index=reservation_coupon_index_)
		reservation_coupon_.coupon_ice_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '12':
		reservation_coupon_category = 'bakery'
		reservation_coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=reservation_coupon_index_)
		reservation_coupon_.coupon_bakery_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '13':
		reservation_coupon_category = 'snack'
		reservation_coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=reservation_coupon_index_)
		reservation_coupon_.coupon_snack_active = 0
		reservation_coupon_.save()

	# give again coupon data
	datas = []

	coupon_data_= COUPON_DAILY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_GREENS.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_FISH.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_RICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_MEAT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_EGG.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_HAM.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SIDE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_WATER.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_INSTANT.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_ICE.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_BAKERY.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SNACK.objects.all()
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# seller controll coupon *used*---------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_used_coupon(request):
	page_title = 'request_used_coupon'

	datas = []
	used_coupon_ = USER_COUPON_USEDLIST.objects.all()

	for d in used_coupon_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# controll favorite---------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_list_favorite(request):
	page_title = 'request_list_favorite'

	list_favorite_userid_ = request.GET.get('list_favorite_userid', False)

	datas = []
	list_favorite_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_)

	for d in list_favorite_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

def request_make_favorite(request):
	page_title = 'request_make_favorite'
	# /request/make/favorite/?list_favorite_userid=spotping&list_favorite_product_index=1&list_favorite_product_name=kimchi&list_favorite_product_brand=kk&list_favorite_product_unit=df&list_favorite_product_category=0

	list_favorite_userid_ = request.GET.get('list_favorite_userid', False)
	list_favorite_product_index_ = request.GET.get('list_favorite_product_index', False)
	list_favorite_product_name_ = request.GET.get('list_favorite_product_name', False)
	list_favorite_product_brand_ = request.GET.get('list_favorite_product_brand', False)
	list_favorite_product_unit_ = request.GET.get('list_favorite_product_unit', False)
	list_favorite_product_category_ = request.GET.get('list_favorite_product_category', False)

	favorite_product_ = USER_FAVORITE_LIST(user_favorite_list_userid=list_favorite_userid_, user_favorite_list_product_index=list_favorite_product_index_, user_favorite_list_product_name=list_favorite_product_name_, user_favorite_list_product_brand=list_favorite_product_brand_, user_favorite_list_product_unit=list_favorite_product_unit_, user_favorite_list_product_category=list_favorite_product_category_)
	
	try:
		favorite_product_.save()
	except:
		json_data = json.dumps('buyer have this product already')
		return HttpResponse(json_data, content_type='application/json')

	datas = []
	list_favorite_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_)

	for d in list_favorite_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

def request_remake_favorite(request):
	page_title = 'request_remake_favorite'
	# /request/remake/favorite/?list_favorite_userid=spotping&list_favorite_product_index_b=1&list_favorite_product_index_n=10&list_favorite_product_name=aaa&list_favorite_product_brand=kk&list_favorite_product_unit=df&list_favorite_product_category=0

	# have to get 'before product index', 'new product index'
	list_favorite_userid_ = request.GET.get('list_favorite_userid', False)
	list_favorite_product_index_b_ = request.GET.get('list_favorite_product_index_b', False)
	list_favorite_product_index_n_ = request.GET.get('list_favorite_product_index_n', False)
	list_favorite_product_name_ = request.GET.get('list_favorite_product_name', False)
	list_favorite_product_brand_ = request.GET.get('list_favorite_product_brand', False)
	list_favorite_product_unit_ = request.GET.get('list_favorite_product_unit', False)
	list_favorite_product_category_ = request.GET.get('list_favorite_product_category', False)

	favorite_product_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_).filter(user_favorite_list_product_index=1)

	# favorite_product_.user_favorite_list_product_index = list_favorite_product_index_n_
	# favorite_product_.user_favorite_list_product_name = list_favorite_product_name_
	# favorite_product_.user_favorite_list_product_brand = list_favorite_product_brand_
	# favorite_product_.user_favorite_list_product_unit = list_favorite_product_unit_
	# favorite_product_.user_favorite_list_product_category = list_favorite_product_category_

	favorite_product_.update()

	# try:
	# 	favorite_product_.save()
	# except:
	# 	json_data = json.dumps('fail update coupon')
	# 	return HttpResponse(json_data, content_type='application/json')

	datas = []
	list_favorite_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_)

	for d in list_favorite_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

def request_delete_favorite(request):
	page_title = 'request_delete_favorite'


	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# buyer join / login---------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def join_page_b(request):
	page_title = 'join_page_b'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('join_page_b.html', ctx)

@csrf_exempt
def request_join_buyer(request):
	callback = request.GET.get('callback')
	page_title = 'request_join_buyer'

	#id = username, firstname = name
	join_buyer_id_ = request.POST.get('join_buyer_id', False)
	join_buyer_pwd_ = request.POST.get('join_buyer_pwd', False)
	join_buyer_name_ = request.POST.get('join_buyer_name', False)
	join_buyer_email_ = request.POST.get('join_buyer_email', False)

	join_buyer_photo_index_ = 1
	join_buyer_address_ = request.POST.get('join_buyer_address', False)
	join_buyer_phone_ = request.POST.get('join_buyer_phone', False)

	join_buyer_ = User.objects.create_user(join_buyer_id_, join_buyer_email_, join_buyer_pwd_)
	join_buyer_.first_name = join_buyer_name_
	join_buyer_.is_staff = False

	try:
		join_buyer_.save()
		join_buyer_info_ = USER_BUYER(user_buyer_id=join_buyer_, user_buyer_photo_index=join_buyer_photo_index_, user_buyer_address=join_buyer_address_, user_buyer_phone=join_buyer_phone_)
		join_buyer_info_.save()
	except:
		return HttpResponse('fail join')

	return HttpResponse('success join, %s' % join_buyer_id_)

#-------------------------------------------------------------------------------------------------------------------------
def login_page_b(request):
	page_title = 'login_page_b'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('login_page_b.html', ctx)

@csrf_exempt
def request_login_buyer(request):
	callback = request.GET.get('callback')
	page_title = 'request_login_buyer'

	login_buyer_id_ = request.POST.get('buyer_id', False)
	login_buyer_pwd_ = request.POST.get('buyer_pwd', False)

	login_buyer_ = authenticate(username=login_buyer_id_, password=login_buyer_pwd_)

	if login_buyer_ is not None:
		if login_buyer_.is_active:
			login(request, login_buyer_)
		else:
			#disabled account
			return HttpResponse('disabled account')
	else:
		#invaild login
		return HttpResponse('invaild login %s, %s' %(login_buyer_id_, login_buyer_pwd_))

	#get userInfo
	user_buyer_ = User.objects.get(username=login_buyer_id_)
	user_buyer_info_ = USER_BUYER.objects.get(user_buyer_id=user_buyer_)

	#make session
	request.session['sess_buyer_id'] = user_buyer_.username

	datas = []
	datas.append(user_buyer_.id) 			#index
	datas.append(user_buyer_.username) 		#id
	datas.append(user_buyer_.first_name) 	#name
	datas.append(user_buyer_.email)
	datas.append(user_buyer_info_.user_buyer_photo_index)
	datas.append(user_buyer_info_.user_buyer_address)
	datas.append(user_buyer_info_.user_buyer_phone)

	json_data = json.dumps(datas, ensure_ascii=False)
	return HttpResponse(json_data, content_type='application/json')



