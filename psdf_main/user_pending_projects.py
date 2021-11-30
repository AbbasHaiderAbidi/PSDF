from .helpers import *

def under_examination(request):
    if useronline(request):
        context = full_user_context(request)
        userobj = users.objects.get(id = context['user']['id'])
        projectobj = temp_projects.objects.filter(userid = userobj, deny = False)
        context['projectobj']= projectobj
        context['noprojobj']= projectobj.count()
        
        return render(request, 'psdf_main/_user_under_examination.html', context)
    else:
        return oops(request)
    
def upload_dpr_docs(request):
    if useronline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req['projid']
            thisproject = temp_projects.objects.get(id = projid)
            projpath = thisproject.projectpath
            if request.FILES:
                files = request.FILES
                if 'dpr' in files.keys():
                    dpr = request.FILES['dpr']
                    try:
                        extension = dpr.name.split('.')[-1]
                    except:
                        extension = ''
                    try:
                        dprfilenames = glob.glob(projpath+'/DPR*')
                        for dprfilename in dprfilenames:
                            sremove(dprfilename)
                        if handle_uploaded_file(projpath+'/DPR.'+extension, dpr):
                            messages.success(request, "Project DPR updated.")
                        else:
                            return oops(request)
                        
                    except :
                        messages.error(request, "Some error has occurred")
                        return redirect('/under_examination')
                if 'forms' in files.keys():
                    forms = request.FILES['forms']
                    try:
                        extension = forms.name.split('.')[-1]
                    except:
                        extension = ''
                    try:
                        formfilenames = glob.glob(projpath+'/forms*')
                        for formfilename in formfilenames:
                            sremove(formfilename)
                        if handle_uploaded_file(projpath+'/forms.'+extension, forms):
                            messages.success(request, "Project Forms updated.")
                        else:
                            return oops(request)
                    except :
                        messages.error(request, "Some error has occurred")
                        return redirect('/under_examination')
                if 'otherdocs' in files.keys():
                    otherdocs = request.FILES['otherdocs']
                    try:
                        extension = otherdocs.name.split('.')[-1]
                    except:
                        extension = ''
                    try:
                        otherfilenames = glob.glob(projpath+'/otherdocs*')
                        for otherfilename in otherfilenames:
                            sremove(otherfilename)
                        if handle_uploaded_file(projpath+'/otherdocs.'+extension, otherdocs):
                            messages.success(request, "Other documents updated.")
                        else:
                            return oops(request)
                    except :
                        messages.error(request, "Some error has occurred")
                        return redirect('/under_examination')
                return redirect('/under_examination')
            else:
                return oops(request)
        else:
            return oops(request)
    else:
        return oops(request)