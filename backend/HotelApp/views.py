from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db import connection
# ระบบส่งไลน์
from songline import Sendline
# ระบบส่ง email เวลาเอาขึ้น server ตปท แล้ว gmail มันจะ block 
# from .emailsystem import sendthai
# Image
from django.core.files.storage import FileSystemStorage
# Paginator
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def Login(request):
    context={}
    if request.method=='POST':
        data=request.POST.copy()
        username=data.get('username')
        password=data.get('password')
        try:
            print('HERE 1\n')
            user=authenticate(username=username, password=password)
            login(request, user)
            print('HERE 2\n')
            return redirect('home-page')
        except:
            context['danger']='Username หรือ Password ไม่ถูกต้อง กรุณาติดต่อแอดมิน!'
            print('HERE 3\n')
    return render(request, 'frontend/login.html', context)

def Home(request):
    # cursor=connection.cursor()   # ทดสอบรัน complex transaction 3
    # query="SELECT h.Hotel_Id, AVG(t.Rating_Score) as Rating_Avg FROM transaction t, allbook a, room r, hotel h WHERE h.Hotel_Id LIKE r.Hotel_Id AND r.Room_Id LIKE a.Room_Id AND a.Transaction_Id LIKE t.Transaction_Id GROUP BY h.Hotel_Id;"
    # cursor.execute(query)
    # #row=cursor.fetchone()  
    # row=cursor.fetchall()
    # checkhotel=[]   # use to check whether we have this hotel rating or not (HTML)
    # for hotel in row:
    #     checkhotel.append(hotel[0])

    # allhotel=Hotel.objects.all()   # SELECT * from Hotel
    # context={'HotelHomePage':allhotel, 'CT3':row, 'checkhotel':checkhotel}
    # return render(request, 'frontend/home.html', context)
    return render(request, 'frontend/home.html')


def Hotels(request):
    return render(request, 'frontend/hotels.html')

def Promotions(request):
    return render(request, 'frontend/promotions.html')

def AboutUs(request):
    return render(request, 'frontend/about.html')
    
def ContactUs(request):
    context={}
    if request.method=='POST':
        data=request.POST.copy()
        title=data.get('title')
        email=data.get('email')
        detail=data.get('detail')
        print(title)
        print(email)
        print(detail)
        print('----------------\n')
        if title=='' or email=='':
            context['danger']='กรุณากรอกแบบฟอร์มให้ครบถ้วน!'
            return render(request, 'frontend/contact.html', context)
        # record info
        # newrecord=ContactList()
        # newrecord.title=title
        # newrecord.email=email
        # newrecord.detail=detail
        # newrecord.save()
        # ContactList(title=title, email=email, detail=detail).save()
        context['message']='ขอบคุณสำหรับข้อความ แอดมินจะติดต่อคุณกลับภายใน 24 ชั่วโมง'

        # ส่งไลน์ from songline import Sendline (https://pypi.org/project/songline/)
        token='o6Tfmj8FPGp6egjxwVjnOrMpLhfoZRb9520DBiWOxuV'  # เอามาจาก Line notify
        linenoti=Sendline(token)
        linenoti.sendtext('\nหัวข้อ: {}\nอีเมลล์: {}\nรายละเอียด: {}'.format(title, email, detail))
        # ส่งอีเมลล์ from .emailsystem import sendthai
        # text='สวัสดีคุณลูกค้า\n\nทางเราได้รับปัญหาที่ท่านสอบถามเรียบร้อยแล้ว แอดมินจะรีบทำการติดต่อกลับโดยเร็วที่สุด\n\n--แอดมิน--\n'
        # sendthai(email, 'Hotel Poonveh: สอบถามปัญหา', text)
    return render(request, 'frontend/contact.html', context)

# from django.contrib.auth.models import User
import uuid
def Register(request):
    context={}
    if request.method=='POST':
        data=request.POST.copy()
        nic=data.get('nic')
        fname=data.get('fname')
        lname=data.get('lname')
        username=data.get('username')
        email=data.get('email')
        tel=data.get('tel')
        address=data.get('address')
        password1=data.get('password1')
        password2=data.get('password2')
        context['GetFirstname']=fname  # ช่วยกรอกให้ใหม่
        context['GetLastname']=lname
        context['GetNIC']=nic
        context['GetTel']=tel
        context['GetAddress']=address
        print("ADDR= ", address)
        # ใช้ try except ซ้อนกันแล้วมัน pass ไปเลย ติด if ไว้ดีกว่า, เผื่อ fill ช่องให้ผู้ใช้ด้วย
        if User.objects.filter(username=username):  
            context['danger_message1']='Username "{}" มีในระบบแล้ว กรุณาใช้ username อื่น'.format(username)
        else:
            context['GetUsername']=username
        if User.objects.filter(email=email):
            context['danger_message2']='Email "{}" มีในระบบแล้ว กรุณาใช้ email อื่น'.format(email)
        else:
            context['GetEmail']=email
        if password1 != password2:  
            context['danger_message3']='password ของคุณไม่ตรงกัน'  
        if 'danger_message1' in context or 'danger_message2' in context or 'danger_message3' in context:
            return render(request, 'frontend/register.html', context)   
        else:
            newuser=User()
            newuser.first_name=fname
            newuser.last_name=lname
            newuser.username=username
            newuser.email=email
            newuser.set_password(password1)
            newuser.save()
            print('F1\n')

            u=uuid.uuid1()  # random UUID https://pynative.com/python-uuid-module-to-generate-universally-unique-identifiers/
            token=str(u)

            print('F2\n')
            newmember=Member()
            newmember.user=User.objects.get(username=username)
            newmember.Member_fName=fname
            newmember.Member_lName=lname
            newmember.Member_Email=email
            newmember.Member_Username=username
            newmember.Member_Password=password1
            newmember.Member_NIC=nic
            newmember.Member_Address=address
            newmember.Member_Tel=tel
            # ใส่รูปภาพ
            if 'picture' in request.FILES:
                print('F3\n')
                file_img=request.FILES['picture']
                file_img_name=file_img.name.replace(' ', '-')
                # from django.core.files.storage import FileSystemStorage
                fs=FileSystemStorage(location='media/profile')  # ระบุบ folder ที่เซฟไป
                filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
                upload_file_url=fs.url(filename)  # ให้ไปเอา URL มา จะได้บอก server ถูกว่ารูปนี้อยู่ไหน (ระบุ MEDIA_ROOT แล้ว)
                print('Pic URL:', upload_file_url)  # Pic URL:  /media/play-5-wow.jpg
                newmember.Member_Pic='/profile'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
            else:
                print('numa numa yeah! numa numa yeah yeah yeah!')

            print('F4\n')
            newmember.save()
            #text='สวัสดีคุณ '+fname+' '+lname+'\n\nเราขอขอบคุณที่ท่านได้ทำการสมัครสมาชิคของเว็บไซต์เรา\nกรุณากดลิงค์นี้เพื่อทำการ ยืนยันการเป็นสมาชิคของท่าน\n\nLink: http://localhost:8000/verify-email/'+token+'\n\n--ทีมงาน PoonVeh--'
            #sendthai(email, 'PoonVeh: ยืนยันการสมัครสมาชิค', text)

        try:
            user=authenticate(username=username, password=password1)
            login(request, user)
            return redirect('profile-page')
        except:
            context['danger_message4']='คุณกรอก Username หรือ Password ไม่ถูกต้อง กรุณาติดต่อแอดมิน!'
    return render(request, 'frontend/register.html', context)

@login_required
def Booking(request):
    return render(request, 'frontend/booking.html')

@login_required
def News(request):
    return render(request, 'frontend/news.html')

@login_required
def ProfilePage(request):
    context={}
    profileuser=User.objects.get(username=request.user.username)
    context['profileInfo']=profileuser
    if request.method == 'POST':
        context['notyet']='To use this feature, we need to complete the signup page in order to continue using member subscription information from DBMS (Devil Based Management Shrine).'
    return render(request, 'frontend/profile.html', context)

def TestStaff(request):
    allbooks=AllBook.objects.all()
    allstuff=StaffManager.objects.all()
    allnews=News.objects.all()
    testcontext={'StaffManagerTest':allstuff, 'NewsTest':allnews, 'AllBookTest':allbooks,}
    return render(request, 'hotelapp/testsql.html', testcontext)
