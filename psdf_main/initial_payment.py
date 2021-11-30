from .helpers import *


def admin_sanction(request):
    # proj = projects.objects.get(id = '1')
    # proj.status = '6'
    # print(proj.id)
    # proj.save(update_fields = ['status'])
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            amt_approved = req.get('grant')
            adminpass = req.get('adminpass')
            if not check_password(adminpass,users.objects.get(id = getadmin_id()).password):
                messages.error(request, "Invalid administrator password")
                return redirect('/admin_sanction')
            try:
                project = projects.objects.get(id = projid)  
            except:
                messages.error(request, "No such project")
                return redirect('/admin_sanction')
            
            # if not isfloat(amt_approved):
            #     messages.error(request, "Grant amount must be a number")
            #     return redirect('/admin_sanction')
            
            if request.FILES:
                if 'reciept' in request.FILES:
                    reciept = request.FILES['reciept']
                    ext = ""
                    try:
                        ext = "."+str(reciept.name.split('.')[-1])
                    except:
                        ext = ""
                    filepath = project.projectpath
                    filepathnew = filepath+'/Sanction_Order/'
                    try:
                        alreadyfile = glob.glob(os.path.join(filepathnew,'Sanction_Order')+'*')[0]
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    if smkdir(filepathnew):
                        filename = 'Sanction_Order'+ext
                        if handle_uploaded_file(filepathnew+filename, reciept):
                            project.amt_approved = amt_approved
                            project.status = '5'
                            project.sanction_date = datetime.now().date()
                            project.save(update_fields = ['amt_approved','sanction_date'])
                            messages.success(request,"Sanction order uploaded for project ID: "+str(project.newid))
                            notification(project.userid.id,"Sanction order for project ID: "+str(project.newid)+" released.")
                            return redirect('/admin_sanction')
                        else:
                            messages.error(request, "Unable to upload file")
                            return redirect('/admin_sanction')
                        
                    else:
                    
                        messages.error(request, "Unable to create directory")
                        return redirect('/admin_sanction')
                else:
                    return oops(request)
            else:
                messages.error(request, "ERROR! No file selected.")
                return redirect('/admin_sanction')
        context['sancs'] = projects.objects.filter(Q(status = '4')| Q(status = '5'), deny=False)
        return render(request, 'psdf_main/_admin_sanction.html',context)
            
    else:
        return oops(request)
    
def download_sanction(request, projid):
    if adminonline(request) or (useronline(request) and projectofuser(request, request.session['user'], projid)):
        try:
            proj = projects.objects.get(id = projid)
        except:
            messages.error(request, 'Invalid project ID')
            return redirect('/admin_sanction')
        try:
            filethere = glob.glob(proj.projectpath+'/Sanction_Order/Sanction_Order'+'*')[0]
        except:
            messages.error(request, 'Sanction Order does not exists')
            return redirect('/admin_sanction')
        if os.path.exists(filethere):
            return handle_download_file(filethere, request)
        else:
            messages.error(request, 'Sanction Order does not exists')
            return redirect('/admin_sanction')
    else:
        return oops(request)

def init_release(request):
    # init_payment.objects.all().delete()
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            thisproject = projects.objects.get(id = projid)
            context['thisproject'] = thisproject
            context['apr_projects'] = projects.objects.filter(status = '6', deny=False)#,  amt_released = 0)
            return render(request, 'psdf_main/_admin_init_payment.html', context)
        context['apr_projects'] = projects.objects.filter(status = '6', deny=False)
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
            if init_payment.objects.filter(project = project):
                messages.error(request, 'A document signing payment entry exists.')
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

            add_amount(inpay.project.id, inpay.amount, request)
            proj = projects.objects.get(id = inpay.project.id)
            proj.status = '7' #init payment entry is there
            proj.save(update_fields = ['status'])
            
            messages.success(request, "Success! Initial Payment of ₹"+amt+ " recorded.")
            workflow(inpay.project.id,"Initial payment of ₹"+inpay.amount+" released on "+str(inpay.release_date))
            # notification(inpay.project.userid.id, "Payment of ₹"+str(inpay.amount)+" for project ID "+str(inpay.project.newid)+" processed.")
            return redirect('/init_release')
    else:
        return oops(request)

def user_init_payment(request):
    # init_payment.objects.all().delete()
    # proj = projects.objects.get(id = 1)
    # proj.status = '7'
    # proj.save(update_fields = ['status'])
    # return False
    # print(proj.status)
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        if request.method == 'POST':
            req = request.POST
            ackno = str(req.get('refno'))
            payid = req.get('payid')
            userpass = req.get('userpass')
            if not check_password(userpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid password.')
                return redirect('/user_init_payement')
            try:
                thispay = init_payment.objects.get(id = payid)
            except:
                messages.error(request, 'Invalid payment entry')
                return redirect('/user_init_payment')
            if not ackno.casefold() == str(thispay.ref_no).casefold():
                messages.error(request, 'Reference number mismatch.')
                return redirect('/user_init_payment')
            else:
                thispay.ack = True
                thispay.recv_date = datetime.now().date()
                thispay.save(update_fields = ['ack','recv_date'])
                notification(getadmin_id(), "Payment of ₹"+str(thispay.amount)+" for project ID "+str(thispay.project.newid)+" acknowledged by entity.")
                workflow(thispay.project.id,"Initial payment of ₹"+str(thispay.amount)+" acknowledged on "+str(thispay.release_date)+" by entity.")
        context['init_pays'] = init_payment.objects.filter(user = getuser(request))
        return render(request, 'psdf_main/_user_init_payment.html', context)
    else:
        return oops(request)


def downloadinitpay(request, payid):
    try:
        pay = init_payment.objects.get(id = payid)
    except:
        return oops(request)
    if proj_of_user(request, pay.project.id):
        return handle_download_file(pay.filepath, request)
    else:
        return oops(request)