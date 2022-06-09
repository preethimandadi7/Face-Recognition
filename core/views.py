from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User ,auth
from django.contrib import messages
import hashlib
from django.conf.urls import url
from core.models import Groups, Member
from django.conf import settings
import cv2
import face_recognition
import uuid
import numpy as np
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json



def home(request):
    return render(request,'index.html',{'name':"navin"})

def login(request):
    if(request.method =="POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
    return render(request,'login.html')

def dashboard(request):
    if not request.user.is_authenticated : 
        return redirect('login')
    
    line = request.user.first_name
    line = line.encode('utf8')
    line = hashlib.md5(line)
    line = line.hexdigest()
    line = line+"-"+str(request.user.id)

    p = Groups.objects.filter(userId= request.user.id);
    
    return render(request,'dashboard.html',{'key': line,'groups':p})

def group(request,name):
    p = Groups.objects.filter(id= name)
    data = Member.objects.filter(groupId=name,userId=request.user.id)
    return render(request,'group.html',{'group_name':p,'groupData':data})



def createGroup(request):
    if not request.user.is_authenticated : 
        return redirect('login')

    if(request.method=="POST"):
        name=request.POST['groupname']
        p = Groups(name=name,userId=request.user.id)
        p.save()
        return redirect('dashboard')
    line = request.user.first_name
    line = line.encode('utf8')
    line = hashlib.md5(line)
    line = line.hexdigest()
    
    return render(request,'createGroup.html',{'key': line})

def logout(request):
    auth.logout(request)
    return redirect('home')

def addmember(request,groupId):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        ids = request.POST['id']
        groupid = request.POST['groupid']
        f = request.FILES['image']

        with open( settings.STATICFILES_DIRS[0] +'/uploads/'+email+f.name, 'wb+') as destination:  
            for chunk in f.chunks():  
                destination.write(chunk)
        image = cv2.imread(settings.STATICFILES_DIRS[0] +'/uploads/'+email+f.name)
        k=""
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
            k = ""
            for x in range(face_encoding.shape[0]):
                k = k + str(face_encoding[x]) + " "
        except IndexError:
            print("failed")
        mod = Member(name= name,email= email,officeId=ids,image='/uploads/'+email+f.name,face = k,userId=request.user.id,groupId=groupId)
        mod.save()
        return redirect('/group/'+str(groupId)+"/")
    return render(request,'adduser.html')

def register(request):
    if(request.method=="POST"):
        first_name=request.POST['first_name']
        second_name=request.POST['second_name']
        email=request.POST['email']
        password=request.POST['password']
        user = User.objects.create_user(username=email,email=email,first_name=first_name,last_name = second_name,password=password)
        user.save()
      
        messages.info(request,"Register Successfully");
    return render(request,'register.html')

@csrf_exempt
def findOne(request,groupId):
    if(request.method=="POST"):
        file = request.FILES['image']
        api2 = request.POST['key']
        nametemp = str(uuid.uuid1())
        api = api2.split("-")
        user = User.objects.filter(id = api[1])

        line = user[0].first_name
        line = line.encode('utf8')
        line = hashlib.md5(line)
        line = line.hexdigest()
        line = line+"-"+str(user[0].id)

        if(line != api2):
            res = HttpResponse("Unauthorized")
            res.status_code = 401
            return res


        with open( settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name, 'wb+') as destination:  
            for chunk in file.chunks():  
                destination.write(chunk)
        
        image = cv2.imread(settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name)
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            return JsonResponse({'error':'Face not found in image'})
           
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        list = Member.objects.filter(groupId=groupId,userId = api[1])
        known_face_encodings = []
        known_face_names = []
        known_face_emails = []
        name=""
        email=""
        
        for x in list:
            text = x.face
            known_face_emails.append(x.email)
            known_face_names.append(x.name)
            face = np.fromstring(text, dtype=float, sep=" ")
            known_face_encodings.append(face)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                email = known_face_emails[best_match_index]
        if name == "": 
            return JsonResponse({'error':'No matches found'})
    return JsonResponse({'name':name,'email':email})


@csrf_exempt
def findMultiple(request,groupId):
    if(request.method=="POST"):
        file = request.FILES['image']
        api2 = request.POST['key']
        nametemp = str(uuid.uuid1())
        api = api2.split("-")
        user = User.objects.filter(id = api[1])

        line = user[0].first_name
        line = line.encode('utf8')
        line = hashlib.md5(line)
        line = line.hexdigest()
        line = line+"-"+str(user[0].id)

        if(line != api2):
            res = HttpResponse("Unauthorized")
            res.status_code = 401
            return res
     
        with open( settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name, 'wb+') as destination:  
            for chunk in file.chunks():  
                destination.write(chunk)
        
        image = cv2.imread(settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name)
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            return JsonResponse({'error':'Face not found in image'})

        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        list = Member.objects.filter(groupId=groupId,userId = api[1])
        known_face_encodings = []
        known_face_names = []
        known_face_emails = []
        name=""
        email=""
        output = []
        for x in list:
            text = x.face
            known_face_emails.append(x.email)
            known_face_names.append(x.name)
            face = np.fromstring(text, dtype=float, sep=" ")
            known_face_encodings.append(face)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                op = {}
                op['name'] = known_face_names[best_match_index]
                op['email'] = known_face_emails[best_match_index]
                output.append(op)
        if len(output) == 0: 
            return JsonResponse({'error':'No matches found'})
    return JsonResponse(output ,safe=False)


@csrf_exempt
def findAllMultiple(request):
    if(request.method=="POST"):
        file = request.FILES['image']
        api2 = request.POST['key']
        nametemp = str(uuid.uuid1())
        api = api2.split("-")

        user = User.objects.filter(id = api[1])

        line = user[0].first_name
        line = line.encode('utf8')
        line = hashlib.md5(line)
        line = line.hexdigest()
        line = line+"-"+str(user[0].id)

        if(line != api2):
            res = HttpResponse("Unauthorized")
            res.status_code = 401
            return res
     
        with open( settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name, 'wb+') as destination:  
            for chunk in file.chunks():  
                destination.write(chunk)
        
        image = cv2.imread(settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name)
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            return JsonResponse({'error':'Face not found in image'})

        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        list = Member.objects.filter(userId = api[1])
        known_face_encodings = []
        known_face_names = []
        known_face_emails = []
        output = []
        for x in list:
            text = x.face
            known_face_emails.append(x.email)
            known_face_names.append(x.name)
            face = np.fromstring(text, dtype=float, sep=" ")
            known_face_encodings.append(face)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                op = {}
                op['name'] = known_face_names[best_match_index]
                op['email'] = known_face_emails[best_match_index]
                output.append(op)
        if len(output) == 0: 
            return JsonResponse({'error':'No matches found'})
    return JsonResponse(output ,safe=False)

@csrf_exempt
def findAllOne(request):
    if(request.method=="POST"):
        file = request.FILES['image']
        api2 = request.POST['key']
        nametemp = str(uuid.uuid1())
        api = api2.split("-")
        user = User.objects.filter(id = api[1])

        line = user[0].first_name
        line = line.encode('utf8')
        line = hashlib.md5(line)
        line = line.hexdigest()
        line = line+"-"+str(user[0].id)

        if(line != api2):
            res = HttpResponse("Unauthorized")
            res.status_code = 401
            return res
       
        with open( settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name, 'wb+') as destination:  
            for chunk in file.chunks():  
                destination.write(chunk)
        
        image = cv2.imread(settings.STATICFILES_DIRS[0] +'/uploads/'+nametemp+file.name)
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            return JsonResponse({'error':'Face not found in image'})
           
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        list = Member.objects.filter(userId = api[1])
        known_face_encodings = []
        known_face_names = []
        known_face_emails = []
        name=""
        email=""
        
        for x in list:
            text = x.face
            known_face_emails.append(x.email)
            known_face_names.append(x.name)
            face = np.fromstring(text, dtype=float, sep=" ")
            known_face_encodings.append(face)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                email = known_face_emails[best_match_index]
        if name == "": 
            return JsonResponse({'error':'No matches found'})
    return JsonResponse({'name':name,'email':email})

