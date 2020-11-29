import hashlib
import random
import time
import urllib
import uuid

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from user.models import Publisher
from django.conf import global_settings

def create(request):
    if request.method=='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state_province = request.POST.get('state_province')
        country = request.POST.get('country')

        pub = Publisher.objects.create(name=name,password=password,address=address,city=city,state_province=state_province,country=country)
        pub.save()
    else:
        return render(request,'register.html')
    return render(request,'login.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if Publisher.objects.filter(name=name,password=password).exists():
           response=redirect(reverse('user:index'))
           # cookies设置
           # response.set_cookie('name',name,max_age=300)
           # session设置
           request.session['name']=name
           return response
        else:
            return render(request,'login.html',{'message':'用户或密码错误'})
    return render(request,'login.html')

def index(request):
    user=Publisher.objects.all()
    count = user.count()
    # 设置cookies
    # name = request.COOKIES.get('name',None)
    # 设置session
    name=request.session.get('name')
    return render(request,'index.html',{'users':user,'counts':count,'name':name})

def logout(request):
    # response = redirect(reverse('user:index'))
    # response.delete_cookie('name')
    # return response
    request.session.flush()
    return redirect(reverse('user:index'))


def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        # user=Publisher.objects.filter(address__istartswith=search)
        user = Publisher.objects.filter(name__istartswith=search).order_by('-id')
        return render(request,'index.html',{'users':user})

def detail(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state_province = request.POST.get('state_province')
        country = request.POST.get('country')
        result=Publisher.objects.filter(id=id).update(name=name,address=address,city=city,state_province=state_province,country=country)
        print(result)
        return redirect(reverse('user:index'))
    else:
        id=request.GET.get('id')
        user=Publisher.objects.get(id=id)
        return render(request,'detail.html',{'user':user})

def delete(request,id):
    # 逻辑删除
    user = Publisher.objects.get(id=id)
    user.delete()
    # user.isdelete=True
    # user.save()
    # 物理删除
    # user=Publisher.objects.filter(id=id).delete()
    return redirect(reverse('user:index'))



def send_message(request):
    mobile=request.GET.get('mobile')
    url='https://api.netease.im/sms/sendcode.action'
    headers={}
    headers['Content-Type']='application/x-www-form-urlencoded;charset=utf-8'
    headers['AppKey']='27c4550ebac18553d1aad61fb5e01512'
    Nonce=str(uuid.uuid4()).replace('-','')
    headers['Nonce']=Nonce
    CurTime=str(int(time.time()))
    headers['CurTime']=CurTime
    AppSecret='7413b1296a89'
    CheckSum=hashlib.sha1((AppSecret + Nonce + CurTime).encode('utf-8')).hexdigest().lower()
    headers['CheckSum']= CheckSum
    respone=requests.post(url,data={'mobile':mobile},headers=headers)
    json_str=respone.json()
    print(json_str)
    if json_str.get('code')==200:
        request.session['code']=json_str.get('obj')
        return JsonResponse({'status':200,'msg':'验证码发送成功'})
    else:
        return JsonResponse({'status':json_str.code, 'msg': '验证码发送失败'})










