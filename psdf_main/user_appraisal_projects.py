from .helpers import *

def user_appraisal_projects(request):
    if useronline(request):
        context = full_user_context(request)
        # context['appraisal_projs'] = Appraisal_admin.objects.filter(userid = users.objects.get(id = userDetails(request.session['user'])['id']))
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


def user_appraisal_report(request, projid):
    if useronline(request) and request.session['user'] == projects.objects.get(id = projid).userid.username:
        context = full_user_context(request)
        filepath = Appraisal_admin.objects.filter(projid = projid)[:1].get().filepath
        if os.path.exists(filepath):
            return handle_download_file(filepath, request)
        else:
            messages.error(request, 'File does not exists')
            return redirect('/user_appraisal_projects')
    else:
        return oops(request)