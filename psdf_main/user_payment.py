from .helpers import *


def new_loa(request):
    if useronline(request) and not adminonline(request):
        context = full_user_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            thisproject = projects.objects.get(id = projid)
            aboq = boqdata.objects.filter(project = thisproject, boqtype = '3') #Change to 3
            context['aboq'] = aboq
            context['approved_boq_total'] = boq_grandtotal(aboq)
            context['loa_project'] = thisproject
            return render(request, 'psdf_main/_user_new_loa.html', context)
        userobj = users.objects.filter(username = request.session['user'])[:1].get()
        print(userobj)
        context['projectlist'] = projects.objects.filter(status = '4', userid = userobj)
        print(context['projectlist'])
        return render(request, 'psdf_main/_user_new_loa.html', context)
    else:
        return oops(request)

def submitloa(request):
    if useronline(request) and not adminonline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projid')
            aboq = boqdata.objects.filter(project = projects.objects.get(id = projid), boqtype = '3') #change to 3
            req_boq = []
            if request.FILES:
                if 'loa' in request.FILES:
                    req_boq = []
                    for boq in aboq:
                        if isnum(req.get('item_'+str(boq.itemno))):
                            if isnum(req.get('item_'+str(boq.itemno))) >= 0:
                                req_boq.append({'itemno':boq.itemno,'itemname':boq.itemname,'itemdesc':boq.itemdesc,'itemqty':int(req.get('item_'+str(boq.itemno))),'itemprice':float(boq.itemprice),'itemcost':float(float(boq.itemprice)*int(req.get('item_'+str(boq.itemno))))})
                            else:
                                messages.error(request, 'Claim entry of item no. '+str(boq.itemno) + ' cannot be negative')
                                redirect('/new_loa')
                        else:
                            messages.error(request, 'Error in claim entry of item no. '+str(boq.itemno))
                            redirect('/new_loa')
            messages.error(request, 'Aborted! LOA file not uploaded.')
            redirect('/new_loa')
            # for boq in aboq:
            #     tboq = boqdata()
            #     tboq.project = boq.project
            #     tboq.boqtype = '4'
            #     tboq.itemno = boq.itemno
            #     tboq.itemname = boq.itemname
            #     tboq.itemqty = boq.itemqty - int(req.get('item_'+str(boq.itemno)))
            #     tboq.itemdesc = boq.itemdesc
            #     tboq.unitcost = boq.unitcost
            #     tboq.save()
    else:
        return oops(request)