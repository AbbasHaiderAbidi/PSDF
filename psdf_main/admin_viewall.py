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
            # try:
            todel = TESG_admin.objects.get(id = tesgid)
            thistesg = str(todel.TESG_no)
            sremove(todel.filepath)
            todel.delete()
            
            for proj in projects.objects.all():
                tesg_list = str(proj.tesg_list).split(',')
                # print(tesg_list)
                if thistesg in tesg_list:
                    tesg_list.remove(thistesg)
                # print(tesg_list)
                new_tesg_list = ''
                for item in tesg_list:
                    if new_tesg_list == '':
                        new_tesg_list = item
                    else:
                        new_tesg_list = new_tesg_list + ',' + item
                proj.tesg_list = new_tesg_list
                # print(proj.tesg_list)
                proj.save(update_fields = ['tesg_list'])
                
                messages.success(request, "TESG entry deleted")
                return redirect('/view_TESGs')
            # except:
            #     return oops(request)
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
        context['all_projs'] = projects.objects.all()
        # context['all_rprojs'] = projects.objects.filter(deny = True, userid = userobj)
        # context['all_rpprojs'] = temp_projects.objects.filter(deny = True, userid = userobj)
        # context['all_temps'] = temp_projects.objects.filter(userid = userobj)
        context['npending'] = temp_projects.objects.filter(deny = False).count()
        context['ntesg'] = projects.objects.filter(status = '1', deny = False).count()
        context['nappr'] = projects.objects.filter(status = '2', deny = False).count()
        context['nmoni'] = projects.objects.filter(status = '3', deny = False).count()
        context['nfinal'] = projects.objects.filter(status = '4', deny = False).count()
        context['npays'] = projects.objects.filter((Q(status='7')|Q(status = '6')), deny = False).count()
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
    else:
        return oops(request)

def view_exts(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['pendingext'] = projects.objects.filter(ext__isnull = False, deny=False)
        # context['pendingextp'] = projects.objects.filter(extF__isnull = False, deny=False)
        extlist =[]
        for k in context['pendingext']:
            kill = {}
            kill['id'] = k.id
            kill['newid'] = k.newid
            kill['name'] = k.name
            kill['schedule'] = k.schedule
            kill['orischedule'] = k.orischedule
            if not (k.ext == None or k.ext == ''):
                kill['extensions'] = transformext(k.ext)
            else:
                kill['extensions'] = ''
            extlist.append(kill)
        # extlistp = []
        # for k in context['pendingextp']:
        #     kill = {}
        #     kill['id'] = k.id
        #     kill['newid'] = k.newid
        #     kill['name'] = k.name
        #     kill['schedule'] = k.schedule
        #     kill['orischedule'] = k.orischedule
        #     try:
        #         kill['filename'] = str(k.extF).split("(@)")[1]
        #         kill['extension'] = str(k.extF).split("(@)")[0]
        #     except:
        #         kill['filename'] = ''
        #         kill['extension'] = ''
        #     extlistp.append(kill)
        context['extlist'] = extlist
        # context['pextlist'] = extlistp
        context['projectlist'] = projects.objects.filter(userid = getuser(request), deny=False)
        return render(request,'psdf_main/_admin_view_exts.html',context)
    else:
        return oops(request)
    
    
def view_loas(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['loadata'] = loadata.objects.all()
        if request.method == 'POST':
            req = request.POST
            adminpass = req.get('adminpass')
            loaid = req.get('loaid')
            if not check_password(adminpass,getuser(request).password):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/view_loas')
            thisloa = loadata.objects.get(id = loaid)
            thisloa.compdate = datetime.now().date()
            thisloa.completed = True
            thisloa.save(update_fields = ['compdate','completed'])
            messages.success(request,'LOA has been closed.')
            notification(thisloa.user.id,'LOA of amount ₹'+str(thisloa.amt)+' submitted on date '+str(thisloa.subdate)+' has been closed with a difference of ₹'+str(int(thisloa.amt)-int(thisloa.amt_released)))
            workflow(thisloa.project.id,'LOA of amount ₹'+str(thisloa.amt)+' submitted on date '+str(thisloa.subdate)+' has been closed with a difference of ₹'+str(int(thisloa.amt)-int(thisloa.amt_released)))
        return render(request,'psdf_main/_admin_view_loas.html',context)
        
    else:
        return oops(request)
        
        
def add_loa_remark(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            loaid = req.get('loaid')
            remark = req.get('remark')
            thisloa = loadata.objects.get(id = loaid)
            thisloa.remark = remark
            thisloa.save(update_fields = ['remark'])
            messages.success(request,'Remark field updated.')
            return redirect('/view_loas')
    else:
        return oops(request)