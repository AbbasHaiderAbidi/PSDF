from openpyxl.cell import cell
from .helper_imports import *


def useronline(request):
    if (request.session.has_key('user')):
        return True
    else:
        return False

def adminonline(request):
    if (request.session.has_key('user') and request.session.has_key('admin')):
        return True
    else:
        return False

def auditoronline(request):
    if (request.session.has_key('auditor')):
        return True
    else:
        return False

def proj_of_user(request, projid):
    if adminonline(request):
        return True
    if useronline(request):
        try:
            thisproj = projects.objects.get(id = projid)
        except:
            return oops(request)
        if (thisproj.userid.username == request.session['user']):
            return True
        else:
            return False
    else:
        return False


def getuser(request):
    try:
        return users.objects.filter(username = request.session['user'])[:1].get()
    except:
        return oops(request)

def projectofuser(request,projid):
    if projects.objects.get(id = projid).userid == getuser(request):
        return True
    else:
        return False

    

def oops(request):
    return render(request, 'psdf_main/404.html')

def getadmin_id():
    userobj = users.objects.filter(admin = True)[:1]
    for user in userobj:
        return user.id

def userDetails(username):
    user = {}
    userobj = users.objects.filter(username = username)[:1]
    for user1 in userobj:
        user['id'] = user1.id
        user['username'] = user1.username
        user['password'] = user1.password
        user['nodal'] = user1.nodal
        user['contact'] = user1.contact
        user['address'] = user1.address
        user['email'] = user1.email
        user['utilname'] = user1.utilname
        user['region'] = user1.region
        user['lastlogin'] = user1.lastlogin
        user['reqdate'] = user1.reqdate
        user['aprdate'] = user1.aprdate
        user['admin'] = user1.admin
        user['auditor'] = user1.auditor
        user['active'] = user1.active
        if user1.notification:
            user['notifications'] = user1.notification.split(']*[')[1:]
        else:
            user['notifications'] = ""
        if user1.tpd:
            user['temp_boq'] = yaml.load(user1.tpd, yaml.FullLoader)
        else:
            user['temp_boq'] = ''
        user['activate'] = user1.activate
    return user

def projectDetails(projid):
    proj = {}
    proj1 = projects.objects.get(id = projid)
    sub_boq = boqdata.objects.filter(project = proj1, boqtype = '1')
    approved_boq = boqdata.objects.filter(project = proj1, boqtype = '2')
    if proj1:
        proj['id'] = proj1.id
        proj['name'] = proj1.name
        proj['dprsubdate'] = proj1.dprsubdate
        proj['amt_asked'] = proj1.amt_asked
        proj['amt_released'] = proj1.amt_released
        proj['schedule'] = proj1.schedule
        proj['orischedule'] = proj1.orischedule
        proj['fundcategory'] = proj1.fundcategory
        proj['quantum'] = proj1.quantumOfFunding
        proj['status'] = proj1.status
        proj['remark'] = proj1.remark
        proj['remark_date'] = proj1.remark_date
        proj['submitted_boq'] = sub_boq
        # proj['submitted_boq'] = get_boq_details(proj1.submitted_boq)
        
        proj['submitted_boq_Gtotal'] = 0
        proj['user_username'] = proj1.userid.username
        proj['user_nodal'] = proj1.userid.nodal
        proj['user_region'] = proj1.userid.region
        proj['user_utilname'] = proj1.userid.utilname
        proj['user_contact'] = proj1.userid.contact
        proj['user_address'] = proj1.userid.address
        proj['user_reqdate'] = proj1.userid.reqdate
        proj['user_aprdate'] = proj1.userid.reqdate
        proj['user_lastlogin'] = proj1.userid.lastlogin
        proj['user_active'] = proj1.userid.active
        return proj
    else:
        return False

def get_boq_details(submitted_boq):
    
    # print()
    eachboq = submitted_boq[1:-1].replace("\'", "\"").replace("}, {","}&%#{").split('&%#')
    abc = []
    for boq in eachboq :
        
        one_boq = json.loads(boq)
        # attrlist = boq.split(', ')
        
        # one_boq={}
        # for attr in attrlist:
        #     # print(attr)
        #     attrname = attr.split(':')[0][1:-1]
        #     attrvalue = attr.split(':')[1][:-1]
        #     one_boq[attrname] = attrvalue
        #     # print(one_boq)
        abc.append(one_boq)
    return abc

def get_Gtotal_list(abc):
    item_Gtotal = {}
    Gtotal_list = []
    for boq in abc:
        if boq['itemname'] in item_Gtotal.keys():
            item_Gtotal[boq['itemname']] = item_Gtotal[boq['itemname']] + boq['itemcost']
        else:
                item_Gtotal[boq['itemname']] = boq['itemcost']
    for key, value in item_Gtotal.items():
        Gtotal_list.append({'itemname':key, 'grandtotal':value})
    return Gtotal_list

def get_Gtotal(abc):
    item_Gtotal = {}
    
    totalval = 0
    for boq in abc:
        if boq['itemname'] in item_Gtotal.keys():
            item_Gtotal[boq['itemname']] = item_Gtotal[boq['itemname']] + boq['itemcost']
        else:
                item_Gtotal[boq['itemname']] = boq['itemcost']
    for key, value in item_Gtotal.items():
        totalval = totalval + value
    return totalval

def boq_grandtotal(givenboq):
    Gtotal = 0
    for boq in givenboq:
        
        Gtotal = Gtotal + float(boq.itemqty)*float(boq.unitcost)
    
    return round(Gtotal)

# def temp_projectDetails(projid):
#     proj = {}
#     proj1 = temp_projects.objects.get(id = projid)
#     if proj1:
#         proj['id'] = proj1.id
#         proj['name'] = proj1.proname
#         proj['dprsubdate'] = proj1.dprsubdate
#         proj['amt_asked'] = proj1.amountasked
#         proj['deny'] = proj1.deny
#         proj['schedule'] = proj1.schedule
#         proj['remark'] = proj1.remark
#         proj['removed'] = proj1.removed
#         proj['submitted_boq'] = get_boq_details(proj1.submitted_boq)
#         proj['submitted_boq_Gtotal'] = get_Gtotal_list(proj['submitted_boq'])
#         proj['user_username'] = proj1.userid.username
#         proj['user_nodal'] = proj1.userid.nodal
#         proj['user_region'] = proj1.userid.region
#         proj['user_utilname'] = proj1.userid.utilname
#         proj['user_contact'] = proj1.userid.contact
#         proj['user_address'] = proj1.userid.address
#         proj['user_reqdate'] = proj1.userid.reqdate
#         proj['user_aprdate'] = proj1.userid.reqdate
#         proj['user_lastlogin'] = proj1.userid.lastlogin
#         proj['user_active'] = proj1.userid.active
#         return proj
#     else:
#         return False

def pen_users(request):
    if adminonline(request):
        penuser = users.objects.filter(activate = False)
        return penuser
    else:
        return oops(request)

def pen_users_num(request):
    if adminonline(request):
        penuser = pen_users(request)
        if penuser:
            return penuser.count()
        else:
            return 0
    else:
        return oops(request)


def get_all_users(request):
    if adminonline(request):
        usersobj = users.objects.filter(admin = False)
        allusers = []
        for userobj in usersobj:
            allusers.append(userDetails(userobj.username))
        return allusers
    else:
        return False


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

def isnum(value):
    try:
        int(value)
        return True
    except:
        return False


def smkdir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True
    except:
        return False

def sremove(filepath):
    try:
        os.remove(filepath)
        return True
    except OSError:
        return False

def srmdir(filename):
    try:
        shutil.rmtree(filename, ignore_errors=True)
        return True
    except OSError:
        return False


def handle_uploaded_file(path, f):
    try:
        destination = open(path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return True
    except:
        return False

def handle_download_file(filepath, request):
    
    if os.path.exists(filepath):
        
        with open(filepath,'rb') as fh:
            response = HttpResponse(fh.read(), content_type = "application/adminupload")
            response['Content-Disposition'] = 'inline;filename =' + filepath.split('/')[-1]
            return response
    else:
        
        return oops(request)

# def getTempProjects(request):
#     if adminonline(request):
#         temp_project_list = []
#         temp_project = temp_projects.objects.all().exclude(deny = True)
#         for proj in temp_project:            
#             temp_project_list.append(temp_projectDetails(proj.id))
#         return temp_project_list
#     return False

def sanitize(str0):
    str1 = str0.replace(",","")
    str2 = str1.replace(":","")
    str3 = str2.replace("/","")
    str4 = str3.replace("]["," ")
    return str4

def sanitize_name(str0):
    str1 = str0.replace("/","_")
    str2 = str1.replace("\'","_")
    str3 = str2.replace("/","")
    str4 = str3.replace("]["," ")
    return str4

def username_sanitize(str0):
    str1 = sanitize(str0)
    str2 = str1.replace(" ","")
    return str2

def emp_check(celldata):   
    if celldata == '' or celldata == ' ' or celldata == '  ' or celldata == None or celldata == ',' or celldata == '..' or celldata == '-':
        return True
    else:
        return False

def getTempProjects_user(request, userid):
    if useronline(request):
        temp_project_list = []
        temp_project = temp_projects.objects.filter(userid = userid).exclude(deny = True)
        for proj in temp_project:
            proj.submitted_boq = get_boq_details(proj.submitted_boq)
            proj.submitted_boq_Gtotal = get_Gtotal_list(proj.submitted_boq)
        return temp_project_list
    return False



def full_admin_context(request):
    if adminonline(request):
        # return {'user':userDetails(request.session['user']), 'nopendingusers' : users.objects.filter(activate = False).count(), 'nopendingprojects' : temp_projects.objects.all().count()}
        context = {'user':userDetails(request.session['user']) , 'nopendingusers' : pen_users_num(request), 'nopendingprojects' : temp_projects.objects.all().exclude(deny = True).count()}
        context['tesgprojects'] = projects.objects.filter(status = '1', deny = False)
        context['appraisal_projects'] = projects.objects.filter(status = '2', deny = False)
        context['monitoring_projects'] = projects.objects.filter(status = '3', deny = False)
        context['noTESG'] = context['tesgprojects'].count()
        context['noappr'] = context['appraisal_projects'].count()
        context['nomon'] = context['monitoring_projects'].count()
        return context 
    else:
        return {}

def full_auditor_context(request):
    if auditoronline(request):
        context = {'user':userDetails('auditor')}
        context['pending_projects'] = temp_projects.objects.all()
        context['all_projs'] = projects.objects.all()
        context['tesgs'] = TESG_admin.objects.all()
        context['apprs'] = Appraisal_admin.objects.all()
        context['monis'] = Monitoring_admin.objects.all()
        return context
    else:
        return {}


def full_user_context(request):
    if useronline(request):
        context = {'user':userDetails(request.session['user'])}
        context['tesgprojects'] = projects.objects.filter(status = '1', userid = users.objects.get(id = context['user']['id']), deny = False)
        context['appraisal_projects'] = projects.objects.filter(status = '2', userid =  users.objects.get(id = context['user']['id']), deny = False)
        context['monitoring_projects'] = projects.objects.filter(status = '3', userid =  users.objects.get(id = context['user']['id']), deny = False)
        context['noTESG'] = context['tesgprojects'].count()
        context['noappr'] = context['appraisal_projects'].count()
        context['nomon'] = context['monitoring_projects'].count()
        userobj = users.objects.get(id = context['user']['id'])
        projectobj = temp_projects.objects.filter(userid = userobj, deny = False)
        context['projectobj']= projectobj
        context['noprojobj']= projectobj.count()
        return context 
    else:
        return {}
    
def notification(userid, notification):
    project_user = users.objects.get(id = userid)
    project_user.notification = str(project_user.notification) + ']*[' + str(notification)
    project_user.save(update_fields=['notification'])
    
    
def workflow(projid, work):
    thisproject = projects.objects.get(id = projid)
    thisproject.workflow = str(thisproject.workflow) + ']*[' + str(work)
    thisproject.save(update_fields= ['workflow'])


def get_TESG_id(request,tesgnum, projid):
    if adminonline(request):
        return TESG_master.objects.filter(tesgnum = TESG_admin.objects.filter(TESG_no = int(tesgnum))[:1].get(), project = projects.objects.get(id = projid))[:1].get().id
    else:
        return oops(request)

def add_amount(projid, amt, request):
    try:
        proj = projects.objects.get(id = projid)
    except:
        return oops(request)
    if proj.amt_released == None or proj.amt_released == '' or proj.amt_released == ' ' or proj.amt_released == 0:
        amt_rel = 0
    else:
        amt_rel = proj.amt_released
    proj.amt_released = int(amt_rel) + int(amt)
    if int(proj.amt_approved) == int(proj.amt_released):
        proj.approved = True
        proj.completedate = datetime.now().date()
        proj.completed = True
        proj.save(update_fields = ['approved','approvedate','amt_released','completed'])
        workflow(proj.id,"Total approved amount for project ID "+str(proj.newid)+' released.')
        notification(getadmin_id(), 'Total approved amount for project ID '+str(proj.newid)+' released.')
        notification(proj.userid.id, 'Total approved amount for project ID '+str(proj.newid)+' released.')
        return True
    else:
        proj.save(update_fields = ['amt_released'])
        workflow(proj.id,"Amount of ₹"+ str(amt)+" released for project ID "+str(proj.newid))
        notification(proj.userid.id, "Amount of ₹"+ str(amt)+" released for project ID "+str(proj.newid))
        return False
    
def add_amount_loa(loaid,amt, request):
    try:
        thisloa = loadata.objects.get(id = loaid)
    except:
        return oops(request)
    if thisloa.amt_released == None or thisloa.amt_released == '' or thisloa.amt_released == ' ' or thisloa.amt_released == 0:
        amt_rel = 0
    else:
        amt_rel = thisloa.amt_released
    thisloa.amt_released = int(amt_rel) + int(amt)
    
    if int(thisloa.amt_released) == int(thisloa.amt):
        thisloa.completed = True
        thisloa.compdate = datetime.now().date()
        thisloa.save(update_fields = ['completed','compdate'])
        workflow(thisloa.project.id,'Total amount of '+str(thisloa.amt)+' against LOA placed on '+str(thisloa.subdate)+' has been released.')
        notification(thisloa.user.id,'Total amount against LOA placed on '+str(thisloa.subdate)+' has been released for project ID '+str(thisloa.project.newid))
        return True
    else:
        thisloa.save(update_fields = ['amt_released'])
        return False

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)    

def pass_valid(joke):
    if len(joke) < 6:
        return False
    special_characters = "@#$%&*"
    if not any(c in special_characters for c in joke):
        return False
    if not has_numbers(joke):
        return False
    if not any(c.isupper() for c in joke):
        return False
    if not any(c.islower() for c in joke):
        return False
    return True
    
    

def transformext(abc):
    abc1 = abc.split(']*[')    
    extensions = []
    p = 1
    for a in abc1:
        lol = a.split('(@)')
        k = {}
        k['uid'] = p
        k['exttime'] = lol[0]
        k['filename'] = lol[1]
        extensions.append(k)
        p = p + 1
    return extensions