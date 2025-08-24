
from django.contrib import admin
from django.urls import path
from AjiraApp import views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView



urlpatterns = [
     path("", views.portal, name="portal"),
     path("upload/", views.upload_timetable, name="upload_timetable"),
     path('timetable/', views.timetable_view, name='timetable'), 
     path("delete-timetable/", views.delete_timetable, name="delete_timetable"),
     path("admin-panel/", views.admin_panel, name="admin_panel"),
     path("chats/",views.chatBoard,name="chat-board"),
     path("confessions/",views.confession,name="confession-board"),
     path("displayer/<str:section>/", views.displayer, name="displayer-board"),
     path("auth/", views.auth_view, name="auth"),
     path("logout/", views.logout_view, name="logout"),

     path("chat/", views.chatBoard, name="chat-board"),
    # Global chat
    path("messages/", views.global_messages, name="get-messages"),
    path("messages/send/", views.send_message, name="send-message"),

    # Private chat
    path("private/<str:username>/", views.private_messages, name="private-messages"),
    path("private/<str:username>/send/", views.send_private_message, name="send-private-message"),

    # Reports
    path("report/", views.report_message, name="report-message"),
     # Admin Management (edit/delete admins)
    path("edit_admin/<int:user_id>/", views.edit_admin, name="edit_admin"),
    # Add URLs
    
    # edit URLs
    # ================= Delete Routes =================
    # DELETE paths
    path("delete-admin/<int:user_id>/", views.delete_admin, name="delete_admin"),
    path("delete-religion/<int:item_id>/", views.delete_religion, name="delete_religion"),
    path("delete-politics/<int:item_id>/", views.delete_politics, name="delete_politics"),
    path("delete-music/<int:item_id>/", views.delete_music, name="delete_music"),
    path("delete-ad/<int:item_id>/", views.delete_ad, name="delete_ad"),
    path("delete-news/<int:item_id>/", views.delete_news, name="delete_news"),
    path("delete-memo/<int:item_id>/", views.delete_memo, name="delete_memo"),
    path("delete-reel/<int:item_id>/", views.delete_reel, name="delete_reel"),
    path("delete-hostel/<int:item_id>/", views.delete_hostel, name="delete_hostel"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


