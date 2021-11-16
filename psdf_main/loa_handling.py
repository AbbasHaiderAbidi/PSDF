from .helpers import *


def new_loa(request):
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            thisproject = projects.objects.get(id = projid)
            aboq = boqdata.objects.filter(project = thisproject, boqtype = '3') #Change to 3
            context['aboq'] = aboq
            context['approved_boq_total'] = boq_grandtotal(aboq)
            context['loa_project'] = thisproject
            return render(request, 'psdf_main/_user_new_loa.html', context)
        userobj = users.objects.filter(username = request.session['user'])[:1].get()
        
        context['projectlist'] = projects.objects.filter(status = '5', userid = userobj)
        
        return render(request, 'psdf_main/_user_new_loa.html', context)
    else:
        return oops(request)

def submitloa(request):
    if useronline(request) and not adminonline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            amt = req.get('amt')
            userpass = req.get('userpass')
            if not check_password(userpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid password. Try again.')
                return redirect('/new_loa')
            try:
                proj = projects.objects.get(id = projid)
            except:
                messages.error(request,'Unable to fetch project')
                return redirect('/new_loa')
            if request.FILES:
                if 'loa' in request.FILES:
                    loa = request.FILES['loa']
                    loapath = proj.projectpath + '/Payment/LOA/'
                    smkdir(loapath)
                    try:
                        extension = str(loa.name.split(".")[-1])
                    except:
                        extension = ''
                        
                    subdate = datetime.now().date()
                    filename = "LOA_"+str(subdate)+"_"+str(amt)+"."+extension
                    try:
                        alreadyfile = glob.glob(os.path.join(loapath,"LOA_"+str(subdate)+"_"+str(amt)+'*'))[0]       
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    
                    fullpath = os.path.join(loapath,filename)
                    if handle_uploaded_file(fullpath,loa):
                        newloa = loadata()
                        newloa.project = projects.objects.get(id = projid)
                        newloa.user = newloa.project.userid
                        newloa.amt = amt
                        newloa.filepath = fullpath
                        newloa.subdate = subdate
                        newloa.save()
                        proj.workflow = str(proj.workflow) + ']*[' + 'LOA of cost ₹'+newloa.amt+'placed by entity on '+str(newloa.subdate)
                        notification(users.objects.filter(admin = True)[:1].get().id, 'New LOA for project ID: '+str(proj.newid)+' submitted by '+str(proj.userid.utilname))
                        messages.success(request, 'New LOA placed for project ID '+str(proj.newid))
                        return redirect('/new_loa') 
                    else:
                        messages.error(request, 'Aborted! Unable to upload LOA file')
                        return redirect('/new_loa')
            else:
                messages.error(request, 'Aborted! LOA file not uploaded.')
                return redirect('/new_loa')
    else:
        return oops(request)
def updateloa(request):
    if useronline(request) and not adminonline(request):
        if request.method == 'POST' and request.FILES:
            req = request.POST
            try:
                loaid = req.get('loaid')
                amt = req.get('amt')
                userpass = req.get('userpass')
            except:
                messages.error(request, 'Aborted! Some fields are missing')
                return redirect('/userloa')
            if not check_password(userpass,userDetails(request.session['user'])['password']):
                    messages.error(request, 'Invalid user password.')
                    return redirect('/userloa')
            try:
                thisloa = loadata.objects.get(id = loaid)
            except:
                messages.error(request, 'Aborted! LOA does not exists')
                return redirect('/userloa')
            if not proj_of_user(request, thisloa.project.id):
                messages.error(request, 'Not a valid LOA for user')
                return redirect('/userloa')
            if 'loa' in request.FILES:
                loa = request.FILES['loa']
                
                sremove(thisloa.filepath)
                loapath = thisloa.project.projectpath + '/Payment/LOA/'
                smkdir(loapath)
                
                try:
                    extension = str(loa.name.split(".")[-1])
                except:
                    extension = ''
                    
                subdate = datetime.now().date()
                filename = "LOA_"+str(thisloa.subdate)+"_"+str(amt)+"."+extension
                
                fullpath = os.path.join(loapath,filename)
                if handle_uploaded_file(fullpath,loa):
                    thisloa.subdate = subdate
                    thisloa.amt = amt
                    thisloa.filepath = fullpath
                    thisloa.save(update_fields=['amt','subdate','filepath'])
                    thisproj = projects.objects.get(id = thisloa.project.id)
                    thisproj.workflow = str(thisproj.workflow) + ']*[' + 'LOA updated for amount ₹'+thisloa.amt+' on '+str(thisloa.subdate)
                    thisproj.save(update_fields = ['workflow'])
                    notification(users.objects.filter(admin = True)[:1].get().id, 'LOA for project ID: '+str(thisproj.newid)+' updated by '+str(thisproj.userid.utilname))
                    messages.success(request, 'Success! LOA updated. ')
                    return redirect('/userloa')
                else:
                    messages.error(request, 'Aborted! unable to update file')
                    return redirect('/userloa')
            else:
                messages.error(request, 'Aborted! LOA file not uploaded.')
                return redirect('/userloa')
        else:
            messages.error(request, 'No changes made')
            return redirect('/userloa')
    else:
        return oops(request)

def downloadloa(request, loaid):
    loa = loadata.objects.get(id = loaid)
    # thisuser = getuser(request, request.session['user'])
    
    if proj_of_user(request, loa.project.id):
        
        return handle_download_file(loa.filepath, request)
    else:
        return oops(request)

def adminloa(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['loaprojs'] = loadata.objects.filter(completed = False, approved = False)
        return render(request, 'psdf_main/_admin_loa.html', context)
    else:
        return oops(request)

def userloa(request):
    
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        thisuser = getuser(request)
        # print(thisuser.id)
        # print(thisuser.username)
        # print(thisuser.password)
        context['loaprojs'] = loadata.objects.filter(user = thisuser, completed = False)
        # print(context['loaprojs'])
        # context['loaprojs'] = loadata.objects.all()
        return render(request, 'psdf_main/_user_loa.html', context)

    else:
        return oops(request)

def ack_loa(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            # try:
            loaid = req.get('loaid')
            adminpass = req.get('adminpass')
            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid administrator password.')
                return redirect('/adminloa')
            thisloa = loadata.objects.get(id = loaid)
            thisloa.approved = True
            thisloa.ackdate = datetime.now().date()
            thisloa.save(update_fields=['approved','ackdate'])
            notification(thisloa.user.id, "LOA of amount ₹ "+str(thisloa.amt)+ " acknowledged by PSDF sectt.")
            thisproj = projects.objects.get(id = thisloa.project.id)
            thisproj.workflow = str(thisproj.workflow) + ']*[' + 'LOA of amount ₹'+str(thisloa.amt)+' placed on '+str(thisloa.subdate)+' acknowledged on '+str(thisloa.ackdate)
            thisproj.save(update_fields = ['workflow'])
            messages.success(request, "LOA acknowledged.")
            return redirect('/adminloa')
            # except:
            #     messages.error(request,"Somthing went wrong, while adding remark.")
            #     return redirect('/adminloa')
    else:
        return oops(request)
    
def sendloaremark(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            try:
                loaid = req.get('loaid')
                remark = req.get('remark')
                
                adminpass = req.get('adminpass')
                if not check_password(adminpass,userDetails(request.session['user'])['password']):
                    messages.error(request, 'Invalid administrator password.')
                    return redirect('/adminloa')
                thisloa = loadata.objects.get(id = loaid)
                thisloa.remark = remark
                thisloa.save(update_fields = ['remark'])
                messages.success(request,"Remark added successfully.")
                return redirect('/adminloa')
            except:
                messages.error(request,"Somthing went wrong, while adding remark.")
                return redirect('/adminloa')
    else:
        return oops(request)