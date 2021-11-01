from .helpers import *

def init_release(request):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            thisproject = projects.objects.get(id = projid)
            context['thisproject'] = thisproject
            context['apr_projects'] = projects.objects.filter(status = '5')
            return render(request, 'psdf_main/_admin_init_payment.html', context)
        context['apr_projects'] = projects.objects.filter(status = '5')
        return render(request, 'psdf_main/_admin_init_payment.html', context)
    else:
        return oops(request)
    
def init_record(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            adminpass = req.get('adminpass')
            amt = req.get('amt')
            if not isfloat(amt):
                messages.error(request, 'Invalid amount entered.')
                return redirect('/init_release')
            refno = sanitize(req.get('refno'))
            try:
                project = projects.objects.get(id = projid)
            except :
                messages.error(request, "No such project exists")
                return redirect('/init_release')
            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/init_release')
            if not isfloat(project.amt_approved):
                return oops(request)
            if float(project.amt_approved) < float(amt):
                messages.error(request, 'ERROR! Amount entered is greater than approved amount of ₹' + str(amt_approved))
                return redirect('/init_release')
            filename = ''
            filepath = ''
            if request.FILES:
                if 'reciept' in request.FILES:
                    reciept = request.FILES['reciept']
                    ext = ""
                    try:
                        ext = "."+str(reciept.name.split('.')[-1])
                    except:
                        ext = ""
                    
                    filepath = project.projectpath
                    filepath = os.path.join(filepath,'/Payment/Initial_Release/')
                    if smkdir(filepath):
                        filename = 'reciept'+ext
                        if handle_uploaded_file(filepath+filename, reciept):
                            pass
                        else:
                            messages.error(request, "Unable to upload file")
                            return redirect('/init_release')
                        
                    else:
                        messages.error(request, "Unable to create directory")
                        return redirect('/init_release')
                else:
                    return oops(request)
            
    else:
        return oops(request)