from .helpers import *



    
def admin_project_details(request, projid):
    if adminonline(request):
        context = full_admin_context(request)
        context['proj'] = projects.objects.get(id = projid)
        context['proj'].workflow = context['proj'].workflow.split(']*[')[1:]
        context['tesgs'] = TESG_master.objects.filter(project = context['proj'])
        return render(request, 'psdf_main/_admin_view_project.html', context)
    else:
        return oops(request)
    
def admin_temp_project_details(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        context['proj'] = projects.objects.get(id = projectid)
        return render(request, 'psdf_main/_admin_project_details.html', context)
    else:
        return oops(request)
    
def appr_mom_download(request, projid):
    if adminonline(request) or auditoronline(request):
        try:
            appr = Appraisal_admin.objects.filter(project = projects.objects.get(id = projid))
            maxid = 0
            thisone = appr[:1].get()
            if appr:
                for app in appr:
                    if app.id > maxid:
                        thisone = app
                        maxid = app.id

                return handle_download_file(thisone.apprpath, request)
            else:
                return oops(request)
        except :
            return oops(request)
            
    else:
        return oops(request)
    
def moni_mom_download(request, projid):
    if adminonline(request) or auditoronline(request):
        try:
            moni = Monitoring_admin.objects.filter(project = projects.objects.get(id = projid))
            maxid = 0
            thisone = moni[:1].get()
            if moni:
                for mon in moni:
                    if mon.id > maxid:
                        thisone = mon
                        maxid = mon.id

                return handle_download_file(thisone.monipath, request)
            else:
                return oops(request)
        except :
            return oops(request)
    else:
        return oops(request)