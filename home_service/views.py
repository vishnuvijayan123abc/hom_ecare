from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from home_service.forms import CustomerServiceSearchForm
from django.core.mail import send_mail
from django.http import HttpResponse
import random
import string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from .forms import ForgotPasswordForm
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .forms import ForgotPasswordForm, OTPForm


from home_service.models import Service
import logging


import datetime

# Create your views here.

def Home(request):
    user=""
    error=""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count=0
        for j in ser1:
            if i.category==j.service_name:
                count+=1
        i.total = count
        i.save()
    d = {'error': error, 'ser': ser}
    return render(request,'home.html',d)

def contact(request):
    error=False
    if request.method=="POST":
        n = request.POST['name']
        e = request.POST['email']
        m = request.POST['message']
        status = Status.objects.get(status="unread")
        Contact.objects.create(status=status,name=n,email=e,message1=m)
        error=True
    d = {'error':error}
    return render(request,'contact.html',d)

def Admin_Home(request):
    cus = Customer.objects.all()
    ser = Service_Man.objects.all()
    cat = Service_Category.objects.all()
    count1=0
    count2=0
    count3=0
    for i in cus:
        count1+=1
    for i in ser:
        count2+=1
    for i in cat:
        count3+=1
    d = {'customer':count1,'service_man':count2,'service':count3}
    
    return render(request,'admin_home.html',d)

def about(request):
    return render(request,'about.html')

class LoginUserView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {'error': ''})

    def post(self, request):
        error = ""
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        sign = ""

        if user:
            try:
                sign = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                pass

            if sign:
                login(request, user)
                return redirect('user_home')  # Replace 'success_redirect_url_pat1' with your desired URL
            else:
                stat = Status.objects.get(status="Accept")
                pure = False

                try:
                    pure = Service_Man.objects.get(status=stat, user=user)
                except Service_Man.DoesNotExist:
                    pass

                if pure:
                    login(request, user)
                    return redirect('user_home')  # Replace 'success_redirect_url_pat2' with your desired URL
                else:
                    login(request, user)
                    return redirect('login')  # Replace 'notmember_redirect_url' with your desired URL

        else:
            error = "not"

        return render(request, self.template_name, {'error': error})
class LoginAdminView(View):
    template_name = 'admin_login.html'

    def get(self, request):
        return render(request, self.template_name, {'error': ''})

    def post(self, request):
        error = ""
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)

        if user and user.is_staff:
            login(request, user)
            error = "pat"
        else:
            error = "not"

        return render(request, self.template_name, {'error': error})


def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type=="customer":
            Customer.objects.create(user=user,contact=con,address=add,image=im)
        else:
            stat = Status.objects.get(status='pending')
            Service_Man.objects.create(doj=dat,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error}
    return render(request,'signup.html',d)


@method_decorator(login_required, name='dispatch')
class UserHomeView(View):
    template_name = 'service_home.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        error = ""

        if user.is_authenticated:
            try:
                sign = Customer.objects.get(user=user)
                error = "pat"
            except Customer.DoesNotExist:
                pass

        context = {'error': error}
        return render(request, self.template_name, context)
def Service_home(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro=""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro="message1"
    d = {'error':error,'terro':terro}
    return render(request,'service_home.html',d)

def Service_Order(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro=""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro="message1"
    order = Order.objects.filter(service=sign)
    d = {'error':error,'terro':terro,'order':order}
    return render(request,'service_order.html',d)

def Admin_Order(request):
    order = Order.objects.all()
    d = {'order':order}
    return render(request,'admin_order.html',d)

def Customer_Order(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.filter(customer=sign)
    d = {'error':error,'order':order}
    return render(request,'customer_order.html',d)


def Customer_Booking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terror=False
    ser1 = Service_Man.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        add = request.POST['add']
        dat = request.POST['date']
        da = request.POST['day']
        ho = request.POST['hour']
        st = Status.objects.get(status="pending")
        Order.objects.create(status=st,service=ser1,customer=sign,book_date=dat,book_days=da,book_hours=ho)
        terror=True
    d = {'error':error,'ser':sign,'terror':terror}
    return render(request,'booking.html',d)

def Booking_detail(request,pid):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.get(id=pid)
    d = {'error':error,'order':order}
    return render(request,'booking_detail.html',d)

def All_Service(request):
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count=0
        for j in ser1:
            if i.category==j.service_name:
                count+=1
        i.total = count
        i.save()
    d = {'error': error,'ser':ser}
    return render(request,'services.html',d)

def Explore_Service(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser = Service_Category.objects.get(id=pid)
    sta = Status.objects.get(status="Accept")
    order = Service_Man.objects.filter(service_name=ser.category,status=sta)
    d = {'error': error,'ser':ser,'order':order}
    return render(request,'explore_services.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def Edit_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        sign.address = ad
        sign.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.save()
        terror = True
    d = {'terror':terror,'error':error,'pro':sign,'ser':ser}
    return render(request, 'edit_profile.html',d)


def Edit_Service_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    car = ID_Card.objects.all()
    city = City.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        try:
            i1 = request.FILES['image1']
            sign.id_card=i1
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        se = request.POST['service']
        card = request.POST['card']
        cit = request.POST['city']
        ex = request.POST['exp']
        dob = request.POST['dob']
        if dob:
            sign.dob=dob
            sign.save()
        ci=City.objects.get(city=cit)
        sign.address = ad
        sign.contact=con
        sign.city=ci
        user.first_name = f
        user.last_name = l
        user.email = e
        sign.id_type = card
        sign.experience = ex
        sign.service_name = se
        user.save()
        sign.save()
        terror = True
    d = {'city':city,'terror':terror,'error':error,'pro':sign,'car':car,'ser':ser}
    return render(request, 'edit_service_profile.html',d)

def Edit_Admin_Profile(request):
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Customer.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image=i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        pro.save()
        error = True
    d = {'error':error,'pro':pro}
    return render(request, 'edit_admin_profile.html',d)

def profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'profile.html',d)

def service_profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'service_profile.html',d)

def admin_profile(request):
    
    user = User.objects.get(id=request.user.id)
    pro = Customer.objects.get(user=user)
    d = {'pro':pro}
    return render(request,'admin_profile.html',d)



def Admin_Change_Password(request):
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'terror':terror}
    return render(request,'admin_change_password.html',d)

def New_Service_man(request):
    status = Status.objects.get(status="pending")
    ser = Service_Man.objects.filter(status=status)
    d = {'ser':ser}
    return render(request,'new_service_man.html',d)

def All_Service_man(request):

    ser = Service_Man.objects.all()
    d = {'ser':ser}
    return render(request,'all_service_man.html',d)

def All_Customer(request):

    ser = Customer.objects.all()
    d = {'ser':ser}
    return render(request,'all_customer.html',d)



def Add_Service(request):

    error=False
    if request.method == "POST":
        n = request.POST['cat']
        i = request.FILES['image']
        de = request.POST['desc']
        Service_Category.objects.create(category=n,image=i,desc=de)
        error=True
    d = {'error':error}
    return render(request,'add_service.html',d)



def Edit_Service(request,pid):

    error=False
    ser = Service_Category.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['cat']
        try:
            i = request.FILES['image']
            ser.image = i
            ser.save()
        except:
            pass
        de = request.POST['desc']
        ser.category = n
        ser.desc = de
        ser.save()
        error=True
    d = {'error':error,'ser':ser}
    return render(request,'edit_service.html',d)

def View_Service(request):

    ser = Service_Category.objects.all()
    d = {'ser':ser}
    return render(request,'view_service.html',d)

def View_City(request):
    
    ser = City.objects.all()
    d = {'ser':ser}
    return render(request,'view_city.html',d)

def accept_confirmation(request,pid):
    ser = Order.objects.get(id=pid)
    sta = Status.objects.get(status='Accept')
    ser.status = sta
    ser.save()
    return redirect('service_order')

def confirm_message(request,pid):
    ser = Contact.objects.get(id=pid)
    sta = Status.objects.get(status='read')
    ser.status = sta
    ser.save()
    return redirect('new_message')

def delete_service(request,pid):
    ser = Service_Category.objects.get(id=pid)
    ser.delete()
    return redirect('view_service')

def delete_city(request,pid):
    ser = City.objects.get(id=pid)
    ser.delete()
    return redirect('view_city')

def delete_admin_order(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('admin_order')

def delete_Booking(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('customer_order')

def delete_service_man(request,pid):
    ser = Service_Man.objects.get(id=pid)
    ser.delete()
    return redirect('all_service_man')

def delete_customer(request,pid):
    ser = Customer.objects.get(id=pid)
    ser.delete()
    return redirect('all_customer')

def Change_status(request,pid):
    
    error = False
    pro1 = Service_Man.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        error=True
    d = {'pro':pro1,'error':error}
    return render(request,'status.html',d)

def Order_status(request,pid):
    
    error = False
    pro1 = Order.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        error=True
    d = {'pro':pro1,'error':error}
    return render(request,'order_status.html',d)

def Order_detail(request,pid):

    pro1 = Order.objects.get(id=pid)
    d = {'pro':pro1}
    return render(request,'order_detail.html',d)

def service_man_detail(request,pid):
    
    pro1 = Service_Man.objects.get(id=pid)
    d = {'pro':pro1}
    return render(request,'service_man_detail.html',d)

def search_cities(request):
    error=""
    try:
        user = User.objects.get(id=request.user.id)
        error = ""
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
   
    terror=False
    pro=""
    car = City.objects.all()
    count1=0
    car1 = Service_Category.objects.all()
    c=""
    c1=""
    if request.method=="POST":
        c=request.POST['city']
        c1 = request.POST['cat']
        ser = City.objects.get(city=c)
        ser1 = Service_Category.objects.get(category=c1)
        pro = Service_Man.objects.filter(service_name=ser1,city=ser)
        for i in pro:
            count1+=1
        terror = True
    d = {'c':c,'c1':c1,'count1':count1,'car1':car1,'car':car,'order':pro,'error':error,'terror':terror}
    return render(request,'search_cities.html',d)

def search_services(request):

    error=False
    pro=""
    car = Service_Category.objects.all()
    c=""
    if request.method=="POST":
        c=request.POST['cat']
        ser = Service_Category.objects.get(category=c)
        pro = Service_Man.objects.filter(service_name=ser)
        error=True
    d = {'service':c,'car':car,'order':pro,'error':error}
    return render(request,'search_services.html',d)

def new_message(request):
    
    sta = Status.objects.get(status='unread')
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser':pro1}
    return render(request,'new_message.html',d)

def read_message(request):

    sta = Status.objects.get(status='read')
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser':pro1}
    return render(request,'read_message.html',d)


def customer_service_search(request):
    if request.method == 'GET':
        form = CustomerServiceSearchForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            print(category)
            # services = Service_Category.objects.filter(category__icontains=category)
            services = Service_Category.objects.filter(category__icontains=category)
            print(services)
            if services:
                return render(request, 'search_results.html', {'services': services})
            else:
                error_message = "No services found for the provided category."
                return render(request, 'search_results.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid search criteria."
            return render(request, 'search_results.html', {'form': form, 'error_message': error_message})
    else:
        form = CustomerServiceSearchForm()
        return render(request, 'search_results.html', {'form': form})


User = get_user_model()

def generate_otp(user):
    otp = get_random_string(length=6, allowed_chars='0123456789')
    user.profile.reset_password_otp = otp  # Assuming you have a UserProfile model with reset_password_otp field
    user.profile.save()
    return otp

def send_otp_to_user_email(user, otp):
    subject = 'Reset Password OTP'
    message = f'Your OTP for resetting the password is: {otp}'
    from_email = 'hcare0254@gmail.com'  # Update with your email
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        pass  # Handle email sending exception

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                otp = generate_otp(user)
                send_otp_to_user_email(user, otp)
                request.session['reset_password_username'] = username  # Store username in session
                return redirect('verify_otp_for_reset')
            except User.DoesNotExist:
                return render(request, 'user_not_found.html')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password_form.html', {'form': form})

def verify_otp_for_reset(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            username = request.session.get('reset_password_username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    if user.profile.reset_password_otp == otp_entered:
                        # OTP verified successfully
                        return redirect('reset_password')
                    else:
                        return render(request, 'verify_otp_for_reset.html', {'form': form, 'error': 'Invalid OTP'})
                except User.DoesNotExist:
                    pass  # Handle User.DoesNotExist as needed
            else:
                return redirect('forgot_password')
    else:
        form = OTPForm()

    return render(request, 'verify_otp_for_reset.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        username = request.session.get('reset_password_username')
        if username and new_password:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                del request.session['reset_password_username']  # Remove username from session
                return render(request, 'password_reset_success.html', {'username': username})
            except User.DoesNotExist:
                pass  # Handle User.DoesNotExist as needed
    return render(request, 'reset_password.html')