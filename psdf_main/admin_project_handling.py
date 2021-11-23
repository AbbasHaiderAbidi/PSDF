from .helpers import *

def acceptdpr(request, projid):
    if adminonline(request):
        if request.POST:
            req = request.POST
            newid = req['newid'+projid]
            fundcategory = req['fundcategory'+projid]
            quantum = req['quantum'+projid]
            remark = ''
            if req['remark'+projid]:
                remark = req['remark'+projid]
            adminpass = req['adminpass'+projid]
            temp_proj = temp_projects.objects.get(id = projid)
            checkingpass = users.objects.filter(username = request.session['user'])[:1].values('password')[0]['password']
            if not check_password(adminpass,checkingpass):
                messages.error(request, 'Invalid admin password, acceptance of project: '+temp_proj.proname+' ABORTED.')
                return redirect('/admin_pending_projects')
            newproject = projects()
            newproject.newid = newid
            newproject.name = temp_proj.proname
            newproject.dprsubdate = temp_proj.dprsubdate
            newproject.amt_asked = temp_proj.amountasked
            newproject.schedule = temp_proj.schedule
            newproject.fundcategory = fundcategory
            newproject.quantumOfFunding = quantum
            newproject.amt_approved = (float(quantum)/100)*float(temp_proj.amountasked)
            newproject.userid = temp_proj.userid
            newproject.tesglist = ''
            if not remark == '':
                newproject.remark = remark
            
            newproject.submitted_boq = temp_proj.submitted_boq
            newproject.remark_date = datetime.now().date()
            newproject.workflow = 'DPR accepted on '+ str(datetime.now().date())
            newproject.save()
            
            sub_boq = get_boq_details(temp_proj.submitted_boq)
            newentry = projects.objects.filter(name = temp_proj.proname, amt_asked = temp_proj.amountasked, userid = temp_proj.userid, schedule = temp_proj.schedule, dprsubdate = temp_proj.dprsubdate, newid=newid)[:1].get()
            for tboq in sub_boq:
                newboq = boqdata()
                newboq.project = newentry
                newboq.boqtype = '1'
                newboq.itemno = tboq['itemno']
                newboq.itemname = tboq['itemname']
                newboq.itemqty = tboq['itemqty']
                newboq.itemdesc = tboq['itemdesc']
                newboq.unitcost = tboq['itemprice']
                newboq.save()
            newpath = '/'.join(temp_proj.projectpath.split('/')[:-2])+'/'+ str(newentry.id)
            if smkdir(newpath):
                for f in glob.glob(temp_proj.projectpath+'/*'):
                    os.replace(f,os.path.join(newpath , f.split('/')[-1]))
                newentry.projectpath = newpath
                newentry.save(update_fields=['projectpath'])
                temp_projects.objects.get(id=temp_proj.id).delete()
                srmdir(temp_proj.projectpath)
                
                project_user = users.objects.get(id = temp_proj.userid.id)
                project_user.notification = str(project_user.notification) + ']*[' + 'Your project : '+ newentry.name +' has been accepted with project ID:' + str(newentry.newid)
                project_user.save(update_fields=['notification'])
                messages.success(request, 'Project: '+newentry.name+' has been successfully accepted with ID: '+str(newentry.newid)+'.')
                return redirect('/admin_pending_projects')

            else:
                messages.error(request, 'Error creating a record.')
                return redirect('/admin_pending_projects')
            return oops(request)
        else:
            return oops(request)
    else:
        return oops(request)


def rejectdpr(request, projid):
    if adminonline(request):
        if request.POST:
            req = request.POST
            rremark = req['rremark'+projid]
            radminpass = req['radminpass'+projid]
            temp_proj = temp_projects.objects.get(id = projid)
            checkingpass = users.objects.filter(username = request.session['user'])[:1].get().password
            if not check_password(radminpass,checkingpass):
                messages.error(request, 'Invalid admin password, acceptance of project: '+temp_proj.proname+' ABORTED.')
                return redirect('/admin_pending_projects')
            temp_proj.deny = True
            temp_proj.remark = rremark
            
            temp_proj.save(update_fields=['dprdenydate','deny','remark'])
            messages.success(request, 'Project : '+ temp_proj.proname + ' has been rejected.')
            return redirect('/admin_pending_projects')
    else:
        return oops(request)


def download_temp_project(request, projid):
    try:
        type_n_id = projid.split('_')
        file_type = type_n_id[0]
        proid = type_n_id[1]
    except:
        return oops(request)
    
    if (adminonline(request) or (useronline(request) and (temp_projects.objects.get(id = proid).userid.username == request.session['user']))):
        if projid:
            filelist = {'DPR':'DPR', 'forms':'forms','otherdocs':'otherdocs'}
            proj_path = temp_projects.objects.get(id = proid)
            
            if proj_path :
                proj_path = proj_path.projectpath
                try:
                    filepath = os.path.join(glob.glob(proj_path+'/'+filelist[file_type]+'*')[0])
                except:
                    return oops(request)
    
                return handle_download_file(filepath, request)
    return oops(request)

def download_project(request, projid):
    try:
        type_n_id = projid.split('_')
        file_type = type_n_id[0]
        proid = type_n_id[1]
    except:
        return oops(request)


    if (adminonline(request) or (useronline(request) and (projects.objects.get(id = proid).userid.username == request.session['user']))):
        if projid:
            filelist = {'DPR':'DPR', 'forms':'forms','otherdocs':'otherdocs'}
            proj_path = projects.objects.get(id = proid)
            if proj_path :
                proj_path = proj_path.projectpath
                try:
                    filepath = os.path.join(glob.glob(proj_path+'/'+filelist[file_type]+'*')[0])
                except:
                    return oops(request)
                return handle_download_file(filepath, request)
    return oops(request)


def rejectproject(request, projid):
    # pages = {'TESG':'/TESG_projects', 'Appraisal':'/appraisal_projects'}
    backpages = {'adminmonitoringprojects':'/monitoring_projects','adminappraisalprojects':'/appraisal_projects','admintesgprojects':'/TESG_projects'}
    if adminonline(request):
        context = full_admin_context(request)
        if request.POST:
            try:
                page_id = projid.split('_')
                proid = page_id[1]
                page = page_id[0]
            except:
                return oops(request)
            req = request.POST
            denydate = req['rejectdate'+proid]
            remark = req['rremark'+proid]
            radmin = req['radminpass'+proid]
            if remark == '':
                messages.success(request, 'Aborted! Remarks cannot be empty')
                return redirect(backpages[page])
            if check_password(radmin,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = proid)
                project.deny = True
                project.denydate = denydate
                project.remark = remark
                project.remark_date = datetime.now().date()
                project.workflow = str(project.workflow) + ']*[' + 'Project rejected on ' + denydate
                project.save(update_fields=['denydate' , 'deny' , 'remark' , 'workflow'])
                messages.success(request, 'Project : ' + project.name + ' has been rejected.')
                notification(project.userid.id, 'Project ID: '+str(project.newid)+' ,name: '+str(project.name)+' has been rejected in '+page+' phase')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            return redirect(backpages[page])
        else:
            return oops(request)
    else:
        return oops(request)
    
    
def update_boq(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)

        projid = projectid
        if request.method == 'POST':
            req = request.POST
            projid = req['projid']
            adminpass = req['adminpass']
            if not check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                messages.warning(request, 'Invalid Administrator password. Aborted!')
                return redirect('/update_boq/0')
            boq_project = projects.objects.get(id = projid)
            if not boq_project:
                messages.warning(request, 'Project does not exist.')
                return redirect('/update_boq/0')
            boqs = []
            for i in range(1,1000):
                if not (req['itemname'+str(i)] == ''):
                    itemqty = req['itemqty'+str(i)]
                    itemprice = req['itemprice'+str(i)]
                    itemno = req['itemno'+str(i)]
                    if isnum(itemqty) and isfloat(itemprice) and isnum(itemno):
                        boqs.append({'itemno':req['itemno'+str(i)],'itemname':req['itemname'+str(i)],'itemdesc': req['itemdesc'+str(i)], 'itemqty': itemqty, 'itemprice': itemprice})
                    else:
                        messages.warning(request, 'BoQ item quantity and Price must be a decimal number')
                        return redirect('/update_boq/0')
                
            boqdata.objects.filter(project = boq_project, boqtype = '2').delete()
            for boq in boqs:
                apr_boq = boqdata()
                apr_boq.project = boq_project
                apr_boq.boqtype = '2'
                apr_boq.itemno = boq['itemno']
                apr_boq.itemname = boq['itemname']
                apr_boq.itemdesc = boq['itemdesc']
                apr_boq.itemqty = boq['itemqty']
                apr_boq.unitcost = boq['itemprice']
                apr_boq.save()
                
            boq_project.workflow = str(boq_project.workflow) + ']*[' + 'BoQ updated on ' + str(datetime.now().date())
            boq_project.save(update_fields=['workflow'])
            notification(boq_project.userid.id, 'BoQ submitted for project ID: '+str(boq_project.newid)+' ' + boq_project.name + ' has been updated by PSDF Sectt.' )
            messages.success(request, 'BoQ successfully updated and intimated to user.')
            return redirect('/update_boq/0')
        if projid == '0':
            context['project_list'] = projects.objects.filter(status = '1')
                
            return render(request, 'psdf_main/_admin_boq.html', context)
        else:
            thisproject = projects.objects.get(id = projid)
            if thisproject:
                
                if boqdata.objects.filter(project = thisproject, boqtype = '2'):
                    context['already_updated'] = '1'
                    context['sub_boq'] = boqdata.objects.filter(project = thisproject, boqtype = '2')
                else:
                    context['already_updated'] = '0'
                    context['sub_boq'] = boqdata.objects.filter(project = thisproject, boqtype = '1')
                
                context['proj'] = thisproject
                context['range'] = range(len(context['sub_boq'])+1,1000)
                return render(request, 'psdf_main/_admin_update_boq.html', context)
            return render(request, 'psdf_main/_admin_boq.html', context)
    else:
        return oops(request)

def add_remark(request,thispage):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            remark = sanitize(req.get('remark'))
            projid = req.get('projid')
            try:
                proj = projects.objects.get(id = projid)
            except:
                return oops(request)
            proj.remark = remark
            proj.remark_date = datetime.now().date()
            proj.save(update_fields = ['remark','remark_date'])
            messages.success(request,'Remark Updated.')
            return redirect('/'+str(thispage))
    else:
        return oops(request)