from django.contrib import admin

from .models import Lesson, Student, Parent, Class, Subject, Time, Course, Schedule


@admin.action(description='Mark selected lessons as done')
def make_done(modeladmin, request, queryset):
    queryset.update(done=True)


@admin.action(description='Mark selected lessons as not done')
def make_not_done(modeladmin, request, queryset):
    queryset.update(done=False)


# admin.site.unregister(User)
# admin.site.unregister(Group)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):

    class CourseInline(admin.TabularInline):
        model = Course
        extra = 0
        readonly_fields = ['description']

    model = Class
    list_filter = ('user', 'subject', 'students', 'active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'title', 'description')
    list_display = ('title', 'description', 'active', 'user')
    filter_horizontal = ('students', )

    inlines = [
        CourseInline,
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    class ClassInline(admin.TabularInline):
        model = Class.students.through
        fields = ('class',)
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        extra = 0

    model = Student
    list_filter = ('user', 'name', 'last_name')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'name', 'last_name', 'discord_username')
    list_display = ('__str__', 'discord_username', 'fb_link', 'user')
    inlines = [
        ClassInline,
    ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = ('__str__', 'student', 'time', 'course_class', 'done', 'user')
    list_filter = ('user', 'student', 'time', 'done')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_editable = ('done',)
    actions = [make_done, make_not_done]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):

    class ChildInline(admin.TabularInline):
        model = Student
        extra = 0
        verbose_name = 'Child'
        verbose_name_plural = 'Children'

    list_display = ('__str__', 'phone_number', 'fb_link', 'user')
    model = Parent
    list_filter = ('user', 'name', 'last_name')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'name', 'last_name')
    inlines = [
        ChildInline,
    ]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_filter = ('user', 'title')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'title', 'description')
    list_display = ('title', 'description', 'user')


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    model = Time
    list_display = ('__str__', 'course', 'user')
    list_filter = ('user', 'course', 'lesson_datetime')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'lesson_datetime', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    class TimeInline(admin.TabularInline):
        model = Time
        extra = 0
        verbose_name = 'Time'
        verbose_name_plural = 'Agenda'
        fields = ('lesson_datetime',)
        readonly_fields = ['description']

    model = Course
    list_filter = ('user', 'month_count', 'course_class', 'done')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'month_count', 'course_class')
    list_display = ('__str__', 'course_class', 'done', 'user')
    list_editable = ('done',)
    inlines = [
        TimeInline
    ]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    list_filter = ('user', 'course_class', 'week_day', 'lesson_time', 'duration')
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'course_class', 'week_day', 'lesson_time', 'duration')
    list_display = ('__str__', 'course_class', 'week_day', 'lesson_time', 'duration', 'user')

