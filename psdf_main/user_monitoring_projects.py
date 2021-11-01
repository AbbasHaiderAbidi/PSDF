from .helpers import *

def user_monitoring_projects(request):
    if useronline(request):
        context = full_user_context(request)
        # context['monitoring_projects'] = Monitoring_admin.objects.filter(userid = users.objects.get(id = userDetails(request.session['user'])['id']))
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