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
            user=authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context['danger']='Username or Password is invalid. Please contact administrator.'
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
    # SELECT * FROM `hotel`;
    allhotel=Hotel.objects.all().order_by('id')
    hotel_per_page=3
    paginator=Paginator(allhotel, hotel_per_page)
    page=request.GET.get('page')   # localhost:800/?page=2
    allhotel=paginator.get_page(page)
    print('count:', len(allhotel))
    context={'AllHotel':allhotel}
    # แยกแถวละ 3
    allrow=[]
    row=[]
    for i, p in enumerate(allhotel):
        if i%3 == 0:
            if i!= 0:
                allrow.append(row)
            row=[]
            row.append(p)
        else:
            row.append(p)
    if len(row) != 0:
        allrow.append(row)
    context['AllRow']=allrow
    print("CHECK:", allrow)
    return render(request, 'frontend/hotels.html', context)

def Promotions(request):
    # SELECT * FRMO `promotion`;
    allpromotion=Promotion.objects.all().order_by('id')
    for i in allpromotion:
        i.Promotion_Discount*=100  # convert when displaying %

    promotion_per_page=3
    paginator=Paginator(allpromotion, promotion_per_page)
    page=request.GET.get('page')
    allpromotion=paginator.get_page(page)
    context={'AllPromotion':allpromotion}
    allrow=[]
    row=[]
    for i, p in enumerate(allpromotion):
        if i%3 == 0:
            if i!= 0:
                allrow.append(row)
            row=[]
            row.append(p)
        else:
            row.append(p)
    if len(row) != 0:
        allrow.append(row)
    context['AllRow']=allrow
    return render(request, 'frontend/promotions.html', context)

def AboutUs(request):
    return render(request, 'frontend/about.html')
    
from dotenv import load_dotenv
import os
load_dotenv()
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
            context['danger']='Please complete the form!'
            return render(request, 'frontend/contact.html', context)
        # record info
        # newrecord=ContactList()
        # newrecord.title=title
        # newrecord.email=email
        # newrecord.detail=detail
        # newrecord.save()
        # ContactList(title=title, email=email, detail=detail).save()
        context['message']='Thank you for the message. Admin will contact you back within 24 hours!'

        # ส่งไลน์ from songline import Sendline (https://pypi.org/project/songline/)
        token=os.getenv('LINE_TOKEN')
        linenoti=Sendline(token)
        linenoti.sendtext('\nTopic: {}\nEmail: {}\nDetail: {}'.format(title, email, detail))
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
            context['danger_message1']='Username "{}" already in the system, please use another username!'.format(username)
        else:
            context['GetUsername']=username
        if User.objects.filter(email=email):
            context['danger_message2']='Email "{}" already in the system, please use another email!'.format(email)
        else:
            context['GetEmail']=email
        if password1 != password2:  
            context['danger_message3']='your passwords do not match.'  
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

            u=uuid.uuid1()  # random UUID https://pynative.com/python-uuid-module-to-generate-universally-unique-identifiers/
            token=str(u)

            newmember=Member()
            newmember.user=User.objects.get(username=username)
            newmember.Member_NIC=nic
            newmember.Member_Tel=tel
            newmember.Member_Address=address
            # ใส่รูปภาพ
            if 'picture' in request.FILES:
                newmember.Member_Pic=request.FILES['picture']  # upload to cloudinary
                print('Cloud PATH:', newmember.Member_Pic)
                # file_img=request.FILES['picture']
                # file_img_name=file_img.name.replace(' ', '-')
                # # from django.core.files.storage import FileSystemStorage
                # fs=FileSystemStorage(location='media/profile')  # ระบุบ folder ที่เซฟไป
                # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
                # upload_file_url=fs.url(filename)  # ให้ไปเอา URL มา จะได้บอก server ถูกว่ารูปนี้อยู่ไหน (ระบุ MEDIA_ROOT แล้ว)
                # print('Pic URL:', upload_file_url)  # Pic URL:  /media/play-5-wow.jpg
                # newmember.Member_Pic='/profile'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป

            newmember.save()
            #text='สวัสดีคุณ '+fname+' '+lname+'\n\nเราขอขอบคุณที่ท่านได้ทำการสมัครสมาชิคของเว็บไซต์เรา\nกรุณากดลิงค์นี้เพื่อทำการ ยืนยันการเป็นสมาชิคของท่าน\n\nLink: http://localhost:8000/verify-email/'+token+'\n\n--ทีมงาน PoonVeh--'
            #sendthai(email, 'PoonVeh: ยืนยันการสมัครสมาชิค', text)

        try:
            user=authenticate(username=username, password=password1)
            login(request, user)
            return redirect('profile-page')
        except:
            context['danger_message4']='you have entered an incorrect Username or Password, please contact the admin!'
    return render(request, 'frontend/register.html', context)

@login_required
def ProfilePage(request):
    context={}
    profileuser=User.objects.get(username=request.user.username)
    context['profileInfo']=profileuser
    if request.method == 'POST':
        data=request.POST.copy()
        fname=data.get('fname')
        lname=data.get('lname')
        nic=data.get('nic')
        tel=data.get('tel')
        address=data.get('address')
        newpass=data.get('password')
        profileuser.first_name=fname
        profileuser.last_name=lname
        profileuser.set_password(newpass)
        profileuser.save()
        editmember=Member.objects.get(id=profileuser.id)
        editmember.Member_NIC=nic
        editmember.Member_Tel=tel
        editmember.Member_Address=address
        if 'picture' in request.FILES:
            editmember.Member_Pic=request.FILES['picture']  # upload to cloudinary
            print('Cloud PATH:', editmember.Member_Pic)
        editmember.save()
        context['update']='Your profile page has been updated!'
    return render(request, 'frontend/profile.html', context)

@login_required
def SearchMember(request):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')
    context={}
    alluser=User.objects.all().order_by('id')
    context['result_user']=alluser
    if request.method == 'POST':
        data=request.POST.copy()
        search_index=data.get('search-in-db')
        search_index=int(search_index)
        print('search Id=', search_index)
        if search_index == 1:
            m_id=data.get('m_id')  # ต้องเช็คว่าเป็น int ไหม เด่วบึ้ม
            if not m_id:  # empty string are false
                context['search_all']='Search all instead!'
                return render(request, 'frontend/searchmember.html', context)
            m_id=m_id[1:]
            if not m_id.isnumeric():
                context['search_boom']='Please input correct format in order to search member!'
                return render(request, 'frontend/searchmember.html', context)
            m_id=int(m_id)
            alluser=User.objects.filter(id=m_id).order_by('id')
        if search_index == 2:
            user=data.get('user')
            if not user:  # empty string are falsy
                context['search_all']='Search all instead!'
                return render(request, 'frontend/searchmember.html', context)
            alluser=User.objects.filter(username__contains=user).order_by('username')
        if search_index == 3:
            fname=data.get('fname')
            if not fname:
                context['search_all']='Search all instead!'
                return render(request, 'frontend/searchmember.html', context)
            alluser=User.objects.filter(first_name__contains=fname).order_by('first_name')
        if search_index == 4:
            lname=data.get('lname')
            if not lname:
                context['search_all']='Search all instead!'
                return render(request, 'frontend/searchmember.html', context)
            alluser=User.objects.filter(last_name__contains=lname).order_by('last_name')
        if search_index == 5:
            email=data.get('email')
            if not email:
                context['search_all']='Search all instead!'
                return render(request, 'frontend/searchmember.html', context)
            alluser=User.objects.filter(email__contains=email).order_by('email')
        context['result_user']=alluser
        context['finish_search']='You can see your search result below!'
    return render(request, 'frontend/searchmember.html', context)

@login_required
def EditMember(request, user_id):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')
    edituser=User.objects.get(id=user_id)
    context={}
    context['profileInfo']=edituser
    hotellist=Hotel.objects.all().order_by('id')  # เอาไว้เผื่อ add staff
    context['hotellist']=hotellist
    if request.method == 'POST':
        data=request.POST.copy()
        if 'save' in data:
            fname=data.get('fname')
            lname=data.get('lname')
            nic=data.get('nic')
            tel=data.get('tel')
            address=data.get('address')
            point=data.get('point')
            edituser.first_name=fname
            edituser.last_name=lname
            edituser.save()
            editmember=Member.objects.get(id=edituser.id)
            editmember.Member_NIC=nic
            editmember.Member_Tel=tel
            editmember.Member_Address=address
            editmember.Member_Point=point
            if 'picture' in request.FILES:
                editmember.Member_Pic=request.FILES['picture']  # upload to cloudinary
                print('Cloud PATH:', editmember.Member_Pic)
            editmember.save()
            context['update']='Updated M'+str(edituser.id)+' profile information!'
        if 'add' in data:
            hotel=data.get('hotel')
            hotel=hotel[1]  # เอาเฉพาะเลข id
            pos=data.get('pos')
            workdate=data.get('date')
            level=data.get('level')
            level=level[6:]  # ตัด 'Level '

            newstaff=Staff()
            newstaff.member=Member.objects.get(id=edituser.id)
            newstaff.Hotel_Id=Hotel.objects.get(id=hotel)
            newstaff.Staff_Position=pos
            newstaff.Staff_Start=workdate
            newstaff.Staff_Level=level
            newstaff.save()
            edituser.is_staff=True
            edituser.save()
            context['adding']='Adding M'+str(edituser.id)+' to be staff!'
        if 'remove' in data:   # 100% be staff
            Staff.objects.get(member=edituser.id).delete()
            edituser.is_staff=False
            edituser.save()
            context['revoke']='Revoke the staff role from M'+str(edituser.id)+' account!'
        if 'ban' in data:
            edituser.is_active=False
            edituser.save()
            context['ban_op']='M'+str(edituser.id)+' account has been suspended!'
        if 'unban' in data:
            edituser.is_active=True
            edituser.save()
            context['ban_op']='M'+str(edituser.id)+' account has been unbanned!'
        if 'resetpassword' in data:
            u=uuid.uuid1()  # random UUID
            newpass=str(u)
            edituser.set_password(newpass)
            edituser.save()
            context['newpass']='M'+str(edituser.id)+"'s password was reset, please copy this new password and send it to user!"
            context['tokenpass']=newpass
    return render(request, 'frontend/editmember.html', context)

@login_required
def AddHotel(request):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')

    context={}
    if request.method == 'POST':
        data=request.POST.copy()
        hotel_name=data.get('name')
        hotel_address=data.get('address')
        hotel_detail=data.get('detail')

        newhotel=Hotel()
        newhotel.Hotel_Name=hotel_name
        newhotel.Hotel_Address=hotel_address
        newhotel.Hotel_Detail=hotel_detail
        if 'picture' in request.FILES:
            newhotel.Hotel_Pic=request.FILES['picture']  # upload to cloudinary
            print('Cloud PATH:', newhotel.Hotel_Pic)
            # file_img=request.FILES['picture']
            # file_img_name=file_img.name.replace(' ', '-')
            # # from django.core.files.storage import FileSystemStorage
            # fs=FileSystemStorage(location='media/hotel')  # ระบุบ folder ที่เซฟไป
            # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
            # upload_file_url=fs.url(filename)  # ให้ไปเอา URL มา จะได้บอก server ถูกว่ารูปนี้อยู่ไหน (ระบุ MEDIA_ROOT แล้ว)
            # print('Pic URL:', upload_file_url)  # Pic URL:  /media/play-5-wow.jpg
            # newhotel.Hotel_Pic='/hotel'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
        newhotel.save()
        context['addnew']='The system has added the hotel to the database.'
    return render(request, 'frontend/addhotel.html', context)

def HotelDetail(request, hotel_id):
    hotel=Hotel.objects.get(id=hotel_id)
    room=Room.objects.all().order_by('id')
    reviews=Transaction.objects.filter(Transaction_Rating__gte=1).order_by('-id')
    # JOIN 3 TABLES
    cur_rating=0
    total_rating=0
    showreviews=[]  # show only the man that gave rating score (in order to save space and can be used to calculate the cumulative rating)
    for i in range(0, len(reviews)):
        if reviews[i].room.hotel == hotel:
            cur_rating+=reviews[i].Transaction_Rating
            total_rating+=1
            if len(showreviews) < 4:
                showreviews.append(reviews[i])
    if cur_rating:
        cur_rating/=total_rating
    context={}
    context['cur_rating']=cur_rating
    context['showreviews']=showreviews
    available_room=Room.objects.filter(hotel=hotel, Room_Status=True)
    context['Hotel']=hotel
    context['available_room']=available_room
    if request.method == 'POST':
        data=request.POST.copy()
        if 'save' in data:
            print('save data')
            name=data.get('name')
            address=data.get('address')
            detail=data.get('detail')
            hotel.Hotel_Name=name
            hotel.Hotel_Address=address
            hotel.Hotel_Detail=detail
            if 'picture' in request.FILES:
                hotel.Hotel_Pic=request.FILES['picture']  # upload to cloudinary
                print('Cloud PATH:', hotel.Hotel_Pic)
                # file_img=request.FILES['picture']
                # file_img_name=file_img.name.replace(' ', '-')
                # fs=FileSystemStorage(location='media/hotel')
                # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
                # upload_file_url=fs.url(filename)
                # print('Pic URL:', upload_file_url)
                # hotel.Hotel_Pic='/hotel'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
            hotel.save()
            context['Hotel']=hotel  # เซฟแล้วให้มันส่งข้อมูลใหม่ไปโชว์ใน field แทน
        elif 'delete' in data:
            print('delete data')
            hotel.delete()
            return redirect('hotels-page')
        elif 'book' in data:
            room_id=data.get('room_id')
            count=data.get('count')
            room_id=room_id[2:]
            for i in range(0, len(room_id)):
                if room_id[i] == ' ':
                    room_id=room_id[:i]
                    break
            newtrans=Transaction()
            newtrans.member=request.user.member
            newtrans.room=Room.objects.get(id=room_id)
            newtrans.Transaction_Night=abs(int(count))  # use abs if jsscript doesn't work
            newtrans.Transaction_Price=abs(int(count))*newtrans.room.roomtype.Type_Pernight
            newtrans.save()
            lock=Room.objects.get(id=room_id)  # lock room
            lock.Room_Status=False
            lock.save()
            context['add_book']='The system has added your booking information. You can check it on your Bookings page!'
    return render(request, 'frontend/hoteldetail.html', context)

@login_required
def AddPromotion(request):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')

    context={}
    if request.method == 'POST':
        data=request.POST.copy()
        name=data.get('name')
        detail=data.get('detail')
        discount=data.get('percent')
        start=data.get('start')
        end=data.get('end')
        print(int(discount[:-1])/100)
        print(start)
        print(end)

        newpromo=Promotion()
        newpromo.Promotion_Name=name
        newpromo.Promotion_Detail=detail
        newpromo.Promotion_Discount=int(discount[:-1])/100   # ด้านหลังสุดเป็น %
        newpromo.Promotion_Start=start
        newpromo.Promotion_End=end
        if 'picture' in request.FILES:
            newpromo.Promotion_Pic=request.FILES['picture']  # upload to cloudinary
            print('Cloud PATH:', newpromo.Promotion_Pic)
            # file_img=request.FILES['picture']
            # file_img_name=file_img.name.replace(' ', '-')
            # # from django.core.files.storage import FileSystemStorage
            # fs=FileSystemStorage(location='media/promotion')  # ระบุบ folder ที่เซฟไป
            # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
            # upload_file_url=fs.url(filename)  # ให้ไปเอา URL มา จะได้บอก server ถูกว่ารูปนี้อยู่ไหน (ระบุ MEDIA_ROOT แล้ว)
            # print('Pic URL:', upload_file_url)  # Pic URL:  /media/play-5-wow.jpg
            # newpromo.Promotion_Pic='/promotion'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
        newpromo.save()
        context['addnew']='The system has added the promotion to the database.'
    return render(request, 'frontend/addpromotion.html', context)

def PromotionDetail(request, promo_id):
    promotion=Promotion.objects.get(id=promo_id)
    context={}
    context['Promotion']=promotion
    context['StartFormat']=promotion.Promotion_Start
    context['EndFormat']=promotion.Promotion_End
    print(promotion.Promotion_Name)
    print(context['StartFormat'])
    print(context['EndFormat'])
    if request.method == 'POST':
        data=request.POST.copy()
        if 'save' in data:
            print('save data')
            name=data.get('name')
            detail=data.get('detail')
            discount=data.get('percent')
            start=data.get('start')
            end=data.get('end')
            promotion.Promotion_Name=name
            promotion.Promotion_Detail=detail
            print(int(discount[:-1]))
            promotion.Promotion_Discount=int(discount[:-1])/100
            promotion.Promotion_Start=start
            promotion.Promotion_End=end
            if 'picture' in request.FILES:
                promotion.Promotion_Pic=request.FILES['picture']  # upload to cloudinary
                print('Cloud PATH:', promotion.Promotion_Pic)
                # file_img=request.FILES['picture']
                # file_img_name=file_img.name.replace(' ', '-')
                # fs=FileSystemStorage(location='media/promotion')
                # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
                # upload_file_url=fs.url(filename)
                # print('Pic URL:', upload_file_url)
                # promotion.Promotion_Pic='/promotion'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
            promotion.save()
            context['Promotion']=promotion  # เซฟแล้วให้มันส่งข้อมูลใหม่ไปโชว์ใน field แทน

        elif 'delete' in data:
            print('delete data')
            promotion.delete()
            return redirect('promotions-page')

    return render(request, 'frontend/promotiondetail.html', context)

@login_required
def AddNews(request):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')
    context={}
    if request.method == 'POST':
        data=request.POST.copy()
        name=data.get('name')
        detail=data.get('detail')
        print(name)
        print(detail)
        newnews=News()
        newnews.News_Name=name
        newnews.News_Detail=detail
        if 'picture' in request.FILES:
            newnews.News_Pic=request.FILES['picture']  # upload to cloudinary
            print('Cloud PATH:', newnews.News_Pic)
            # file_img=request.FILES['picture']
            # file_img_name=file_img.name.replace(' ', '-')
            # # from django.core.files.storage import FileSystemStorage
            # fs=FileSystemStorage(location='media/news')  # ระบุบ folder ที่เซฟไป
            # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
            # upload_file_url=fs.url(filename)  # ให้ไปเอา URL มา จะได้บอก server ถูกว่ารูปนี้อยู่ไหน (ระบุ MEDIA_ROOT แล้ว)
            # print('Pic URL:', upload_file_url)  # Pic URL:  /media/play-5-wow.jpg
            # newnews.News_Pic='/news'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
        newnews.save()
        context['addnew']='The system has added the news to the database.'
    return render(request, 'frontend/addnews.html', context)

@login_required
def SendNews(request):
    if not request.user.is_staff:
        return redirect('home-page')
    memberlist=User.objects.filter(is_staff=False).order_by('id')
    newslist=News.objects.all().order_by('id')
    context={'memberlist':memberlist, 'newslist':newslist}
    if request.method == 'POST':
        data=request.POST.copy()
        send_index=data.get('rank-in-db')
        send_index=int(send_index)
        topic=data.get('topic')
        getid_topic=""
        for i in range(0, len(topic)):
            if topic[i].isnumeric():
                getid_topic+=topic[i]
            if topic[i] == '-':
                break
        # Send by Member Rank
        if send_index == 1:
            rank=data.get('rank')
            getrank=data.get('')
            if rank.find('ALL') != -1:
                cnt=0
                allmember=Member.objects.all()
                for i in allmember:
                    if not i.user.is_staff:
                        mailbox=GetNews()
                        mailbox.news=News.objects.get(id=int(getid_topic))
                        mailbox.member=i
                        mailbox.save()
                        cnt+=1
                context['send_success']='Sending message to '+str(cnt)+' members.'
            if rank.find('ORDINARY') != -1:  # 0-999 pts
                cnt=0
                ordinarymember=Member.objects.filter(Member_Point__range=(0, 999))
                for i in ordinarymember:
                    if not i.user.is_staff:
                        mailbox=GetNews()
                        mailbox.news=News.objects.get(id=int(getid_topic))
                        mailbox.member=i
                        mailbox.save()
                        cnt+=1
                context['send_success']='Sending message to '+str(cnt)+' ordinary members.'
            if rank.find('VIP') != -1:  # 1000-9999 pts
                cnt=0
                vipmember=Member.objects.filter(Member_Point__range=(1000, 9999))
                for i in vipmember:
                    if not i.user.is_staff:
                        mailbox=GetNews()
                        mailbox.news=News.objects.get(id=int(getid_topic))
                        mailbox.member=i
                        mailbox.save()
                        cnt+=1
                context['send_success']='Sending message to '+str(cnt)+' vip members.'
            if rank.find('PRIME') != -1:  # 10000-99999 pts
                cnt=0
                primemember=Member.objects.filter(Member_Point__range=(10000, 99999))
                for i in primemember:
                    if not i.user.is_staff:
                        mailbox=GetNews()
                        mailbox.news=News.objects.get(id=int(getid_topic))
                        mailbox.member=i
                        mailbox.save()
                        cnt+=1
                context['send_success']='Sending message to '+str(cnt)+' prime members.'
            if rank.find('ELITE') != -1:  # > 100000 pts
                cnt=0
                elitemember=Member.objects.filter(Member_Point__gte=100000)
                for i in elitemember:
                    if not i.user.is_staff:
                        mailbox=GetNews()
                        mailbox.news=News.objects.get(id=int(getid_topic))
                        mailbox.member=i
                        mailbox.save()
                        cnt+=1
                context['send_success']='Sending message to '+str(cnt)+' elite members.'
        # Specify Member
        if send_index == 2:
            receiver=data.get('receiver')
            getid_receiver=""
            for i in range(0, len(receiver)):
                if receiver[i].isnumeric():
                    getid_receiver+=receiver[i]
                if receiver[i] == '-':
                    break
            try:
                mailbox=GetNews()
                recipient=Member.objects.get(id=int(getid_receiver))
                mailbox.member=recipient
                mailbox.news=News.objects.get(id=int(getid_topic))
                mailbox.save()
                context['send_success']='Sending message to M'+getid_receiver+' ('+recipient.user.username+')'
            except:
                context['send_fail']='Cannot found this member please contact admin.'
    return render(request, 'frontend/sendnews.html', context)

@login_required
def NewsInbox(request):
    context={}
    try:
        newsinbox=GetNews.objects.filter(member=Member.objects.get(id=request.user.id))  # Join GetNews Member News
        context['newsinbox']=newsinbox
    except:
        context['newsinbox']=None
    if request.method == 'POST':
        data=request.POST.copy()
        getnewid=data.get('getnewid')
        # DELETE FROM getnews WHERE `getnews`.`id` = 5"
        GetNews.objects.get(id=getnewid).delete()
    return render(request, 'frontend/newsinbox.html', context)

@login_required
def AllBookMember(request):
    context={}
    try:
        all_booking=Transaction.objects.filter(member=Member.objects.get(id=request.user.id), payment=None)
        context['allbooking']=all_booking
        first_price=0
        for i in all_booking:
            first_price+=i.Transaction_Price
        context['firstprice']=first_price
        all_promo=Promotion.objects.all()
        for i in all_promo:
            i.Promotion_Discount*=100
        context['allpromo']=all_promo
    except:
        context['allbooking']=None
    if request.method == 'POST':
        data=request.POST.copy()
        if 'getbookid' in data:
            getbookid=data.get('getbookid')
            # free deleted room
            freeroom=Transaction.objects.get(id=getbookid)
            freeroom.room.Room_Status=True
            freeroom.room.save()
            freeroom.delete()
            all_booking=Transaction.objects.filter(member=Member.objects.get(id=request.user.id), payment=None)
            first_price=0
            for i in all_booking:
                first_price+=i.Transaction_Price
            context['firstprice']=first_price
            context['allbooking']=all_booking  # ส่งไปใหม่ให้มัน refresh
        if 'confirm' in data:
            promocode=data.get('promocode')
            if promocode[0] == '-':
                TotalPrice=first_price*1.1
                context['discount']=0
            else:
                promocode=promocode[3:]
                for i in range(0, len(promocode)):
                    if promocode[i] == ' ':
                        promocode=promocode[:i]
                        break
                getcode=Promotion.objects.get(id=promocode)
                percent_discount=getcode.Promotion_Discount
                print('dicount%=', percent_discount)
                context['discount']=first_price*percent_discount
                context['hpromocode']=promocode
                TotalPrice=float(first_price*(1-percent_discount))*1.1
            context['vat']=first_price*0.1
            context['TotalPrice']=TotalPrice
        if 'pay' in data:
            print('got paid\n')
            bank=data.get('bank')
            time=data.get('time')
            vat=data.get('vat')
            total=data.get('allprice')
            hpromocode=data.get('hpromocode')
            print('hidden promocode', hpromocode)
            newpayment=Payment()
            if hpromocode:
                newpayment.promotion=Promotion.objects.get(id=hpromocode)
            newpayment.Payment_Date=time
            newpayment.Payment_Allprice=float(total)
            newpayment.Payment_Vat10=float(vat)
            newpayment.Payment_Banking=bank
            print(vat)
            print(total)
            if 'slip' in request.FILES:
                newpayment.Payment_Slip=request.FILES['slip']  # upload to cloudinary
                print('Cloud PATH:', newpayment.Payment_Slip)
                # file_img=request.FILES['slip']
                # file_img_name=file_img.name.replace(' ', '-')
                # fs=FileSystemStorage(location='media/slip')
                # filename=fs.save(file_img_name, file_img)  # เซฟชื่อไฟล์ กับ ตัวไฟล์
                # upload_file_url=fs.url(filename)
                # print('Pic URL:', upload_file_url)
                # newpayment.Payment_Slip='/slip'+upload_file_url[6:]  # ตัดคำว่า '/media' ด้านหน้าออกไป
            newpayment.save()
            setroom=Transaction.objects.filter(member=request.user.member)  # free room for other customers can reserve
            for free in setroom:
                free.room.Room_Status=True
                free.room.save()
            context['waitadmin']='PoonVeh Hotels will contact you as soon as possible to arrange your hotel stay.'
            # set payment_id to transaction (currently None)
            for i in all_booking:
                i.payment=newpayment
                i.save()
                print(i.payment)
            # Refresh page
            all_booking=Transaction.objects.filter(member=Member.objects.get(id=request.user.id), payment=None)
            first_price=0
            for i in all_booking:
                first_price+=i.Transaction_Price
            context['firstprice']=first_price
            context['allbooking']=all_booking
    return render(request, 'frontend/allbook.html', context)

from datetime import datetime
@login_required
def BooksList(request):
    if not request.user.is_staff:
        return redirect('home-page')
    booklist=Payment.objects.filter(Payment_Status=False).order_by('Payment_Date')
    context={'booklist':booklist}
    if request.method == 'POST':
        data=request.POST.copy()
        if 'accept' in data:
            pid=data.get('accept')
            getpay=Payment.objects.get(id=pid)
            getpay.Payment_Status=True
            getpay.Payment_Confirm=datetime.now()
            getpay.save()
            booklist=Payment.objects.filter(Payment_Status=False)  # Not delete but refresh again
            context={'booklist':booklist}
        if 'deny' in data:
            pid=data.get('deny')
            Transaction.objects.filter(payment=Payment.objects.get(id=pid)).delete()
            Payment.objects.get(id=pid).delete()
    return render(request, 'frontend/bookslist.html', context)

def ReviewPage(request):
    context={}
    confirmpayment=Payment.objects.filter(Payment_Status=True)
    usertransaction=Transaction.objects.filter(member=request.user.member, Transaction_Review=False)
    reviewlist=[]
    for i in range(0, len(usertransaction)):
        if usertransaction[i].payment in confirmpayment:
            reviewlist.append(usertransaction[i])
    context['reviewlist']=reviewlist
    if request.method == 'POST':
        data=request.POST.copy()
        tid=data.get('reviewid')
        rating=data.get('rating')
        comment=data.get('comment')
        thisreview=Transaction.objects.get(id=tid)
        thisreview.Transaction_Review=True
        if rating[0] != '-':
            thisreview.Transaction_Rating=int(rating)
        thisreview.Transaction_Comment=comment
        thisreview.save()
        rewardpoint=int(thisreview.Transaction_Night*thisreview.room.roomtype.Type_Pernight/100)
        request.user.member.Member_Point+=rewardpoint   # เมื่อทำการรีวิวโรงแรมจะได้ point, point นั้นจะเป็นจำนวนเต็มเพื่อความสวยงามตอนโชว์ อิอิ
        request.user.member.save()
        context['reward']='You have gained '+str(rewardpoint)+' additional points, now you have '+str(request.user.member.Member_Point)+' total points!'
        # noop O(N)
        usertransaction=Transaction.objects.filter(member=request.user.member, Transaction_Review=False)
        reviewlist=[]
        for i in range(0, len(usertransaction)):
            if usertransaction[i].payment in confirmpayment:
                reviewlist.append(usertransaction[i])
        context['reviewlist']=reviewlist
    return render(request, 'frontend/reviews.html', context)

@login_required
def AddRoom(request):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')
    context={}
    hotellist=Hotel.objects.all().order_by('id')
    context['hotellist']=hotellist
    roomtypelist=RoomType.objects.all().order_by('id')
    context['roomtypelist']=roomtypelist
    if request.method == 'POST':
        data=request.POST.copy()
        hotel=data.get('hotel')
        hotel=hotel[1:]  # cut H
        for i in range(0, len(hotel)):
            if hotel[i] == ' ':
                hotel=hotel[:i]
                break
        rt=data.get('roomtype')
        rt=rt[2:]  # cut TY
        for i in range(0, len(rt)):
            if rt[i] == ' ':
                rt=rt[:i]
                break
        rn=data.get('roomnum')
        newroom=Room()
        gethotel=Hotel.objects.get(id=hotel)
        newroom.hotel=gethotel
        newroom.roomtype=RoomType.objects.get(id=rt)
        newroom.Room_Number=rn
        newroom.save()
        context['addnew']='Added '+rn+' to '+gethotel.Hotel_Name+'.'
    return render(request, 'frontend/addroom.html', context)

@login_required
def AddRoomType(request):
    allow_user=['MANAGER', 'ADMIN']
    if not request.user.is_staff or request.user.member.staff.Staff_Position not in allow_user:
        return redirect('home-page')
    context={}
    if request.method == 'POST':
        data=request.POST.copy()
        name=data.get('name')
        price=data.get('price')
        cap=data.get('cap')
        detail=data.get('detail')
        newtype=RoomType()
        newtype.Type_Name=name
        newtype.Type_Pernight=abs(int(price))  # incase javascript did not work well
        newtype.Type_Capacity=abs(int(cap))
        newtype.Type_Detail=detail
        if 'picture' in request.FILES:
            newtype.Type_Pic=request.FILES['picture']  # upload to cloudinary
            print('Cloud PATH:', newtype.Type_Pic)
        newtype.save()
        context['addnew']='The system has added new roomtype to the database.'
    return render(request, 'frontend/addroomtype.html', context)

@login_required
def AnalyticReport(request):
    if not request.user.is_staff:
        return redirect('home-page')
    context={}
    allhotel=Hotel.objects.all()

    # Advanced Analytic 1: Top 5 rated hotels
    hotellist=[0]*len(allhotel)  # initialize array size
    countH=[0]*len(allhotel)
    reviews=Transaction.objects.filter(Transaction_Rating__gte=1)
    for i in range(0, len(reviews)):
        hotellist[reviews[i].room.hotel.id-1]+=reviews[i].Transaction_Rating
        countH[reviews[i].room.hotel.id-1]+=1
    for i in range(0, len(allhotel)):
        if hotellist[i] > 0:
            hotellist[i]/=countH[i]
    an1=[]
    for i in range(0, 5):
        cur_ind=-1
        cur_val=0  # not count 0 time, change it to < 0 if you want to count 0
        for j in range(0, len(allhotel)):
            if hotellist[j] > cur_val and j+1 not in an1:
                cur_val=hotellist[j]
                cur_ind=j
        if cur_ind >= 0:
            an1.append(cur_ind+1)
    for i in range(0, len(an1)):
        an1.append(Hotel.objects.get(id=an1[i]))
    wan1=[]  # store rating column  ถ้าเอา hotellist มาใช้เลยมันจะเจอตัวที่ไม่ top 5 แล้วจะเลื่อน Ex. [5, 5, 3, 5 ,5 ,5 ] ติด 3 แล้วมันจะดึง 3 มา มีปรินต์เช็คด้านล่าง
    for i in range(0, int(len(an1)/2)):
        wan1.append(hotellist[an1[0]-1])
        an1.pop(0)
    for i in range(0, len(an1)):
        an1[i].Hotel_Detail=wan1[i]   # change data i don't want to pass many arguments.
    context['AN1']=an1
    # print(hotellist)  # ปรินต์เช็คดูได้ว่าทำไมต้องมี with an1
    # print(wan1)

    # Advanced Analytic 2: Top 5 most booked hotels (count only successful booked)
    hotellist=[0]*len(allhotel)  # initialize array size
    allbooked=Transaction.objects.filter(payment__isnull=False)  # actually payment will not null XD i just wanna show you!
    for i in range(0, len(allbooked)):
        if allbooked[i].payment.Payment_Status == True:
            hotellist[allbooked[i].room.hotel.id-1]+=1
    an2=[]
    for i in range(0, 5):
        cur_ind=-1
        cur_val=-1
        for j in range(0, len(allhotel)):
            if hotellist[j] > cur_val and j+1 not in an2:
                cur_val=hotellist[j]
                cur_ind=j
        if cur_ind >= 0:
            an2.append(cur_ind+1)
    for i in range(0, len(an2)):
        an2.append(Hotel.objects.get(id=an2[i]))
    wan2=[]  # store booked number column
    for i in range(0, int(len(an2)/2)):
        wan2.append(hotellist[an2[0]-1])
        an2.pop(0)
    for i in range(0, len(an2)):
        an2[i].Hotel_Detail=wan2[i]   # change data i don't want to pass many arguments.
    context['AN2']=an2

    # Advanced Analytic 3: Top 5 most booked types
    alltype=RoomType.objects.all()
    typelist=[0]*len(alltype)
    for i in range(0, len(allbooked)):
        if allbooked[i].payment.Payment_Status == True:
            typelist[allbooked[i].room.roomtype.id-1]+=1
    an3=[]
    for i in range(0, 5):
        cur_ind=-1
        cur_val=0  # not count 0 time
        for j in range(0, len(alltype)):
            if typelist[j] > cur_val and j+1 not in an3:
                cur_val=typelist[j]
                cur_ind=j
        if cur_ind >= 0:
            an3.append(cur_ind+1)
    for i in range(0, len(an3)):
        an3.append(RoomType.objects.get(id=an3[i]))
    wan3=[]  # store booked number column
    for i in range(0, int(len(an3)/2)):
        wan3.append(typelist[an3[0]-1])  # Enter the number of times booked by ref. according to the list index.
        an3.pop(0)
    for i in range(0, len(an3)):
        an3[i].Type_Detail=wan3[i]
    context['AN3']=an3
    # Advanced Analytic 4: Top 5 members 
    allmember=Member.objects.all()
    memberlist=[]
    for i in range(0, len(allmember)):
        if not allmember[i].user.is_staff:
            memberlist.append(allmember[i].id)
    an4=[]
    for i in range(0, 5):
        member_ind=-1
        cur_val=0  # not count 0 time
        for j in range(0, len(memberlist)):
            pv_point=Member.objects.get(id=memberlist[j]).Member_Point
            if pv_point > cur_val and memberlist[j] not in an4:
                cur_val=pv_point
                member_ind=memberlist[j]
        if member_ind >= 0:
            an4.append(member_ind)
    for i in range(0, len(an4)):  # insert objects
        an4.append(Member.objects.get(id=an4[i]))
    for i in range(0, int(len(an4)/2)):
        an4.pop(0)
    context['AN4']=an4

    # Advanced Analytic 5: Latest 10 reviews
    allreview=Transaction.objects.filter(Transaction_Review=True).order_by('-id')
    an5=[]
    for i in range(0, len(allreview)):
        if allreview[i].Transaction_Review:
            an5.append(allreview[i])
            if len(an5) == 10:
                break
    context['AN5']=an5

    return render(request, 'frontend/analytic.html', context)