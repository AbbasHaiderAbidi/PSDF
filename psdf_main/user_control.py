from .helpers import *



def newdpr(request):
    # form = NewDPR_form()
    if useronline(request) and not adminonline(request):
        user = userDetails(request.session['user'])
        context = full_user_context(request)
        if request.method == 'POST':
            req = request.POST
            if req['subtype'] == 'submit':
                if request.FILES:
                    amount = sanitize(req['amount'])
                    schedle = sanitize(req['schedule'])
                    proname = sanitize(req['proname'])
                    if not ('boq' in request.FILES):
                        messages.warning(request, 'No BoQ file selected')
                        return render(request, 'psdf_main/_user_new_dpr.html', context)
                    if not ('dpr' in request.FILES and 'a1' in request.FILES):
                        messages.warning(request, 'Please select files to upload')
                        return render(request, 'psdf_main/_user_new_dpr.html', context)

                    if(not isfloat(amount)):
                        messages.warning(request, 'Amount should be a decimal number')
                        return render(request, 'psdf_main/_user_new_dpr.html', context)

                    if(not isnum(schedle)):
                        messages.warning(request, 'Schedule should be a number')
                        return render(request, 'psdf_main/_user_new_dpr.html', context)

                    if len(proname) < 3:
                        messages.warning(request, 'Enter a valid project name')
                        return render(request, 'psdf_main/_user_new_dpr.html', context)
                    
                    proname = sanitize(proname)
                    

                    boq_workbook = xl.load_workbook(request.FILES['boq'])
                    boq = boq_workbook.active
                    m_rows = boq.max_row
                    total_cost = 0
                    for j in range(1,6):
                        if emp_check(boq.cell(row = m_rows, column = j)):
                            messages.error(request, "Extra rows in BOQ file.")
                            return render(request, 'psdf_main/_user_new_dpr.html', context)
                    for i in range(2, m_rows+1):
                        temp_temp = boq.cell(row = i, column = 2).value
                        if temp_temp == None or temp_temp == '':
                            pass
                        else:
                            temp_itemname = sanitize_name(temp_temp)
                            if emp_check(temp_itemname):
                                pass
                            else:
                                if not isnum(boq.cell(row = i, column = 1).value):
                                    messages.error(request, "Error in Row no. "+str(i)+" ITEM NUMBER column of BOQ")
                                    return render(request, 'psdf_main/_user_new_dpr.html', context)
                                if not isnum(boq.cell(row = i, column = 4).value):
                                    messages.error(request, "Error in Row no. "+str(i)+" QUANTITY column of BOQ")
                                    return render(request, 'psdf_main/_user_new_dpr.html', context)
                                if not isfloat(boq.cell(row = i, column = 5).value):
                                    messages.error(request, "Error in Row no. "+str(i)+" UNIT PRICE column of BOQ")
                                    return render(request, 'psdf_main/_user_new_dpr.html', context)
                                total_cost = total_cost + float(float(boq.cell(row = i, column = 4).value)*int(boq.cell(row = i, column = 5).value))
                    if not int(total_cost) == int(amount):
                        messages.error(request, "BOQ total amount should be equal to entered amount")
                        return render(request, 'psdf_main/_user_new_dpr.html', context)
                    boqlist = []
                    # {'itemname':sanitize(req['itemname'+str(i)]),'itemno':sanitize(req['itemno'+str(i)]),'itemdesc': sanitize(req['itemdesc'+str(i)]), 'itemqty': itemqty, 'itemprice': itemprice, 'itemcost' : str(float(float(itemprice)*float(itemqty)))}
                    for i in range(2, m_rows+1):
                        temp_temp = boq.cell(row = i, column = 2).value
                        if temp_temp == None or temp_temp == '':
                            pass
                        else:
                            temp_itemname = sanitize_name(temp_temp)
                            if emp_check(temp_itemname):
                                pass
                            else:
                                itemname = sanitize_name(boq.cell(row = i, column = 2).value)
                                itemno = boq.cell(row = i, column = 1).value
                                itemdesc = sanitize(boq.cell(row = i, column = 3).value)
                                itemqty = float(boq.cell(row = i, column = 4).value)
                                itemprice = int(boq.cell(row = i, column = 5).value)
                                itemcost = float(itemqty * itemprice)
                                boqlist.append({'itemname':itemname, 'itemno':itemno, 'itemdesc': itemdesc, 'itemqty':itemqty, 'itemprice': itemprice, 'itemcost': itemcost})
                    
                    ## CHECK FOR AMOUNT EQUALITY
                    dpr = request.FILES['dpr']
                    a1 = request.FILES['a1']
                    if 'otherdoc' in request.FILES:
                        otherdoc = request.FILES['otherdoc']
                    newdprpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'),os.path.join(request.session['user'],'temp/'+proname+'_'+amount+'_'+schedle))
                    if smkdir(newdprpath):
                        try:
                            
                            
                            if 'otherdoc' in request.FILES:
                                try:
                                    otherdoc_filename = secure_filename("otherdocs."+otherdoc.name.split('.')[-1])
                                except:
                                    otherdoc_filename = secure_filename("otherdocs")
                            try:
                                dpr_filename = secure_filename("DPR."+dpr.name.split('.')[-1])
                            except:
                                dpr_filename = secure_filename("DPR")
                            try:
                                a1_filename = secure_filename("forms."+a1.name.split('.')[-1])
                            except:
                                a1_filename = secure_filename("forms")
                                
                            if 'otherdoc' in request.FILES:
                                otherdoc_filename = secure_filename("otherdocs")
                                if handle_uploaded_file(os.path.join(newdprpath,otherdoc_filename),otherdoc):
                                    pass
                                else:
                                    return oops(request)
                            if handle_uploaded_file(os.path.join(newdprpath,dpr_filename),dpr):
                                pass
                            else:
                                return oops(request)
                            if handle_uploaded_file(os.path.join(newdprpath,a1_filename),a1):
                                pass
                            else:
                                return oops(request)
                        except :
                            return oops(request)
                        
                        temp_project = temp_projects()
                        temp_project.proname = proname
                        temp_project.amountasked = amount
                        temp_project.projectpath = newdprpath
                        temp_project.schedule = schedle
                        temp_project.submitted_boq = boqlist
                        temp_project.userid = users.objects.get(id = userDetails(request.session['user'])['id'])
                        temp_project.save()
                        temp_dpr = users.objects.get(id = user['id'])
                        temp_dpr.tpd = ''
                        temp_dpr.save(update_fields=['tpd'])
                        admin_user = users.objects.get(id = getadmin_id())
                        admin_user.notification = str(admin_user.notification) + ']*[' + 'New project : '+ proname +' has been submitted by user: ' + str(temp_project.userid.username)
                        admin_user.save(update_fields=['notification'])
                        messages.success(request, 'DPR for Project : '+ proname +' has been submitted for examination.')
                        return render(request, 'psdf_main/_user_new_dpr.html', context)
                    else:
                        messages.error(request, "Error in creating record")
                        return render(request, 'psdf_main/_user_new_dpr.html', context)

                else:

                    messages.warning(request, 'Please upload supporting documents')
                    return render(request, 'psdf_main/_user_new_dpr.html', context)
            elif req['subtype'] == 'save':
                amount = req['amount']
                schedle = req['schedule']
                proname = req['proname']
                saveddpr = {}
                saveddpr['amountasked'] = amount
                saveddpr['schedule'] = schedle
                saveddpr['proname'] = proname
                temp_dpr = users.objects.get(id = user['id'])
                temp_dpr.tpd = saveddpr
                temp_dpr.save(update_fields=['tpd'])
            elif req['subtype'] == 'clear':
                temp_dpr = users.objects.get(id = user['id'])
                temp_dpr.tpd = ''
                temp_dpr.save(update_fields=['tpd'])
            context = full_user_context(request)
        return render(request, 'psdf_main/_user_new_dpr.html', context)
    return oops(request)



def downloadformat(request,thisdoc):
    filelist = {'support':'DPR_Supporting_documents', 'format':'DPR_Forms','sample1':'sample1','sample2':'sample2','sample3':'sample3', 'boqformat':'BOQ_Format'}
    try:
        if useronline(request) and not adminonline(request):
            formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), os.path.join('Admin/Formats/',filelist[thisdoc]))
            formatpath = glob.glob(formatpath+'*')[0]
            # if os.path.exists(formatpath):
            return handle_download_file(formatpath, request)
            # else:
            #     messages.error(request, "File not available")
            #     return redirect('/newdpr')
        else:
            return oops(request)
    except:
        messages.error(request, 'Function unavailable.')
        return redirect('/newdpr')


def notificationread(request, userid):
    user = users.objects.get(id = userid)
    if str(user.username) == request.session['user']:
        if useronline(request):
            user.notification = ''
            user.save(update_fields=['notification'])
            
            messages.success(request, 'Notifications now marked as read.')
            return redirect('/')
            context  = full_user_context(request)
            return render(request, 'psdf_main/dashboard.html', context)
    else:
        return oops(request)

def user_boq_view(request, projid):
    if useronline(request):
        splits = projid.split('_')
        projid = splits[0]
        backpage = splits[1]
        if backpage == 'underexamination':
            proj = temp_projects.objects.get(id = projid)
        else:
            proj = projects.objects.get(id = projid)
        backpages = {'underexamination' : 'under_examination', 'usermonitoringprojects':'user_monitoring_projects','userappraisalprojects':'user_appraisal_projects','usertesgprojects':'user_tesg'}
        try:
            a = backpages[backpage]
        except:
            return oops(request)
        if proj.userid.username == request.session['user']:
            
            context = full_user_context(request)
            if backpage == 'underexamination':
                # project = temp_projectDetails(proj.id)
                context['proj'] = temp_projects.objects.filter(id = proj.id)
                context['proj'].submitted_boq = get_boq_details(proj.submitted_boq)
                
                context['backpage'] = backpages[backpage]
                return render(request, 'psdf_main/_user_view_boq.html', context)
            else:
                context['proj'] = proj
                context['sub_boq'] = boqdata.objects.filter(project = context['proj'], boqtype = '1')
                context['sub_boq_total'] = boq_grandtotal(context['sub_boq'])
                context['approved_boq'] = boqdata.objects.filter(project = context['proj'], boqtype = '2')
                context['approved_boq_total'] = boq_grandtotal(context['approved_boq'])
                context['backpage'] = backpages[backpage]
                return render(request, 'psdf_main/_user_view_project_boq.html', context)
    else:
        return oops(request)
    
def user_back(request, backpage):
    if useronline(request):
        return redirect('/'+backpage)
    else:
        return oops(request)
    
def user_view_all_projs(request):
    if useronline(request):
        context = full_user_context(request)
        userid = context['user']['id']
        userobj = users.objects.get(id = userid)
        context['all_projs'] = projects.objects.filter(deny = False, userid = userobj)
        context['all_rprojs'] = projects.objects.filter(deny = True, userid = userobj)
        context['all_rpprojs'] = temp_projects.objects.filter(deny = True, userid = userobj)
        context['all_temps'] = temp_projects.objects.filter(userid = userobj)
        context['npending'] = temp_projects.objects.filter(deny = False, userid = userobj).count()
        context['ntesg'] = projects.objects.filter(status = '1', deny = False, userid = userobj).count()
        context['nappr'] = projects.objects.filter(status = '2', deny = False, userid = userobj).count()
        context['nmoni'] = projects.objects.filter(status = '3', deny = False, userid = userobj).count()
        context['nfinal'] = projects.objects.filter(status = '4', deny = False, userid = userobj).count()
        context['nreject'] = projects.objects.filter(deny = True, userid = userobj).count() + temp_projects.objects.filter(deny = True, userid = userobj).count()
        
        return render(request, 'psdf_main/_user_view_all_projects.html', context)
    else:
        return oops(request)

def user_project_details(request, projid):
    context = full_user_context(request)
    context['proj'] = projects.objects.get(id = projid)
    if useronline(request) and context['proj'].userid.username == request.session['user']:
        context['proj'].workflow = context['proj'].workflow.split(']*[')[1:]
        context['tesgs'] = TESG_master.objects.filter(project = context['proj'])
        return render(request, 'psdf_main/_user_view_project.html', context)
    else:
        return oops(request)