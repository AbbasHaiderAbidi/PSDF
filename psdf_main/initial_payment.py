from .helpers import *

def init_release(request):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            thisproject = projects.objects.get(id = projid)
            context['thisproject'] = thisproject
            context['apr_projects'] = projects.objects.filter(status = '5')#,  amt_released = 0)
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
            refno = sanitize(req.get('refno'))
            if not isfloat(amt):
                messages.error(request, 'Invalid amount entered.')
                return redirect('/init_release')
            try:
                project = projects.objects.get(id = projid)
            except :
                messages.error(request, "No such project exists")
                return redirect('/init_release')
            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/init_release')
            if not isnum(project.amt_approved):
                return oops(request)
            if int(project.amt_approved) < int(amt):
                messages.error(request, 'ERROR! Amount entered is greater than approved amount of ₹' + str(project.amt_approved))
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
                    filepathnew = filepath+'/Payment/Initial_payment/'
                    try:
                        alreadyfile = glob.glob(os.path.join(filepathnew,'reciept')+'*')[0]
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    print(filepath) 
                    print(filepathnew)
                    if smkdir(filepathnew):
                        filename = 'reciept'+ext
                        if handle_uploaded_file(filepathnew+filename, reciept):
                            pass
                        else:
                            messages.error(request, "Unable to upload file")
                            return redirect('/init_release')
                        
                    else:
                        print("phir nahi hua")
                        messages.error(request, "Unable to create directory")
                        return redirect('/init_release')
                else:
                    return oops(request)
            else:
                messages.error(request, "ERROR! No file selected.")
                return redirect('/init_release')
            inpay = init_payment()
            inpay.project = projects.objects.get(id = projid)
            inpay.user = users.objects.get(id = inpay.project.userid.id)
            inpay.ref_no = refno
            inpay.amount = amt
            inpay.release_date = datetime.now().date()
            inpay.filepath = filepathnew+filename
            inpay.save()
            proj = projects.objects.get(id = inpay.project.id)

            if proj.amt_released == None or proj.amt_released == '' or proj.amt_released == ' ' or proj.amt_released == 0:
                amt_rel = 0
            else:
                amt_rel = proj.amt_released
            proj.amt_released = int(amt_rel) + int(inpay.amount)
            proj.save(update_fields = ['amt_released'])
            messages.success(request, "Success! Payment of ₹"+amt+ " recorded.")
            workflow(inpay.project.id,"Initial payment of ₹"+inpay.amount+" released on "+str(inpay.release_date))
            notification(inpay.project.userid.id, "Payment of ₹"+str(inpay.amount)+" for project ID "+str(inpay.project.newid)+" processed.")
            return redirect('/init_release')
    else:
        return oops(request)

def user_init_payment(request):
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        context['init_pays'] = init_payment.objects.filter(user = getuser(request, request.session['user']))
        return render(request, 'psdf_main/_user_init_payment.html', context)
    else:
        return oops(request)
