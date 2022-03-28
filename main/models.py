import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import IntegerChoices, Choices, Sum


class Lesson(models.Model):
    id = models.BigAutoField(primary_key=True)

    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')
    student = models.ForeignKey('Student', default=None, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='lessons', verbose_name='Student')
    time = models.ForeignKey('Time', default=None, null=True, blank=True, on_delete=models.CASCADE,
                             related_name='lessons', verbose_name='Time')
    done = models.BooleanField(default=False, verbose_name='Done')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', null=True)

    @property
    def course(self):
        if self.time is None:
            return None

        return self.time.course

    @property
    def course_class(self):
        if self.course is None:
            return None

        return self.course.course_class

    def __str__(self):
        if self.course_class is None:
            return f'Lesson id_{self.id}'

        return f'{self.course_class}'


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=30, default='', null=True, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='Last Name')
    phone_number = models.BigIntegerField(default=0, null=True, blank=True, verbose_name='Phone Number')
    fb_link = models.URLField(max_length=300, default='', null=True, blank=True, verbose_name='Facebook Profile')
    discord_username = models.CharField(default='', max_length=100, null=True, blank=True, verbose_name='Discord Nickname')
    parent = models.ForeignKey('Parent', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children', verbose_name='Parent')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students', null=True)

    def __str__(self):
        if self.name == '' or self.name is None:
            return f'Student id_{self.id}'

        return f'{self.name} {self.last_name}'


class Parent(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=30, default='', null=True, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='Last Name')
    phone_number = models.BigIntegerField(default=0, null=True, blank=True, verbose_name='Phone Number')
    fb_link = models.URLField(max_length=300, default='', null=True, blank=True, verbose_name='Facebook Profile')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parents', null=True)

    def __str__(self):
        if self.name == '' or self.name is None:
            return f'Parent id_{self.id}'

        return f'{self.name} {self.last_name}'


class Class(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=30, default='', null=True, blank=True, verbose_name='Title')
    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')
    subject = models.ForeignKey('Subject', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='classes', verbose_name='Subject')
    students = models.ManyToManyField('Student', related_name='classes', verbose_name='Students')
    active = models.BooleanField(default=True, verbose_name='Active')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes', null=True)

    @property
    def completed_course(self):
        return self.courses.filter(done=True).count()

    def __salary_sum(self, doned: bool):
        ss = self.courses.filter(done=doned).aggregate(Sum('price')).get('price__sum', 0)
        if ss:
            ss *= self.students.count()
        return f'{ss:.2f} ₾' if ss else '0.00 ₾'

    @property
    def salary_sum_doned(self):
        return self.__salary_sum(True)

    @property
    def salary_sum_undoned(self):
        return self.__salary_sum(False)

    def __str__(self):
        if self.title == '' or self.title is None:
            return f'Class id_{self.id}'

        return f'{self.title.capitalize()} id_{self.id}'

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'


class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=30, default='', verbose_name='Title')
    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects', null=True)

    def __str__(self):
        if self.title == '' or self.title is None:
            return f'Subject id_{self.id}'

        return f'{self.title.capitalize()} {self.description}'


class Time(models.Model):
    id = models.BigAutoField(primary_key=True)

    course = models.ForeignKey('Course', default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='agenda', verbose_name='Course')
    lesson_datetime = models.DateTimeField(default=datetime.datetime.now, verbose_name='Time')
    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='times', null=True)

    def students_count(self):
        if self.course:
            if self.course.course_class:
                if self.course.course_class.students:
                    return self.course.course_class.students.count()

        return None

    def date(self):
        if self.lesson_datetime is None:
            return f'Time id_{self.id}'

        return f'{self.lesson_datetime.strftime("%d.%m.%Y")}'

    def date_for_jurnal(self):
        t = self.lesson_datetime
        if t is None:
            return f'Time id_{self.id}'

        return f'{int(t.strftime("%d"))} {t.strftime("%b")}'

    def week_for_jurnal(self):
        t = self.lesson_datetime
        if t is None:
            return f'Time id_{self.id}'

        return f'{t.strftime("%a")}'

    def time(self):
        if self.lesson_datetime is None:
            return f'Time id_{self.id}'

        return f'{self.lesson_datetime.strftime("%H:%M")}'

    def __str__(self):
        if self.lesson_datetime is None:
            return f'Time id_{self.id}'

        return f'{self.lesson_datetime.strftime("%d %B (%a) %H:%M")}'


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)

    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')
    month_count = models.BigIntegerField(verbose_name='Month Count', null=True, blank=True)
    course_class = models.ForeignKey('Class', on_delete=models.SET_NULL,
                                     null=True, related_name='courses', verbose_name='Class')
    price = models.DecimalField(default=0, null=True, blank=True, verbose_name='Salary', max_digits=5, decimal_places=2)
    done = models.BooleanField(default=False, verbose_name='Done')

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', null=True)

    @property
    def salary(self):
        return f'{self.price:.2f} ₾' if self.price else '0.00 ₾'

    def __str__(self):
        if self.course_class is None or self.course_class.subject is None or self.month_count is None:
            return f'Course id_{self.id}'

        return f'{self.course_class.subject} N-{self.month_count}'


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)

    course_class = models.ForeignKey('Class', on_delete=models.CASCADE,
                                     null=True, blank=True, related_name='schedules', verbose_name='Class')

    class WeekDay(IntegerChoices):
        monday = 1, 'Monday'
        tuesday = 2, 'Tuesday'
        wednesday = 3, 'Wednesday'
        thursday = 4, 'Thursday'
        friday = 5, 'Friday'
        saturday = 6, 'Saturday'
        sunday = 0, 'Sunday'

    class DurationChoices(IntegerChoices):
        m15 = 15, '0:15'
        m30 = 30, '0:30'
        m45 = 45, '0:45'
        h1 = 60, '1:00'
        h1m15 = 75, '1:15'
        h1m30 = 90, '1:30'
        h1m45 = 105, '1:45'
        h2 = 120, '2:00'
        h2m15 = 135, '2:15'
        h2m30 = 150, '2:30'

    week_day = models.PositiveSmallIntegerField(default=WeekDay.monday, choices=WeekDay.choices)
    lesson_time = models.TimeField(default='12:00', verbose_name='Time')
    duration = models.PositiveSmallIntegerField(default=DurationChoices.h1, choices=DurationChoices.choices)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules', null=True)

    def week_day_enum(self):
        return self.WeekDay(self.week_day)

    def week_day_str(self):
        return self.WeekDay(self.week_day).label

    def duration_enum(self):
        return self.DurationChoices(self.duration)

    def duration_str(self):
        return self.DurationChoices(self.duration).label

    def lesson_end_time(self):
        minutes = self.lesson_time.hour * 60 + self.lesson_time.minute
        minutes += self.duration
        end_time = datetime.time(hour=(minutes // 60) % 24, minute=minutes % 60)

        return end_time

    def __str__(self):
        return f'{self.course_class} - {self.week_day_str()} {self.lesson_time.strftime("%H:%M")}'
