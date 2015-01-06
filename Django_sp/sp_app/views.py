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
from django.core.files.storage import default_storage
from django.contrib.sessions.models import Session

from django.contrib.auth import *
from django.contrib.auth.models import User, UserManager

from sp_app.models import *


"""
과일 : 1, 채소 : 2, 두부 : 3, 콩나물 : 4, 달걀 : 5, 
수산 : 6 ,정육 : 7, 햄 : 8, 어묵 : 9 , 반찬 : 10,
생수 : 11, 음료 : 12, 우유 : 13, 요구르트 : 14, 라면 : 15, 
통조림 : 16, 즉석식품 : 17, 냉동식품 : 18, 빙과 : 19, 과자 : 20          
"""


@csrf_exempt
def test_photo_open_t(request):
	page_title = 'test_photo_open_t'

	return render_to_response('imgForm_t.html')

@csrf_exempt
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

# android <- server (photos)
@csrf_exempt
def test_photo_download_s(request):
	page_title = 'test_photo_download_s'

	image_name = request.GET.get('image_name')

	link = 'sp_app/sp_pictures/sp_pictures/' + 'daily' + image_name + '.png'

	images = []
	image_data_2 = open(link, "rb").read()
	images.append(image_data_2)

	return HttpResponse(images, content_type="image/png")


# seller join / login--------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
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
		join_seller_info_ = USER_SELLER(user_seller_id=join_seller_, 
										user_seller_photo_index=join_seller_photo_index_, 
										user_seller_market_name=join_seller_market_name_, 
										user_seller_address=join_seller_address_, 
										user_seller_latitude=user_seller_latitude_, 
										user_seller_longitude=user_seller_longitude_, 
										user_seller_phone=join_seller_phone_)
		join_seller_info_.save()
	except:
		return HttpResponse('fail join')

	return HttpResponse('success join, %s' % join_seller_id_)


#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def login_page_s(request):
	page_title = 'login_page_s'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('login_page_s.html', ctx)

@csrf_exempt
def request_login_seller(request):
	callback = request.GET.get('callback')
	page_title = 'request_login_seller'

	login_seller_id_ = request.GET.get('seller_id', False)
	login_seller_pwd_ = request.GET.get('seller_pwd', False)

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
	datas.append(user_seller_info_.user_seller_longitude)
	datas.append(user_seller_info_.user_seller_latitude)

	json_data = json.dumps(datas, ensure_ascii=False)
	return HttpResponse(json_data, content_type='application/json')


# photo upload/update [post]---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_photo_upload(request):
	page_title = 'request_photo_upload'

	coupon_category_index_ = request.POST.get('coupon_category_index')
	coupon_product_index_ = request.POST.get('coupon_product_index')
	coupon_name_ = request.POST.get('coupon_index')

	if coupon_category_index_ == '1':
		coupon_category_index_k_ = 'm_daily'
		coupon_ = COUPON_DAILY.objects.get(coupon_daily_name=coupon_name_)
		coupon_index_ = coupon_.coupon_daily_index

	elif coupon_category_index_ == '2':
		coupon_category_index_k_ = 'm_greens'
		coupon_ = COUPON_GREENS.objects.get(coupon_greens_name=coupon_name_)
		coupon_index_ = coupon_.coupon_greens_index

	elif coupon_category_index_ == '3':
		coupon_category_index_k_ = 'm_fish'
		coupon_ = COUPON_FISH.objects.get(coupon_fish_name=coupon_name_)
		coupon_index_ = coupon_.coupon_fish_index

	elif coupon_category_index_ == '4':
		coupon_category_index_k_ = 'm_rice'
		coupon_ = COUPON_RICE.objects.get(coupon_rice_name=coupon_name_)
		coupon_index_ = coupon_.coupon_rice_index

	elif coupon_category_index_ == '5':
		coupon_category_index_k_ = 'm_meat'
		coupon_ = COUPON_MEAT.objects.get(coupon_meat_name=coupon_name_)
		coupon_index_ = coupon_.coupon_meat_index

	elif coupon_category_index_ == '6':
		coupon_category_index_k_ = 'm_egg'
		coupon_ = COUPON_egg.objects.get(coupon_egg_name=coupon_name_)
		coupon_index_ = coupon_.coupon_egg_index

	elif coupon_category_index_ == '7':
		coupon_category_index_k_ = 'm_ham'
		coupon_ = COUPON_HAM.objects.get(coupon_ham_name=coupon_name_)
		coupon_index_ = coupon_.coupon_ham_index

	elif coupon_category_index_ == '8':
		coupon_category_index_k_ = 'm_side'
		coupon_ = COUPON_SIDE.objects.get(coupon_side_name=coupon_name_)
		coupon_index_ = coupon_.coupon_side_index

	elif coupon_category_index_ == '9':
		coupon_category_index_k_ = 'm_water'
		coupon_ = COUPON_WATER.objects.get(coupon_water_name=coupon_name_)
		coupon_index_ = coupon_.coupon_water_index

	elif coupon_category_index_ == '10':
		coupon_category_index_k_ = 'm_instant'
		coupon_ = COUPON_INSTANT.objects.get(coupon_instant_name=coupon_name_)
		coupon_index_ = coupon_.coupon_instant_index

	elif coupon_category_index_ == '11':
		coupon_category_index_k_ = 'm_ice'
		coupon_ = COUPON_ICE.objects.get(coupon_ice_name=coupon_name_)
		coupon_index_ = coupon_.coupon_ice_index

	elif coupon_category_index_ == '12':
		coupon_category_index_k_ = 'm_bakery'
		coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_name=coupon_name_)
		coupon_index_ = coupon_.coupon_bakery_index

	elif coupon_category_index_ == '13':
		coupon_category_index_k_ = 'm_snack'
		coupon_ = COUPON_SNACK.objects.get(coupon_snack_name=coupon_name_)
		coupon_index_ = coupon_.coupon_snack_index


	# have to change photo
	if request.method == 'POST':
		if 'file' in request.FILES:
			file = request.FILES['file']
			filename = '' + coupon_category_index_k_ + '_' + str(coupon_product_index_ )+ '_' + str(coupon_index_)

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get make photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_index_ = pic_now.sp_photo_index

	if coupon_category_index_ == '1':
		coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=coupon_index_)
		coupon_.coupon_daily_index = coupon_index_

	elif coupon_category_index_ == '2':
		coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=coupon_index_)
		coupon_.coupon_greens_index = coupon_index_

	elif coupon_category_index_ == '3':
		coupon_ = COUPON_FISH.objects.get(coupon_fish_index=coupon_index_)
		coupon_.coupon_fish_index = coupon_index_

	elif coupon_category_index_ == '4':
		coupon_ = COUPON_RICE.objects.get(coupon_rice_index=coupon_index_)
		coupon_.coupon_rice_index = coupon_index_

	elif coupon_category_index_ == '5':
		coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=coupon_index_)
		coupon_.coupon_meat_index = coupon_index_

	elif coupon_category_index_ == '6':
		coupon_ = COUPON_EGG.objects.get(coupon_egg_index=coupon_index_)
		coupon_.coupon_egg_index = coupon_index_

	elif coupon_category_index_ == '7':
		coupon_ = COUPON_HAM.objects.get(coupon_ham_index=coupon_index_)
		coupon_.coupon_ham_index = coupon_index_

	elif coupon_category_index_ == '8':
		coupon_ = COUPON_SIDE.objects.get(coupon_side_index=coupon_index_)
		coupon_.coupon_side_photo_index = coupon_index_

	elif coupon_category_index_ == '9':
		coupon_ = COUPON_WATER.objects.get(coupon_water_index=coupon_index_)
		coupon_index_ = coupon_.coupon_water_index
		coupon_.coupon_water_index = coupon_index_

	elif coupon_category_index_ == '10':
		coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=coupon_index_)
		coupon_.coupon_instant_index = coupon_index_

	elif coupon_category_index_ == '11':
		coupon_ = COUPON_ICE.objects.get(coupon_ice_index=coupon_index_)
		coupon_.coupon_ice_index = coupon_index_

	elif coupon_category_index_ == '12':
		coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=coupon_index_)
		coupon_.coupon_bakery_index = coupon_index_

	elif coupon_category_index_ == '13':
		coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=coupon_index_)
		coupon_.coupon_snack_index = coupon_index_

	# swich coupon photo index
	coupon_.save()

	json_data = json.dumps('success save photo')
	return HttpResponse(json_data, content_type='application/json')	

@csrf_exempt
def request_photo_update(request):
	page_title = 'request_photo_update'

	coupon_category_index_ = request.POST.get('coupon_category_index')
	coupon_product_index_ = request.POST.get('coupon_product_index')
	coupon_name_ = request.POST.get('coupon_index')

	if coupon_category_index_ == '1':
		coupon_category_index_k_ = 'm_daily'
		coupon_ = COUPON_DAILY.objects.get(coupon_daily_name=coupon_name_)
		coupon_index_ = coupon_.coupon_daily_index

	elif coupon_category_index_ == '2':
		coupon_category_index_k_ = 'm_greens'
		coupon_ = COUPON_GREENS.objects.get(coupon_greens_name=coupon_name_)
		coupon_index_ = coupon_.coupon_greens_index

	elif coupon_category_index_ == '3':
		coupon_category_index_k_ = 'm_fish'
		coupon_ = COUPON_FISH.objects.get(coupon_fish_name=coupon_name_)
		coupon_index_ = coupon_.coupon_fish_index

	elif coupon_category_index_ == '4':
		coupon_category_index_k_ = 'm_rice'
		coupon_ = COUPON_RICE.objects.get(coupon_rice_name=coupon_name_)
		coupon_index_ = coupon_.coupon_rice_index

	elif coupon_category_index_ == '5':
		coupon_category_index_k_ = 'm_meat'
		coupon_ = COUPON_MEAT.objects.get(coupon_meat_name=coupon_name_)
		coupon_index_ = coupon_.coupon_meat_index

	elif coupon_category_index_ == '6':
		coupon_category_index_k_ = 'm_egg'
		coupon_ = COUPON_egg.objects.get(coupon_egg_name=coupon_name_)
		coupon_index_ = coupon_.coupon_egg_index

	elif coupon_category_index_ == '7':
		coupon_category_index_k_ = 'm_ham'
		coupon_ = COUPON_HAM.objects.get(coupon_ham_name=coupon_name_)
		coupon_index_ = coupon_.coupon_ham_index

	elif coupon_category_index_ == '8':
		coupon_category_index_k_ = 'm_side'
		coupon_ = COUPON_SIDE.objects.get(coupon_side_name=coupon_name_)
		coupon_index_ = coupon_.coupon_side_index

	elif coupon_category_index_ == '9':
		coupon_category_index_k_ = 'm_water'
		coupon_ = COUPON_WATER.objects.get(coupon_water_name=coupon_name_)
		coupon_index_ = coupon_.coupon_water_index

	elif coupon_category_index_ == '10':
		coupon_category_index_k_ = 'm_instant'
		coupon_ = COUPON_INSTANT.objects.get(coupon_instant_name=coupon_name_)
		coupon_index_ = coupon_.coupon_instant_index

	elif coupon_category_index_ == '11':
		coupon_category_index_k_ = 'm_ice'
		coupon_ = COUPON_ICE.objects.get(coupon_ice_name=coupon_name_)
		coupon_index_ = coupon_.coupon_ice_index

	elif coupon_category_index_ == '12':
		coupon_category_index_k_ = 'm_bakery'
		coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_name=coupon_name_)
		coupon_index_ = coupon_.coupon_bakery_index

	elif coupon_category_index_ == '13':
		coupon_category_index_k_ = 'm_snack'
		coupon_ = COUPON_SNACK.objects.get(coupon_snack_name=coupon_name_)
		coupon_index_ = coupon_.coupon_snack_index

	# have to change photo
	if request.method == 'POST':
		if 'file' in request.FILES:
			file = request.FILES['file']
			filename = '' + coupon_category_index_k_ + '_' + str(coupon_product_index_ )+ '_' + str(coupon_index_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get make photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_index_ = pic_now.sp_photo_index

	if coupon_category_index_ == '1':
		coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=coupon_index_)
		coupon_.coupon_daily_index = coupon_index_

	elif coupon_category_index_ == '2':
		coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=coupon_index_)
		coupon_.coupon_greens_index = coupon_index_

	elif coupon_category_index_ == '3':
		coupon_ = COUPON_FISH.objects.get(coupon_fish_index=coupon_index_)
		coupon_.coupon_fish_index = coupon_index_

	elif coupon_category_index_ == '4':
		coupon_ = COUPON_RICE.objects.get(coupon_rice_index=coupon_index_)
		coupon_.coupon_rice_index = coupon_index_

	elif coupon_category_index_ == '5':
		coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=coupon_index_)
		coupon_.coupon_meat_index = coupon_index_

	elif coupon_category_index_ == '6':
		coupon_ = COUPON_EGG.objects.get(coupon_egg_index=coupon_index_)
		coupon_.coupon_egg_index = coupon_index_

	elif coupon_category_index_ == '7':
		coupon_ = COUPON_HAM.objects.get(coupon_ham_index=coupon_index_)
		coupon_.coupon_ham_index = coupon_index_

	elif coupon_category_index_ == '8':
		coupon_ = COUPON_SIDE.objects.get(coupon_side_index=coupon_index_)
		coupon_.coupon_side_photo_index = coupon_index_

	elif coupon_category_index_ == '9':
		coupon_ = COUPON_WATER.objects.get(coupon_water_index=coupon_index_)
		coupon_index_ = coupon_.coupon_water_index
		coupon_.coupon_water_index = coupon_index_

	elif coupon_category_index_ == '10':
		coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=coupon_index_)
		coupon_.coupon_instant_index = coupon_index_

	elif coupon_category_index_ == '11':
		coupon_ = COUPON_ICE.objects.get(coupon_ice_index=coupon_index_)
		coupon_.coupon_ice_index = coupon_index_

	elif coupon_category_index_ == '12':
		coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=coupon_index_)
		coupon_.coupon_bakery_index = coupon_index_

	elif coupon_category_index_ == '13':
		coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=coupon_index_)
		coupon_.coupon_snack_index = coupon_index_

	# swich coupon photo index
	coupon_.save()

	json_data = json.dumps('success update photo')
	return HttpResponse(json_data, content_type='application/json')	

@csrf_exempt
def request_market_list(request):
	page_title = 'request_market_list'

	datas = []
	list_market_ = USER_SELLER.objects.all()

	for d in list_market_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# photo download---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_photo_download_daily(request):
	page_title = 'request_photo_download_daily'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_daily' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_greens(request):
	page_title = 'request_photo_download_greens'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_greens' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_fish(request):
	page_title = 'request_photo_download_fish'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_fish' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_rice(request):
	page_title = 'request_photo_download_rice'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_rice' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_meat(request):
	page_title = 'request_photo_download_meat'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_meat' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_egg(request):
	page_title = 'request_photo_download_egg'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_egg' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_ham(request):
	page_title = 'request_photo_download_ham'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_ham' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_side(request):
	page_title = 'request_photo_download_side'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_side' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_water(request):
	page_title = 'request_photo_download_water'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_water' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_instant(request):
	page_title = 'request_photo_download_instant'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_instant' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_ice(request):
	page_title = 'request_photo_download_ice'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_ice' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_bakery(request):
	page_title = 'request_photo_download_bakery'

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_bakery' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")

@csrf_exempt
def request_photo_download_snack(request):
	page_title = 'request_photo_download_snack'

	# 127.0.0.1:8000/request/photo/download/snack/?product_index=1&coupon_index=1

	product_index_ = request.GET.get('product_index')
	coupon_index_ = request.GET.get('coupon_index')
	marketname_ = request.GET.get('marketname')

	image_name = 'm_snack' + '_' +product_index_+ '_' +coupon_index_ + '_' + marketname_

	link = 'sp_app/sp_pictures/sp_pictures/' + image_name + '.png'

	images = []
	image = open(link, "rb").read()
	images.append(image)

	return HttpResponse(images, content_type="image/png")


# all data---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_product_all(request):
   page_title = 'request_product_all'

   coupon_data_= PRODUCT.objects.all()

   datas = []
   for d in coupon_data_:
      data = model_to_dict(d)
      datas.append(data)

   json_data = json.dumps(datas)
   return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
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


@csrf_exempt
def request_product_market(request):
   page_title = 'request_product_market'

   market_name_ = request.GET.get('market_name')

   coupon_data_= PRODUCT.objects.filter(product_market_name=market_name_)

   datas = []
   for d in coupon_data_:
      data = model_to_dict(d)
      datas.append(data)

   json_data = json.dumps(datas)
   return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_market(request):
	page_title = 'request_coupon_market'

	datas = []

	coupon_data_= COUPON_DAILY.objects.filter(coupon_daily_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_GREENS.objects.filter(coupon_greens_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_FISH.objects.filter(coupon_fish_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_RICE.objects.filter(coupon_rice_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_MEAT.objects.filter(coupon_meat_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_EGG.objects.filter(coupon_egg_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_HAM.objects.filter(coupon_ham_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SIDE.objects.filter(coupon_side_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_WATER.objects.filter(coupon_water_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_INSTANT.objects.filter(coupon_instant_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_ICE.objects.filter(coupon_ice_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_BAKERY.objects.filter(coupon_bakery_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	coupon_data_= COUPON_SNACK.objects.filter(coupon_snack_market_name=market_name_)
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')



# each coupon data---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_coupon_daily(request):
	page_title = 'request_coupon_daily'

	coupon_data_= COUPON_DAILY.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_greens(request):
	page_title = 'request_coupon_greens'

	coupon_data_= COUPON_GREENS.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_fish(request):
	page_title = 'request_coupon_fish'

	coupon_data_= COUPON_FISH.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_rice(request):
	page_title = 'request_coupon_rice'

	coupon_data_= COUPON_RICE.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_meat(request):
	page_title = 'request_coupon_meat'

	coupon_data_= COUPON_MEAT.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_egg(request):
	page_title = 'request_coupon_egg'

	coupon_data_= COUPON_EGG.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_ham(request):
	page_title = 'request_coupon_ham'

	coupon_data_= COUPON_HAM.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_side(request):
	page_title = 'request_coupon_side'

	coupon_data_= COUPON_SIDE.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_water(request):
	page_title = 'request_coupon_water'

	coupon_data_= COUPON_WATER.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_instant(request):
	page_title = 'request_coupon_instant'

	coupon_data_= COUPON_INSTANT.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_ice(request):
	page_title = 'request_coupon_ice'

	coupon_data_= COUPON_ICE.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_coupon_bakery(request):
	page_title = 'request_coupon_bakery'

	coupon_data_= COUPON_BAKERY.objects.all()

	datas = []
	for d in coupon_data_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
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
	coupon_daily_photo_index_ = request.POST.get('coupon_daily_photo_index')
	coupon_daily_market_name_ =  request.POST.get('coupon_daily_market_name')
	coupon_daily_name_ = request.POST.get('coupon_daily_name')
	coupon_daily_brand_ = request.POST.get('coupon_daily_brand')
	coupon_daily_unit_ = request.POST.get('coupon_daily_unit')
	coupon_daily_price_ = request.POST.get('coupon_daily_price')
	coupon_daily_disprice_ = request.POST.get('coupon_daily_disprice')
	coupon_daily_start_ = request.POST.get('coupon_daily_start')
	coupon_daily_finish_ = request.POST.get('coupon_daily_finish')
	coupon_daily_times_ = request.POST.get('coupon_daily_times')
	coupon_daily_detail_ = request.POST.get('coupon_daily_detail')
	coupon_daily_detail_b_ = request.POST.get('coupon_daily_detail_b')
	coupon_daily_type_ = request.POST.get('coupon_daily_type')
	coupon_daily_active_ = request.POST.get('coupon_daily_active')
	coupon_daily_making_ = request.POST.get('coupon_daily_making')

	# make coupon
	coupon_daily = COUPON_DAILY(coupon_daily_product_index = coupon_daily_product_index_, 
								coupon_daily_photo_index = coupon_daily_photo_index_, 
								coupon_daily_market_name = coupon_daily_market_name_, 
								coupon_daily_name = coupon_daily_name_, 
								coupon_daily_brand = coupon_daily_brand_, 
								coupon_daily_unit = coupon_daily_unit_, 
								coupon_daily_price = coupon_daily_price_, 
								coupon_daily_disprice = coupon_daily_disprice_,
								coupon_daily_start = coupon_daily_start_, 
								coupon_daily_finish = coupon_daily_finish_, 
								coupon_daily_times = coupon_daily_times_, 
								coupon_daily_detail=coupon_daily_detail_, 
								coupon_daily_detail_b=coupon_daily_detail_b_,
								coupon_daily_type = coupon_daily_type_, 
								coupon_daily_making=coupon_daily_making_, 
								coupon_daily_active=coupon_daily_active_)
	coupon_daily.save()

	coupon_ = COUPON_DAILY.objects.get(coupon_daily_making=coupon_daily_making_)
	coupon_daily_index_ = coupon_.coupon_daily_index

	# have to change photo
	if coupon_daily_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_daily' + '_' + str(coupon_daily_product_index_)+ '_' + str(coupon_daily_index_) + '_' + str(coupon_daily_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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


@csrf_exempt
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
	coupon_greens_disprice_ = request.POST.get('coupon_greens_disprice')
	coupon_greens_start_ = request.POST.get('coupon_greens_start')
	coupon_greens_finish_ = request.POST.get('coupon_greens_finish')
	coupon_greens_times_ = request.POST.get('coupon_greens_times')
	coupon_greens_detail_ = request.POST.get('coupon_greens_detail')
	coupon_greens_detail_b_ = request.POST.get('coupon_greens_detail_b')
	coupon_greens_type_ = request.POST.get('coupon_greens_type')
	coupon_greens_active_ = request.POST.get('coupon_greens_active')
	coupon_greens_making_ = request.POST.get('coupon_greens_making')

	# make coupon
	coupon_greens = COUPON_GREENS(coupon_greens_product_index = coupon_greens_product_index_,
								  coupon_greens_photo_index = coupon_greens_photo_index_, 
								  coupon_greens_market_name = coupon_greens_market_name_, 
								  coupon_greens_name = coupon_greens_name_, 
								  coupon_greens_brand = coupon_greens_brand_, 
								  coupon_greens_unit = coupon_greens_unit_, 
								  coupon_greens_area = coupon_greens_area_,
								  coupon_greens_price = coupon_greens_price_, 
								  coupon_greens_disprice = coupon_greens_disprice_,
								  coupon_greens_start = coupon_greens_start_, 
								  coupon_greens_finish = coupon_greens_finish_, 
								  coupon_greens_times = coupon_greens_times_, 
								  coupon_greens_detail=coupon_greens_detail_, 
								  coupon_greens_detail_b=coupon_greens_detail_b_,
								  coupon_greens_type = coupon_greens_type_, 
								  coupon_greens_active=coupon_greens_active_, 
								  coupon_greens_making=coupon_greens_making_)
	coupon_greens.save()

	coupon_ = COUPON_GREENS.objects.get(coupon_greens_making=coupon_greens_making_)
	coupon_greens_index_ = coupon_.coupon_greens_index

	# have to change photo
	if coupon_greens_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_greens' + '_' + str(coupon_greens_product_index_)+ '_' + str(coupon_greens_index_) + '_' + str(coupon_greens_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_fish_disprice_ = request.POST.get('coupon_fish_disprice')
	coupon_fish_start_ = request.POST.get('coupon_fish_start')
	coupon_fish_finish_ = request.POST.get('coupon_fish_finish')
	coupon_fish_times_ = request.POST.get('coupon_fish_times')
	coupon_fish_detail_ = request.POST.get('coupon_fish_detail')
	coupon_fish_detail_b_ = request.POST.get('coupon_fish_detail_b')
	coupon_fish_type_ = request.POST.get('coupon_fish_type')
	coupon_fish_active_ = request.POST.get('coupon_fish_active')
	coupon_fish_making_ = request.POST.get('coupon_fish_making')

 
	# make coupon
	coupon_fish = COUPON_FISH(coupon_fish_product_index = coupon_fish_product_index_, 
							  coupon_fish_photo_index = coupon_fish_photo_index_, 
							  coupon_fish_market_name = coupon_fish_market_name_, 
							  coupon_fish_name = coupon_fish_name_, 
							  coupon_fish_brand = coupon_fish_brand_, 
							  coupon_fish_unit = coupon_fish_unit_, 
							  coupon_fish_area = coupon_fish_area_,
							  coupon_fish_price = coupon_fish_price_, 
							  coupon_fish_disprice = coupon_fish_disprice_,
							  coupon_fish_start = coupon_fish_start_, 
							  coupon_fish_finish = coupon_fish_finish_, 
							  coupon_fish_times = coupon_fish_times_, 
							  coupon_fish_detail=coupon_fish_detail_, 
							  coupon_fish_detail_b=coupon_fish_detail_b_,
							  coupon_fish_type = coupon_fish_type_, 
							  coupon_fish_active = coupon_fish_active_,
							  coupon_fish_making=coupon_fish_making_)
	coupon_fish.save()

	coupon_ = COUPON_FISH.objects.get(coupon_fish_making=coupon_fish_making_)
	coupon_fish_index_ = coupon_.coupon_fish_index

	# have to change photo
	if coupon_fish_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_fish' + '_' + str(coupon_fish_product_index_)+ '_' + str(coupon_fish_index_) + '_' + str(coupon_fish_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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


@csrf_exempt
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
	coupon_rice_disprice_ = request.POST.get('coupon_rice_disprice')
	coupon_rice_start_ = request.POST.get('coupon_rice_start')
	coupon_rice_finish_ = request.POST.get('coupon_rice_finish')
	coupon_rice_times_ = request.POST.get('coupon_rice_times')
	coupon_rice_detail_ = request.POST.get('coupon_rice_detail')
	coupon_rice_detail_b_ = request.POST.get('coupon_rice_detail_b')
	coupon_rice_type_ = request.POST.get('coupon_rice_type')
	coupon_rice_active_ = request.POST.get('coupon_rice_active')
	coupon_rice_making_ = request.POST.get('coupon_rice_making')

 
	# make coupon
	coupon_rice = COUPON_RICE(coupon_rice_product_index = coupon_rice_product_index_, 
							  coupon_rice_photo_index = coupon_rice_photo_index_, 
							  coupon_rice_market_name = coupon_rice_market_name_, 
							  coupon_rice_name = coupon_rice_name_, 
							  coupon_rice_brand = coupon_rice_brand_, 
							  coupon_rice_unit = coupon_rice_unit_, 
							  coupon_rice_area = coupon_rice_area_,
							  coupon_rice_price = coupon_rice_price_, 
							  coupon_rice_disprice = coupon_rice_disprice_,
							  coupon_rice_start = coupon_rice_start_, 
							  coupon_rice_finish = coupon_rice_finish_, 
							  coupon_rice_detail=coupon_rice_detail_, 
							  coupon_rice_detail_b=coupon_rice_detail_b_,
							  coupon_rice_times = coupon_rice_times_, 
							  coupon_rice_type = coupon_rice_type_, 
							  coupon_rice_active = coupon_rice_active_,
							  coupon_rice_making=coupon_rice_making_)
	coupon_rice.save()

	coupon_ = COUPON_RICE.objects.get(coupon_rice_making=coupon_rice_making_)
	coupon_rice_index_ = coupon_.coupon_rice_index

	# have to change photo
	if coupon_rice_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_rice' + '_' + str(coupon_rice_product_index_)+ '_' + str(coupon_rice_index_) + '_' + str(coupon_rice_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_meat_disprice_ = request.POST.get('coupon_meat_disprice')
	coupon_meat_start_ = request.POST.get('coupon_meat_start')
	coupon_meat_finish_ = request.POST.get('coupon_meat_finish')
	coupon_meat_times_ = request.POST.get('coupon_meat_times')
	coupon_meat_detail_ = request.POST.get('coupon_meat_detail')
	coupon_meat_detail_b_ = request.POST.get('coupon_meat_detail_b')
	coupon_meat_type_ = request.POST.get('coupon_meat_type')
	coupon_meat_active_ = request.POST.get('coupon_meat_active')
	coupon_meat_making_ = request.POST.get('coupon_meat_making')

 
	# make coupon
	coupon_meat = COUPON_MEAT(coupon_meat_product_index = coupon_meat_product_index_, 
							  coupon_meat_photo_index = coupon_meat_photo_index_, 
							  coupon_meat_market_name = coupon_meat_market_name_, 
							  coupon_meat_name = coupon_meat_name_, 
							  coupon_meat_brand = coupon_meat_brand_, 
							  coupon_meat_unit = coupon_meat_unit_, 
							  coupon_meat_area = coupon_meat_area_,
							  coupon_meat_price = coupon_meat_price_, 
							  coupon_meat_disprice = coupon_meat_disprice_,
							  coupon_meat_start = coupon_meat_start_, 
							  coupon_meat_finish = coupon_meat_finish_, 
							  coupon_meat_times = coupon_meat_times_, 
							  coupon_meat_detail=coupon_meat_detail_,
							  coupon_meat_detail_b=coupon_meat_detail_b_, 
							  coupon_meat_type = coupon_meat_type_, 
							  coupon_meat_active = coupon_meat_active_,
							  coupon_meat_making=coupon_meat_making_)
	coupon_meat.save()

	coupon_ = COUPON_MEAT.objects.get(coupon_meat_making=coupon_meat_making_)
	coupon_meat_index_ = coupon_.coupon_meat_index

	# have to change photo
	if coupon_meat_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_meat' + '_' + str(coupon_meat_product_index_)+ '_' + str(coupon_meat_index_) + '_' + str(coupon_meat_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_egg_disprice_ = request.POST.get('coupon_egg_disprice')
	coupon_egg_start_ = request.POST.get('coupon_egg_start')
	coupon_egg_finish_ = request.POST.get('coupon_egg_finish')
	coupon_egg_times_ = request.POST.get('coupon_egg_times')
	coupon_egg_detail_ = request.POST.get('coupon_egg_detail')
	coupon_egg_detail_b_ = request.POST.get('coupon_egg_detail_b')
	coupon_egg_type_ = request.POST.get('coupon_egg_type')
	coupon_egg_active_ = request.POST.get('coupon_egg_active')
	coupon_egg_making_ = request.POST.get('coupon_egg_making')

 
	# make coupon
	coupon_egg = COUPON_EGG(coupon_egg_product_index = coupon_egg_product_index_, 
						    coupon_egg_photo_index = coupon_egg_photo_index_, 
						    coupon_egg_market_name = coupon_egg_market_name_, 
						    coupon_egg_name = coupon_egg_name_, 
						    coupon_egg_brand = coupon_egg_brand_, 
						    coupon_egg_unit = coupon_egg_unit_, 
						    coupon_egg_area = coupon_egg_area_,
						    coupon_egg_price = coupon_egg_price_, 
						    coupon_egg_disprice = coupon_egg_disprice_,
						    coupon_egg_start = coupon_egg_start_, 
						    coupon_egg_finish = coupon_egg_finish_, 
						    coupon_egg_detail=coupon_egg_detail_, 
						    coupon_egg_detail_b=coupon_egg_detail_b_,
						    coupon_egg_times = coupon_egg_times_, 
						    coupon_egg_type = coupon_egg_type_, 
						    coupon_egg_active = coupon_egg_active_,
						    coupon_egg_making=coupon_egg_making_)
	coupon_egg.save()

	coupon_ = COUPON_EGG.objects.get(coupon_egg_making=coupon_egg_making_)
	coupon_egg_index_ = coupon_.coupon_egg_index

	# have to change photo
	if coupon_egg_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_egg' + '_' + str(coupon_egg_product_index_)+ '_' + str(coupon_egg_index_) + '_' + str(coupon_egg_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_ham_disprice_ = request.POST.get('coupon_ham_disprice')
	coupon_ham_start_ = request.POST.get('coupon_ham_start')
	coupon_ham_finish_ = request.POST.get('coupon_ham_finish')
	coupon_ham_times_ = request.POST.get('coupon_ham_times')
	coupon_ham_detail_ = request.POST.get('coupon_ham_detail')
	coupon_ham_detail_b_ = request.POST.get('coupon_ham_detail_b')
	coupon_ham_type_ = request.POST.get('coupon_ham_type')
	coupon_ham_active_ = request.POST.get('coupon_ham_active')
	coupon_ham_making_ = request.POST.get('coupon_ham_making')

 
	# make coupon
	coupon_ham = COUPON_HAM(coupon_ham_product_index = coupon_ham_product_index_, 
						    coupon_ham_photo_index = coupon_ham_photo_index_, 
						    coupon_ham_market_name = coupon_ham_market_name_, 
						    coupon_ham_name = coupon_ham_name_, 
						    coupon_ham_brand = coupon_ham_brand_, 
						    coupon_ham_unit = coupon_ham_unit_, 
						    coupon_ham_price = coupon_ham_price_, 
						    coupon_ham_disprice = coupon_ham_disprice_,
						    coupon_ham_start = coupon_ham_start_, 
						    coupon_ham_finish = coupon_ham_finish_, 
						    coupon_ham_detail=coupon_ham_detail_, 
						    coupon_ham_detail_b=coupon_ham_detail_b_,
						    coupon_ham_times = coupon_ham_times_, 
						    coupon_ham_type = coupon_ham_type_, 
						    coupon_ham_active = coupon_ham_active_,
						    coupon_ham_making=coupon_ham_making_)
	coupon_ham.save()

	coupon_ = COUPON_HAM.objects.get(coupon_ham_making=coupon_ham_making_)
	coupon_ham_index_ = coupon_.coupon_ham_index

	# have to change photo
	if coupon_ham_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_ham' + '_' + str(coupon_ham_product_index_)+ '_' + str(coupon_ham_index_) + '_' + str(coupon_ham_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_side_disprice_ = request.POST.get('coupon_side_disprice')
	coupon_side_start_ = request.POST.get('coupon_side_start')
	coupon_side_finish_ = request.POST.get('coupon_side_finish')
	coupon_side_times_ = request.POST.get('coupon_side_times')
	coupon_side_detail_ = request.POST.get('coupon_side_detail')
	coupon_side_detail_b_ = request.POST.get('coupon_side_detail_b')
	coupon_side_type_ = request.POST.get('coupon_side_type')
	coupon_side_active_ = request.POST.get('coupon_side_active')
	coupon_side_making_ = request.POST.get('coupon_side_making')

 
	# make coupon
	coupon_side = COUPON_SIDE(coupon_side_product_index = coupon_side_product_index_, 
							  coupon_side_photo_index = coupon_side_photo_index_, 
							  coupon_side_market_name = coupon_side_market_name_, 
							  coupon_side_name = coupon_side_name_, 
							  coupon_side_brand = coupon_side_brand_, 
							  coupon_side_unit = coupon_side_unit_, 
							  coupon_side_price = coupon_side_price_, 
							  coupon_side_disprice = coupon_side_disprice_,
							  coupon_side_start = coupon_side_start_, 
							  coupon_side_finish = coupon_side_finish_, 
							  coupon_side_detail=coupon_side_detail_, 
							  coupon_side_detail_b=coupon_side_detail_b_,
							  coupon_side_times = coupon_side_times_,
							  coupon_side_active = coupon_side_active_, 
							  coupon_side_type = coupon_side_type_, 
							  coupon_side_making=coupon_side_making_)
	coupon_side.save()

	coupon_ = COUPON_SIDE.objects.get(coupon_side_making=coupon_side_making_)
	coupon_side_index_ = coupon_.coupon_side_index

	# have to change photo
	if coupon_side_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_side' + '_' + str(coupon_side_product_index_)+ '_' + str(coupon_side_index_) + '_' + str(coupon_side_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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


@csrf_exempt
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
	coupon_water_disprice_ = request.POST.get('coupon_water_disprice')
	coupon_water_start_ = request.POST.get('coupon_water_start')
	coupon_water_finish_ = request.POST.get('coupon_water_finish')
	coupon_water_times_ = request.POST.get('coupon_water_times')
	coupon_water_detail_ = request.POST.get('coupon_water_detail')
	coupon_water_detail_b_ = request.POST.get('coupon_water_detail_b')
	coupon_water_type_ = request.POST.get('coupon_water_type')
	coupon_water_active_ = request.POST.get('coupon_water_active')
	coupon_water_making_ = request.POST.get('coupon_water_making')

 
	# make coupon
	coupon_water = COUPON_WATER(coupon_water_product_index = coupon_water_product_index_, 
								coupon_water_photo_index = coupon_water_photo_index_, 
								coupon_water_market_name = coupon_water_market_name_, 
								coupon_water_name = coupon_water_name_, 
								coupon_water_brand = coupon_water_brand_, 
								coupon_water_unit = coupon_water_unit_, 
								coupon_water_price = coupon_water_price_, 
								coupon_water_disprice = coupon_water_disprice_,
								coupon_water_start = coupon_water_start_, 
								coupon_water_finish = coupon_water_finish_, 
								coupon_water_times = coupon_water_times_, 
								coupon_water_type = coupon_water_type_, 
								coupon_water_detail=coupon_water_detail_, 
								coupon_water_detail_b=coupon_water_detail_b_,
								coupon_water_active=coupon_water_active_,
								coupon_water_making=coupon_water_making_)
	coupon_water.save()

	coupon_ = COUPON_WATER.objects.get(coupon_water_making=coupon_water_making_)
	coupon_water_index_ = coupon_.coupon_water_index

	# have to change photo
	if coupon_water_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_water' + '_' + str(coupon_water_product_index_)+ '_' + str(coupon_water_index_) + '_' + str(coupon_water_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_instant_disprice_ = request.POST.get('coupon_instant_disprice')
	coupon_instant_start_ = request.POST.get('coupon_instant_start')
	coupon_instant_finish_ = request.POST.get('coupon_instant_finish')
	coupon_instant_times_ = request.POST.get('coupon_instant_times')
	coupon_instant_detail_ = request.POST.get('coupon_instant_detail')
	coupon_instant_detail_b_ = request.POST.get('coupon_instant_detail_b')
	coupon_instant_type_ = request.POST.get('coupon_instant_type')
	coupon_instant_active_ = request.POST.get('coupon_instant_active')
	coupon_instant_making_ = request.POST.get('coupon_instant_making')

 
	# make coupon
	coupon_instant = COUPON_INSTANT(coupon_instant_product_index = coupon_instant_product_index_, 
									coupon_instant_photo_index = coupon_instant_photo_index_, 
									coupon_instant_market_name = coupon_instant_market_name_, 
									coupon_instant_name = coupon_instant_name_, 
									coupon_instant_brand = coupon_instant_brand_, 
									coupon_instant_unit = coupon_instant_unit_, 
									coupon_instant_price = coupon_instant_price_,
									coupon_instant_disprice = coupon_instant_disprice_, 
									coupon_instant_start = coupon_instant_start_, 
									coupon_instant_finish = coupon_instant_finish_, 
									coupon_instant_times = coupon_instant_times_, 
									coupon_instant_type = coupon_instant_type_, 
									coupon_instant_detail=coupon_instant_detail_,
									coupon_instant_detail_b=coupon_instant_detail_b_, 
									coupon_instant_active = coupon_instant_active_,
									coupon_instant_making=coupon_instant_making_)
	coupon_instant.save()

	coupon_ = COUPON_INSTANT.objects.get(coupon_instant_making=coupon_instant_making_)
	coupon_instant_index_ = coupon_.coupon_instant_index

	# have to change photo
	if coupon_instant_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_instant' + '_' + str(coupon_instant_product_index_)+ '_' + str(coupon_instant_index_) + '_' + str(coupon_instant_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_ice_disprice_ = request.POST.get('coupon_ice_disprice')
	coupon_ice_start_ = request.POST.get('coupon_ice_start')
	coupon_ice_finish_ = request.POST.get('coupon_ice_finish')
	coupon_ice_times_ = request.POST.get('coupon_ice_times')
	coupon_ice_detail_ = request.POST.get('coupon_ice_detail')
	coupon_ice_detail_b_ = request.POST.get('coupon_ice_detail_b')
	coupon_ice_type_ = request.POST.get('coupon_ice_type')
	coupon_ice_active_ = request.POST.get('coupon_ice_active')
	coupon_ice_making_ = request.POST.get('coupon_ice_making')

 
	# make coupon
	coupon_ice = COUPON_ICE(coupon_ice_product_index = coupon_ice_product_index_, 
							coupon_ice_photo_index = coupon_ice_photo_index_, 
							coupon_ice_market_name = coupon_ice_market_name_, 
							coupon_ice_name = coupon_ice_name_, 
							coupon_ice_brand = coupon_ice_brand_, 
							coupon_ice_unit = coupon_ice_unit_, 
							coupon_ice_price = coupon_ice_price_, 
							coupon_ice_disprice = coupon_ice_disprice_,
							coupon_ice_start = coupon_ice_start_, 
							coupon_ice_finish = coupon_ice_finish_, 
							coupon_ice_detail=coupon_ice_detail_, 
							coupon_ice_detail_b=coupon_ice_detail_b_,
							coupon_ice_times = coupon_ice_times_, 
							coupon_ice_type = coupon_ice_type_, 
							coupon_ice_active = coupon_ice_active_,
							coupon_ice_making=coupon_ice_making_)
	coupon_ice.save()

	coupon_ = COUPON_ICE.objects.get(coupon_ice_making=coupon_ice_making_)
	coupon_ice_index_ = coupon_.coupon_ice_index

	# have to change photo
	if coupon_ice_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_ice' + '_' + str(coupon_ice_product_index_)+ '_' + str(coupon_ice_index_) + '_' + str(coupon_ice_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
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
	coupon_bakery_price_ = request.POST.get('coupon_bakery_price')
	coupon_bakery_disprice_ = request.POST.get('coupon_bakery_disprice')
	coupon_bakery_start_ = request.POST.get('coupon_bakery_start')
	coupon_bakery_finish_ = request.POST.get('coupon_bakery_finish')
	coupon_bakery_times_ = request.POST.get('coupon_bakery_times')
	coupon_bakery_detail_ = request.POST.get('coupon_bakery_detail')
	coupon_bakery_detail_b_ = request.POST.get('coupon_bakery_detail_b')
	coupon_bakery_type_ = request.POST.get('coupon_bakery_type')
	coupon_bakery_active_ = request.POST.get('coupon_bakery_active')
	coupon_bakery_making_ = request.POST.get('coupon_bakery_making')

 
	# make coupon
	coupon_bakery = COUPON_BAKERY(coupon_bakery_product_index = coupon_bakery_product_index_, 
								  coupon_bakery_photo_index = coupon_bakery_photo_index_, 
								  coupon_bakery_market_name = coupon_bakery_market_name_, 
								  coupon_bakery_name = coupon_bakery_name_, 
								  coupon_bakery_brand = coupon_bakery_brand_, 
								  coupon_bakery_unit = coupon_bakery_unit_, 
								  coupon_bakery_price = coupon_bakery_price_, 
								  coupon_bakery_disprice = coupon_bakery_disprice_,
								  coupon_bakery_start = coupon_bakery_start_, 
								  coupon_bakery_finish = coupon_bakery_finish_, 
								  coupon_bakery_times = coupon_bakery_times_, 
								  coupon_bakery_detail=coupon_bakery_detail_, 
								  coupon_bakery_detail_b=coupon_bakery_detail_b_,
								  coupon_bakery_type = coupon_bakery_type_, 
								  coupon_bakery_active = coupon_bakery_active_,
								  coupon_bakery_making=coupon_bakery_making_)
	coupon_bakery.save()

	coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_making=coupon_bakery_making_)
	coupon_bakery_index_ = coupon_.coupon_bakery_index

	# have to change photo
	if coupon_bakery_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_bakery' + '_' + str(coupon_bakery_product_index_)+ '_' + str(coupon_bakery_index_) + '_' + str(coupon_bakery_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

@csrf_exempt
def request_make_snack(request):
	page_title = 'request_make_snack'
	# /request/make/snack/?coupon_snack_product_index=1&coupon_snack_photo_index=1&coupon_snack_market_name=nabak&coupon_snack_name=milk&coupon_snack_brand=pul&coupon_snack_unit=0&coupon_snack_psnack=100&coupon_snack_start=0&coupon_snack_finish=0&coupon_snack_times=0&coupon_snack_detail=0&coupon_snack_type=0&coupon_snack_active=0&coupon_snack_making=0

	coupon_snack_product_index_ = request.POST.get('coupon_snack_product_index')
	# not change: 0 / change: 1
	coupon_snack_photo_index_ = request.POST.get('coupon_snack_photo_index')
	coupon_snack_market_name_ =  request.POST.get('coupon_snack_market_name')
	coupon_snack_name_ = request.POST.get('coupon_snack_name')
	coupon_snack_brand_ = request.POST.get('coupon_snack_brand')
	coupon_snack_unit_ = request.POST.get('coupon_snack_unit')
	coupon_snack_price_ = request.POST.get('coupon_snack_price')
	coupon_snack_disprice_ = request.POST.get('coupon_snack_disprice')
	coupon_snack_start_ = request.POST.get('coupon_snack_start')
	coupon_snack_finish_ = request.POST.get('coupon_snack_finish')
	coupon_snack_times_ = request.POST.get('coupon_snack_times')
	coupon_snack_detail_ = request.POST.get('coupon_snack_detail')
	coupon_snack_detail_b_ = request.POST.get('coupon_snack_detail_b')
	coupon_snack_type_ = request.POST.get('coupon_snack_type')
	coupon_snack_active_ = request.POST.get('coupon_snack_active')
	coupon_snack_making_ = request.POST.get('coupon_snack_making')

 
	# make coupon
	coupon_snack = COUPON_SNACK(coupon_snack_product_index = coupon_snack_product_index_, 
								coupon_snack_photo_index = coupon_snack_photo_index_, 
								coupon_snack_market_name = coupon_snack_market_name_, 
								coupon_snack_name = coupon_snack_name_, 
								coupon_snack_brand = coupon_snack_brand_, 
								coupon_snack_unit = coupon_snack_unit_, 
								coupon_snack_price = coupon_snack_price_, 
								coupon_snack_disprice = coupon_snack_disprice_,
								coupon_snack_start = coupon_snack_start_, 
								coupon_snack_finish = coupon_snack_finish_, 
								coupon_snack_detail=coupon_snack_detail_, 
								coupon_snack_detail_b=coupon_snack_detail_b_,
								coupon_snack_times = coupon_snack_times_, 
								coupon_snack_type = coupon_snack_type_, 
								coupon_snack_active = coupon_snack_active_, 
								coupon_snack_making=coupon_snack_making_)
	coupon_snack.save()

	coupon_ = COUPON_SNACK.objects.get(coupon_snack_making=coupon_snack_making_)
	coupon_snack_index_ = coupon_.coupon_snack_index

	# have to change photo
	if coupon_snack_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_snack' + '_' + str(coupon_snack_product_index_)+ '_' + str(coupon_snack_index_) + '_' + str(coupon_snack_market_name_)

				try:
					pic_ = SP_PICTURE()
					pic_.sp_name = filename
					pic_.sp_picture.save(filename+'.png', File(file), save=True)	
				except:
					# code1 : save photo fail
					json_data = json.dumps('save photo fail')
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
 

# make coupon-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_remake_daily(request):
	page_title = 'request_remake_daily'
	
	# /request/remake/daily/?coupon_daily_index=1&coupon_daily_product_index=1&coupon_daily_photo_index=2&coupon_daily_market_name=bkabka&coupon_daily_name=sfs&coupon_daily_brand=dfdf&coupon_daily_unit=plp&coupon_daily_price=10&coupon_daily_disprice=5&coupon_daily_start=1&coupon_daily_finish=3&coupon_daily_detail=0&coupon_daily_type=0&coupon_daily_active=0&coupon_daily_making=111

	coupon_daily_index_ = request.POST.get('coupon_daily_index')
	coupon_daily_product_index_ = request.POST.get('coupon_daily_product_index')
	coupon_daily_photo_index_ = request.POST.get('coupon_daily_photo_index')
	coupon_daily_market_name_ =  request.POST.get('coupon_daily_market_name')
	coupon_daily_name_ = request.POST.get('coupon_daily_name')
	coupon_daily_brand_ = request.POST.get('coupon_daily_brand')
	coupon_daily_unit_ = request.POST.get('coupon_daily_unit')
	coupon_daily_price_ = request.POST.get('coupon_daily_price')
	coupon_daily_disprice_ = request.POST.get('coupon_daily_disprice')
	coupon_daily_start_ = request.POST.get('coupon_daily_start')
	coupon_daily_finish_ = request.POST.get('coupon_daily_finish')
	coupon_daily_detail_ = request.POST.get('coupon_daily_detail')
	coupon_daily_detail_b_ = request.POST.get('coupon_daily_detail_b')
	coupon_daily_type_ = request.POST.get('coupon_daily_type')
	coupon_daily_active_ = request.POST.get('coupon_daily_active')
	coupon_daily_making_ = request.POST.get('coupon_daily_making')

	try:
		coupon_daily_ = COUPON_DAILY.objects.get(coupon_daily_index=coupon_daily_index_)
	except:
		json_data = json.dumps(coupon_daily_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_daily_.coupon_daily_product_index = coupon_daily_product_index_
		coupon_daily_.coupon_daily_photo_index = coupon_daily_photo_index_
		coupon_daily_.coupon_daily_market_name = coupon_daily_market_name_
		coupon_daily_.coupon_daily_name = coupon_daily_name_
		coupon_daily_.coupon_daily_brand = coupon_daily_brand_
		coupon_daily_.coupon_daily_unit = coupon_daily_unit_
		coupon_daily_.coupon_daily_price = coupon_daily_price_
		coupon_daily_.coupon_daily_disprice = coupon_daily_disprice_
		coupon_daily_.coupon_daily_start = coupon_daily_start_
		coupon_daily_.coupon_daily_finish = coupon_daily_finish_
		coupon_daily_.coupon_daily_detail = coupon_daily_detail_
		coupon_daily_.coupon_daily_detail_b = coupon_daily_detail_b_
		coupon_daily_.coupon_daily_type = coupon_daily_type_
		coupon_daily_.coupon_daily_making = coupon_daily_making_

		coupon_daily_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_daily_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_daily' + '_' + str(coupon_daily_product_index_)+ '_' + str(coupon_daily_index_) + '_' + str(coupon_daily_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_daily_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_daily_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_daily_product_index_)
		coupon_daily_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_daily_photo_index_ == '2':
		coupon_daily_photo_index_ = coupon_daily_.coupon_daily_photo_index
		
	# swich coupon photo index
	coupon_daily_ = COUPON_DAILY.objects.get(coupon_daily_index=coupon_daily_index_)

	coupon_daily_.coupon_daily_photo_index = coupon_daily_photo_index_
	coupon_daily_.save()

	# code0 : success
	text = coupon_daily_.coupon_daily_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_remake_greens(request):
	page_title = 'request_remake_greens'
	# /request/remake/greens/?coupon_greens_index=1&coupon_greens_product_index=1&coupon_greens_photo_index=2&coupon_greens_market_name=bkabka&coupon_greens_name=sfs&coupon_greens_brand=dfdf&coupon_greens_unit=plp&coupon_greens_price=10&coupon_greens_disprice=5&coupon_greens_start=1&coupon_greens_finish=3&coupon_greens_detail=0&coupon_greens_type=0&coupon_greens_active=0&coupon_greens_making=111

	coupon_greens_index_ = request.POST.get('coupon_greens_index')
	coupon_greens_product_index_ = request.POST.get('coupon_greens_product_index')
	coupon_greens_photo_index_ = request.POST.get('coupon_greens_photo_index')
	coupon_greens_market_name_ =  request.POST.get('coupon_greens_market_name')
	coupon_greens_name_ = request.POST.get('coupon_greens_name')
	coupon_greens_brand_ = request.POST.get('coupon_greens_brand')
	coupon_greens_unit_ = request.POST.get('coupon_greens_unit')
	coupon_greens_area_ = request.POST.get('coupon_greens_area')
	coupon_greens_price_ = request.POST.get('coupon_greens_price')
	coupon_greens_disprice_ = request.POST.get('coupon_greens_disprice')
	coupon_greens_start_ = request.POST.get('coupon_greens_start')
	coupon_greens_finish_ = request.POST.get('coupon_greens_finish')
	coupon_greens_detail_ = request.POST.get('coupon_greens_detail')
	coupon_greens_detail_b_ = request.POST.get('coupon_greens_detail_b')
	coupon_greens_type_ = request.POST.get('coupon_greens_type')
	coupon_greens_active_ = request.POST.get('coupon_greens_active')
	coupon_greens_making_ = request.POST.get('coupon_greens_making')

	try:
		coupon_greens_ = COUPON_GREENS.objects.get(coupon_greens_index=coupon_greens_index_)
	except:
		json_data = json.dumps(coupon_greens_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_greens_.coupon_greens_product_index = coupon_greens_product_index_
		coupon_greens_.coupon_greens_photo_index = coupon_greens_photo_index_
		coupon_greens_.coupon_greens_market_name = coupon_greens_market_name_
		coupon_greens_.coupon_greens_name = coupon_greens_name_
		coupon_greens_.coupon_greens_brand = coupon_greens_brand_
		coupon_greens_.coupon_greens_unit = coupon_greens_unit_
		coupon_greens_.coupon_greens_area = coupon_greens_area_
		coupon_greens_.coupon_greens_price = coupon_greens_price_
		coupon_greens_.coupon_greens_disprice = coupon_greens_disprice_
		coupon_greens_.coupon_greens_start = coupon_greens_start_
		coupon_greens_.coupon_greens_finish = coupon_greens_finish_
		coupon_greens_.coupon_greens_detail = coupon_greens_detail_
		coupon_greens_.coupon_greens_detail_b = coupon_greens_detail_b_
		coupon_greens_.coupon_greens_type = coupon_greens_type_
		coupon_greens_.coupon_greens_making = coupon_greens_making_

		coupon_greens_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_greens_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_greens' + '_' + str(coupon_greens_product_index_)+ '_' + str(coupon_greens_index_) + '_' + str(coupon_greens_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_greens_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_greens_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_greens_product_index_)
		coupon_greens_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_greens_photo_index_ == '2':
		coupon_greens_photo_index_ = coupon_greens_.coupon_greens_photo_index
		
	# swich coupon photo index
	coupon_greens_ = COUPON_GREENS.objects.get(coupon_greens_index=coupon_greens_index_)

	coupon_greens_.coupon_greens_photo_index = coupon_greens_photo_index_
	coupon_greens_.save()

	# code0 : success
	text = coupon_greens_.coupon_greens_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')
 

@csrf_exempt
def request_remake_fish(request):
	page_title = 'request_remake_fish'
	# /request/remake/fish/?coupon_fish_index=1&coupon_fish_product_index=1&coupon_fish_photo_index=2&coupon_fish_market_name=bkabka&coupon_fish_name=sfs&coupon_fish_brand=dfdf&coupon_fish_unit=plp&coupon_fish_price=10&coupon_fish_disprice=5&coupon_fish_start=1&coupon_fish_finish=3&coupon_fish_detail=0&coupon_fish_type=0&coupon_fish_active=0&coupon_fish_making=111

	coupon_fish_index_ = request.POST.get('coupon_fish_index')
	coupon_fish_product_index_ = request.POST.get('coupon_fish_product_index')
	coupon_fish_photo_index_ = request.POST.get('coupon_fish_photo_index')
	coupon_fish_market_name_ =  request.POST.get('coupon_fish_market_name')
	coupon_fish_name_ = request.POST.get('coupon_fish_name')
	coupon_fish_brand_ = request.POST.get('coupon_fish_brand')
	coupon_fish_unit_ = request.POST.get('coupon_fish_unit')
	coupon_fish_area_ = request.POST.get('coupon_fish_area')
	coupon_fish_price_ = request.POST.get('coupon_fish_price')
	coupon_fish_disprice_ = request.POST.get('coupon_fish_disprice')
	coupon_fish_start_ = request.POST.get('coupon_fish_start')
	coupon_fish_finish_ = request.POST.get('coupon_fish_finish')
	coupon_fish_detail_ = request.POST.get('coupon_fish_detail')
	coupon_fish_detail_b_ = request.POST.get('coupon_fish_detail_b')
	coupon_fish_type_ = request.POST.get('coupon_fish_type')
	coupon_fish_active_ = request.POST.get('coupon_fish_active')
	coupon_fish_making_ = request.POST.get('coupon_fish_making')

	try:
		coupon_fish_ = COUPON_FISH.objects.get(coupon_fish_index=coupon_fish_index_)
	except:
		json_data = json.dumps(coupon_fish_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_fish_.coupon_fish_product_index = coupon_fish_product_index_
		coupon_fish_.coupon_fish_photo_index = coupon_fish_photo_index_
		coupon_fish_.coupon_fish_market_name = coupon_fish_market_name_
		coupon_fish_.coupon_fish_name = coupon_fish_name_
		coupon_fish_.coupon_fish_brand = coupon_fish_brand_
		coupon_fish_.coupon_fish_unit = coupon_fish_unit_
		coupon_fish_.coupon_fish_area = coupon_fish_area_
		coupon_fish_.coupon_fish_price = coupon_fish_price_
		coupon_fish_.coupon_fish_disprice = coupon_fish_disprice_
		coupon_fish_.coupon_fish_start = coupon_fish_start_
		coupon_fish_.coupon_fish_finish = coupon_fish_finish_
		coupon_fish_.coupon_fish_detail = coupon_fish_detail_
		coupon_fish_.coupon_fish_detail_b = coupon_fish_detail_b_
		coupon_fish_.coupon_fish_type = coupon_fish_type_
		coupon_fish_.coupon_fish_making = coupon_fish_making_

		coupon_fish_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_fish_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_fish' + '_' + str(coupon_fish_product_index_)+ '_' + str(coupon_fish_index_) + '_' + str(coupon_fish_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_fish_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_fish_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_fish_product_index_)
		coupon_fish_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_fish_photo_index_ == '2':
		coupon_fish_photo_index_ = coupon_fish_.coupon_fish_photo_index
		
	# swich coupon photo index
	coupon_fish_ = COUPON_FISH.objects.get(coupon_fish_index=coupon_fish_index_)

	coupon_fish_.coupon_fish_photo_index = coupon_fish_photo_index_
	coupon_fish_.save()

	# code0 : success
	text = coupon_fish_.coupon_fish_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_remake_rice(request):
	page_title = 'request_remake_rice'
	# /request/remake/rice/?coupon_rice_index=1&coupon_rice_product_index=1&coupon_rice_photo_index=2&coupon_rice_market_name=bkabka&coupon_rice_name=sfs&coupon_rice_brand=dfdf&coupon_rice_unit=plp&coupon_rice_price=10&coupon_rice_disprice=5&coupon_rice_start=1&coupon_rice_finish=3&coupon_rice_detail=0&coupon_rice_type=0&coupon_rice_active=0&coupon_rice_making=111

	coupon_rice_index_ = request.POST.get('coupon_rice_index')
	coupon_rice_product_index_ = request.POST.get('coupon_rice_product_index')
	coupon_rice_photo_index_ = request.POST.get('coupon_rice_photo_index')
	coupon_rice_market_name_ =  request.POST.get('coupon_rice_market_name')
	coupon_rice_name_ = request.POST.get('coupon_rice_name')
	coupon_rice_brand_ = request.POST.get('coupon_rice_brand')
	coupon_rice_unit_ = request.POST.get('coupon_rice_unit')
	coupon_rice_area_ = request.POST.get('coupon_rice_area')
	coupon_rice_price_ = request.POST.get('coupon_rice_price')
	coupon_rice_disprice_ = request.POST.get('coupon_rice_disprice')
	coupon_rice_start_ = request.POST.get('coupon_rice_start')
	coupon_rice_finish_ = request.POST.get('coupon_rice_finish')
	coupon_rice_detail_ = request.POST.get('coupon_rice_detail')
	coupon_rice_detail_b_ = request.POST.get('coupon_rice_detail_b')
	coupon_rice_type_ = request.POST.get('coupon_rice_type')
	coupon_rice_active_ = request.POST.get('coupon_rice_active')
	coupon_rice_making_ = request.POST.get('coupon_rice_making')

	try:
		coupon_rice_ = COUPON_RICE.objects.get(coupon_rice_index=coupon_rice_index_)
	except:
		json_data = json.dumps(coupon_rice_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_rice_.coupon_rice_product_index = coupon_rice_product_index_
		coupon_rice_.coupon_rice_photo_index = coupon_rice_photo_index_
		coupon_rice_.coupon_rice_market_name = coupon_rice_market_name_
		coupon_rice_.coupon_rice_name = coupon_rice_name_
		coupon_rice_.coupon_rice_brand = coupon_rice_brand_
		coupon_rice_.coupon_rice_unit = coupon_rice_unit_
		coupon_rice_.coupon_rice_area = coupon_rice_area_
		coupon_rice_.coupon_rice_price = coupon_rice_price_
		coupon_rice_.coupon_rice_disprice = coupon_rice_disprice_
		coupon_rice_.coupon_rice_start = coupon_rice_start_
		coupon_rice_.coupon_rice_finish = coupon_rice_finish_
		coupon_rice_.coupon_rice_detail = coupon_rice_detail_
		coupon_rice_.coupon_rice_detail_b = coupon_rice_detail_b_
		coupon_rice_.coupon_rice_type = coupon_rice_type_
		coupon_rice_.coupon_rice_making = coupon_rice_making_

		coupon_rice_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_rice_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_rice' + '_' + str(coupon_rice_product_index_)+ '_' + str(coupon_rice_index_) + '_' + str(coupon_rice_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_rice_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_rice_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_rice_product_index_)
		coupon_rice_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_rice_photo_index_ == '2':
		coupon_rice_photo_index_ = coupon_rice_.coupon_rice_photo_index
		
	# swich coupon photo index
	coupon_rice_ = COUPON_RICE.objects.get(coupon_rice_index=coupon_rice_index_)

	coupon_rice_.coupon_rice_photo_index = coupon_rice_photo_index_
	coupon_rice_.save()

	# code0 : success
	text = coupon_rice_.coupon_rice_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')

 
@csrf_exempt
def request_remake_meat(request):
	page_title = 'request_remake_meat'
	# /request/remake/meat/?coupon_meat_index=1&coupon_meat_product_index=1&coupon_meat_photo_index=2&coupon_meat_market_name=bkabka&coupon_meat_name=sfs&coupon_meat_brand=dfdf&coupon_meat_unit=plp&coupon_meat_price=10&coupon_meat_disprice=5&coupon_meat_start=1&coupon_meat_finish=3&coupon_meat_detail=0&coupon_meat_type=0&coupon_meat_active=0&coupon_meat_making=111

	coupon_meat_index_ = request.POST.get('coupon_meat_index')
	coupon_meat_product_index_ = request.POST.get('coupon_meat_product_index')
	coupon_meat_photo_index_ = request.POST.get('coupon_meat_photo_index')
	coupon_meat_market_name_ =  request.POST.get('coupon_meat_market_name')
	coupon_meat_name_ = request.POST.get('coupon_meat_name')
	coupon_meat_brand_ = request.POST.get('coupon_meat_brand')
	coupon_meat_unit_ = request.POST.get('coupon_meat_unit')
	coupon_meat_area_ = request.POST.get('coupon_meat_area')
	coupon_meat_price_ = request.POST.get('coupon_meat_price')
	coupon_meat_disprice_ = request.POST.get('coupon_meat_disprice')
	coupon_meat_start_ = request.POST.get('coupon_meat_start')
	coupon_meat_finish_ = request.POST.get('coupon_meat_finish')
	coupon_meat_detail_ = request.POST.get('coupon_meat_detail')
	coupon_meat_detail_b_ = request.POST.get('coupon_meat_detail_b')
	coupon_meat_type_ = request.POST.get('coupon_meat_type')
	coupon_meat_active_ = request.POST.get('coupon_meat_active')
	coupon_meat_making_ = request.POST.get('coupon_meat_making')

	try:
		coupon_meat_ = COUPON_MEAT.objects.get(coupon_meat_index=coupon_meat_index_)
	except:
		json_data = json.dumps(coupon_meat_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_meat_.coupon_meat_product_index = coupon_meat_product_index_
		coupon_meat_.coupon_meat_photo_index = coupon_meat_photo_index_
		coupon_meat_.coupon_meat_market_name = coupon_meat_market_name_
		coupon_meat_.coupon_meat_name = coupon_meat_name_
		coupon_meat_.coupon_meat_brand = coupon_meat_brand_
		coupon_meat_.coupon_meat_unit = coupon_meat_unit_
		coupon_meat_.coupon_meat_area = coupon_meat_area_
		coupon_meat_.coupon_meat_price = coupon_meat_price_
		coupon_meat_.coupon_meat_disprice = coupon_meat_disprice_
		coupon_meat_.coupon_meat_start = coupon_meat_start_
		coupon_meat_.coupon_meat_finish = coupon_meat_finish_
		coupon_meat_.coupon_meat_detail = coupon_meat_detail_
		coupon_meat_.coupon_meat_detail_b = coupon_meat_detail_b_
		coupon_meat_.coupon_meat_type = coupon_meat_type_
		coupon_meat_.coupon_meat_making = coupon_meat_making_

		coupon_meat_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_meat_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_meat' + '_' + str(coupon_meat_product_index_)+ '_' + str(coupon_meat_index_) + '_' + str(coupon_meat_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_meat_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_meat_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_meat_product_index_)
		coupon_meat_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_meat_photo_index_ == '2':
		coupon_meat_photo_index_ = coupon_meat_.coupon_meat_photo_index
		
	# swich coupon photo index
	coupon_meat_ = COUPON_MEAT.objects.get(coupon_meat_index=coupon_meat_index_)

	coupon_meat_.coupon_meat_photo_index = coupon_meat_photo_index_
	coupon_meat_.save()

	# code0 : success
	text = coupon_meat_.coupon_meat_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_remake_egg(request):
	page_title = 'request_remake_egg'
	# /request/remake/egg/?coupon_egg_index=1&coupon_egg_product_index=1&coupon_egg_photo_index=2&coupon_egg_market_name=bkabka&coupon_egg_name=sfs&coupon_egg_brand=dfdf&coupon_egg_unit=plp&coupon_egg_price=10&coupon_egg_disprice=5&coupon_egg_start=1&coupon_egg_finish=3&coupon_egg_detail=0&coupon_egg_type=0&coupon_egg_active=0&coupon_egg_making=111

	coupon_egg_index_ = request.POST.get('coupon_egg_index')
	coupon_egg_product_index_ = request.POST.get('coupon_egg_product_index')
	coupon_egg_photo_index_ = request.POST.get('coupon_egg_photo_index')
	coupon_egg_market_name_ =  request.POST.get('coupon_egg_market_name')
	coupon_egg_name_ = request.POST.get('coupon_egg_name')
	coupon_egg_brand_ = request.POST.get('coupon_egg_brand')
	coupon_egg_unit_ = request.POST.get('coupon_egg_unit')
	coupon_egg_area_ = request.POST.get('coupon_egg_area')
	coupon_egg_price_ = request.POST.get('coupon_egg_price')
	coupon_egg_disprice_ = request.POST.get('coupon_egg_disprice')
	coupon_egg_start_ = request.POST.get('coupon_egg_start')
	coupon_egg_finish_ = request.POST.get('coupon_egg_finish')
	coupon_egg_detail_ = request.POST.get('coupon_egg_detail')
	coupon_egg_detail_b_ = request.POST.get('coupon_egg_detail_b')
	coupon_egg_type_ = request.POST.get('coupon_egg_type')
	coupon_egg_active_ = request.POST.get('coupon_egg_active')
	coupon_egg_making_ = request.POST.get('coupon_egg_making')

	try:
		coupon_egg_ = COUPON_EGG.objects.get(coupon_egg_index=coupon_egg_index_)
	except:
		json_data = json.dumps(coupon_egg_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_egg_.coupon_egg_product_index = coupon_egg_product_index_
		coupon_egg_.coupon_egg_photo_index = coupon_egg_photo_index_
		coupon_egg_.coupon_egg_market_name = coupon_egg_market_name_
		coupon_egg_.coupon_egg_name = coupon_egg_name_
		coupon_egg_.coupon_egg_brand = coupon_egg_brand_
		coupon_egg_.coupon_egg_unit = coupon_egg_unit_
		coupon_egg_.coupon_egg_area = coupon_egg_area_
		coupon_egg_.coupon_egg_price = coupon_egg_price_
		coupon_egg_.coupon_egg_disprice = coupon_egg_disprice_
		coupon_egg_.coupon_egg_start = coupon_egg_start_
		coupon_egg_.coupon_egg_finish = coupon_egg_finish_
		coupon_egg_.coupon_egg_detail = coupon_egg_detail_
		coupon_egg_.coupon_egg_detail_b = coupon_egg_detail_b_
		coupon_egg_.coupon_egg_type = coupon_egg_type_
		coupon_egg_.coupon_egg_making = coupon_egg_making_

		coupon_egg_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_egg_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_egg' + '_' + str(coupon_egg_product_index_)+ '_' + str(coupon_egg_index_) + '_' + str(coupon_egg_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_egg_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_egg_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_egg_product_index_)
		coupon_egg_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_egg_photo_index_ == '2':
		coupon_egg_photo_index_ = coupon_egg_.coupon_egg_photo_index
		
	# swich coupon photo index
	coupon_egg_ = COUPON_EGG.objects.get(coupon_egg_index=coupon_egg_index_)

	coupon_egg_.coupon_egg_photo_index = coupon_egg_photo_index_
	coupon_egg_.save()

	# code0 : success
	text = coupon_egg_.coupon_egg_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')
 

@csrf_exempt
def request_remake_ham(request):
	page_title = 'request_remake_ham'
	# /request/remake/ham/?coupon_ham_index=1&coupon_ham_product_index=1&coupon_ham_photo_index=2&coupon_ham_market_name=bkabka&coupon_ham_name=sfs&coupon_ham_brand=dfdf&coupon_ham_unit=plp&coupon_ham_price=10&coupon_ham_disprice=5&coupon_ham_start=1&coupon_ham_finish=3&coupon_ham_detail=0&coupon_ham_type=0&coupon_ham_active=0&coupon_ham_making=111

	coupon_ham_index_ = request.POST.get('coupon_ham_index')
	coupon_ham_product_index_ = request.POST.get('coupon_ham_product_index')
	coupon_ham_photo_index_ = request.POST.get('coupon_ham_photo_index')
	coupon_ham_market_name_ =  request.POST.get('coupon_ham_market_name')
	coupon_ham_name_ = request.POST.get('coupon_ham_name')
	coupon_ham_brand_ = request.POST.get('coupon_ham_brand')
	coupon_ham_unit_ = request.POST.get('coupon_ham_unit')
	coupon_ham_price_ = request.POST.get('coupon_ham_price')
	coupon_ham_disprice_ = request.POST.get('coupon_ham_disprice')
	coupon_ham_start_ = request.POST.get('coupon_ham_start')
	coupon_ham_finish_ = request.POST.get('coupon_ham_finish')
	coupon_ham_detail_ = request.POST.get('coupon_ham_detail')
	coupon_ham_detail_b_ = request.POST.get('coupon_ham_detail_b')
	coupon_ham_type_ = request.POST.get('coupon_ham_type')
	coupon_ham_active_ = request.POST.get('coupon_ham_active')
	coupon_ham_making_ = request.POST.get('coupon_ham_making')

	try:
		coupon_ham_ = COUPON_HAM.objects.get(coupon_ham_index=coupon_ham_index_)
	except:
		json_data = json.dumps(coupon_ham_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_ham_.coupon_ham_product_index = coupon_ham_product_index_
		coupon_ham_.coupon_ham_photo_index = coupon_ham_photo_index_
		coupon_ham_.coupon_ham_market_name = coupon_ham_market_name_
		coupon_ham_.coupon_ham_name = coupon_ham_name_
		coupon_ham_.coupon_ham_brand = coupon_ham_brand_
		coupon_ham_.coupon_ham_unit = coupon_ham_unit_
		coupon_ham_.coupon_ham_price = coupon_ham_price_
		coupon_ham_.coupon_ham_disprice = coupon_ham_disprice_
		coupon_ham_.coupon_ham_start = coupon_ham_start_
		coupon_ham_.coupon_ham_finish = coupon_ham_finish_
		coupon_ham_.coupon_ham_detail = coupon_ham_detail_
		coupon_ham_.coupon_ham_detail_b = coupon_ham_detail_b_
		coupon_ham_.coupon_ham_type = coupon_ham_type_
		coupon_ham_.coupon_ham_making = coupon_ham_making_

		coupon_ham_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_ham_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_ham' + '_' + str(coupon_ham_product_index_)+ '_' + str(coupon_ham_index_) + '_' + str(coupon_ham_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_ham_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_ham_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_ham_product_index_)
		coupon_ham_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_ham_photo_index_ == '2':
		coupon_ham_photo_index_ = coupon_ham_.coupon_ham_photo_index
		
	# swich coupon photo index
	coupon_ham_ = COUPON_HAM.objects.get(coupon_ham_index=coupon_ham_index_)

	coupon_ham_.coupon_ham_photo_index = coupon_ham_photo_index_
	coupon_ham_.save()

	# code0 : success
	text = coupon_ham_.coupon_ham_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')
 

@csrf_exempt
def request_remake_side(request):
	page_title = 'request_remake_side'
	# /request/remake/side/?coupon_side_index=1&coupon_side_product_index=1&coupon_side_photo_index=2&coupon_side_market_name=bkabka&coupon_side_name=sfs&coupon_side_brand=dfdf&coupon_side_unit=plp&coupon_side_price=10&coupon_side_disprice=5&coupon_side_start=1&coupon_side_finish=3&coupon_side_detail=0&coupon_side_type=0&coupon_side_active=0&coupon_side_making=111

	coupon_side_index_ = request.POST.get('coupon_side_index')
	coupon_side_product_index_ = request.POST.get('coupon_side_product_index')
	coupon_side_photo_index_ = request.POST.get('coupon_side_photo_index')
	coupon_side_market_name_ =  request.POST.get('coupon_side_market_name')
	coupon_side_name_ = request.POST.get('coupon_side_name')
	coupon_side_brand_ = request.POST.get('coupon_side_brand')
	coupon_side_unit_ = request.POST.get('coupon_side_unit')
	coupon_side_price_ = request.POST.get('coupon_side_price')
	coupon_side_disprice_ = request.POST.get('coupon_side_disprice')
	coupon_side_start_ = request.POST.get('coupon_side_start')
	coupon_side_finish_ = request.POST.get('coupon_side_finish')
	coupon_side_detail_ = request.POST.get('coupon_side_detail')
	coupon_side_detail_b_ = request.POST.get('coupon_side_detail_b')
	coupon_side_type_ = request.POST.get('coupon_side_type')
	coupon_side_active_ = request.POST.get('coupon_side_active')
	coupon_side_making_ = request.POST.get('coupon_side_making')

	try:
		coupon_side_ = COUPON_SIDE.objects.get(coupon_side_index=coupon_side_index_)
	except:
		json_data = json.dumps(coupon_side_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_side_.coupon_side_product_index = coupon_side_product_index_
		coupon_side_.coupon_side_photo_index = coupon_side_photo_index_
		coupon_side_.coupon_side_market_name = coupon_side_market_name_
		coupon_side_.coupon_side_name = coupon_side_name_
		coupon_side_.coupon_side_brand = coupon_side_brand_
		coupon_side_.coupon_side_unit = coupon_side_unit_
		coupon_side_.coupon_side_price = coupon_side_price_
		coupon_side_.coupon_side_disprice = coupon_side_disprice_
		coupon_side_.coupon_side_start = coupon_side_start_
		coupon_side_.coupon_side_finish = coupon_side_finish_
		coupon_side_.coupon_side_detail = coupon_side_detail_
		coupon_side_.coupon_side_detail_b = coupon_side_detail_b_
		coupon_side_.coupon_side_type = coupon_side_type_
		coupon_side_.coupon_side_making = coupon_side_making_

		coupon_side_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_side_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_side' + '_' + str(coupon_side_product_index_)+ '_' + str(coupon_side_index_) + '_' + str(coupon_side_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_side_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_side_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_side_product_index_)
		coupon_side_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_side_photo_index_ == '2':
		coupon_side_photo_index_ = coupon_side_.coupon_side_photo_index
		
	# swich coupon photo index
	coupon_side_ = COUPON_SIDE.objects.get(coupon_side_index=coupon_side_index_)

	coupon_side_.coupon_side_photo_index = coupon_side_photo_index_
	coupon_side_.save()

	# code0 : success
	text = coupon_side_.coupon_side_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_remake_water(request):
	page_title = 'request_remake_water'
	# /request/remake/water/?coupon_water_index=1&coupon_water_product_index=1&coupon_water_photo_index=2&coupon_water_market_name=bkabka&coupon_water_name=sfs&coupon_water_brand=dfdf&coupon_water_unit=plp&coupon_water_price=10&coupon_water_disprice=5&coupon_water_start=1&coupon_water_finish=3&coupon_water_detail=0&coupon_water_type=0&coupon_water_active=0&coupon_water_making=111

	coupon_water_index_ = request.POST.get('coupon_water_index')
	coupon_water_product_index_ = request.POST.get('coupon_water_product_index')
	coupon_water_photo_index_ = request.POST.get('coupon_water_photo_index')
	coupon_water_market_name_ =  request.POST.get('coupon_water_market_name')
	coupon_water_name_ = request.POST.get('coupon_water_name')
	coupon_water_brand_ = request.POST.get('coupon_water_brand')
	coupon_water_unit_ = request.POST.get('coupon_water_unit')
	coupon_water_price_ = request.POST.get('coupon_water_price')
	coupon_water_disprice_ = request.POST.get('coupon_water_disprice')
	coupon_water_start_ = request.POST.get('coupon_water_start')
	coupon_water_finish_ = request.POST.get('coupon_water_finish')
	coupon_water_detail_ = request.POST.get('coupon_water_detail')
	coupon_water_detail_b_ = request.POST.get('coupon_water_detail_b')
	coupon_water_type_ = request.POST.get('coupon_water_type')
	coupon_water_active_ = request.POST.get('coupon_water_active')
	coupon_water_making_ = request.POST.get('coupon_water_making')

	try:
		coupon_water_ = COUPON_WATER.objects.get(coupon_water_index=coupon_water_index_)
	except:
		json_data = json.dumps(coupon_water_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_water_.coupon_water_product_index = coupon_water_product_index_
		coupon_water_.coupon_water_photo_index = coupon_water_photo_index_
		coupon_water_.coupon_water_market_name = coupon_water_market_name_
		coupon_water_.coupon_water_name = coupon_water_name_
		coupon_water_.coupon_water_brand = coupon_water_brand_
		coupon_water_.coupon_water_unit = coupon_water_unit_
		coupon_water_.coupon_water_price = coupon_water_price_
		coupon_water_.coupon_water_disprice = coupon_water_disprice_
		coupon_water_.coupon_water_start = coupon_water_start_
		coupon_water_.coupon_water_finish = coupon_water_finish_
		coupon_water_.coupon_water_detail = coupon_water_detail_
		coupon_water_.coupon_water_detail_b = coupon_water_detail_b_
		coupon_water_.coupon_water_type = coupon_water_type_
		coupon_water_.coupon_water_making = coupon_water_making_

		coupon_water_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_water_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_water' + '_' + str(coupon_water_product_index_)+ '_' + str(coupon_water_index_) + '_' + str(coupon_water_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_water_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_water_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_water_product_index_)
		coupon_water_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_water_photo_index_ == '2':
		coupon_water_photo_index_ = coupon_water_.coupon_water_photo_index
		
	# swich coupon photo index
	coupon_water_ = COUPON_WATER.objects.get(coupon_water_index=coupon_water_index_)

	coupon_water_.coupon_water_photo_index = coupon_water_photo_index_
	coupon_water_.save()

	# code0 : success
	text = coupon_water_.coupon_water_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')
 

@csrf_exempt
def request_remake_instant(request):
	page_title = 'request_remake_instant'
	# /request/remake/instant/?coupon_instant_index=1&coupon_instant_product_index=1&coupon_instant_photo_index=2&coupon_instant_market_name=bkabka&coupon_instant_name=sfs&coupon_instant_brand=dfdf&coupon_instant_unit=plp&coupon_instant_price=10&coupon_instant_disprice=5&coupon_instant_start=1&coupon_instant_finish=3&coupon_instant_detail=0&coupon_instant_type=0&coupon_instant_active=0&coupon_instant_making=111

	coupon_instant_index_ = request.POST.get('coupon_instant_index')
	coupon_instant_product_index_ = request.POST.get('coupon_instant_product_index')
	coupon_instant_photo_index_ = request.POST.get('coupon_instant_photo_index')
	coupon_instant_market_name_ =  request.POST.get('coupon_instant_market_name')
	coupon_instant_name_ = request.POST.get('coupon_instant_name')
	coupon_instant_brand_ = request.POST.get('coupon_instant_brand')
	coupon_instant_unit_ = request.POST.get('coupon_instant_unit')
	coupon_instant_price_ = request.POST.get('coupon_instant_price')
	coupon_instant_disprice_ = request.POST.get('coupon_instant_disprice')
	coupon_instant_start_ = request.POST.get('coupon_instant_start')
	coupon_instant_finish_ = request.POST.get('coupon_instant_finish')
	coupon_instant_detail_ = request.POST.get('coupon_instant_detail')
	coupon_instant_detail_b_ = request.POST.get('coupon_instant_detail_b')
	coupon_instant_type_ = request.POST.get('coupon_instant_type')
	coupon_instant_active_ = request.POST.get('coupon_instant_active')
	coupon_instant_making_ = request.POST.get('coupon_instant_making')

	try:
		coupon_instant_ = COUPON_INSTANT.objects.get(coupon_instant_index=coupon_instant_index_)
	except:
		json_data = json.dumps(coupon_instant_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_instant_.coupon_instant_product_index = coupon_instant_product_index_
		coupon_instant_.coupon_instant_photo_index = coupon_instant_photo_index_
		coupon_instant_.coupon_instant_market_name = coupon_instant_market_name_
		coupon_instant_.coupon_instant_name = coupon_instant_name_
		coupon_instant_.coupon_instant_brand = coupon_instant_brand_
		coupon_instant_.coupon_instant_unit = coupon_instant_unit_
		coupon_instant_.coupon_instant_price = coupon_instant_price_
		coupon_instant_.coupon_instant_disprice = coupon_instant_disprice_
		coupon_instant_.coupon_instant_start = coupon_instant_start_
		coupon_instant_.coupon_instant_finish = coupon_instant_finish_
		coupon_instant_.coupon_instant_detail = coupon_instant_detail_
		coupon_instant_.coupon_instant_detail_b = coupon_instant_detail_b_
		coupon_instant_.coupon_instant_type = coupon_instant_type_
		coupon_instant_.coupon_instant_making = coupon_instant_making_

		coupon_instant_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_instant_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_instant' + '_' + str(coupon_instant_product_index_)+ '_' + str(coupon_instant_index_) + '_' + str(coupon_instant_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_instant_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_instant_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_instant_product_index_)
		coupon_instant_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_instant_photo_index_ == '2':
		coupon_instant_photo_index_ = coupon_instant_.coupon_instant_photo_index
		
	# swich coupon photo index
	coupon_instant_ = COUPON_INSTANT.objects.get(coupon_instant_index=coupon_instant_index_)

	coupon_instant_.coupon_instant_photo_index = coupon_instant_photo_index_
	coupon_instant_.save()

	# code0 : success
	text = coupon_instant_.coupon_instant_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')
 

@csrf_exempt
def request_remake_ice(request):
	page_title = 'request_remake_ice'
	# /request/remake/ice/?coupon_ice_index=1&coupon_ice_product_index=1&coupon_ice_photo_index=2&coupon_ice_market_name=bkabka&coupon_ice_name=sfs&coupon_ice_brand=dfdf&coupon_ice_unit=plp&coupon_ice_price=10&coupon_ice_disprice=5&coupon_ice_start=1&coupon_ice_finish=3&coupon_ice_detail=0&coupon_ice_type=0&coupon_ice_active=0&coupon_ice_making=111

	coupon_ice_index_ = request.POST.get('coupon_ice_index')
	coupon_ice_product_index_ = request.POST.get('coupon_ice_product_index')
	coupon_ice_photo_index_ = request.POST.get('coupon_ice_photo_index')
	coupon_ice_market_name_ =  request.POST.get('coupon_ice_market_name')
	coupon_ice_name_ = request.POST.get('coupon_ice_name')
	coupon_ice_brand_ = request.POST.get('coupon_ice_brand')
	coupon_ice_unit_ = request.POST.get('coupon_ice_unit')
	coupon_ice_price_ = request.POST.get('coupon_ice_price')
	coupon_ice_disprice_ = request.POST.get('coupon_ice_disprice')
	coupon_ice_start_ = request.POST.get('coupon_ice_start')
	coupon_ice_finish_ = request.POST.get('coupon_ice_finish')
	coupon_ice_detail_ = request.POST.get('coupon_ice_detail')
	coupon_ice_detail_b_ = request.POST.get('coupon_ice_detail_b')
	coupon_ice_type_ = request.POST.get('coupon_ice_type')
	coupon_ice_active_ = request.POST.get('coupon_ice_active')
	coupon_ice_making_ = request.POST.get('coupon_ice_making')

	try:
		coupon_ice_ = COUPON_ICE.objects.get(coupon_ice_index=coupon_ice_index_)
	except:
		json_data = json.dumps(coupon_ice_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_ice_.coupon_ice_product_index = coupon_ice_product_index_
		coupon_ice_.coupon_ice_photo_index = coupon_ice_photo_index_
		coupon_ice_.coupon_ice_market_name = coupon_ice_market_name_
		coupon_ice_.coupon_ice_name = coupon_ice_name_
		coupon_ice_.coupon_ice_brand = coupon_ice_brand_
		coupon_ice_.coupon_ice_unit = coupon_ice_unit_
		coupon_ice_.coupon_ice_price = coupon_ice_price_
		coupon_ice_.coupon_ice_disprice = coupon_ice_disprice_
		coupon_ice_.coupon_ice_start = coupon_ice_start_
		coupon_ice_.coupon_ice_finish = coupon_ice_finish_
		coupon_ice_.coupon_ice_detail = coupon_ice_detail_
		coupon_ice_.coupon_ice_detail_b = coupon_ice_detail_b_
		coupon_ice_.coupon_ice_type = coupon_ice_type_
		coupon_ice_.coupon_ice_making = coupon_ice_making_

		coupon_ice_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_ice_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_ice' + '_' + str(coupon_ice_product_index_)+ '_' + str(coupon_ice_index_) + '_' + str(coupon_ice_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_ice_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_ice_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_ice_product_index_)
		coupon_ice_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_ice_photo_index_ == '2':
		coupon_ice_photo_index_ = coupon_ice_.coupon_ice_photo_index
		
	# swich coupon photo index
	coupon_ice_ = COUPON_ICE.objects.get(coupon_ice_index=coupon_ice_index_)

	coupon_ice_.coupon_ice_photo_index = coupon_ice_photo_index_
	coupon_ice_.save()

	# code0 : success
	text = coupon_ice_.coupon_ice_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')
 

@csrf_exempt
def request_remake_bakery(request):
	page_title = 'request_remake_bakery'
	# /request/remake/bakery/?coupon_bakery_index=1&coupon_bakery_product_index=1&coupon_bakery_photo_index=2&coupon_bakery_market_name=bkabka&coupon_bakery_name=sfs&coupon_bakery_brand=dfdf&coupon_bakery_unit=plp&coupon_bakery_price=10&coupon_bakery_disprice=5&coupon_bakery_start=1&coupon_bakery_finish=3&coupon_bakery_detail=0&coupon_bakery_type=0&coupon_bakery_active=0&coupon_bakery_making=111

	coupon_bakery_index_ = request.POST.get('coupon_bakery_index')
	coupon_bakery_product_index_ = request.POST.get('coupon_bakery_product_index')
	coupon_bakery_photo_index_ = request.POST.get('coupon_bakery_photo_index')
	coupon_bakery_market_name_ =  request.POST.get('coupon_bakery_market_name')
	coupon_bakery_name_ = request.POST.get('coupon_bakery_name')
	coupon_bakery_brand_ = request.POST.get('coupon_bakery_brand')
	coupon_bakery_unit_ = request.POST.get('coupon_bakery_unit')
	coupon_bakery_price_ = request.POST.get('coupon_bakery_price')
	coupon_bakery_disprice_ = request.POST.get('coupon_bakery_disprice')
	coupon_bakery_start_ = request.POST.get('coupon_bakery_start')
	coupon_bakery_finish_ = request.POST.get('coupon_bakery_finish')
	coupon_bakery_detail_ = request.POST.get('coupon_bakery_detail')
	coupon_bakery_detail_b_ = request.POST.get('coupon_bakery_detail_b')
	coupon_bakery_type_ = request.POST.get('coupon_bakery_type')
	coupon_bakery_active_ = request.POST.get('coupon_bakery_active')
	coupon_bakery_making_ = request.POST.get('coupon_bakery_making')

	try:
		coupon_bakery_ = COUPON_BAKERY.objects.get(coupon_bakery_index=coupon_bakery_index_)
	except:
		json_data = json.dumps(coupon_bakery_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_bakery_.coupon_bakery_product_index = coupon_bakery_product_index_
		coupon_bakery_.coupon_bakery_photo_index = coupon_bakery_photo_index_
		coupon_bakery_.coupon_bakery_market_name = coupon_bakery_market_name_
		coupon_bakery_.coupon_bakery_name = coupon_bakery_name_
		coupon_bakery_.coupon_bakery_brand = coupon_bakery_brand_
		coupon_bakery_.coupon_bakery_unit = coupon_bakery_unit_
		coupon_bakery_.coupon_bakery_price = coupon_bakery_price_
		coupon_bakery_.coupon_bakery_disprice = coupon_bakery_disprice_
		coupon_bakery_.coupon_bakery_start = coupon_bakery_start_
		coupon_bakery_.coupon_bakery_finish = coupon_bakery_finish_
		coupon_bakery_.coupon_bakery_detail = coupon_bakery_detail_
		coupon_bakery_.coupon_bakery_detail_b = coupon_bakery_detail_b_
		coupon_bakery_.coupon_bakery_type = coupon_bakery_type_
		coupon_bakery_.coupon_bakery_making = coupon_bakery_making_

		coupon_bakery_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_bakery_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_bakery' + '_' + str(coupon_bakery_product_index_)+ '_' + str(coupon_bakery_index_) + '_' + str(coupon_bakery_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_bakery_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_bakery_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_bakery_product_index_)
		coupon_bakery_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_bakery_photo_index_ == '2':
		coupon_bakery_photo_index_ = coupon_bakery_.coupon_bakery_photo_index
		
	# swich coupon photo index
	coupon_bakery_ = COUPON_BAKERY.objects.get(coupon_bakery_index=coupon_bakery_index_)

	coupon_bakery_.coupon_bakery_photo_index = coupon_bakery_photo_index_
	coupon_bakery_.save()

	# code0 : success
	text = coupon_bakery_.coupon_bakery_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def request_remake_snack(request):
	page_title = 'request_remake_snack'
	# /request/remake/snack/?coupon_snack_index=1&coupon_snack_product_index=1&coupon_snack_photo_index=2&coupon_snack_market_name=bkabka&coupon_snack_name=sfs&coupon_snack_brand=dfdf&coupon_snack_unit=plp&coupon_snack_price=10&coupon_snack_disprice=5&coupon_snack_start=1&coupon_snack_finish=3&coupon_snack_detail=0&coupon_snack_type=0&coupon_snack_active=0&coupon_snack_making=111

	coupon_snack_index_ = request.POST.get('coupon_snack_index')
	coupon_snack_product_index_ = request.POST.get('coupon_snack_product_index')
	coupon_snack_photo_index_ = request.POST.get('coupon_snack_photo_index')
	coupon_snack_market_name_ =  request.POST.get('coupon_snack_market_name')
	coupon_snack_name_ = request.POST.get('coupon_snack_name')
	coupon_snack_brand_ = request.POST.get('coupon_snack_brand')
	coupon_snack_unit_ = request.POST.get('coupon_snack_unit')
	coupon_snack_price_ = request.POST.get('coupon_snack_price')
	coupon_snack_disprice_ = request.POST.get('coupon_snack_disprice')
	coupon_snack_start_ = request.POST.get('coupon_snack_start')
	coupon_snack_finish_ = request.POST.get('coupon_snack_finish')
	coupon_snack_detail_ = request.POST.get('coupon_snack_detail')
	coupon_snack_detail_b_ = request.POST.get('coupon_snack_detail_b')
	coupon_snack_type_ = request.POST.get('coupon_snack_type')
	coupon_snack_active_ = request.POST.get('coupon_snack_active')
	coupon_snack_making_ = request.POST.get('coupon_snack_making')

	try:
		coupon_snack_ = COUPON_SNACK.objects.get(coupon_snack_index=coupon_snack_index_)
	except:
		json_data = json.dumps(coupon_snack_index_)
		return HttpResponse(json_data, content_type='application/json')

	# remake coupon
	try:
		coupon_snack_.coupon_snack_product_index = coupon_snack_product_index_
		coupon_snack_.coupon_snack_photo_index = coupon_snack_photo_index_
		coupon_snack_.coupon_snack_market_name = coupon_snack_market_name_
		coupon_snack_.coupon_snack_name = coupon_snack_name_
		coupon_snack_.coupon_snack_brand = coupon_snack_brand_
		coupon_snack_.coupon_snack_unit = coupon_snack_unit_
		coupon_snack_.coupon_snack_price = coupon_snack_price_
		coupon_snack_.coupon_snack_disprice = coupon_snack_disprice_
		coupon_snack_.coupon_snack_start = coupon_snack_start_
		coupon_snack_.coupon_snack_finish = coupon_snack_finish_
		coupon_snack_.coupon_snack_detail = coupon_snack_detail_
		coupon_snack_.coupon_snack_detail_b = coupon_snack_detail_b_
		coupon_snack_.coupon_snack_type = coupon_snack_type_
		coupon_snack_.coupon_snack_making = coupon_snack_making_

		coupon_snack_.save()

	except:
		json_data = json.dumps('fail remake coupon')
		return HttpResponse(json_data, content_type='application/json')

	# have to change photo
	if coupon_snack_photo_index_ == '1':
		if request.method == 'POST':
			if 'file' in request.FILES:
				file = request.FILES['file']
				filename = 'm_snack' + '_' + str(coupon_snack_product_index_)+ '_' + str(coupon_snack_index_) + '_' + str(coupon_snack_market_name_)

			try:
				# default_storage
				pic_ = SP_PICTURE.objects.get(sp_name=filename)
				pic_.delete()

				link = 'sp_app/sp_pictures/sp_pictures/' + filename + '.png'
				default_storage.delete(link)
			except:
				# code1 : save photo fail
				json_data = json.dumps(filename)
				return HttpResponse(json_data, content_type='application/json')	

			try:
				pic_ = SP_PICTURE()
				pic_.sp_name = filename
				pic_.sp_picture.save(filename+'.png', File(file), save=True)	
			except:
				# code1 : save photo fail
				json_data = json.dumps('save photo fail')
				return HttpResponse(json_data, content_type='application/json')	
			pic_.save()

			# get remake photo index
			pic_now = SP_PICTURE.objects.get(sp_name=filename)
			coupon_snack_photo_index_ = pic_now.sp_photo_index

	# change photo to default
	elif coupon_snack_photo_index_ == '0':
		product_ = PRODUCT.objects.get(product_index=coupon_snack_product_index_)
		coupon_snack_photo_index_ = product_.product_photo_index

	# dont have to change photo
	elif coupon_snack_photo_index_ == '2':
		coupon_snack_photo_index_ = coupon_snack_.coupon_snack_photo_index
		
	# swich coupon photo index
	coupon_snack_ = COUPON_SNACK.objects.get(coupon_snack_index=coupon_snack_index_)

	coupon_snack_.coupon_snack_photo_index = coupon_snack_photo_index_
	coupon_snack_.save()

	# code0 : success
	text = coupon_snack_.coupon_snack_name
	json_data = json.dumps(text)
	return HttpResponse(json_data, content_type='application/json')



# coupon-----------------------------------------------------
# get coupones by state-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
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
@csrf_exempt
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
@csrf_exempt
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


# controll coupones-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
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


# ******************************************** ask index!!!
# chanage coupones state-----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
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

	json_data = json.dumps('success')
	return HttpResponse(json_data, content_type='application/json')
	
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
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

	json_data = json.dumps('success')
	return HttpResponse(json_data, content_type='application/json')

#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_reservation_change(request):
	page_title = 'request_reservation_change'

	reservation_coupon_category_ = request.GET.get('reservation_coupon_category')
	reservation_coupon_index_ = request.GET.get('reservation_coupon_index')

	if reservation_coupon_category_ == '1':
		reservation_coupon_category = 'daily'
		reservation_coupon_ = COUPON_DAILY.objects.get(coupon_daily_index=reservation_coupon_index_)
		reservation_coupon_.coupon_daily_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '2':
		reservation_coupon_category = 'greens'
		reservation_coupon_ = COUPON_GREENS.objects.get(coupon_greens_index=reservation_coupon_index_)
		reservation_coupon_.coupon_greens_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '3':
		reservation_coupon_category = 'fish'
		reservation_coupon_ = COUPON_FISH.objects.get(coupon_fish_index=reservation_coupon_index_)
		reservation_coupon_.coupon_fish_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '4':
		reservation_coupon_category = 'rice'
		reservation_coupon_ = COUPON_RICE.objects.get(coupon_rice_index=reservation_coupon_index_)
		reservation_coupon_.coupon_rice_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '5':
		reservation_coupon_category = 'meat'
		reservation_coupon_ = COUPON_MEAT.objects.get(coupon_meat_index=reservation_coupon_index_)
		reservation_coupon_.coupon_meat_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '6':
		reservation_coupon_category = 'egg'
		reservation_coupon_ = COUPON_EGG.objects.get(coupon_egg_index=reservation_coupon_index_)
		reservation_coupon_.coupon_egg_active = 0
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '7':
		reservation_coupon_category = 'ham'
		reservation_coupon_ = COUPON_HAM.objects.get(coupon_ham_index=reservation_coupon_index_)
		reservation_coupon_.coupon_ham_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '8':
		reservation_coupon_category = 'side'
		reservation_coupon_ = COUPON_SIDE.objects.get(coupon_side_index=reservation_coupon_index_)
		reservation_coupon_.coupon_side_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '9':
		reservation_coupon_category = 'water'
		reservation_coupon_ = COUPON_WATER.objects.get(coupon_water_index=reservation_coupon_index_)
		reservation_coupon_.coupon_water_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '10':
		reservation_coupon_category = 'instant'
		reservation_coupon_ = COUPON_INSTANT.objects.get(coupon_instant_index=reservation_coupon_index_)
		reservation_coupon_.coupon_instant_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '11':
		reservation_coupon_category = 'ice'
		reservation_coupon_ = COUPON_ICE.objects.get(coupon_ice_index=reservation_coupon_index_)
		reservation_coupon_.coupon_ice_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '12':
		reservation_coupon_category = 'bakery'
		reservation_coupon_ = COUPON_BAKERY.objects.get(coupon_bakery_index=reservation_coupon_index_)
		reservation_coupon_.coupon_bakery_active = 2
		reservation_coupon_.save()

	elif reservation_coupon_category_ == '13':
		reservation_coupon_category = 'snack'
		reservation_coupon_ = COUPON_SNACK.objects.get(coupon_snack_index=reservation_coupon_index_)
		reservation_coupon_.coupon_snack_active = 2
		reservation_coupon_.save()

	json_data = json.dumps('success')
	return HttpResponse(json_data, content_type='application/json')


# seller controll coupon *used*---------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_used_coupon(request):
	page_title = 'request_used_coupon'

	datas = []
	used_coupon_ = USER_COUPON_USEDLIST.objects.all()

	for d in used_coupon_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def request_used_make(request):
	page_title = 'request_used_coupon'


	used_make_coupon_index_ = request.GET.get('used_make_coupon_index', False)
	used_make_photo_index_ = request.GET.get('used_make_photo_index_', False)
	used_make_product_index_ = request.GET.get('used_make_product_index', False)
	used_make_userid_ = request.GET.get('used_make_userid', False)
	used_make_product_name_ = request.GET.get('used_make_product_name', False)
	used_make_product_brand_ = request.GET.get('used_make_product_brand', False)
	used_make_product_unit_ = request.GET.get('used_make_product_unit', False)
	used_make_product_price_ = request.GET.get('used_make_product_price', False)
	used_make_product_disprice_ = request.GET.get('used_make_product_disprice', False)
	used_make_product_photoindex_ = request.GET.get('used_make_photo_index', False)
	used_make_product_disprice_ = request.GET.get('used_make_product_disprice', False)
	used_make_product_category_ = request.GET.get('used_make_product_category', False)
	used_make_type_ = request.GET.get('used_make_type', False)
	used_make_when_ = request.GET.get('used_make_when', False)

	used_make_ = USER_COUPON_USEDLIST(user_coupon_usedlist_coupon_index=used_make_coupon_index_,
                                   user_coupon_usedlist_photo_index=used_make_product_photoindex_,
									  user_coupon_usedlist_userid=used_make_userid_,
									  user_coupon_usedlist_product_index=used_make_product_index_,
									  user_coupon_usedlist_product_name=used_make_product_name_,
									  user_coupon_usedlist_product_brand=used_make_product_brand_,
									  user_coupon_usedlist_product_unit=used_make_product_unit_,
									  user_coupon_usedlist_product_category=used_make_product_category_,
                                      user_coupon_usedlist_product_price=used_make_product_price_,
                                      user_coupon_usedlist_product_disprice=used_make_product_disprice_,
									  user_coupon_usedlist_type=used_make_type_,
									  user_coupon_usedlist_when=used_make_when_,)
	used_make_.save()

	json_data = json.dumps('used_list save success')
	return HttpResponse(json_data, content_type='application/json')
	

# controll favorite---------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def request_list_favorite(request):
	page_title = 'request_list_favorite'

	# list_favorite_userid_ = request.GET.get('list_favorite_userid', False)

	datas = []
	# list_favorite_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_)
	list_favorite_ = USER_FAVORITE_LIST.objects.all()

	for d in list_favorite_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def request_make_favorite(request):
	page_title = 'request_make_favorite'
	# /request/make/favorite/?list_favorite_userid=spotping&list_favorite_product_index=1&list_favorite_product_name=kimchi&list_favorite_product_brand=kk&list_favorite_product_unit=df&list_favorite_product_category=0

	list_favorite_userid_ = request.GET.get('list_favorite_userid', False)
	list_favorite_product_index_ = request.GET.get('list_favorite_product_index', False)
	list_favorite_product_name_ = request.GET.get('list_favorite_product_name', False)
	list_favorite_product_brand_ = request.GET.get('list_favorite_product_brand', False)
	list_favorite_product_unit_ = request.GET.get('list_favorite_product_unit', False)
	list_favorite_product_category_ = request.GET.get('list_favorite_product_category', False)

	favorite_product_ = USER_FAVORITE_LIST(user_favorite_list_userid=list_favorite_userid_, 
										   user_favorite_list_product_index=list_favorite_product_index_, 
										   user_favorite_list_product_name=list_favorite_product_name_, 
										   user_favorite_list_product_brand=list_favorite_product_brand_, 
										   user_favorite_list_product_unit=list_favorite_product_unit_, 
										   user_favorite_list_product_category=list_favorite_product_category_)
	
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

@csrf_exempt
def request_remake_favorite(request):
	page_title = 'request_remake_favorite'
	# 127.0.0.1:8000/request/remake/favorite/?list_favorite_userid=spotping&list_favorite_product_index_b=1&list_favorite_product_index_n=10&list_favorite_product_name=milk&list_favorite_product_brand=kkk&list_favorite_product_unit=df&list_favorite_product_category=0

	# have to get 'before product index', 'new product index'
	list_favorite_userid_ = request.GET.get('list_favorite_userid', False)
	list_favorite_product_index_b_ = request.GET.get('list_favorite_product_index_b', False)
	list_favorite_product_index_n_ = request.GET.get('list_favorite_product_index_n', False)
	list_favorite_product_name_ = request.GET.get('list_favorite_product_name', False)
	list_favorite_product_brand_ = request.GET.get('list_favorite_product_brand', False)
	list_favorite_product_unit_ = request.GET.get('list_favorite_product_unit', False)
	list_favorite_product_category_ = request.GET.get('list_favorite_product_category', False)

	favorite_product_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_).filter(user_favorite_list_product_index=list_favorite_product_index_b_)

	try:
		favorite_product_.update(user_favorite_list_product_index=list_favorite_product_index_n_, 
								 user_favorite_list_product_name=list_favorite_product_name_, 
								 user_favorite_list_product_brand=list_favorite_product_brand_, 
								 user_favorite_list_product_unit=list_favorite_product_unit_, 
								 user_favorite_list_product_category = list_favorite_product_category_)
	except:
		json_data = json.dumps('fail update coupon')
		return HttpResponse(json_data, content_type='application/json')

	datas = []
	list_favorite_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_)

	for d in list_favorite_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def request_delete_favorite(request):
	# page_ti127.0.0.1:8000/request/delete/favorite/?list_favorite_userid=spotping&list_favorite_product_index=2

	# have to get 'before product index', 'new product index'
	list_favorite_userid_ = request.GET.get('list_favorite_userid', False)
	list_favorite_product_index_ = request.GET.get('list_favorite_product_index_', False)

	favorite_product_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_).filter(user_favorite_list_product_index=list_favorite_product_index_)
	favorite_product_.delete()

	datas = []
	list_favorite_ = USER_FAVORITE_LIST.objects.filter(user_favorite_list_userid=list_favorite_userid_)

	for d in list_favorite_:
		data = model_to_dict(d)
		datas.append(data)

	json_data = json.dumps(datas)
	return HttpResponse(json_data, content_type='application/json')


# buyer join / login---------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
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
	join_buyer_id_ = request.GET.get('join_buyer_id', False)
	join_buyer_pwd_ = request.GET.get('join_buyer_pwd', False)
	join_buyer_name_ = request.GET.get('join_buyer_name', False)
	join_buyer_email_ = request.GET.get('join_buyer_email', False)

	join_buyer_photo_index_ = 1
	join_buyer_address_ = request.GET.get('join_buyer_address', False)
	join_buyer_phone_ = request.GET.get('join_buyer_phone', False)

	join_buyer_ = User.objects.create_user(join_buyer_id_, join_buyer_email_, join_buyer_pwd_)
	join_buyer_.first_name = join_buyer_name_
	join_buyer_.is_staff = False

	try:
		join_buyer_.save()
		join_buyer_info_ = USER_BUYER(user_buyer_id=join_buyer_, 
									  user_buyer_photo_index=join_buyer_photo_index_, 
									  user_buyer_address=join_buyer_address_, 
									  user_buyer_phone=join_buyer_phone_)
		join_buyer_info_.save()
	except:
		return HttpResponse('fail join')

	return HttpResponse('success join, %s' % join_buyer_id_)

#-------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def login_page_b(request):
	page_title = 'login_page_b'

	ctx = Context({'page_title':page_title,})
	ctx.update(csrf(request))

	return render_to_response('login_page_b.html', ctx)

@csrf_exempt
def request_login_buyer(request):
	callback = request.GET.get('callback')
	page_title = 'request_login_buyer'

	login_buyer_id_ = request.GET.get('buyer_id', False)
	login_buyer_pwd_ = request.GET.get('buyer_pwd', False)

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



