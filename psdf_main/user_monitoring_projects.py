from .helpers import *

def user_monitoring_projects(request):
    if useronline(request):
        context = full_user_context(request)
        context['monitoring_projects'] = projects.objects.filter(Q(status = '3')|Q(status = '4'), userid = getuser(request).id)
        # context['moni_admin'] = Monitoring_admin.objects.filter(userid = getuser(request).id)
        workflow = {}
        workflow_list = []
        for proj in context['monitoring_projects']:
            workflow['id'] = proj.id
            workflow['events'] = proj.workflow.split(']*[')[1:]
            workflow_list.append(workflow)
        context['workflow_list'] = workflow_list
        return render(request, 'psdf_main/_user_monitoring_projects.html', context)
    else:
        return oops(request)


   
def udownload_moni_mom(request, moniid):
    try:
        oro = Monitoring_admin.objects.filter(project = projects.objects.get(id = moniid))[:1].get()
    except:
        messages.error(request,'Monitoring report not available')
        return oops(request)
    
    if proj_of_user(request,oro.project.id) or auditoronline(request):
        try:
            return handle_download_file(oro.monipath, request)
        except:
            messages.error(request,'Unable to fetch report')
            return oops(request)
    else:
        return oops(request)
    
