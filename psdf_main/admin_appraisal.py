from .helpers import *


def appraisal_projects(request):
    if adminonline(request):
        context = full_admin_context(request)
        
        context['appr_projects'] = Appraisal_admin.objects.all()
        return render(request, 'psdf_main/_admin_appraisal_projects.html', context)
    else:
        return oops(request)
    
def approve_appraisal(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            # if not Appraisal_admin.objects.filter(projid = projectid)[:1].get():
            #     messages.success(request, 'Aborted! No entry regarding appraisal exists.')
            #     return redirect('/appraisal_projects/')
            if check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = projectid)
                project.status = '3'
                appraprdate =  datetime.now().date()
                project.workflow = str(project.workflow) + ']*[' + 'Project approved in Appraisal phase on ' + str(appraprdate)
                project.appraprdate = appraprdate
                project.save(update_fields=['status','appraprdate'])
                messages.success(request, 'Project : '+ project.name + ' has been approved Appraisal Committee.')
                notification(projects.objects.get(id = projectid).userid.id, 'Project ID: '+projectid+' has been approved by Appraisal committee')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            
            return redirect('/appraisal_projects/')
        else:
            return oops(request)
    else:
        return oops(request)


    
def delete_appr_doc(request, projid):
    if adminonline(request):
        thisproject = Appraisal_admin.objects.filter(projid = projid)[:1].get()
        filepathway = thisproject.filepath
        thisproject.filepath = ''
        thisproject.save(update_fields = ['filepath'])
        if sremove(filepathway):
            messages.error(request, 'File removed successfully')
            return redirect('/appraisal_projects/')
        else:
            messages.error(request, 'Unable to remove the file.')
            return redirect('/appraisal_projects/')
        
    else:
        return oops(request)
    
def send_to_tesg(request, projid):
    if adminonline(request):
        thisproject = projects.objects.get(id = projid)
        thisproject.status = '1'
        thisproject.workflow = str(thisproject.workflow) + ']*[' + 'Reverted back to TESG by Appraisal committee on ' + str(datetime.now().date())
        thisproject.appraprdate = None
        thisproject.tesgaprdate = None
        thisproject.save(update_fields = ['status', 'workflow','appraprdate','tesgaprdate'])
        notification(thisproject.userid.id, 'Project '+ thisproject.name +' sent back to TESG by PSDF Sectt.')
        messages.success(request, 'Project '+ thisproject.name +' sent back to TESG.')
        return redirect('/appraisal_projects')
    else:
        return oops(request)