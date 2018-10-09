from django.utils import timezone
from .models import Interest,Document,Rate,Follow,Community,Join,Advertise,Readpending,Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , authenticate,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm,InterestForm,DocumentForm,RatingForm,CommunityForm,AdvertiseForm,DocumentCForm,ProfileForm
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .filters import DocumentFilter,AdvertiseFilter
from django.contrib import messages

#view for the home page of the user,view is called by home url,returns to home.html 
@login_required
def home(request):
    documents = Document.objects.order_by('published_date').filter(user=request.user,searchshow=True)
    ads = Advertise.objects.order_by('published_date').filter(user=request.user)
    interest = Interest.objects.get(user=request.user)
    choices=['Fiction','LoveandRomance',"Mystery","Thriller","ScienceandFiction","Fantasy","Horror","ActionandAdventure","Comedy","Poetry","Study"]
    doc=Document.objects.order_by('published_date').filter(genre__in=interest.my_field,searchshow=True).exclude(user=request.user)
    Communities=Community.objects.all().exclude(admin=request.user)
    communities=[c for c in Communities]
    jpclist=map(lambda x:[x,x.jrequests.all()],communities)
    oCom=Community.objects.filter(admin=request.user)
    ocom=[c for c in oCom]
    opclist=map(lambda x:[x,x.jrequests.all().count()],ocom)
    jcom=Join.objects.get(user=request.user).jlist.all()
    readreq=Readpending.objects.filter(user=request.user)
    rplist=map(lambda x:[x.doc,x.rplist.all()],readreq)
    return render(request, 'home.html',{'documents': documents,'ads':ads,'interest':interest,'doc':doc,'jpclist':jpclist,'jcom':jcom,'opclist':opclist,'rplist':rplist,'choices':choices})

#view for the signup page for a new user,view is called by signup url,returns to signup.html
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Interest.objects.create(user=user,my_field=['Fiction','Study','Comedy','Thriller','ScienceandFiction'])
            Follow.objects.create(user=user)
            Profile.objects.create(user=user)
            Join.objects.create(user=user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#view to edit profile of a user,view is called by editprofile url,returns to editprofile.html 
def editprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email=form.cleaned_data.get('email',None)
            request.user.first_name=form.cleaned_data.get('first_name',None)
            request.user.last_name=form.cleaned_data.get('last_name',None)
            request.user.save()
            return redirect('settings')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'editprofile.html', {'form': form})

#view to edit interets of a user,view is called by interests url,returns to interests.html 
def interests(request):
    if request.method == "POST":
        form = InterestForm(request.POST,instance=request.user.interest)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = InterestForm(instance=request.user.interest)
    return render(request, 'interests.html', {'form': form})

#view to upload document,view is called by upfile url,returns to model_form_upload.html 
def upfile(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user=request.user
            post.uploader = request.user.username.encode('ascii','ignore')
            post.published_date = timezone.now()
            post.save()
            Readpending.objects.create(user=request.user,doc=post)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {'form': form})

#view for settings page,view is called by settings url,returns to settings.html
def settings(request):
    return render(request,'settings.html')

#brief view for search page,view is called by search url,returns to search.html
def search(request):
    Document_list = Document.objects.all()
    Document_filter = DocumentFilter(request.POST, queryset=Document_list)   
    if request.method == 'POST':
        le=Document_list.count()
        return render(request, 'search.html', {'filter': Document_filter,'le':le})
    else:
        return render(request, 'search.html',{'filter': Document_filter,'le':0})

##view to delete a book. This view is called by delete url, returns to home.html
def delete1(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    doc.delete()
    return redirect('home')

#view for book page,view is called by bookpage url, returns to bookpage.html
def bookpage(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    mlist=doc.rmembers.all()
    if(doc.searchshow):
        rplist=Readpending.objects.get(doc=doc).rplist.all()
    else:
        rplist=[]
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            r = Rate.objects.filter(doc=doc,user=request.user)
            if not r:
                r=Rate.objects.create(user=request.user, doc=doc, rating=form.cleaned_data.get('rating',None))
            r=Rate.objects.get(doc=doc,user=request.user)
            r.rating=form.cleaned_data.get('rating',None)
            r.save()
            tr=list(Rate.objects.filter(doc=doc).values_list('rating',flat=True))
            if tr!=[]:
                r1=float(sum(tr))/float(len(tr))
                t=len(tr)
                d1=Document.objects.get(document=doc.document)
                d1.rating=r1
                d1.no_ratings=t
                d1.save()
            else:
                r1=0
                t=0
                doc.rating=r1
                doc.no_ratings=t
                doc.save()
            return render(request,'bookpage.html',{'doc':doc,'form':form,'r':r,'r1':round(r1,2),'t':t,'user':request.user,'mlist':mlist,'rplist':rplist})
    else:
        form = RatingForm()
        tr=list(Rate.objects.filter(doc=doc).values_list('rating',flat=True))
        if tr!=[]:
            r1=float(sum(tr))/float(len(tr))
            t=len(tr)
            doc.rating=r1
            doc.no_ratings=t
            doc.save()
        else:
            r1=0
            t=0
            doc.rating=r1
            doc.no_ratings=t 
            doc.save() 
    return render(request,'bookpage.html',{'doc':doc,'form':form,'r1':round(r1,2),'t':t,'mlist':mlist,'rplist':rplist})

#view to edit profile of a user view is called by reset url returns to change_password.html 
def reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

#view for genre page,view is called by genre url,returns to genre.html
def genre(request,pk):
    documents=Document.objects.filter(genre=pk,searchshow=True)
    return render(request,'genre.html',{'docs':documents})

#view for author page,view is called by author url,returns to author.html
def author(request,pk):
    documents=Document.objects.filter(author=pk,searchshow=True)
    return render(request,'author.html',{'docs':documents})

#view for uploader page,view is called by uploader url,returns to uploader.html
def uploader(request,pk):
    documents=Document.objects.filter(uploader=pk,searchshow=True)
    u=documents.first().user
    f=Follow.objects.get(user=request.user).flist.all()
    if u in f:
        s=1
    else:
        s=0
    return render(request,'uploader.html',{'docs':documents,'s':s,'pk':pk})
