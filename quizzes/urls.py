from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'), 
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    # Admin URLs
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/add-quiz/', views.add_quiz, name='add_quiz'),
    path('admin_dashboard/edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('admin_dashboard/delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('admin_dashboard/add-question/', views.add_question, name='add_question'),
]