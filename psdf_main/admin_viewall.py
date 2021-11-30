from .helpers import *



def view_user(request, userid):
    if adminonline(request):
        context = full_admin_context(request)
        context['THIS_USER'] = users.objects.get(id = userid)
        context['THIS_PROJECTS'] = projects.objects.filter(userid = userid)
        context['THIS_temp_PROJECTS'] = temp_projects.objects.filter(userid = userid)
       
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
    

def del_tesg(request, tesgid):
    if adminonline(request):
        istheretesg = TESG_master.objects.filter(tesgnum = TESG_admin.objects.get(id = tesgid))
        if istheretesg:
            messages.error(request, "Cannot delete a valid TESG entry")
            return view_TESGs(request)
        else:
            try:
                todel = TESG_admin.objects.get(id = tesgid)
                sremove(todel.filepath)
                todel.delete()
                messages.success(request, "TESG entry deleted")
                return view_TESGs(request)
            except:
                return oops(request)
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
    # proj = projects.objects.filter(status = '7')[:1].get()
    # proj.status = '6'
    # proj.save(update_fields=['status'])
    if adminonline(request):
        context = full_admin_context(request)
        context['all_aprojs'] = projects.objects.filter((Q(status = '1')| Q(status = '2')| Q(status = '3')| Q(status = '4')| Q(status = '5')| Q(status = '6')| Q(status = '7')),deny = False)
        
        context['all_rprojs'] = projects.objects.filter(deny = True)
        context['all_docprojs'] = projects.objects.filter(status = '5')
        context['all_pays'] = projects.objects.filter(status = '6')
        context['all_rpprojs'] = temp_projects.objects.filter(deny = True)
        context['all_temps'] = temp_projects.objects.filter(deny = False)
        context['all_comp'] = projects.objects.filter(status = '9', deny = False)
        
        context['npays'] = context['all_pays'].count()
        context['ncomp'] = context['all_comp'].count()
        context['ndocs'] = context['all_docprojs'].count()
        context['npending'] = context['all_temps'].count()
        context['ntesg'] = projects.objects.filter(status = '1', deny = False).count()
        context['nappr'] = projects.objects.filter(status = '2', deny = False).count()
        context['nmoni'] = projects.objects.filter(status = '3', deny = False).count()
        context['nfinal'] = projects.objects.filter(status = '4', deny = False).count()
        context['nreject'] = context['all_rprojs'].count() + context['all_rpprojs'].count()
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
    
    
def view_all_pays(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['all_pays'] = payment.objects.all()
        
        paytotal = 0
        for pay in context['all_pays']:
            paytotal = paytotal + int(pay.amount)
        context['paytotal'] = paytotal
        
        loatotal = 0
        loas = loadata.objects.all()
        for loa in loas:
            loatotal = loatotal + int(loa.amt)
        context['loatotal'] = loatotal
        
        context['pendingamt'] = loatotal - paytotal
        
        init_pays = init_payment.objects.all()
        totalinit = 0
        for init in init_pays:
            totalinit = totalinit + int(init.amount)
        context['totalinit'] = totalinit
        
        
            
        context['all_init_pays'] = init_payment.objects.all()
        return render(request,'psdf_main/_admin_view_pays.html',context)
    else:
        return oops(request)
    
def download_data_bank(request, projid):
    if proj_of_user(request, projid):
        thisproj = projects.objects.get(id = projid)
        userpath = ''
        splits = str(thisproj.projectpath).split('/')
        for i in range(1,len(splits)-1):
            userpath = userpath +'/' + str(splits[i])
            
        datapath = str(userpath)+'/'+str(thisproj.newid)
        if os.path.exists(datapath+'.zip'):
            sremove(datapath+'.zip')
        
        try:
            shutil.make_archive(datapath, 'zip', thisproj.projectpath)
        except:
            return oops(request)
        try:
            return handle_download_file(datapath+'.zip', request)
        except:
            return oops(request)
        
        
        