from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import registerUser, loginUser
from django.contrib.sessions.backends.db import SessionStore

import json
import requests
import psycopg2

# Connection to database
try:
    connection = psycopg2.connect(
            host = "127.0.0.1",
            port = "5432",
            database = "meme",
            user = "postgres",
            password = "r@hulp@ndey"
    )

    print("Database Connected")
except Exception as e:
    print("Error: ",e)
    print("Database Connection Failed")


connection.autocommit = True
cursor = connection.cursor()

#MiddleWare

s = SessionStore()

def checkSession():
    try:
        email = s['email']
        return True
    except Exception as e:
        print("Error: ",e)
        return False

# Create your views here.

def home(request):
    return HttpResponse("<h1>Welcome, to meme application</h1>")

def register(request):

    sessionExists = checkSession()

    if sessionExists == False:

        if request.method == "POST":

            form_data = json.loads(request.body.decode("utf-8"))

            # Collect Data From User
            name = form_data.get('name')
            contact = form_data.get('contact')
            email = form_data.get('email')
            password = form_data.get('password')

            # print data
            print(f"Name: {name}")
            print(f"contact: {contact}")
            print(f"Email: {email}")
            print(f"Password: {password}")

            userData = {
                'name' : name,
                'contact' : contact,
                'email' : email,
                'password' : password
            }

            response = registerUser(userData,cursor)

            # statusCode
            print(f"statusCode: {response['statusCode']}")

            # user Details

            if response['statusCode'] == 200:

                #session handle
                s['email'] = userData['email']
                s['password'] = userData['password']

                print("Session: ")
                print(s)
                
                # return render(request, "register.html", {'message' : response['message']})
                # return redirect("/main/memes/")
                return JsonResponse({'status_code' : 200, 'message' : 'success'}) 
            else:
                # return render(request, "register.html", {'message' : response['message']})
                return JsonResponse({'status_code' : 503, 'message' : 'already_registered'})
        else:
            return render(request, "register.html")
    else:
        return redirect("/main/memes/")

def login(request):

    sessionExists = checkSession()

    if sessionExists == False:

        if request.method == 'POST':

            form_data = json.loads(request.body.decode("utf-8"))

            # Collect Details from user
            email = form_data.get('email')
            password = form_data.get('password')

            #print Details
            print(f"Email : {email}")
            print(f"Password : {password}")

            userData = {
                'email' : email,
                'password' : password
            }

            response = loginUser(userData,cursor)

            if response['statusCode'] == 200:
                
                #session handle
                s['email'] = userData['email']
                s['password'] = userData['password']

                print("Session: ")
                print(s)
                

                # return render(request, 'login.html', {'message' : response['message']})
                # return redirect("/main/memes/")
                return JsonResponse({'status_code' : 200, 'message' : 'success'})
            elif response['message'] == 503 and response['message'] == 'passwordError':
                return render(request, 'login.html', {'message' : response['message']})
            else:
                # return render(request, 'login.html', {'message' : response['message']})
                return JsonResponse({'status_code' : 503, 'message' : 'authentication_error'})
        else:
            return render(request, 'login.html')
    else:
        return redirect("/main/memes/")

def logout(request):
    try:
        s.clear()
        return redirect("/main/login/")
    except:
        return redirect("/main/memes/")

def getmemes(request):
    sessionExists = checkSession()

    r = requests.get('https://api.imgflip.com/get_memes')

    memeData = r.json()
    print(memeData)

    if sessionExists == False:
        return redirect('/main/login/')
    else:

        context = {
            'memes_metadata' : r.json()['data']['memes']
        }


        return render(request,'memes.html',context=context)


def editmeme(request):

    sessionStatus = checkSession()

    if sessionStatus:
        # Details of Edit memes

        template_id = request.GET['id']

        context ={
            'meme_id' : template_id
        }

        return render(request,"editmeme.html",context=context)
    else:
        return redirect("/main/login/")


def editmeme_details(request):

    sessionStatus = checkSession()

    if sessionStatus:
        
        if request.method == 'POST':

            template_id = request.POST['id']
            text0 = request.POST['text0']
            text1 = request.POST['text1']

            payload = {
                'template_id' : template_id,
                'username' : 'rahul_pandey',
                'password' : 'r@hulp@ndey',
                'text0' : text0,
                'text1' : text1           
            }

            response = requests.request('POST','https://api.imgflip.com/caption_image',params=payload).json()

            print("Response: ")
            print(response)

            html_string = f'''
                            <h1> Response </h1>
                            <img src={response['data']['url']} alt="meme"/>
                            <a href="{response['data']['url']}"> view Image </a>
                        '''

            return HttpResponse(html_string)
    else:
        return redirect("/main/login/")
