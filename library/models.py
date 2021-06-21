from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)

    # used in issue book
    def __str__(self):
        return self.user.first_name + '[' + str(self.enrollment) + ']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Property(models.Model):
    catchoice= [
        ('Villa', 'Villa'),
        ('Bungalow', 'Bungalow'),
        ('Pg', 'Pg'),
        ('Apartments', 'Apartments'),
        ('Hostel', 'Hostel'),
        ]
    name=models.CharField(max_length=30)
    Phone_no=models.PositiveIntegerField()
    Address=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='Villa')
    propImage = models.ImageField(null=True, blank=True, upload_to='images/')
    price=models.IntegerField(max_length=30)
    def __str__(self):
        return str(self.name)+"["+str(self.Phone_no)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)

class booking(models.Model):
    usernames=models.CharField(max_length=500)
    email=models.CharField(max_length=122)
    address=models.CharField(max_length=122)
    ids=models.CharField(max_length=122)
    mobile=models.CharField(max_length=122)
   # date=models.DateField()
    #pid=models.CharField(max_length=500)
   # userid=models.CharField(max_length=100)
    def __str__(self):
        return self.usernames
        
# class IssuedBook(models.Model):
#     # moved this in forms.py
#     # enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
#     enrollment = models.CharField(max_length=30)
#     # isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
#     isbn = models.CharField(max_length=30)
#     issuedate = models.DateField(auto_now=True)
#     expirydate = models.DateField(default=get_expiry)
#
#     def __str__(self):
#         return self.enrollment


