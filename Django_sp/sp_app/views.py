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


def test_photo_open(request):
	page_title = 'test_photo_open'

	return render_to_response('imgForm.html')

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


# seller controll coupon-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def request_active_coupon(request):
	page_title = 'request_active_coupon'

	active_coupon_ = PRODUCT.objects.filter(product_coupon_active=1)

	datas = []
	for d in active_coupon_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

def response_active_coupon(request):
	page_title = 'response_active_coupon'

	return HttpResponse('this page is : %s' % (page_title))

#-------------------------------------------------------------------------------------------------------------------------
def request_reservation_coupon(request):
	page_title = 'request_reservation_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_reservation_coupon(request):
	page_title = 'response_reservation_coupon'

	return HttpResponse('this page is : %s' % (page_title))

#-------------------------------------------------------------------------------------------------------------------------
def request_inactive_coupon(request):
	page_title = 'request_inactive_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_inactive_coupon(request):
	page_title = 'response_inactive_coupon'

	return HttpResponse('this page is : %s' % (page_title))


# seller controll coupone *used*---------------------------------------------
def request_stat_coupon(request):
	page_title = 'request_stat_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_stat_coupon(request):
	page_title = 'response_stat_coupon'

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


