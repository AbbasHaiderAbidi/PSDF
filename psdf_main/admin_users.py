from .helpers import *


    
def admin_users(request):
    context = full_admin_context(request)
    context['allusers']= get_all_users(request)
    return render(request, 'psdf_main/_admin_users.html', context)



def admin_pending_users(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['userobj'] = pen_users(request)
        return render(request, 'psdf_main/_admin_pending_users.html', context)


def approve_user(request, userid):
    if adminonline(request):
        user = users.objects.get(id = userid)
        user.aprdate = datetime.now().date()
        user.activate = True
        user.admin = False
        user.active = True
        user.lastlogin = user.aprdate
        user.save(update_fields=['lastlogin','aprdate','activate','admin','active'])
        
        context = full_admin_context(request)
        messages.error(request, 'User ' + user.username + ' has been approved.')
        return render(request, 'psdf_main/_admin_pending_users.html', context)
    else:
        return oops(request)
    
def reject_user(request, userid):
    if adminonline(request):
        userreject = users.objects.get(id=userid)
        usernamereject = userreject.username
        userreject.delete()
        context = full_admin_context(request)
        messages.error(request, 'User ' + usernamereject + ' has been Rejected.')
        return render(request, 'psdf_main/_admin_pending_users.html', context)
    else:
        return oops(request)
    
def allow_user(request, userid):
    if adminonline(request):
        user = users.objects.get(id = userid)
        user.admin = False
        user.active = True
        user.save(update_fields=['admin','active'])
        context = full_admin_context(request)
        context['allusers']= get_all_users(request)
        messages.success(request, 'User ' + user.username + ' has been allowed.')
        return render(request, 'psdf_main/_admin_users.html', context)
    else:
        return oops(request)

def ban_user(request, userid):
    if adminonline(request):
        user = users.objects.get(id = userid)
        user.admin = False
        user.active = False
        user.save(update_fields=['admin','active'])
        context = full_admin_context(request)
        context['allusers']= get_all_users(request)
        messages.error(request, 'User ' + user.username + ' has been banned.')
        return render(request, 'psdf_main/_admin_users.html', context)
    else:
        return oops(request)

