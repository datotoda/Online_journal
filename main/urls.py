from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),

    path('classes/', views.classes, name='classes'),
    path('parents/', views.parents, name='parents'),
    path('students/', views.students, name='students'),
    path('lessons/', views.lessons, name='lessons'),
    path('times/', views.times, name='times'),
    path('courses/', views.courses, name='courses'),
    path('subjects/', views.subjects, name='subjects'),

    path('class/<int:pk>/', views.class_detail, name='class-detail'),
    path('parent/<int:pk>/', views.parent_detail, name='parent-detail'),
    path('student/<int:pk>/', views.student_detail, name='student-detail'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('time/<int:pk>/', views.time_detail, name='time-detail'),
    path('course/<int:pk>/', views.course_detail, name='course-detail'),
    path('subject/<int:pk>/', views.subject_detail, name='subject-detail'),

    path('class/<int:pk>/delete/', views.class_delete, name='class-delete'),
    path('parent/<int:pk>/delete/', views.parent_delete, name='parent-delete'),
    path('student/<int:pk>/delete/', views.student_delete, name='student-delete'),
    path('lesson/<int:pk>/delete/', views.lesson_delete, name='lesson-delete'),
    path('time/<int:pk>/delete/', views.time_delete, name='time-delete'),
    path('course/<int:pk>/delete/', views.course_delete, name='course-delete'),
    path('subject/<int:pk>/delete/', views.subject_delete, name='subject-delete'),

    path('class/<int:pk>/update/', views.class_update, name='class-update'),
    path('parent/<int:pk>/update/', views.parent_update, name='parent-update'),
    path('student/<int:pk>/update/', views.student_update, name='student-update'),
    path('lesson/<int:pk>/update/', views.lesson_update, name='lesson-update'),
    path('time/<int:pk>/update/', views.time_update, name='time-update'),
    path('course/<int:pk>/update/', views.course_update, name='course-update'),
    path('subject/<int:pk>/update/', views.subject_update, name='subject-update'),


    path('add/', views.class_add, name='root-add'),
    path('classes/add/', views.class_add, name='class-add'),
    path('parents/add/', views.parent_add, name='parent-add'),
    path('students/add/', views.student_add, name='student-add'),
    path('lessons/add/', views.lesson_add, name='lesson-add'),
    path('times/add/', views.time_add, name='time-add'),
    path('courses/add/', views.course_add, name='course-add'),
    path('subjects/add/', views.subject_add, name='subject-add'),


    path('time/<int:pk>/lessons_done/', views.lessons_done, name='lessons-done'),
    path('lesson/<int:pk>/lesson_done/', views.lesson_done, name='lesson-done'),
    path('course/<int:pk>/course_done/', views.course_done, name='course-done'),
    path('today/<int:pk>/lesson_done/', views.lesson_done_today, name='lesson-done-today'),
    path('lesson/<int:pk>/lesson_done_journal/', views.lesson_done_journal, name='lesson-done-journal'),
    path('journals/', views.journals, name='journals'),
    path('class/<int:pk>/journal/', views.class_journal, name='class-journal'),
    path('today/lessons/', views.today_lessons, name='today-lessons'),

    path('class/<int:pk>/schedule/', views.class_schedule, name='class-schedule'),
    path('class/<int:c_pk>/schedule/<int:s_pk>/', views.schedule_detail, name='schedule-detail'),
    path('class/<int:c_pk>/schedule/<int:s_pk>/delete/', views.schedule_delete, name='schedule-delete'),
    path('class/<int:c_pk>/schedule/<int:s_pk>/update/', views.schedule_update, name='schedule-update'),
    path('class/<int:c_pk>/schedule/add/', views.schedule_add, name='schedule-add'),
    path('class/<int:pk>/generate_course/', views.class_generate_course, name='class-generate-course'),

    # path('', views.project, name='project'),
    # path('', views.createProject, name='create-project'),
    # path('', views.updateProject, name='forms-project'),
    # path('', views.deleteProject, name='delete-project'),
    # path('', lambda request: redirect('/projects/')),
]

