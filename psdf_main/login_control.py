from .helpers import *


def loginPage(request):
    
    if adminonline(request):
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_dashboard.html', context)
    elif useronline(request):
        context = full_user_context(request)
        return render(request, 'psdf_main/dashboard.html', context)
    elif auditoronline(request):
        context = full_auditor_context(request)
        return render(request, 'psdf_main/_auditor_dashboard.html', context)
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            context = {}
            user = users.objects.filter(username = username)[:1]
            if not user:
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request, 'psdf_main/login.html')
            for item in user:
                r_username = item.username
                if not user.values('activate')[0]['activate']:
                    messages.error(request, 'User ' + username + ' is pending for verification. Please contact PSDF Sectt.')
                    return render(request, 'psdf_main/login.html')
                if user.values('active')[0]['active']:
                    if check_password(password,user.values('password')[0]['password']):
                        user_m = userDetails(r_username)
                        if user_m['auditor']:
                            request.session['auditor'] = 'auditor'
                            context = full_auditor_context(request)
                            return render(request, 'psdf_main/_auditor_dashboard.html', context)
                        request.session['user'] = user_m['username']
                        if user_m['admin']:
                            request.session['admin'] = "admin"
                            context = full_admin_context(request)
                            return render(request, 'psdf_main/_admin_dashboard.html', context)
                        return render(request, 'psdf_main/dashboard.html', context = full_user_context(request))
                    else:
                        messages.error(request, 'Invalid username or password. Please try again.')
                        return render(request, 'psdf_main/login.html')
            else:
                messages.error(request, 'User ' + username + ' is currently inactive. Please contact administrator.')
                return render(request, 'psdf_main/login.html')
    return render(request, 'psdf_main/login.html')

def registeruser(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        cnfpassword = request.POST['cnfpassword']
        username = username_sanitize(request.POST['username'])
        password = request.POST['password']
        if(password != cnfpassword):
            form.add_error("password" ,"Both password fields must match")
        elif not pass_valid(password):
            form.add_error("password" ,"Password must be of atleast 6 chracters, with atleast 1 uppercase letter, 1 lowercase letter, 1 speacial character (i.e. @ # $ & ! *), and atleast 1 number.")
        else:
            if form.is_valid():
                form_main = form.save(commit=False)
                form_main.username = username
                form_main.password = make_password(password)
                
                # form_main.admin = True
                # form_main.active = True
                # form_main.activate = True
                form_main.save()
                username = form.cleaned_data['username']
                messages.warning(request, 'User : ' +username + ' pending for verification. ')
                return redirect('/')
    context ={'form':form}
    
    return render(request, 'psdf_main/userRegister.html', context)


def logout(request):
    try:
        user = users.objects.get(username = request.session['user'])
        user.lastlogin = datetime.now()
        user.save(update_fields=['lastlogin'])
    except:
        pass
    if request.session.has_key('user'):
        del request.session['user']
    if request.session.has_key('admin'):
        del request.session['admin']
    if request.session.has_key('auditor'):
        user = users.objects.get(username = 'auditor')
        user.lastlogin = datetime.now().date()
        user.save(update_fields=['lastlogin'])
        del request.session['auditor']
    
    return redirect('/')

def admin_password_page(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['user_list'] = users.objects.all()
        if request.method == 'POST':
            req = request.POST
            adminpass = req.get('adminpass')
            adminnewpass = req.get('adminnewpass')
            radminnewpass = req.get('radminnewpass')
            if adminnewpass != radminnewpass:
                messages.error(request,'Both password fields must match')
                return redirect('/admin_password_page')
            thisuser = users.objects.get(id = getadmin_id())
            if not check_password(adminpass, thisuser.password):
                messages.error(request,'Invalid administrator password')
                return redirect('/admin_password_page')
            if not pass_valid(adminnewpass):
                messages.error(request,'Password must be of atleast 6 chracters, with atleast 1 uppercase letter, 1 lowercase letter, 1 speacial character (i.e. @ # $ & ! *), and atleast 1 number.')
                return redirect('/admin_password_page')
            adminnewpass1 = make_password(adminnewpass)
            thisuser.password = adminnewpass1
            thisuser.save(update_fields = ['password'])
            messages.success(request,'Adminstrator password updated.')
            return redirect('/admin_password_page')
        return render(request, 'psdf_main/_admin_password_change.html',context)
    else:
        return oops(request)
    
def admin_password_user(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            
    else:
        return oops(request)