from .helpers import *

def admin_pay_proj(request):
    
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            try:
                proj = projects.objects.get(id = projid)
            except:
                return oops(request)
            context['loas'] = loadata.objects.filter(project = proj, completed = False)
            context['thisproj'] = proj
            return render(request, 'psdf_main/_admin_payment.html', context)
        else:
            return redirect('/admin_pay')
        
    else:
        return oops(request)



def admin_pay(request):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            loaid = req.get('loaid')
            projid = req.get('projid')
            context['thisloa'] = loadata.objects.get(id = loaid)
            context['proj'] = projects.objects.get(id = projid)
        context['projs'] = projects.objects.filter(status = '6', completed = False, deny=False)
        # context['loas'] = loadata.objects.filter(completed = False)
        return render(request, 'psdf_main/_admin_payment.html', context)
    else:
        return oops(request)


def approve_admin_pay(request):
    
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            adminpass = req.get('adminpass')
            amt = req.get('amt')
            loaid = req.get('loaid')
            ref_no = sanitize(req.get('refno'))
            remark = req.get('remark')
            if not isfloat(amt):
                messages.error(request, 'Invalid amount entered.')
                return redirect('/admin_pay')
            try:
                project = projects.objects.get(id = projid)
            except :
                messages.error(request, "No such project exists")
                return redirect('/admin_pay')
            try:
                thisloa = loadata.objects.get(id = loaid)
            except :
                messages.error(request, "No such LOA exists")
                return redirect('/admin_pay')

            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/admin_pay')
            if int(project.amt_approved) < int(amt):
                messages.error(request, 'ERROR! Amount entered is greater than approved amount of ₹' + str(project.amt_approved))
                return redirect('/admin_pay')
            if thisloa.amt_released == None or thisloa.amt_released == '' or thisloa.amt_released == ' ' or thisloa.amt_released == 0:
                amtx = 0
            else:
                amtx = int(thisloa.amt_released)
            x = amtx + int(amt)
            if int(thisloa.amt) < x:
                messages.error(request, 'ERROR! Total requested amount is greater than LOA amount of ₹' + str(thisloa.amt))
                return redirect('/admin_pay')
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
                    
                    filepathnew = filepath+'/Payment/LOA/'+str(thisloa.subdate)+'_'+str(amt)+'/'
                    try:
                        alreadyfile = glob.glob(os.path.join(filepathnew,'LOA_payment_'+str(amt))+'*')[0]
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    
                    if smkdir(filepathnew):
                        filename = 'LOA_'+str(thisloa.amt)+ext
                        if handle_uploaded_file(filepathnew+filename, reciept):
                            messages.success(request,'Payment file uploaded')
                            newpay = payment()
                            newpay.project = thisloa.project
                            newpay.user = thisloa.user
                            newpay.loa = thisloa
                            newpay.ref_no = str(ref_no)
                            newpay.amount = int(amt)
                            newpay.release_date = datetime.now().date()
                            newpay.filepath = filepathnew+filename
                            add_amount_loa(thisloa.id,amt,request)
                            add_amount(thisloa.project.id,amt,request)
                            if emp_check(remark):
                                pass
                            else:
                                newpay.remark = remark
                            newpay.save()
                            messages.success(request, "Payment of "+str(newpay.amount)+' approved on date: '+str(newpay.release_date))
                            return redirect('/admin_pay')
                        else:
                            messages.error(request, "Unable to upload file")
                            return redirect('/admin_pay')
                    else:
                        messages.error(request, "Unable to create directory")
                        return redirect('/admin_pay')
                else:
                    return oops(request)
                
            else:
                messages.error(request, "ERROR! No file selected.")
                return redirect('/admin_pay')
            
        else:
            return oops(request)
    else:
        return oops(request)
    
def user_ack_pay(request):
    if useronline(request):
        context = full_user_context(request)
        
        if request.method == 'POST':
            req = request.POST
            refno = str(req.get('refno'))
            userpass = req.get('userpass')
            payid = req.get('payid')
            
            try:
                thispay = payment.objects.get(id = payid)
            except:
                messages.error(request, 'No payment record exists')
                return redirect('/user_ack_pay')
            if not check_password(userpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Enter correct password.')
                return redirect('/user_ack_pay')
            if refno == " " or refno == " " or refno == "-":
                messages.error(request, 'Enter valid reference number')
                return redirect('/user_ack_pay')
            
            if not str(refno).casefold() == str(thispay.ref_no).casefold():
                messages.error(request, 'Reference number mismatch.')
                return redirect('/user_ack_pay')
            else:
                thispay.ack = True
                thispay.recv_date = datetime.now().date()
                thispay.save(update_fields = ['ack','recv_date'])
                messages.success(request, 'Payment Successfully acknowledged.')
        context['pays'] = payment.objects.filter(user = getuser(request))
        return render(request, 'psdf_main/_user_payments.html', context)
    else:
        return oops(request)


    
def downloadpay(request, payid):
    try:
        pay = payment.objects.get(id = payid)
    except:
        return oops(request)
    if proj_of_user(request, pay.project.id):
        return handle_download_file(pay.filepath, request)
    else:
        return oops(request)