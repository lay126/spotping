# _*_ coding: utf-8 _*_

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


@csrf_exempt
def test_json_1(request):
	callback = request.GET.get('callback')
	page_title = 'test_json_1'

	id_ = request.GET.get('user_id', False)
	pwd_ = request.GET.get('user_pwd', False)

	request.session['s_id'] = id_

	# 데이터 저장
	dump_ = DUMP(dump_id=id_, dump_pwd=pwd_)
	dump_.save()

	return HttpResponse('id is : %s' % request.session['s_id'])


@csrf_exempt
def test_json_2(request):
	callback = request.GET.get('callback')

	product_index_ = 1
	product_ = PRODUCT.objects.all()

	datas = []
	for i in product_:
		data = model_to_dict(i)
		datas.append(data)

	json_data = json.dumps(datas, ensure_ascii=False)
	return HttpResponse(json_data, content_type='application/json')


def test_photo_open(request):
	page_title = 'test_photo_open'

	return render_to_response('imgForm.html')

# 안드로이드 -> 서버 
@csrf_exempt
def test_photo_upload(request):
	page_title = 'test_photo_upload'

	if request.method == 'POST':
		if 'file' in request.FILES:
			file = request.FILES['file']
			file_name_ = request.POST.get('file_name', 'False')
			file_day_ = request.POST.get('file_day', '00000')
			filename = file_name_ + '_' + file_day_

			pic_ = SP_PICTURE()
			pic_.sp_name = filename
			pic_.sp_picture.save(filename+'.jpg', File(file), save=True)
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



# 안드로이드 <- 서버 
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

# 안드로이드 <- 서버 (photos)
def test_photo_download_s(request):
	page_title = 'test_photo_download_s'

	image_data_1 = open("sp_app/sp_pictures/sp_pictures/mung_2.jpg", "rb").read()
	image_data_2 = open("sp_app/sp_pictures/sp_pictures/mung_1.jpg", "rb").read()

	images = []
	images.append(image_data_2)
	images.append(image_data_1)

	return HttpResponse(images, mimetype="image/png")

# 안드로이드 <- 서버 (base64)
def test_photo_download_2(request):
	page_title = 'test_photo_download_2'

	pic_1 = SP_PICTURE.objects.get(sp_name='mung_4')
	pic_2 = SP_PICTURE.objects.get(sp_name='mung_3')

	images = []
	images.append(pic_1.sp_picture)
	images.append(pic_2.sp_picture) 

	return HttpResponse(images, mimetype='image/png')


# seller join
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def join_page(request):
	page_title = 'join_page'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('join_page.html', ctx)

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

# 상인 로그인
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def login_page(request):
	page_title = 'login_page'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('login_page.html', ctx)

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


# 상인 사용하는 모든 데이터
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def request_allData_seller(request):
	page_title = 'request_allData_seller'

	return HttpResponse('this page is : %s' % (page_title))

def response_allData_seller(request):
	page_title = 'response_allData_seller'

	return HttpResponse('this page is : %s' % (page_title))


# 상인 쿠폰 관리
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def request_active_coupon(request):
	page_title = 'request_active_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_active_coupon(request):
	page_title = 'response_active_coupon'

	return HttpResponse('this page is : %s' % (page_title))

#----------------------------------------------------------------------------
def request_reservation_coupon(request):
	page_title = 'request_reservation_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_reservation_coupon(request):
	page_title = 'response_reservation_coupon'

	return HttpResponse('this page is : %s' % (page_title))

#----------------------------------------------------------------------------
def request_inactive_coupon(request):
	page_title = 'request_inactive_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_inactive_coupon(request):
	page_title = 'response_inactive_coupon'

	return HttpResponse('this page is : %s' % (page_title))


# 상인 쿠폰 사용 관리
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def request_stat_coupon(request):
	page_title = 'request_stat_coupon'

	return HttpResponse('this page is : %s' % (page_title))

def response_stat_coupon(request):
	page_title = 'response_stat_coupon'

	return HttpResponse('this page is : %s' % (page_title))




# 사용자 회원가입
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def request_join_buyer(request):
	page_title = 'request_join_buyer'

	return HttpResponse('this page is : %s' % (page_title))

def response_join_buyer(request):
	page_title = 'response_join_buyer'

	return HttpResponse('this page is : %s' % (page_title))


# 사용자 로그인
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def request_login_buyer(request):
	page_title = 'request_login_buyer'

	return HttpResponse('this page is : %s' % (page_title))

def response_login_buyer(request):
	page_title = 'response_login_buyer'

	return HttpResponse('this page is : %s' % (page_title))



