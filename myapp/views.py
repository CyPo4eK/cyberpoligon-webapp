from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import random, subprocess
from django.http import HttpResponse


otp_block = {}
# Store OTPs temporarily in session for simplicity
def login_view(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    if request.user.is_authenticated:
        return redirect('/admin')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(username + " is authenticated")
                request.session['otp'] = random.randint(1000, 9999)
                print(str(request.session.get('otp')))
                request.session['authenticated_user'] = username
                request.session['password'] = password
                return JsonResponse({'success': True, 'otp_required': True})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'},status=401)

        return render(request, 'index.html',{"ip":ip})

def verify_otp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    if request.method == 'POST':
        if ip not in otp_block:
            otp_block[ip] = 0
        elif otp_block[ip] >= 25:
            return JsonResponse({'success': False, 'message': 'Your IP is blocked!','ip':ip},status=403)
        otp = request.POST.get('otp')
        print(otp)
        #print(type(int(otp)))
        #print(str(request.session.get('otp')))
        #print(type(int(request.session.get('otp'))))
        #print(int(otp)==int(request.session.get('otp')))
        #print(request.session.get('authenticated_user'))
        if int(request.session.get('otp')) == int(otp):
            #print("otp matched")
            user = authenticate(password = request.session.get('password'), username=request.session.get('authenticated_user'))
            #print(user)
            if user is not None:
                print(str(user) + "'s OTP verified. login successful")
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful','ip':ip})
        else:
            otp_block[ip] = otp_block[ip]+1
            #print(otp_block)
            return JsonResponse({'success': False, 'message': 'Invalid OTP','ip':ip},status=401)

    return redirect('login_view')


def admin_page(request):
    if request.user.is_authenticated:
            if request.method == 'GET':
                    return render(request, 'admin.html')
                   # if x_forwarded_for:
                       # ip = x_forwarded_for.split(',')[0]

            #print(x_forwarded_for.split(',')[0])
            #print(x_forwarded_for)
            #print(request.META.get('HTTP_X_FORWARDED_FOR'))
               ##return render(request, 'admin.html')
            if request.method == 'POST':
                ip = request.POST.get('ip')
                command = "ping -c 3 "+ip
                out = subprocess.check_output(command, shell=True, text=True)
                return HttpResponse(out, status=200)
    else:
        return HttpResponse('Unauthorized', status=401)
