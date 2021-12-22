from .helpers import *

def user_appraisal_projects(request):
    if useronline(request):
        context = full_user_context(request)
        context['appraisal_projs'] = projects.objects.filter(status = '2')
        context['appr_proj'] = Appraisal_admin.objects.filter(userid = getuser(request))
        workflow = {}
        workflow_list = []
        for proj in context['appraisal_projects']:
            workflow['id'] = proj.id
            workflow['events'] = proj.workflow.split(']*[')[1:]
            workflow_list.append(workflow)
        context['workflow_list'] = workflow_list
        return render(request, 'psdf_main/_user_appraisal_projects.html', context)
    else:
        return oops(request)


    
def udownload_appr_mom(request, apprid):
    try:
        oro = Appraisal_admin.objects.filter(project = projects.objects.get(id = apprid))[:1].get()
    except:
        messages.error(request,'Appraisal Report not availble')
        return oops(request)
    
    if proj_of_user(request,oro.project.id) or auditoronline(request) :
        try:
            return handle_download_file(oro.apprpath, request)
        except:
            messages.error(request,'Unable to fetch report')
            return oops(request)
    else:
        return oops(request)
    
 
 
 