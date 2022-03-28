from django.forms import ModelForm
from django import forms
from .models import Lesson, Student, Parent, Class, Subject, Time, Course, Schedule


class LessonForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4'}), required=False)

    class Meta:
        model = Lesson
        fields = ['description', 'student', 'time', 'done']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'last_name', 'phone_number', 'fb_link', 'discord_username', 'parent']


class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ['name', 'last_name', 'phone_number', 'fb_link']


class ClassForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4'}), required=False)

    class Meta:
        model = Class
        fields = ['title', 'description', 'subject', 'students', 'active']


class SubjectForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4'}), required=False)

    class Meta:
        model = Subject
        fields = ['title', 'description']


class TimeForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4'}), required=False)

    class Meta:
        model = Time
        fields = ['course', 'lesson_datetime', 'description']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['price', 'course_class', 'description', 'done']


class ScheduleForm(ModelForm):
    lesson_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Schedule
        fields = ['week_day', 'lesson_time', 'duration']

