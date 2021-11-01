from .helpers import *



def view_user(request, userid):
    if adminonline(request):
        context = full_admin_context(request)
        context['THIS_USER'] = users.objects.get(id = userid)
        context['THIS_PROJECTS'] = projects.objects.filter(userid = userid)
        context['THIS_temp_PROJECTS'] = temp_projects.objects.filter(userid = userid)
        context['numpending'] = temp_projects.objects.filter(userid = userid).count()
        context['numaccept'] = projects.objects.filter(userid = context['THIS_USER']).count()
        context['numapprove'] = projects.objects.filter(userid = userid, status = '5').count()
        context['numreject'] = projects.objects.filter(userid = userid, deny = True).count() + temp_projects.objects.filter(userid = userid, deny = True).count()
        
        return render(request, 'psdf_main/_admin_view_user.html', context)
    else:
        return oops(request)
    

def view_TESGs(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['tesgs'] = TESG_admin.objects.all()
        return render(request, 'psdf_main/_admin_view_tesgs.html', context)
    else:
        return oops(request)
    

def view_apprs(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['apprs'] = Appraisal_admin.objects.all()
        return render(request, 'psdf_main/_admin_view_apprs.html', context)
    else:
        return oops(request)


def view_monis(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['monis'] = Monitoring_admin.objects.all()
        return render(request, 'psdf_main/_admin_view_monis.html', context)
    else:
        return oops(request)

def view_all_projs(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['all_projs'] = projects.objects.filter(deny = False)
        context['all_rprojs'] = projects.objects.filter(deny = True)
        context['all_rpprojs'] = temp_projects.objects.filter(deny = True)
        context['all_temps'] = temp_projects.objects.filter(deny = False)
        context['npending'] = temp_projects.objects.filter(deny = False).count()
        context['ntesg'] = projects.objects.filter(status = '1', deny = False).count()
        context['nappr'] = projects.objects.filter(status = '2', deny = False).count()
        context['nmoni'] = projects.objects.filter(status = '3', deny = False).count()
        context['nfinal'] = projects.objects.filter(status = '4', deny = False).count()
        context['nreject'] = projects.objects.filter(deny = True).count() + temp_projects.objects.filter(deny = True).count()
        return render(request, 'psdf_main/_admin_view_all_projects.html', context)
    else:
        return oops(request)





def download_tesg_report(request, tesgid):
    if adminonline(request) or auditoronline(request):
        try:
            return handle_download_file(TESG_admin.objects.get(id = tesgid).filepath, request)
        except:
            return oops(request)
    else:
        return oops(request)
    
def download_appr_mom(request, apprid):
    if adminonline(request) or auditoronline(request):
        try:
            return handle_download_file(Appraisal_admin.objects.get(id = apprid).apprpath, request)
        except:
            return oops(request)
    else:
        return oops(request)
    
    
def download_moni_mom(request, moniid):
    if adminonline(request) or auditoronline(request):
        try:
            return handle_download_file(Monitoring_admin.objects.get(id = moniid).monipath, request)
        except:
            return oops(request)
    else:
        return oops(request)
    

def admin_boq_view(request, projid):
    if adminonline(request):
        splits = projid.split('_')
        projid = splits[0]
        backpage = splits[1]
        if backpage == 'underexamination':
            proj = temp_projects.objects.get(id = projid)
        else:
            proj = projects.objects.get(id = projid)
        backpages = {'adminmonitoringprojects':'monitoring_projects','adminappraisalprojects':'appraisal_projects','admintesgprojects':'TESG_projects', 'adminallprojects':'view_all_projects'}
        try:
            a = backpages[backpage]
        except:
            return oops(request)
        context = full_admin_context(request)
        if backpage == 'underexamination':
            project = projects.objects.get(id = proj.id)
            context['proj'] = project
            
            context['backpage'] = backpages[backpage]
                
            return render(request, 'psdf_main/_admin_view_boq.html', context)
        else:
            context['proj'] = proj
            context['sub_boq'] = boqdata.objects.filter(project = context['proj'], boqtype = '1')
            context['sub_boq_total'] = boq_grandtotal(context['sub_boq'])
            context['approved_boq'] = boqdata.objects.filter(project = context['proj'], boqtype = '2')
            context['approved_boq_total'] = boq_grandtotal(context['approved_boq'])
            context['backpage'] = backpages[backpage]
            return render(request, 'psdf_main/_admin_view_project_boq.html', context)
    else:
        return oops(request)