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
	join_seller_phone_ = request.POST.get('join_seller_phone', False)

	join_seller_ = User.objects.create_user(join_seller_id_, join_seller_email_, join_seller_pwd_)
	join_seller_.first_name = join_seller_name_
	join_seller_.is_staff = False

	try:
		join_seller_.save()
		join_seller_info_ = USER_SELLER(user_seller_id=join_seller_, user_seller_photo_index=join_seller_photo_index_, user_seller_market_name=join_seller_market_name_, user_seller_address=join_seller_address_, user_seller_phone=join_seller_phone_)
		join_seller_info_.save()
	except:
		return HttpResponse('fail join')

	return HttpResponse('success join, %s' % join_seller_id_)

def response_join_seller(request):
	page_title = 'response_join_seller'

	return HttpResponse('this page is : %s' % (page_title))

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


def response_login_seller(request):
	page_title = 'response_login_seller'

	return HttpResponse('this page is : %s' % (page_title))



# use by seller : all data---------------------------------------------------
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

def response_coupon_all(request):
	page_title = 'response_coupon_all'

	return HttpResponse('this page is : %s' % (page_title))


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

	make_data_= COUPON_MEAT.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_egg(request):
	page_title = 'request_make_egg'

	make_data_= COUPON_EGG.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_ham(request):
	page_title = 'request_make_ham'

	make_data_= COUPON_HAM.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_side(request):
	page_title = 'request_make_side'

	make_data_= COUPON_SIDE.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_water(request):
	page_title = 'request_make_water'

	make_data_= COUPON_WATER.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_instant(request):
	page_title = 'request_make_instant'

	make_data_= COUPON_INSTANT.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_ice(request):
	page_title = 'request_make_ice'

	make_data_= COUPON_ICE.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

def request_make_bakery(request):
	page_title = 'request_make_bakery'

	make_data_= COUPON_BAKERY.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


def request_make_snack(request):
	page_title = 'request_make_snack'

	make_data_= COUPON_SNACK.objects.all()

	datas = []
	for d in make_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')



# seller controll coupon-----------------------------------------------------
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

def response_active_coupon(request):
	page_title = 'response_active_coupon'

	return HttpResponse('this page is : %s' % (page_title))

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

def response_reservation_coupon(request):
	page_title = 'response_reservation_coupon'

	return HttpResponse('this page is : %s' % (page_title))

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

def response_inactive_coupon(request):
	page_title = 'response_inactive_coupon'

	return HttpResponse('this page is : %s' % (page_title))


# seller controll coupone *used*---------------------------------------------
def request_used_coupon(request):
	page_title = 'request_used_coupon'

	datas = []
	used_coupon_ = USER_COUPON_USEDLIST.objects.all()

	for d in used_coupon_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

def response_used_coupon(request):
	page_title = 'response_used_coupon'

	return HttpResponse('this page is : %s' % (page_title))


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


def response_join_buyer(request):
	page_title = 'response_join_buyer'

	return HttpResponse('this page is : %s' % (page_title))

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


def response_login_buyer(request):
	page_title = 'response_login_buyer'

	return HttpResponse('this page is : %s' % (page_title))


