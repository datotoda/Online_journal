import datetime
import operator

import pytz
from django.shortcuts import render, redirect

from main.forms import LessonForm, StudentForm, ParentForm, ClassForm, SubjectForm, TimeForm, CourseForm, ScheduleForm
from main.models import Lesson, Student, Parent, Class, Subject, Time, Course, Schedule


def list_objs(request, obj_list, form, obj_name_prefix):
    context = {
        f'{obj_name_prefix}': obj_list,
        'form': form
    }
    return render(request, f'main/list/{obj_name_prefix}.html', context)


def detail_obj(request, obj, form, obj_name_prefix):

    context = {
        f'{obj_name_prefix}_obj': obj,
        'edit_form': form
    }
    return render(request, f'main/detail/{obj_name_prefix}.html', context)


def delete_obj(request, pk, model_class, redirect_name):
    obj = model_class.objects.filter(user=request.user).get(id=pk)

    if request.method == 'POST':
        print(f'{redirect_name} delete POST', obj)
        obj.delete()
        return redirect(redirect_name)

    print(f'{redirect_name} delete GET ', obj)
    return redirect(redirect_name)


def edit_obj(request, pk, model_class, form_class, redirect_prefix):
    obj = model_class.objects.filter(user=request.user).get(id=pk)

    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # print('{redirect_prefix}_update POST', form.cleaned_data)
            return redirect(f'{redirect_prefix}-detail', pk)
        print('form is not valid')

    print(f'{redirect_prefix}_update GET ', obj)
    return redirect(f'{redirect_prefix}-detail', pk)


def add_obj(request, model_class, form_class, redirect_prefix, sufix='s'):
    if request.method == 'POST':
        obj = model_class()
        form = form_class(request.POST, obj)
        if form.is_valid():
            obj = form.save()
            obj.user = request.user

            if model_class is Course:
                if obj.course_class is not None:
                    obj.month_count = obj.course_class.courses.order_by('month_count').last().month_count + 1

            obj.save()
            return redirect(f'{redirect_prefix}-detail', obj.id)
        print('form is not valid')

    print(f'{redirect_prefix}_update GET ')
    return redirect(f'{redirect_prefix}{sufix}')


# ACTIONS


def lessons_done(request, pk):
    lessons_objects = request.user.times.get(id=pk).lessons

    if request.method == 'POST':
        lessons_for_bulk = []

        for lesson in lessons_objects.all():
            if 'lessons_done' in request.POST and not lesson.done:
                lesson.done = True
                lessons_for_bulk.append(lesson)
            elif 'lessons_undone' in request.POST and lesson.done:
                lesson.done = False
                lessons_for_bulk.append(lesson)

        Lesson.objects.bulk_update(lessons_for_bulk, ['done'])
        return redirect('time-detail', pk)

    return redirect('time-detail', pk)


def done_lesson(request, lesson, redirect_name, redirect_pk=None):
    if request.method == 'POST':
        if 'lesson_done' in request.POST and not lesson.done:
            lesson.done = True
            lesson.save()
        elif 'lesson_undone' in request.POST and lesson.done:
            lesson.done = False
            lesson.save()

    if redirect_pk:
        return redirect(redirect_name, redirect_pk)
    return redirect(redirect_name)


def lesson_done(request, pk):
    lesson = request.user.lessons.get(id=pk)
    return done_lesson(request, lesson, 'lesson-detail', pk)


def lesson_done_journal(request, pk):
    lesson = request.user.lessons.get(id=pk)
    return done_lesson(request, lesson, 'class-journal', lesson.time.course.course_class.id)


def lesson_done_today(request, pk):
    lesson = request.user.lessons.get(id=pk)
    return done_lesson(request, lesson, 'today-lessons',)


def course_done(request, pk):
    course = request.user.courses.get(id=pk)

    if request.method == 'POST':
        if 'course_done' in request.POST and not course.done:
            course.done = True
            course.save()
        elif 'course_undone' in request.POST and course.done:
            course.done = False
            course.save()

        return redirect('course-detail', pk)

    return redirect('course-detail', pk)


def class_journal(request, pk):
    class_obj = request.user.classes.get(id=pk)
    students_list = class_obj.students.all()
    courses_list = class_obj.courses.all()
    times_list = []
    for course in courses_list:
        for a in course.agenda.all():
            times_list.append(a)

    if len(times_list + list(students_list)) == 0:
        return redirect('class-detail', pk)

    times_list.sort(key=operator.attrgetter('lesson_datetime'))
    all_lessons = request.user.lessons

    lss = []
    result_list = []

    for s in students_list:
        r_l = (s, [])
        for t in times_list:
            ls = all_lessons.filter(student=s, time=t).first()

            if ls is None:
                ls = Lesson(student=s, time=t, user=request.user)
                ls.save()
                lss.append(ls)

            r_l[1].append(ls)
        result_list.append(r_l)
    # Lesson.objects.bulk_create(lss)

    context = {
        'cls': class_obj,
        'times_list': times_list,
        'result_list': result_list,
    }
    return render(request, 'main/feature/journal.html', context)


def journals(request):
    return render(request, 'main/feature/journals.html')


def today_lessons(request):
    # [
    #     ['cls id_1', ['les id_12', 'les id_42']],
    #     ['cls id_1', ['les id_11', 'les id_52']],
    # ]
    today_date = datetime.datetime.utcnow().date()
    today_date_formated = today_date.strftime("%A {} %B").format(int(today_date.day))

    result_list = []
    today_times_list = request.user.times.filter(lesson_datetime__day=today_date.day,
                                                 lesson_datetime__month=today_date.month,
                                                 lesson_datetime__year=today_date.year).all()
    classes_list = sorted(list(set(
        map(lambda tm: tm.course.course_class, filter(lambda tm: tm.course is not None, today_times_list))
    )),
        key=operator.attrgetter('id'))

    for cls in classes_list:
        result_list.append([cls, []])

        students_list = cls.students.all()
        courses_list = cls.courses.all()
        times_list = []
        for course in courses_list:
            for t in course.agenda.filter(lesson_datetime__day=today_date.day,
                                          lesson_datetime__month=today_date.month,
                                          lesson_datetime__year=today_date.year).all():
                times_list.append(t)

        times_list.sort(key=operator.attrgetter('lesson_datetime'))
        all_lessons = request.user.lessons

        for s in students_list:
            for t in times_list:
                ls = all_lessons.filter(student=s, time=t).first()

                if ls is None:
                    ls = Lesson(student=s, time=t, user=request.user)
                    ls.save()

                result_list[-1][-1].append(ls)

    for _class, _times in result_list:
        _times.sort(key=operator.attrgetter('time.lesson_datetime'))

    result_list.sort(key=lambda cts: cts[1][0].time.lesson_datetime)

    context = {
        'result_list': result_list,
        'today_date': today_date_formated,
    }
    return render(request, 'main/feature/today_lessons.html', context)


def class_schedule(request, pk):
    class_obj = request.user.classes.get(id=pk)
    form = ScheduleForm()

    result_list = [(i, []) for i in Schedule.WeekDay.labels]
    for schedule in class_obj.schedules.all().order_by('lesson_time'):
        result_list[schedule.week_day - 1][1].append(schedule)
    context = {
        'cls': class_obj,
        'result_list': result_list,
        'form': form
    }
    return render(request, 'main/feature/class_schedule.html', context)


######################################################################


# OBJECTS LIST


def classes(request):
    if request.user.is_anonymous:
        return redirect('login')

    obj_list = request.user.classes.all()

    form = ClassForm()
    form.fields['students'].queryset = request.user.students
    form.fields['subject'].queryset = request.user.subjects

    return list_objs(request, obj_list, form, 'classes')


def parents(request):
    obj_list = request.user.parents.all()

    form = ParentForm()

    return list_objs(request, obj_list, form, 'parents')


def students(request):
    obj_list = request.user.students.all()

    form = StudentForm()
    form.fields['parent'].queryset = request.user.parents

    return list_objs(request, obj_list, form, 'students')


def lessons(request):
    obj_list = request.user.lessons.all()

    form = LessonForm()
    form.fields['student'].queryset = request.user.students.all()
    form.fields['time'].queryset = request.user.times.all()

    return list_objs(request, obj_list, form, 'lessons')


def times(request):
    obj_list = request.user.times.all()

    form = TimeForm()
    form.fields['course'].queryset = request.user.courses.all()

    return list_objs(request, obj_list, form, 'times')


def courses(request):
    obj_list = request.user.courses.all()

    form = CourseForm()
    form.fields['course_class'].queryset = request.user.classes.all()

    return list_objs(request, obj_list, form, 'courses')


def subjects(request):
    obj_list = request.user.subjects.all()

    form = SubjectForm()

    return list_objs(request, obj_list, form, 'subjects')


# DETAIL


def class_detail(request, pk):
    obj = request.user.classes.get(id=pk)
    form = ClassForm(instance=obj)

    form.fields['students'].queryset = request.user.students.all()
    form.fields['subject'].queryset = request.user.subjects.all()

    context = {
        'class_obj': obj,
        'edit_form': form,
    }
    return render(request, 'main/detail/class.html', context)


def parent_detail(request, pk):
    obj = request.user.parents.get(id=pk)
    form = ParentForm(instance=obj)

    return detail_obj(request, obj, form, 'parent')


def student_detail(request, pk):
    obj = request.user.students.get(id=pk)
    form = StudentForm(instance=obj)

    form.fields['parent'].queryset = request.user.parents.all()

    return detail_obj(request, obj, form, 'student')


def lesson_detail(request, pk):
    obj = request.user.lessons.get(id=pk)
    form = LessonForm(instance=obj)

    form.fields['student'].queryset = request.user.students.all()
    form.fields['time'].queryset = request.user.times.all()

    return detail_obj(request, obj, form, 'lesson')


def time_detail(request, pk):
    obj = request.user.times.get(id=pk)
    form = TimeForm(instance=obj)

    form.fields['course'].queryset = request.user.courses.all()

    return detail_obj(request, obj, form, 'time')


def course_detail(request, pk):
    obj = request.user.courses.get(id=pk)
    form = CourseForm(instance=obj)

    form.fields['course_class'].queryset = request.user.classes.all()

    return detail_obj(request, obj, form, 'course')


def subject_detail(request, pk):
    obj = request.user.subjects.get(id=pk)
    form = SubjectForm(instance=obj)

    return detail_obj(request, obj, form, 'subject')


# DELETE


def class_delete(request, pk):
    return delete_obj(request, pk, Class, 'classes')


def parent_delete(request, pk):
    return delete_obj(request, pk, Parent, 'parents')


def student_delete(request, pk):
    return delete_obj(request, pk, Student, 'students')


def lesson_delete(request, pk):
    return delete_obj(request, pk, Lesson, 'lessons')


def time_delete(request, pk):
    return delete_obj(request, pk, Time, 'times')


def course_delete(request, pk):
    return delete_obj(request, pk, Course, 'courses')


def subject_delete(request, pk):
    return delete_obj(request, pk, Subject, 'subjects')


# UPDATE


def class_update(request, pk):
    return edit_obj(request, pk, Class, ClassForm, 'class')


def parent_update(request, pk):
    return edit_obj(request, pk, Parent, ParentForm, 'parent')


def student_update(request, pk):
    return edit_obj(request, pk, Student, StudentForm, 'student')


def lesson_update(request, pk):
    return edit_obj(request, pk, Lesson, LessonForm, 'lesson')


def time_update(request, pk):
    return edit_obj(request, pk, Time, TimeForm, 'time')


def course_update(request, pk):
    return edit_obj(request, pk, Course, CourseForm, 'course')


def subject_update(request, pk):
    return edit_obj(request, pk, Subject, SubjectForm, 'subject')


# ADD


def class_add(request):
    return add_obj(request, Class, ClassForm, 'class', 'es')


def parent_add(request):
    return add_obj(request, Parent, ParentForm, 'parent')


def student_add(request):
    return add_obj(request, Student, StudentForm, 'student')


def lesson_add(request):
    return add_obj(request, Lesson, LessonForm, 'lesson')


def time_add(request):
    return add_obj(request, Time, TimeForm, 'time')


def course_add(request):
    return add_obj(request, Course, CourseForm, 'course')


def subject_add(request):
    return add_obj(request, Subject, SubjectForm, 'subject')


def schedule_detail(request, c_pk, s_pk):
    obj = request.user.classes.get(id=c_pk).schedules.get(id=s_pk)
    form = ScheduleForm(instance=obj)

    # form.fields['parent'].queryset = request.user.parents.all()

    return detail_obj(request, obj, form, 'schedule')


def schedule_delete(request, c_pk, s_pk):
    obj = request.user.classes.get(id=c_pk).schedules.get(id=s_pk)

    if request.method == 'POST':
        print('schedule_delete delete POST', obj)
        obj.delete()
        return redirect('class-schedule', c_pk)

    print('schedule_delete delete GET ', obj)
    return redirect('class-schedule', c_pk)


def schedule_update(request, c_pk, s_pk):
    obj = request.user.classes.get(id=c_pk).schedules.get(id=s_pk)

    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('schedule-detail', c_pk, s_pk)
        print('form is not valid')

    print('schedule-detail_update GET ', obj)
    return redirect('schedule-detail', c_pk, s_pk)


def schedule_add(request, c_pk):
    class_obj = request.user.classes.get(id=c_pk)

    if request.method == 'POST':
        obj = Schedule()
        form = ScheduleForm(request.POST, obj)
        if form.is_valid():
            obj = form.save()

            obj.user = request.user
            obj.course_class = class_obj

            obj.save()
            return redirect('class-schedule', class_obj.id)
        print('form is not valid')

    print('class-schedule GET ')
    return redirect('class-schedule', class_obj.id)


def class_generate_course(request, pk):
    class_obj = request.user.classes.get(id=pk)

    if request.method == 'POST':
        count = int(request.POST['count'])
        start_time = request.POST['start_time']

        if count > 0:
            temp_last = class_obj.courses.order_by('month_count').last()
            if temp_last:
                new_month_count = temp_last.month_count + 1
                new_price = temp_last.price
            else:
                new_month_count = 1
                new_price = 0

            new_course = Course(course_class=class_obj,
                                description=request.POST['description'],
                                month_count=new_month_count,
                                price=new_price,
                                done=False,
                                user=request.user)

            new_course.save()

            # 0-ორშაბაში, 1-სამშაბაში ... 5-შაბათი, 6-კვირა

            if start_time:
                o_last_time = datetime.datetime.fromisoformat(start_time)
            else:
                o_last_time = request.user.times.filter(course__course_class=class_obj).order_by('-lesson_datetime').first()
                if o_last_time is None:
                    o_last_time = datetime.datetime.now()
                else:
                    o_last_time = o_last_time.lesson_datetime
            o_last_time = datetime.datetime(o_last_time.year, o_last_time.month, o_last_time.day,
                                            o_last_time.hour, o_last_time.minute)

            sch_list = [(sch.week_day - 1, sch.lesson_time) for sch in class_obj.schedules.order_by('week_day', 'lesson_time').all()]

            last_time = datetime.datetime(o_last_time.year, o_last_time.month, o_last_time.day)

            while last_time.weekday() != 0:
                last_time -= datetime.timedelta(days=1)
            new_lesson_datetime = last_time + datetime.timedelta(days=sch_list[0][0], hours=sch_list[0][1].hour, minutes=sch_list[0][1].minute)

            dts = []
            for i in range(len(sch_list) - 1):
                dt = datetime.timedelta(days=sch_list[i + 1][0], hours=sch_list[i + 1][1].hour, minutes=sch_list[i + 1][1].minute) - \
                     datetime.timedelta(days=sch_list[i][0], hours=sch_list[i][1].hour, minutes=sch_list[i][1].minute)
                dts.append(dt)

            dts.append(datetime.timedelta(days=sch_list[0][0]+7, hours=sch_list[0][1].hour, minutes=sch_list[0][1].minute) -
                       datetime.timedelta(days=sch_list[-1][0], hours=sch_list[-1][1].hour, minutes=sch_list[-1][1].minute))

            new_times = []
            i = 0
            while new_lesson_datetime < o_last_time:
                new_lesson_datetime += dts[i % len(dts)]
                i += 1
            for j in range(count):
                tz = pytz.UTC
                new_times.append(
                    Time(course=new_course,
                         lesson_datetime=tz.localize(new_lesson_datetime),
                         description='',
                         user=request.user))
                new_lesson_datetime += dts[i % len(dts)]
                i += 1

            Time.objects.bulk_create(new_times)

    return redirect('class-detail', class_obj.id)
