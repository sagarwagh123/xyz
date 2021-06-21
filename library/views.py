from django.shortcuts import render
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.core.mail import send_mail
from .models import booking
#from librarymanagement.settings import EMAIL_HOST_USER


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/index.html')


# for showing signup/login button for tenant
def tenantclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/tenantclick.html')


# for showing signup/login button for owner
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/adminclick.html')


def adminsignup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request, 'library/adminsignup.html', {'form': form})


def tenantsignup_view(request):
    form1 = forms.TenantUserForm()
    mydict = {'form1': form1}
    if request.method == 'POST':
        form1 = forms.TenantUserForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            my_tenant_group = Group.objects.get_or_create(name='TENANT')
            my_tenant_group[0].user_set.add(user)

        return HttpResponseRedirect('tenantlogin')
    return render(request, 'library/tenantsignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    else:
        return render(request, 'library/tenantafterlogin.html')


def bookProp(request):
    if request.method == "POST":
        usernames = request.POST.get('usernames')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ids = request.POST.get('ids')
        mobile = request.POST.get('mobile')
        # pid=request.POST.get('pid');
        # userid=request.user;
        bookings = booking(usernames=usernames, email=email,
                           address=address, ids=ids, mobile=mobile)
        bookings.save()
    return render(request, 'bookProp.html')


def myBooking(request):
    if request.method == "POST":
        ids = request.POST.get('ids')
        bookingSearchObj = booking.objects.raw(
            'select * from library_booking where ids="'+ids+'"')
        # propertySearchObj = property.objects.raw('select * from myapp_property where pk="'+pid+'"')
        return render(request, 'myBooking.html', {"booking": bookingSearchObj})


def SearchPage(request):
    # srh = request.GET['query']
    # properties = property.objects.filter(location__icontains=srh)
    # params = {'properties': properties, 'search':srh}
    # return render(request, 'search.html', params)
    if request.method == "POST":
        category = request.POST.get('category')
        Address = request.POST.get('Address')
        propertySearchObj = models.Property.objects.raw(
            'select * from library_Property where category="'+category+'" or Address = "'+Address+'"')
        return render(request, 'search.html', {"property": propertySearchObj})
    else:
        propertyObj = models.Property.objects.raw(
            'select * from library_Property')
        return render(request, 'search.html', {"property": propertyObj})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addProperty_view(request):
    # now it is empty property form for sending to html
    form = forms.PropertyForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'library/Propertyadded.html')
    return render(request, 'library/addProp.html', {'form': form})

# def viewProp(request):
#     items=property.objects.all()
#     return render(request,'viewProp.html',{'items':items})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewProperty_view(request):
    properties = models.Property.objects.all()
    return render(request, 'library/viewProperty.html', {'property': properties})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')
            obj.isbn = request.POST.get('isbn2')
            obj.save()
            return render(request, 'library/bookissued.html')
    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    for ib in issuedbooks:
        issdate = str(ib.issuedate.day)+'-' + \
            str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate = str(ib.expirydate.day)+'-' + \
            str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        # fine calculation
        days = (date.today()-ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*10

        books = list(models.Book.objects.filter(isbn=ib.isbn))
        students = list(models.StudentExtra.objects.filter(
            enrollment=ib.enrollment))
        i = 0
        for l in books:
            t = (students[i].get_name, students[i].enrollment,
                 books[i].name, books[i].author, issdate, expdate, fine)
            i = i+1
            li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})


@login_required(login_url='tenantlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook = models.IssuedBook.objects.filter(
        enrollment=student[0].enrollment)

    li1 = []

    li2 = []
    for ib in issuedbook:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t = (request.user, student[0].enrollment,
                 student[0].branch, book.name, book.author)
            li1.append(t)
        issdate = str(ib.issuedate.day)+'-' + \
            str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate = str(ib.expirydate.day)+'-' + \
            str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        # fine calculation
        days = (date.today()-ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*10
        t = (issdate, expdate, fine)
        li2.append(t)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})


def aboutus_view(request):
    return render(request, 'library/aboutus.html')


# def contactus_view(request):
#     sub = forms.ContactusForm()
#     if request.method == 'POST':
#         sub = forms.ContactusForm(request.POST)
#         if sub.is_valid():
#             email = sub.cleaned_data['Email']
#             name=sub.cleaned_data['Name']
#             message = sub.cleaned_data['Message']
#             send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently = False)
#             return render(request, 'library/contactussuccess.html')
#     return render(request, 'library/contactus.html', {'form':sub})
