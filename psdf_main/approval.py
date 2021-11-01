from .helpers import *

def admin_in_doc_sign(request):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            try:
                projid = req['projid']
                adminpass = req['adminpass']
            except :
                messages.error(request, "Unable to fetch admin password or project ID")
                return redirect('/admin_in_doc_sign')
            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/admin_in_doc_sign')
            try:
                thisproj = projects.objects.get(id = projid)
            except :
                messages.error(request, "Invalid Project")
                return redirect('/admin_in_doc_sign')
            thisproj.approved = True
            thisproj.status = '5'
            
            appr_boq = boqdata.objects.filter(project = thisproj, boqtype = '3')
            appr_boq_tot = boq_grandtotal(appr_boq)

            ###################
            ##APPROVED AMOUNT##
            ###################

            thisproj.amt_approved = float(float(appr_boq_tot)*float(thisproj.quantumOfFunding))

            ###################
            ##APPROVED AMOUNT##
            ###################
            thisproj.doc_sign_date = datetime.now().date()
            thisproj.workflow = str(thisproj.workflow) + ']*[' + 'Project approved by admin on '+ str(datetime.now().date())
            thisproj.save(update_fields=['approved', 'status', 'amt_approved', 'doc_sign_date','workflow'])
            messages.success(request, 'Project Approved and document accepted.')
        context['projs'] = projects.objects.filter(status = '5')
        return render(request, 'psdf_main/_admin_doc_sign.html', context)
    else:
        return oops(request)

def user_in_doc_sign(request):
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        if request.method == 'POST':
            req = request.POST
            try:
                projid = req['projid']
            except:
                messages.error(request, "Invalid Project")
                return redirect('/user_in_doc_sign')
            if projectofuser(request, request.session['user'], projid):
                if 'docsign' in request.FILES:
                    docsign = request.FILES['docsign']
                    try:
                        extension = str(docsign.name.split(".")[-1])
                    except:
                        extension = ''
                    thisproj = projects.objects.get(id = projid)
                    doc_path = thisproj.projectpath + "/Signed_Document/"
                    srmdir(doc_path)
                    smkdir(doc_path)
                    
                    # try:
                    #     alreadyfile = glob.glob(os.path.join(doc_path,str(thisproj.newid)+'_document')+'*')[0]
                    #     if os.path.exists(alreadyfile):
                    #         sremove(alreadyfile)
                    #     else:
                    #         print("NOT EXISTS")
                    # except:
                    #     pass
                    doc_path_file = os.path.join(doc_path,str(thisproj.newid)+'_document.'+extension)
                    if handle_uploaded_file(doc_path_file, docsign):
                        messages.success(request, 'Document Uploaded ')
                    else:
                        return oops(request)
                    thisproj.doc_path = doc_path_file
                    
                    thisproj.approved = False
                    thisproj.workflow = str(thisproj.workflow) + ']*[' + 'Project document submitted by entity on '+ str(datetime.now().date())
                    thisproj.status = '5'
                    thisproj.save(update_fields=['doc_path','approved', 'status', 'workflow'])
                
            else:
                return oops(request)
        context['projs'] = projects.objects.filter((Q(status = '4')| Q(status = '5')),userid = getuser(request, request.session['user']))
        return render(request, 'psdf_main/_user_in_doc_sign.html', context)
    else:
        return oops(request)

    
def download_doc_sign(request, projid):
    if adminonline(request) or (useronline(request) and projectofuser(request, request.session['user'], projid)):
        thisproj = projects.objects.get(id = projid)
        if os.path.exists(thisproj.doc_path) and not (thisproj.doc_path == None or thisproj.doc_path == ''):
            try:
                return handle_download_file(thisproj.doc_path, request)
            except :
                return oops(request)
        else:
            return oops(request)
    else:
        return oops(request)