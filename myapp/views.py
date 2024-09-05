from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import random



# Store OTPs temporarily in session for simplicity
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['otp'] = random.randint(100000, 999999)
            print(str(request.session.get('otp')))
            request.session['authenticated_user'] = username
            request.session['password'] = password
            return JsonResponse({'success': True, 'otp_required': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})

    return render(request, 'index.html')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        print(type(int(otp)))
        print(str(request.session.get('otp')))
        print(type(int(request.session.get('otp'))))
        print(int(otp)==int(request.session.get('otp')))
        print(request.session.get('authenticated_user'))
        if int(request.session.get('otp')) == int(otp):
            print("otp matched")
            user = authenticate(password = request.session.get('password'), username=request.session.get('authenticated_user'))
            print(user)
            if user is not None:
                print("User is not none")
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'})
        return JsonResponse({'success': False, 'message': 'Invalid OTP'})

    return redirect('login_view')
