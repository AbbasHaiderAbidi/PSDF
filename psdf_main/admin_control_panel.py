from psdf_main.admin_appraisal import delete_appr_doc
from .helpers import *
# Create your views here.


def admin_dashboard(request):
    
    if adminonline(request):
        
        context = full_admin_context(request)
        allproj = projects.objects.filter(deny = False)
        context['totalprojs'] = allproj.count()
        totalcost = 0
        totalgrant = 0
        totalreleased = 0
        for proj in allproj:
            if proj.amt_updated != None:
                totalcost = totalcost + int(proj.amt_updated)
            if proj.amt_approved != None:
                totalgrant = totalgrant + int(proj.amt_approved)
            if proj.amt_approved != None:
                totalreleased = totalreleased + int(proj.amt_released)
        context['totalcost'] = totalcost
        context['totalgrant'] = totalgrant
        context['totalreleased'] = totalreleased
        
        dprprojs = temp_projects.objects.filter(deny = False)
        context['dprnoproj'] = dprprojs.count()
        dprcost = 0
        for proj in dprprojs:
            if proj.amountasked != None:
                dprcost = dprcost + int(proj.amountasked)
        context['dprsubcost'] = dprcost
        
        
        tesgprojs = projects.objects.filter(deny = False, status = '1')
        context['tesgnoproj'] = tesgprojs.count()
        tesgsubcost = 0
        tesgupcost = 0
        for proj in tesgprojs:
            if proj.amt_asked != None:
                tesgsubcost = tesgsubcost + int(proj.amt_asked)
            if proj.amt_updated != None:
                tesgupcost = tesgupcost + int(proj.amt_updated)
        context['tesgsubcost'] = tesgsubcost
        context['tesgupcost'] = tesgupcost
        
        aprprojs = projects.objects.filter(deny = False, status = '2')
        context['aprnoproj'] = aprprojs.count()
        aprsubcost = 0
        aprupcost = 0
        for proj in aprprojs:
            if proj.amt_asked != None:
                aprsubcost = aprsubcost + int(proj.amt_asked)
            if proj.amt_updated != None:
                aprupcost = aprupcost + int(proj.amt_updated)
        context['aprsubcost'] = aprsubcost
        context['aprupcost'] = aprupcost
        
        moniprojs = projects.objects.filter(deny = False, status = '3')
        context['moninoproj'] = moniprojs.count()
        monisubcost = 0
        moniupcost = 0
        for proj in moniprojs:
            if proj.amt_asked != None:
                monisubcost = monisubcost + int(proj.amt_asked)
            if proj.amt_updated != None:
                moniupcost = moniupcost + int(proj.amt_updated)
        context['monisubcost'] = monisubcost
        context['moniupcost'] = moniupcost
        
        sacprojs = projects.objects.filter(deny = False, status = '4')
        context['sacnoproj'] = sacprojs.count()
        sacsubcost = 0
        sacupcost = 0
        for proj in sacprojs:
            if proj.amt_asked != None:
                sacsubcost = sacsubcost + int(proj.amt_asked)
            if proj.amt_updated != None:
                sacupcost = sacupcost + int(proj.amt_updated)
        context['sacsubcost'] = sacsubcost
        context['sacupcost'] = sacupcost
        
        docprojs = projects.objects.filter(deny = False, status = '5')
        context['docnoproj'] = docprojs.count()
        docsubcost = 0
        docupcost = 0
        for proj in docprojs:
            if proj.amt_asked != None:
                docsubcost = docsubcost + int(proj.amt_asked)
            if proj.amt_updated != None:
                docupcost = docupcost + int(proj.amt_updated)
        context['docsubcost'] = docsubcost
        context['docupcost'] = docupcost
        
        payprojs = projects.objects.filter(deny = False, status = '6')
        context['paynoproj'] = payprojs.count()
        
        payupcost = 0
        paidcost = 0
        for proj in payprojs:
            if proj.amt_updated != None:
                payupcost = payupcost + int(proj.amt_updated)
            if proj.amt_released != None:
                paidcost = paidcost + int(proj.amt_released) 
                
        context['totalremain'] = payupcost - paidcost
        
        return render(request, 'psdf_main/_admin_dashboard.html', context)
    else:
        return oops(request)




def admin_pending_projects(request):
    if adminonline(request):
        context = full_admin_context(request)

        context['projectobj']  = temp_projects.objects.all().exclude(deny = True)
        for proj in context['projectobj']:
            proj.submitted_boq = get_boq_details(proj.submitted_boq)
            proj.submitted_boq_Gtotal = get_Gtotal_list(proj.submitted_boq)
            proj.GrandTotal = get_grand_total(proj.submitted_boq)
        return render(request, 'psdf_main/_admin_pending_projects.html', context)



def control_panel(request):
    if adminonline(request):
        # user = userDetails(request.session['user'])
        nopendingusers = pen_users_num(request)
        if not nopendingusers:
            nopendingusers = 0
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_control_panel.html', context)
    else:
        return oops(request)
    
    
def uploadformat(request):
    filelist = {'support':'DPR_Supporting_documents', 'format':'DPR_Forms','sample1':'sample1','sample2':'sample2','sample3':'sample3','boqformat':'BOQ_Format'}
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if not 'adminpassF' in req.keys():
                messages.error(request, 'Enter Administrator password.')
                return redirect('/admin_control_panel')
            adminpassF = req['adminpassF']
            if not check_password(adminpassF,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/admin_control_panel')
            if request.FILES:
                files = request.FILES
                formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/')
                smkdir(formatpath)
                if 'support' in files.keys():
                    naam = 'support'
                    support = files['support']
                    try:
                        ext = '.' + support.name.split('.')[-1]
                    except:
                        ext = ''
                    name = filelist[naam] + ext
                    try:
                        alreadyfile = glob.glob(os.path.join(formatpath,filelist[naam])+'*')[0]
                    
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    if handle_uploaded_file(os.path.join(formatpath,name),files[naam]):
                        messages.success(request, 'Supporting Documents updated.')
                    else:
                        return oops(request)
                    
                if 'format' in files.keys():
                    naam = 'format'
                    support = files[naam]
                    try:
                        ext = '.' + support.name.split('.')[-1]
                    except:
                        ext = ''
                    name = filelist[naam] + ext
                    try:
                        alreadyfile = glob.glob(os.path.join(formatpath,filelist[naam])+'*')[0]
                    
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    if handle_uploaded_file(os.path.join(formatpath,name),files[naam]):
                    # formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/')
                    
                        messages.success(request, 'Format updated.')
                    else:
                        return oops(request)
                if 'sample1' in files.keys():
                    naam = 'sample1'
                    support = files[naam]
                    try:
                        ext = '.' + support.name.split('.')[-1]
                    except:
                        ext = ''
                    name = filelist[naam] + ext
                    try:
                        alreadyfile = glob.glob(os.path.join(formatpath,filelist[naam])+'*')[0]
                    
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    if handle_uploaded_file(os.path.join(formatpath,name),files[naam]):
                    # formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/')
                        messages.success(request, 'Sample 1 updated.')
                    else:
                        return oops(request)
                if 'sample2' in files.keys():
                    naam = 'sample2'
                    support = files[naam]
                    try:
                        ext = '.' + support.name.split('.')[-1]
                    except:
                        ext = ''
                    name = filelist[naam] + ext
                    
                    try:
                        alreadyfile = glob.glob(os.path.join(formatpath,filelist[naam])+'*')[0]
                    
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                            
                    except:
                        pass
                    if handle_uploaded_file(os.path.join(formatpath,name),files[naam]):
                    # formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/')                    
                        messages.success(request, 'Sample 2 updated.')
                    else:
                        return oops(request)
                if 'sample3' in files.keys():
                    naam = 'sample3'
                    support = files[naam]
                    try:
                        ext = '.' + support.name.split('.')[-1]
                    except:
                        ext = ''
                    name = filelist[naam] + ext
                    try:
                        alreadyfile = glob.glob(os.path.join(formatpath,filelist[naam])+'*')[0]
                    
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    if handle_uploaded_file(os.path.join(formatpath,name),files[naam]):
                    # formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/')
                        messages.success(request, 'Sample 3 updated.')
                    else:
                        return oops(request)
                if 'boqformat' in files.keys():
                    naam = 'boqformat'
                    support = files[naam]
                    try:
                        ext = '.' + support.name.split('.')[-1]
                    except:
                        ext = ''
                    name = filelist[naam] + ext
                    try:
                        alreadyfile = glob.glob(os.path.join(formatpath,filelist[naam])+'*')[0]
                    
                        if os.path.exists(alreadyfile):
                            sremove(alreadyfile)
                    except:
                        pass
                    if handle_uploaded_file(os.path.join(formatpath,name),files[naam]):
                    # formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/')
                    
                        messages.success(request, 'BOQ Format updated.')
                    else:
                        return oops(request)
                    
                return redirect('/admin_control_panel')
            else:
                return redirect('/admin_control_panel')
    else:
        return oops(request)

def TESG_upload(request):
    # if adminonline(request):
    #     if request.method == 'POST':
    #         req = request.POST
    #         if not 'adminpassT' in req.keys():
    #             messages.error(request, 'Enter Administrator password.')
    #             return redirect('/admin_control_panel')
    #         adminpassF = req['adminpassT']
    #         if not check_password(adminpassF,userDetails(request.session['user'])['password']):
    #             messages.error(request, 'Invalid Administrator password.')
    #             return redirect('/admin_control_panel')
            
    #         if request.FILES:
    #             tesgnum = req['tesgnum']
    #             tesgdate = req['tesgdate']
    #             projids = req['projids']
    #             tesgpath = ''
    #             allTESG = TESG_admin.objects.values_list('TESG_no')
    #             projids = projids.replace(" ","")
    #             allproj = projects.objects.all()
    #             files = request.FILES
    #             allids = []
    #             if projids == '':
    #                 messages.error(request,"Please enter comma seperated Project IDs")
    #                 return redirect('/admin_control_panel')

    #             for proj in allproj:
    #                 allids.append(str(proj.newid))
                
    #             givenids = projids.split(",")
                
    #             for givenid in givenids:
    #                 if not givenid in allids:
    #                     messages.error(request,"The Project for ID: "+givenid+" does not exists")
    #                     return redirect('/admin_control_panel')

    #             for TESGnum in allTESG:
    #                 if int(tesgnum) in TESGnum:
    #                     messages.error(request, 'ERROR! TESG number '+ tesgnum +' entry already exists')
    #                     return redirect('/admin_control_panel')

    #             if 'momupload' in files.keys():
    #                 mompload = files['momupload']
    #                 try:
    #                     ext = '.' + mompload.name.split('.')[1]
    #                 except:
    #                     ext = ''
    #                 naam = 'TESG_'+tesgnum + str(ext)
    #                 tesgpath =os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/TESG/')
    #                 if smkdir(tesgpath):
    #                     tesgpath = os.path.join(tesgpath, naam)
    #                     handle_uploaded_file(tesgpath,files['momupload'])
    #                 else:
    #                     return oops(request)
    #             else:
    #                 messages.error(request, "No MoM file uploaded")
    #                 return redirect('/admin_control_panel')



    #             TESG_admin1 = TESG_admin()
    #             TESG_admin1.TESG_no = tesgnum
    #             TESG_admin1.filepath = tesgpath
    #             TESG_admin1.TESG_date = tesgdate
    #             TESG_admin1.projects = projids
    #             TESG_admin1.save()
    #             tesgprojs = projids.split(',')
    #             print(tesgprojs)
    #             allprojs = projects.objects.all()
    #             for proj in allprojs:
    #                 if str(proj.newid) in tesgprojs:
    #                     projectid = projects.objects.get(id = proj.id)
    #                     if projectid.tesg_list:
    #                         projectid.tesg_list = str(projectid.tesg_list) +',' + str(tesgnum)
    #                     else:
    #                         projectid.tesg_list = str(tesgnum)
    #                     projectid.save(update_fields=['tesg_list'])
    #             messages.success(request, 'New TESG number: '+tesgnum+' added.')
    #             return redirect('/admin_control_panel')
    #     else:
    #         return oops(request)
    # else:
    #     return oops(request)
    

    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if not 'adminpassT' in req.keys():
                messages.error(request, 'Enter Administrator password.')
                return redirect('/admin_control_panel')
            adminpassF = req['adminpassT']
            if not check_password(adminpassF,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/admin_control_panel')
            
            if request.FILES:
                tesgnum = req['tesgnum']
                tesgdate = req['tesgdate']
                projids = str(req['projids'])
                tesgpath = ''
                files = request.FILES
                allTESG = TESG_admin.objects.values_list('TESG_no')
                for TESGnum in allTESG:
                    if int(tesgnum) in TESGnum:
                        messages.error(request, 'TESG upload error: TESG number '+ tesgnum +' entry already exists')
                        return redirect('/admin_control_panel')
                projids = projids.replace(" ","")
                projids = projids.split(',')
                allprojects = projects.objects.all()
                newids = []
                for proj in allprojects:
                    newids.append(str(proj.newid))
                for projid in projids:
                    if not(projid in newids):
                        messages.error(request, 'TESG upload error: Project ID '+ projid +' does not exists.')
                        return redirect('/admin_control_panel')
                if 'momupload' in files.keys():
                    mompload = files['momupload']
                    try:
                        ext = '.' + mompload.name.split('.')[-1]
                    except:
                        ext = ''
                    naam = 'TESG_'+tesgnum + str(ext)
                    tesgpath =os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/TESG/')
                    if smkdir(tesgpath):
                        tesgpath = os.path.join(tesgpath, naam)
                        try:
                            alreadyfile = glob.glob(os.path.join(tesgpath,'TESG_'+str(tesgnum))+'*')[0]
                        
                            if os.path.exists(alreadyfile):
                                sremove(alreadyfile)
                            
                            
                        except:
                            pass
                        if handle_uploaded_file(tesgpath,files['momupload']):
                            messages.success(request, 'TESG upload successful, report for TESG '+tesgnum+' uploaded.')
                        else:
                            return oops(request)
                    else:
                        return oops(request)
                else:
                    messages.error(request, 'TESG upload error: Please upload report file.')
                    return redirect('/admin_control_panel')
                TESG_admin1 = TESG_admin()
                TESG_admin1.TESG_no = tesgnum
                TESG_admin1.filepath = tesgpath
                TESG_admin1.TESG_date = tesgdate
                TESG_admin1.projects = projids
                TESG_admin1.save()
                tesgprojs = projids
                allprojs = projects.objects.all()
                for proj in allprojs:
                    if str(proj.newid) in tesgprojs:
                        projectid = projects.objects.get(id = proj.id)
                        if projectid.tesg_list:
                            projectid.tesg_list = str(projectid.tesg_list) +',' + str(tesgnum)
                        else:
                            projectid.tesg_list = str(tesgnum)
                        projectid.save(update_fields=['tesg_list'])
                messages.success(request, 'New TESG number: '+tesgnum+' added.')
                return redirect('/admin_control_panel')
            else:
                messages.error(request, 'ERROR! Please upload MoM file.')
                return redirect('/admin_control_panel')
        else:
            return oops(request)
    else:
        return oops(request)


    
def APPR_upload(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if not 'adminpassA' in req.keys():
                messages.error(request, 'Enter Administrator password.')
                return redirect('/admin_control_panel')
            adminpassF = req['adminpassA']
            if not check_password(adminpassF,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/admin_control_panel')
            apprdate = req.get('apprdate')
            projid1 = req.get('projid')
            apprid = req.get('apprid')
            try:
                oro = projects.objects.filter(newid = projid1)[:1].get()
                projid = str(oro.id)
            except:
                messages.error(request, 'No project with project ID ' +str(projid1)+ ' exists.')
                return  redirect('/admin_control_panel')
            
            
            apprpath = ''
            if request.FILES:
                files = request.FILES
                if 'momupload' in files.keys():
                    mompload = files['momupload']
                    try:
                        ext = '.' + mompload.name.split('.')[-1]
                    except:
                        ext = ''
                    naam = 'Appraisal_'+ projid + '_' + apprdate + str(ext)
                    apprpath = os.path.join(oro.projectpath, 'Appraisal/')
                    if smkdir(apprpath):
                        apprpath = os.path.join(apprpath, naam)
                        if handle_uploaded_file(apprpath,files['momupload']):
                            messages.success(request, 'Outcome file uploaded')
                        else:
                            return oops(request)
                    else:
                        return oops(request)
                allthere = Appraisal_admin.objects.filter(project = oro)
                for there in allthere:
                    sremove(there.apprpath)
                allthere.delete()
                
                appr = Appraisal_admin()
                appr.aprid = apprid
                appr.project = oro
                appr.apprpath = apprpath
                appr.apprdate = apprdate
                appr.userid = oro.userid
                appr.save()
                oro.aproutdate = datetime.now().date()
                oro.save(update_fields = ['aproutdate'])
                messages.success(request, 'Appraisal committee entry added for project '+ appr.project.name)
                return redirect('/admin_control_panel')
            else:
                messages.success(request, 'Please select the outcome file of the project')
                return redirect('/admin_control_panel')
        else:
            return oops(request)
    else:
        return oops(request)
    
    
    
def MONI_upload(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if not 'adminpassM' in req.keys():
                messages.error(request, 'Enter Administrator password.')
                return  redirect('/admin_control_panel')
            adminpassF = req['adminpassM']
            if not check_password(adminpassF,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return  redirect('/admin_control_panel')
            apprdate = req.get('monidate')
            projid = req.get('projid')
            moniid = req.get('moniid')
            apprpath = ''
            projectpath = ''
            try:
                oro = projects.objects.filter(newid = projid)[:1].get()
                projid = str(oro.id)
                print(str(projid)+" ye hai id")
                projectpath = oro.projectpath
                # print(project)
            except:
                messages.error(request, 'No project with project ID ' +projid+ ' exists.')
                return  redirect('/admin_control_panel')
            if request.FILES:
                files = request.FILES
                if 'momupload' in files.keys():
                    mompload = files['momupload']
                    try:
                        ext = '.' + mompload.name.split('.')[-1]
                    except:
                        ext = ''
                    naam = 'Monitoring_'+ projid + '_' + apprdate + str(ext)
                    apprpath = os.path.join(projectpath , 'Monitoring/')
                    print(apprpath)
                    if smkdir(apprpath):
                        apprpath = os.path.join(apprpath, naam)
                        if handle_uploaded_file(apprpath,files['momupload']):
                            messages.success(request, 'Outcomes uploaded.')
                        else:
                            return oops(request)
                    else:
                        return oops(request)
                else:
                    messages.error(request, 'Invalid File selected')
                    return redirect('/admin_control_panel')
                oror = projects.objects.get(id = projid)
                allthere = Monitoring_admin.objects.filter(project = oror)
                for there in allthere:
                    sremove(there.monipath)    
                allthere.delete()
                
                moni = Monitoring_admin()
                moni.project = oror
                moni.moniid = moniid
                moni.userid = oror.userid
                moni.monipath = apprpath
                moni.monidate = apprdate
                moni.save()
                oror.monioutdate = datetime.now().date()
                oror.save(update_fields = ['monioutdate'])
                messages.success(request, 'Monitoring committee entry added for project '+ moni.project.name)
                return redirect('/admin_control_panel')
            else:
                messages.success(request, 'Please select the outcome file of the project')
                return redirect('/admin_control_panel')
        else:
            return oops(request)    
    else:
        return oops(request)


