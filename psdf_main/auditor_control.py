from .helpers import *

def auditor_dashboard(request):
    if auditoronline(request):
        context = full_auditor_context(request)
        return render(request, 'psdf_main/_auditor_dashboard.html', context)
    else:
        return oops(request)


def auditor_view_TESGs(request):
    if auditoronline(request):
        context = full_auditor_context(request)
        context['tesgs'] = TESG_admin.objects.all()
        context['adt'] = '1'
        return render(request, 'psdf_main/_auditor_view_tesgs.html', context)
    else:
        return oops(request)
    
def auditor_view_apprs(request):
    if auditoronline(request):
        context = full_auditor_context(request)
        context['apprs'] = Appraisal_admin.objects.all()
        context['adt'] = '1'
        return render(request, 'psdf_main/_auditor_view_apprs.html', context)
    else:
        return oops(request)
    
def auditor_view_monis(request):
    if auditoronline(request):
        context = full_auditor_context(request)
        context['monis'] = Monitoring_admin.objects.all()
        context['adt'] = '1'
        return render(request, 'psdf_main/_auditor_view_monis.html', context)
    else:
        return oops(request)
    
def auditor_view_projects(request):
    if auditoronline(request):
        context = full_auditor_context(request)
        context['temp_projs'] = temp_projects.objects.all()
        context['projs'] = projects.objects.all()
        return render(request, 'psdf_main/_auditor_view_projects.html', context)
    else:
        return oops(request)
    
def auditor_project_details(request, projid):
    if auditoronline(request):
        context = full_auditor_context(request)
        context['proj'] = projects.objects.get(id = projid)
        context['proj'].workflow = context['proj'].workflow.split(']*[')[1:]
        context['tesgs'] = TESG_master.objects.filter(project = context['proj'])
        return render(request, 'psdf_main/_auditor_view_project.html', context)
    else:
        return oops(request)
    
def auditor_view_user(request, userid):
    if auditoronline(request):
        context = full_auditor_context(request)
        context['THIS_USER'] = users.objects.get(id = userid)
        context['THIS_PROJECTS'] = projects.objects.filter(userid = userid)
        context['THIS_temp_PROJECTS'] = temp_projects.objects.filter(userid = userid)
        context['numpending'] = temp_projects.objects.filter(userid = userid).count()
        context['numaccept'] = projects.objects.filter(userid = context['THIS_USER']).count()
        context['numapprove'] = projects.objects.filter(userid = userid, status = '5').count()
        context['numreject'] = projects.objects.filter(userid = userid, deny = True).count() + temp_projects.objects.filter(userid = userid, deny = True).count()
        
        return render(request, 'psdf_main/_auditor_view_user.html', context)
    else:
        return oops(request)
    

def auditor_download_project(request, projid):
    try:
        type_n_id = projid.split('_')
        file_type = type_n_id[0]
        proid = type_n_id[1]
    except:
        return oops(request)

    if auditoronline(request):
        if projid:
            filelist = {'DPR':'DPR', 'forms':'forms','otherdocs':'otherdocs'}
            proj_path = projects.objects.get(id = proid)
            if proj_path :
                proj_path = proj_path.projectpath
                filepath = os.path.join(glob.glob(proj_path+'/'+filelist[file_type]+'*')[0])
                return handle_download_file(filepath, request)
    return oops(request)
