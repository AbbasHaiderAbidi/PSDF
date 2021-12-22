
# from django.db.models.fields import NullBooleanField
from .helpers import *


def apply_ext(request):
    # proj = projects.objects.get(id = '1')
    
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            try:
                context['project'] = projects.objects.get(id = projid, userid = getuser(request))
            except:
                messages.error(request,"No such project exists")
                return redirect('/apply_ext')
        context['pendingext'] = projects.objects.filter(ext__isnull = False, deny=False, userid = getuser(request))
        context['pendingextp'] = projects.objects.filter(extF__isnull = False, deny=False, userid = getuser(request))
        extlist =[]
        for k in context['pendingext']:
            kill = {}
            kill['id'] = k.id
            kill['newid'] = k.newid
            kill['name'] = k.name
            kill['schedule'] = k.schedule
            kill['orischedule'] = k.orischedule
            if not (k.ext == None or k.ext == ''):
                kill['extensions'] = transformext(k.ext)
            else:
                kill['extensions'] = ''
            extlist.append(kill)
        extlistp = []
        for k in context['pendingextp']:
            kill = {}
            kill['id'] = k.id
            kill['newid'] = k.newid
            kill['name'] = k.name
            kill['schedule'] = k.schedule
            kill['orischedule'] = k.orischedule
            try:
                kill['filename'] = str(k.extF).split("(@)")[1]
                kill['extension'] = str(k.extF).split("(@)")[0]
            except:
                kill['filename'] = ''
                kill['extension'] = ''
            extlistp.append(kill)
        context['extlist'] = extlist
        context['pextlist'] = extlistp
        context['projectlist'] = projects.objects.filter(userid = getuser(request), deny=False)
        return render(request, 'psdf_main/_user_extension.html', context)
    else:
        return oops(request)
    
def apply_ext_conf(request):
    if useronline(request) and not adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if request.FILES:
                if 'extfile' in request.FILES:
                    projid = req.get('projid')
                    ext = req.get('ext')
                    userpass = req.get('userpass')
                    extfile = request.FILES['extfile']
                    try:
                        thisproj = projects.objects.get(id = projid)
                    except:
                        messages.error(request,"No such project exists")
                        return redirect('/apply_ext')
                    if not proj_of_user(request, projid):
                        messages.error(request,"No such project exists")
                        return redirect('/apply_ext')
                    if not check_password(userpass,getuser(request).password):
                        messages.error(request,"Invalid User password")
                        return redirect('/apply_ext')
                    if not isnum(ext):
                        messages.error(request,"Extension must be the number of months.")
                        return redirect('/apply_ext')
                    try:
                        extension = str(extfile.name.split(".")[-1])
                    except:
                        extension = ''
                    thisdate = str(datetime.now())
                    filename = str(thisdate).replace(' ','') +'.'+extension
                    extend = str(ext)+'(@)'+filename 
                    if smkdir(str(thisproj.projectpath)+'/Extensions/'):
                        
                        if handle_uploaded_file(str(thisproj.projectpath)+'/Extensions/'+filename, extfile):
                            thisproj.extF = extend
                            thisproj.workflow = str(thisproj.workflow) + ']*[' + "Project Scheducle extension requested on "+thisdate
                            thisproj.save(update_fields = ['extF','workflow'])
                            messages.success(request, "Extension filed successfully, awaiting confirmation.")
                            notification(getadmin_id(),"Extension request for project ID: "+str(thisproj.newid)+" of "+str(ext)+" months submitted by "+str(thisproj.userid.username))
                            return redirect('/apply_ext')
                    return oops(request)
                else:
                    return oops(request)
            else:
                messages.error(request,"No supporting file uploaded")
                return redirect('/apply_ext')
    else:
        return oops(request)
    
    
def download_ext_file(request, idstr):
    try:
        projid = idstr.split('_')[0]
        filename = idstr.split('_')[1]
    except:
        
        return oops(request)
    if proj_of_user(request, projid):
        try:
            thisproj = projects.objects.get(id = projid)
        except:
            
            return oops(request)
        filepath = str(thisproj.projectpath)+'/Extensions/'+filename
        if os.path.exists(filepath):
            
            return handle_download_file(filepath, request)
        else:
        
            return oops(request)


def admin_approve_ext(request):
    # ab= projects.objects.get(id = '1')
    # ab.extF  = None
    # ab.save(update_fields=['extF'])
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            adminpass = req.get('adminpass')
            remark = req.get('remark')
            if not check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                messages.error(request, 'Invalid administrator password')
                return redirect('/admin_approve_ext')
            try:
                thisproj = projects.objects.get(id = projid)
            except:
                messages.error(request, 'Invalid project selected.')
                return redirect('/admin_approve_ext')
            extF = thisproj.extF
            print(extF)
            filename = str(extF).split('(@)')[1]
            exte = str(extF).split('(@)')[0]
            thisproj.schedule = int(thisproj.schedule) + int(exte)
            if thisproj.ext == '' or thisproj.ext == ' ' or thisproj.ext == None :
                thisproj.ext = extF
            else:
                thisproj.ext = thisproj.ext + ']*[' + str(extF)
            thisproj.extF = None
            thisproj.remark = remark
            thisproj.remark_date = datetime.now().date()
            thisproj.save(update_fields = ['ext','extF','remark','remark_date'])
            workflow(thisproj.id,"Extension of "+str(exte)+" months for project ID: "+str(thisproj.newid)+" approved by PSDF sectt.")
            notification(thisproj.userid.id,"Extension of "+str(exte)+" months for project: "+str(thisproj.newid)+" approved by PSDF sectt.")
            messages.success(request, 'Extension Request Approved')
        context['pendingext'] = projects.objects.filter(extF__isnull = False, deny=False)
        # abc = projects.objects.filter(newid = '209')[:1].get()
        
        # print(abc.extF)
        print(context['pendingext'])
        extlist =[]
        for k in context['pendingext']:
            kill = {}
            kill['id'] = k.id
            
            kill['reqext'] = str(k.extF).split('(@)')[0]
            kill['filename'] = str(k.extF).split('(@)')[1]
            kill['newid'] = k.newid
            kill['name'] = k.name
            kill['schedule'] = k.schedule
            kill['orischedule'] = k.orischedule
            if not (k.ext == None or k.ext == ''):
                kill['extensions'] = transformext(k.ext)
            else:
                kill['extensions'] = ''
            extlist.append(kill)
            
        context['extlist'] = extlist
        print(extlist)
        return render(request,'psdf_main/_admin_approve_extension.html',context)
    else:
        return oops(request)


def admin_reject_ext(request):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            adminpass = req.get('adminpass')
            remark = req.get('remark')
            if not check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                messages.error(request, 'Invalid administrator password')
                return redirect('/admin_approve_ext')
            try:
                thisproj = projects.objects.get(id = projid)
            except:
                messages.error(request, 'Invalid project selected.')
                return redirect('/admin_approve_ext')
            extF = thisproj.extF
            filename = str(extF).split('(@)')[1]
            exte = str(extF).split('(@)')[0]
            if sremove(thisproj.projectpath+str('/Extensions/')+str(filename)):
                messages.error(request, 'Supporting file removed.')
                
            thisproj.extF = None
            thisproj.remark = remark
            thisproj.remark_date = datetime.now().date()
            thisproj.save(update_fields = ['extF','remark', 'remark_date'])
            workflow(thisproj.id,"Extension of "+str(exte)+" months for project: "+str(thisproj.newid)+" REJECTED by PSDF sectt. ")
            notification(thisproj.userid.id,"Extension of "+str(exte)+" months for project: "+str(thisproj.newid)+" REJECTED by PSDF sectt. (See project remark)")
            context['pendingext'] = projects.objects.filter(extF__isnull = False, deny=False, userid = getuser(request))
            extlist =[]
            for k in context['pendingext']:
                kill = {}
                kill['id'] = k.id
                kill['reqext'] = str(k.extF).split('(@)')[0]
                kill['filename'] = str(k.extF).split('(@)')[1]
                kill['newid'] = k.newid
                kill['name'] = k.name
                kill['schedule'] = k.schedule
                if not (k.ext == None or k.ext == ''):
                    kill['extensions'] = transformext(k.ext)
                else:
                    kill['extensions'] = ''
                extlist.append(kill)
            
            context['extlist'] = extlist
            messages.error(request, 'Extension Request Rejected.')
            return render(request,'psdf_main/_admin_approve_extension.html',context)
        return oops(request)
    else:
        return oops(request)
    
    
def delete_ext_req(request, idstr):
    try:
        filename = idstr.split('_')[1]
        projid = idstr.split('_')[0]
    except:
        return oops(request)
    if useronline(request):
        try:
            thisproj = projects.objects.get(id = projid)
        except:
            messages.error(request, 'Invalid project selected.')
            return redirect('/apply_ext')
        thisproj.extF = None
        if sremove(thisproj.projectpath+str('/Extensions/')+str(filename)):
            messages.success(request,"File has been deleted.")
        thisproj.save(update_fields = ['extF'])
        notification(getadmin_id(),"Extension request for project ID: "+str(thisproj.newid)+" has been deleted by "+ str(thisproj.userid.username))
        workflow(thisproj.id,"Extension request for project ID: "+str(thisproj.newid)+" has been deleted by "+ str(thisproj.userid.username))
        messages.success(request,"Request has been deleted.")
        return redirect('/apply_ext')
    else:
        return oops(request)