from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name = ""),
    path('registeruser/', views.registeruser , name = "registeruser"),
    path('newdpr/', views.newdpr , name = "newdpr"),
    path('upload_dpr_docs', views.upload_dpr_docs, name = 'upload_dpr_docs'),
    path('logout/', views.logout, name="logout"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_pending_users/', views.admin_pending_users, name="admin_pending_users"),
    path('admin_pending_projects/', views.admin_pending_projects, name="admin_pending_projects"),
    path('admin_users/', views.admin_users, name="admin_users"),
    path('update_boq/<str:projectid>', views.update_boq, name="update_boq"),
    path('admin_control_panel/', views.control_panel, name="admin_control_panel"),

    path('approve_user/<str:userid>',views.approve_user, name='approve_user' ),
    path('reject_user/<str:userid>',views.reject_user, name='reject_user' ),
    path('ban_user/<str:userid>',views.ban_user, name='ban_user' ),
    path('allow_user/<str:userid>',views.allow_user, name='allow_user' ),
    path('downloadformat/<str:thisdoc>', views.downloadformat, name="downloadformat"),
    path('uploadformat/', views.uploadformat, name="uploadformat"),

    #Project_handling
    path('download_temp_project/<str:projid>', views.download_temp_project, name="download_temp_project"),
    path('download_project/<str:projid>', views.download_project, name="download_project"),
    path('acceptdpr/<str:projid>', views.acceptdpr, name="acceptdpr"),
    path('rejectdpr/<str:projid>', views.rejectdpr, name="rejectdpr"),
    path('notificationread/<str:userid>', views.notificationread, name="notificationread"),
    path('add_remark/<str:thispage>',views.add_remark,name='add_remark'),

    #pending_projects
    path('under_examination/', views.under_examination, name="under_examination"),

    #view Users
    path('view_user/<str:userid>', views.view_user, name="view_user"),

    #Control
    path('del_tesg/<str:tesgid>', views.del_tesg, name="del_tesg"),

    #TESG
    path('TESG_chain/<str:project_id>', views.TESG_chain, name = "TESG_chain"),
    path('tesgchain_form/', views.tesgchain_form, name = "tesgchain_form"),
    path('TESG_projects/', views.TESG_projects, name="TESG_projects"),
    path('TESG_upload/', views.TESG_upload, name="TESG_upload"),
    path('rejectproject/<str:projid>', views.rejectproject, name="rejectproject"),
    path('acceptTESG/', views.acceptTESG, name="acceptTESG"),
    path('rejectTESG/', views.rejectTESG, name="rejectTESG"),
    path('user_tesg/', views.user_tesg, name="user_tesg"),
    path('downloadTESGresponse/<str:tesgid_projid>', views.downloadTESGresponse, name = "downloadTESGresponse"),
    path('downloadTESGrequest/<str:tesgid_projid>', views.downloadTESGrequest, name = "downloadTESGrequest"),
    path('user_TESG_chain/<str:projid>', views.user_TESG_chain, name = "user_TESG_chain"),
    path('user_tesg_response', views.user_tesg_response, name = "user_tesg_response"),
    path('approveTESG/<str:projid>', views.approveTESG, name = "approveTESG"),
    path('download_tesg_user_outcome/<str:tesgid>', views.download_tesg_user_outcome, name = "download_tesg_user_outcome"),
    path('download_tesg_user_response/<str:tesgid>', views.download_tesg_user_response, name = "download_tesg_user_response"),
    
    path('view_TESGs', views.view_TESGs, name = "view_TESGs"),
    path('download_tesg_report/<str:tesgid>', views.download_tesg_report, name = "download_tesg_report"),

    #Appraisal
    path('appraisal_projects/', views.appraisal_projects, name="appraisal_projects"),
    path('approve_appraisal/<str:projectid>', views.approve_appraisal, name="approve_appraisal"),
    # path('delete_appr_doc/<str:projid>', views.delete_appr_doc, name = 'delete_appr_doc'),
    path('send_to_tesg/<str:projid>', views.send_to_tesg, name = 'send_to_tesg'),
    path('user_appraisal_projects/', views.user_appraisal_projects, name="user_appraisal_projects"),
    path('APPR_upload/', views.APPR_upload, name="APPR_upload"),
    path('view_apprs/', views.view_apprs, name="view_apprs"),
    path('download_appr_mom/<str:apprid>', views.download_appr_mom, name = 'download_appr_mom'),
    path('del_appr_mom/<str:aprid>', views.del_appr_mom, name = 'del_appr_mom'),
    
    
    
    
    #monitoring
    path('monitoring_projects/', views.monitoring_projects, name="monitoring_projects"),
    path('approve_monitoring/<str:projectid>', views.approve_monitoring, name="approve_monitoring"),
    path('send_to_appr/<str:projid>', views.send_to_appr, name="send_to_appr"),
    path('msend_to_tesg/<str:projid>', views.msend_to_tesg, name="msend_to_tesg"),
    path('user_monitoring_projects/', views.user_monitoring_projects, name="user_monitoring_projects"),
    path('MONI_upload/', views.MONI_upload, name="MONI_upload"),
    path('view_monis/', views.view_monis, name="view_monis"),
    path('download_moni_mom/<str:moniid>', views.download_moni_mom, name = 'download_moni_mom'),
    path('approve_monitoring/<str:projectid>', views.approve_monitoring, name = "approve_monitoring"),
    path('del_moni_mom/<str:aprid>', views.del_moni_mom, name = 'del_moni_mom'),


    #approval
    path('user_in_doc_sign/', views.user_in_doc_sign, name="user_in_doc_sign"),
    path('admin_in_doc_sign/', views.admin_in_doc_sign, name="admin_in_doc_sign"),
    path('download_doc_sign/<str:projid>', views.download_doc_sign, name="download_doc_sign"),
    
    #ViewAll
    path('view_all_projs/', views.view_all_projs, name="view_all_projs"),
    path('user_view_all_projs/', views.user_view_all_projs, name="user_view_all_projs"),
    path('user_project_details/<str:projid>', views.user_project_details, name = "user_project_details"),
    path('admin_project_details/<str:projid>', views.admin_project_details, name = "admin_project_details"),
    path('admin_temp_project_details/<str:projectid>', views.admin_temp_project_details, name = "admin_temp_project_details"),
    path('appr_mom_download/<str:projid>', views.appr_mom_download, name = "appr_mom_download"),
    path('moni_mom_download/<str:projid>', views.moni_mom_download, name = "moni_mom_download"),
    path('admin_boq_view/<str:projid>', views.admin_boq_view, name = "admin_boq_view"),

    path('user_boq_view/<str:projid>', views.user_boq_view, name = "user_boq_view"),
    path('user_back/<str:backpage>', views.user_back, name = "user_back"),
    
    #Auditor
    path('auditor_view_TESGs/', views.auditor_view_TESGs, name="auditor_view_TESGs"),
    path('auditor_view_apprs/', views.auditor_view_apprs, name="auditor_view_apprs"),
    path('auditor_view_monis/', views.auditor_view_monis, name="auditor_view_monis"),
    path('auditor_view_projects/', views.auditor_view_projects, name="auditor_view_projects"),
    path('auditor_project_details/<str:projid>', views.auditor_project_details, name="auditor_project_details"),
    path('auditor_view_user/<str:userid>', views.auditor_view_user, name="auditor_view_user"),
    path('auditor_download_project/<str:projid>', views.auditor_download_project, name="auditor_download_project"),
    

    #LOA Handling
    path('new_loa/', views.new_loa, name="new_loa"),
    path('submitloa/', views.submitloa, name="submitloa"),
    path('updateloa/', views.updateloa, name="updateloa"),
    path('downloadloa/<str:loaid>', views.downloadloa, name="downloadloa"),
    path('userloa/', views.userloa, name="userloa"),    
    path('adminloa/', views.adminloa, name="adminloa"),
    path('ack_loa/', views.ack_loa, name="ack_loa"),
    path('sendloaremark/', views.sendloaremark, name="sendloaremark"),
    
    
    
    #Payment
    
    path('view_all_pays/', views.view_all_pays, name="view_all_pays"),
    path('admin_sanction/', views.admin_sanction, name="admin_sanction"),
    path('download_sanction/<str:projid>', views.download_sanction, name="download_sanction" ),
    path('init_record/', views.init_record, name="init_record"),
    path('init_release/', views.init_release, name="init_release"),
    path('user_init_payment/', views.user_init_payment, name="user_init_payment"),
    path('admin_pay/', views.admin_pay, name="admin_pay"),
    path('admin_pay_proj/', views.admin_pay_proj, name="admin_pay_proj"),
    path('approve_admin_pay/', views.approve_admin_pay, name="approve_admin_pay"),
    path('user_ack_pay/', views.user_ack_pay, name="user_ack_pay"),
    
    
]