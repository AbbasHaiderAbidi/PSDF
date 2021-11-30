from .helpers import *


def appraisal_projects(request):
    # pro = projects.objects.filter(status = '3')[:1].get()
    # pro.status ='2'
    # pro.save(update_fields=['status'])
    if adminonline(request):
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_appraisal_projects.html', context)
    else:
        return oops(request)
    
def approve_appraisal(request, projectid):
    if adminonline(request):
        # context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            try:
                if not Appraisal_admin.objects.filter(project = projects.objects.get(id = projectid))[:1].get():
                    messages.success(request, 'Aborted! No entry regarding appraisal exists.')
                    return redirect('/appraisal_projects/')
            except:
                messages.success(request, 'Aborted! No entry regarding appraisal exists.')
                return redirect('/appraisal_projects/')
            if check_password(adminpass,users.objects.get(id = getadmin_id()).password):
                project = projects.objects.get(id = projectid)
                project.status = '3'
                appraprdate =  datetime.now().date()
                project.workflow = str(project.workflow) + ']*[' + 'Project approved in Appraisal phase on ' + str(appraprdate)
                project.appraprdate = appraprdate
                project.save(update_fields=['status','appraprdate'])
                messages.success(request, 'Project : '+ project.name + ' has been approved Appraisal Committee.')
                proji = projects.objects.get(id = projectid)
                notification(proji.userid.id, 'Project ID: '+str(proji.newid)+', name: '+str(proji.name)+' has been approved by Appraisal committee')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            
            return redirect('/appraisal_projects/')
        else:
            return oops(request)
    else:
        return oops(request)



def delete_appr_doc(aprid):
    thisapr = Appraisal_admin.objects.get(id = aprid)
    if sremove(thisapr.apprpath):
        return True
    else:
        return False
def del_appr_mom(request, aprid):
    if adminonline(request):
        delete_appr_doc(aprid)
        Appraisal_admin.objects.get(id = aprid).delete()
        messages.success(request,'Appraisal Entry deleted')
        return redirect('/view_apprs')
    else:
        return oops(request)

# def delete_appr_doc(request, projid):
#     if adminonline(request):
#         thisproject = Appraisal_admin.objects.filter(projid = projid)[:1].get()
#         filepathway = thisproject.filepath
#         thisproject.filepath = ''
#         thisproject.save(update_fields = ['filepath'])
#         if sremove(filepathway):
#             messages.error(request, 'File removed successfully')
#             return redirect('/appraisal_projects/')
#         else:
#             messages.error(request, 'Unable to remove the file.')
#             return redirect('/appraisal_projects/')
        
#     else:
#         return oops(request)
    
def send_to_tesg(request, projid):
    if adminonline(request):
        thisproject = projects.objects.get(id = projid)
        thisproject.status = '1'
        thisproject.workflow = str(thisproject.workflow) + ']*[' + 'Reverted back to TESG by Appraisal committee on ' + str(datetime.now().date())
        thisproject.appraprdate = None
        thisproject.tesgaprdate = None
        thisproject.save(update_fields = ['status', 'workflow','appraprdate','tesgaprdate'])
        notification(thisproject.userid.id, 'Project ID: '+str(thisproject.newid)+ ' ,name: '+str(thisproject.name) +' sent back to TESG by PSDF Sectt.')
        messages.success(request, 'Project '+ thisproject.name +' sent back to TESG.')
        return redirect('/appraisal_projects')
    else:
        return oops(request)