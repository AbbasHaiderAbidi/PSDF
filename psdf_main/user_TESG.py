from .helpers import *


def user_tesg(request):
    if useronline(request):
        context = full_user_context(request)
        return render(request, 'psdf_main/_user_TESG_projects.html', context)
    else:
        return oops(request)
    
def user_TESG_chain(request, projid):
    if useronline(request):
        if proj_of_user(request, projid):
            context = full_user_context(request)
            context['proj'] = projects.objects.get(id = projid)
            context['proj_tesg'] = TESG_master.objects.filter(project = context['proj'])
            if TESG_master.objects.filter(project = context['proj'], active = True):
                context['current_tesg'] = TESG_master.objects.filter(project = context['proj'], active = True)[:1].get()
            return render(request, 'psdf_main/_user_TESG.html', context)
        else:
            return oops(request)
    else:
        return oops(request)

def user_tesg_response(request):
    if useronline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req['projid']
            tesg_no = req['tesg_no']
            userpass = req['userpass']
            tesg_response = req['tesg_response']
            if tesg_response == '' or tesg_response == None:
                messages.error(request, 'Enter a valid response')
                return user_TESG_chain(request, projid)
            if proj_of_user(request, projid):
                if not check_password(userpass,userDetails(request.session['user'])['password']):
                    messages.error(request, 'Invalid user password.')
                    return user_TESG_chain(request, projid)
                
                admin_tesg = TESG_admin.objects.filter(TESG_no = tesg_no)[:1].get()
                admin_project = projects.objects.filter(id = projid, deny=False)[:1].get()
                this_tesg = TESG_master.objects.filter(project = admin_project, tesgnum = admin_tesg, active = True)[:1].get()
                tesgpath = ''
                fullpath = ''
                if 'responses' in request.FILES:
                    responses = request.FILES['responses']
                    tesgpath = projects.objects.get(id = projid).projectpath + '/TESG/'
                    smkdir(tesgpath)
                    try:
                        alreadyfile = glob.glob(os.path.join(tesgpath,str(tesg_no)+'_response')+'*')[0]
                        
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                        
                    except:
                        pass
                    try:
                        extension = str(responses.name.split(".")[-1])
                    except:
                        extension = ''
                    fullpath = os.path.join(tesgpath,str(str(tesg_no)+'_response'+ "." +extension ))
                    if handle_uploaded_file(fullpath,responses):
                        pass
                    else:
                        return oops(request)
                    
                this_tesg.user_res_date = datetime.now().date()
                this_tesg.user_response = tesg_response
                this_tesg.user_filepath = fullpath
                this_tesg.save(update_fields=['user_res_date','user_response','user_filepath'])
                messages.success(request, 'Response of TESG '+tesg_no+' have been intimated to PSDF Sectt.')
                notification(users.objects.filter(admin = True)[:1].get().id, 'TESG #'+tesg_no+' response updated by user '+request.session['user'])
                return user_TESG_chain(request, projid)
            else:
                return oops(request)
        else:
            return oops(request)


def download_tesg_user_outcome(request, tesgid):
    if useronline(request):
        
        thisisimp = TESG_master.objects.get(id = tesgid)
        username = thisisimp.project.userid.username
        if not username == request.session['user']:
            return oops(request)
        
        tesgpath = TESG_master.objects.get(id = tesgid).admin_filepath
        if tesgpath == '' or tesgpath == None:
            messages.error(request, 'Function is not available.')
            return redirect('/user_TESG_chain/'+str(thisisimp.project.id))
        if not os.path.exists(thisisimp.admin_filepath):
            messages.error(request, 'Function is not available.')
            return redirect('/user_TESG_chain/'+str(thisisimp.project.id))
        
        return handle_download_file(thisisimp.admin_filepath, request)
    else:
        return oops(request)
    
def download_tesg_user_response(request, tesgid):
    if useronline(request):
        thisisimp = TESG_master.objects.get(id = tesgid)
        username = thisisimp.project.userid.username
        if not username == request.session['user']:
            return oops(request)
        
        tesgpath = TESG_master.objects.get(id = tesgid).user_filepath
        if tesgpath == '' or tesgpath == None:
            messages.error(request, 'Function is not available.')
            return redirect('/user_TESG_chain/'+str(thisisimp.project.id))
        if not os.path.exists(thisisimp.user_filepath):
            messages.error(request, 'Function is not available.')
            return redirect('/user_TESG_chain/'+str(thisisimp.project.id))
        
        return handle_download_file(thisisimp.user_filepath, request)
    else:
        return oops(request)