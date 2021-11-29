from .helpers import *


    
    
def user_view_all_pays(request):
    if useronline(request):
        context = full_user_context(request)
        thisuser = getuser(request)
        context['all_pays'] = payment.objects.filter(user = thisuser)
        
        paytotal = 0
        for pay in context['all_pays']:
            paytotal = paytotal + int(pay.amount)
        context['paytotal'] = paytotal
        
        loatotal = 0
        loas = loadata.objects.filter(user = thisuser)
        for loa in loas:
            loatotal = loatotal + int(loa.amt)
        context['loatotal'] = loatotal
        
        context['pendingamt'] = loatotal - paytotal
        
        init_pays = init_payment.objects.filter(user = thisuser)
        totalinit = 0
        for init in init_pays:
            totalinit = totalinit + int(init.amount)
        context['totalinit'] = totalinit
        
        
            
        context['all_init_pays'] = init_payment.objects.filter(user = thisuser)
        return render(request,'psdf_main/_user_view_pays.html',context)
    else:
        return oops(request)