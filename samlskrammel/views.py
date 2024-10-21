#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CreateUserForm, LoginForm, CreatePostForm, TilfoejVen
from django.contrib.auth.models import User
from .models import Post, Friend
from django.utils import timezone
from django.db.models import Sum

def login(request):
  if request.method=="POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      m = User.objects.get(username=form.cleaned_data["your_name"])
      if m.check_password(form.cleaned_data["your_pass"]):
        request.session["member_id"] = m.id
        return render(request,'message.html',{'message': 'Velkommen '+form.cleaned_data["your_name"],
                                              'dest': '/samlskrammel/',
                                              'user': m.username})
      else:
        return render(request,'submitform.html', {'form': form,
                                                  'dest': '/samlskrammel/log-på',
                                                  'title': 'Log på',
                                                  'error': 'Kodeord passer ikke!',
                                                  'user': None})
    else:
      return render(request,'submitform.html', {'form': form,
                                                'dest': '/samlskrammel/log-på',
                                                'title': 'Log på',
                                                'error': 'Brugernavn ikke oprettet!',
                                                'user': None})
  else:
    form=LoginForm()
    return render(request,'submitform.html', {'form': form,
                                              'dest': '/samlskrammel/log-på',
                                              'title': 'Log på',
                                              'user': None})

def logout(request):
  try:
    del request.session["member_id"]
  except KeyError:
    pass
  return render(request,'message.html',{'message': 'Du er nu logget ud.\nPå gensyn!',
                                        'dest': '/samlskrammel/',
                                        'user': None})

def opret_bruger(request):
  if request.method=="POST":
    form = CreateUserForm(request.POST)
    if form.is_valid():
# Test if user exists
      if User.objects.filter(username=form.cleaned_data["your_name"]).exists():
        return render(request,'createuser.html', {'form': form,
                                                  'error': 'User Exists!',
                                                  'user': None})
      if User.objects.filter(email=form.cleaned_data["your_email"]).exists():
        return render(request,'createuser.html', {'form': form,
                                                  'error': 'Email anready in use!',
                                                  'user': None})
      u=User.objects.create_user(form.cleaned_data["your_name"],form.cleaned_data["your_email"],form.cleaned_data["your_pass"])
      u.save()
      request.session["member_id"] = u.id
      return render(request,'message.html',{'message': 'Bruger '+form.cleaned_data["your_name"]+' oprettet.',
                                            'dest': '/samlskrammel/',
                                            'user': None})
    else:
      return render(request,'createuser.html', {'form': form,
                                                'error': 'Error in form!',
                                                'user': None})
  else:
    form=CreateUserForm()
    return render(request,'createuser.html', {'form': form,
                                              'user': None})

def opret_oplaeg(request):
  # Test if logged in and valid user
  if not request.session.has_key('member_id'):
    return render(request,'userprofile.html',{'user': None})
  if not User.objects.filter(id=request.session["member_id"]).exists():
    return render(request,'userprofile.html',{'user': None, 'error': 'Session afsluttet.'})
  u=User.objects.get(id=request.session["member_id"])
  if request.method!="POST":
    form=CreatePostForm()
    return render(request,'createpost.html', {'form': form,
                                              'user': u})
  else:
    form = CreatePostForm(request.POST,request.FILES)
    if not form.is_valid():
      return render(request,'createpost.html', {'form': form,
                                                'error': 'Fejl i post',
                                                'user': u})
    else:
      post=Post(myWhat=form.cleaned_data["field_what"],
                myWeight=form.cleaned_data["field_weight"],
                myWhen=timezone.now(),
                myWhereLat=form.cleaned_data["field_lat"],
                myWhereLon=form.cleaned_data["field_lon"],
                myImage=form.cleaned_data["field_image"],
                myOwner=u)
      post.save()
      return render(request,'message.html',{'message': 'Post oprettet.',
                                            'dest': '/samlskrammel/',
                                            'user': u})

def tilfoej_ven(request):
  if not request.session.has_key('member_id'):
    return render(request,'userprofile.html',{'user': None})
  if not User.objects.filter(id=request.session["member_id"]).exists():
    return render(request,'userprofile.html',{'user': None, 'error': 'Session afsluttet.'})
  u=User.objects.get(id=request.session["member_id"])
  if request.method!="POST":
    form=TilfoejVen()
    return render(request,'submitform.html', {'form': form,
                                              'dest': '/samlskrammel/tilføj-ven',
                                              'title': 'Tilføj ven',
                                              'user': u})
  else:
    form = TilfoejVen(request.POST,request.FILES)
    if not form.is_valid():
      return render(request,'submitform.html', {'form': form,
                                                'dest': '/samlskrammel/tilføj-ven',
                                                'title': 'Tilføj ven',
                                                'error': 'Fejl i input',
                                                'user': u})
    if not User.objects.filter(username=form.cleaned_data["friend_name"]).exists():
      return render(request,'submitform.html', {'form': form,
                                                'dest': '/samlskrammel/tilføj-ven',
                                                'title': 'Tilføj ven',
                                                'error': 'Kunne ikke finde brugeren '+str(form.cleaned_data["friend_name"]),
                                                'user': u})
    ven=User.objects.get(username=form.cleaned_data["friend_name"])
    if Friend.objects.filter(myOwner=u, myFriend=ven).exists():
      return render(request,'submitform.html', {'form': form,
                                                'dest': '/samlskrammel/tilføj-ven',
                                                'title': 'Tilføj ven',
                                                'error': str(form.cleaned_data["friend_name"])+' er allerede i din venneliste',
                                                'user': u})
    venskab=Friend(myFriend=ven,myOwner=u)
    venskab.save()
    return render(request,'message.html',{'message': str(form.cleaned_data["friend_name"])+' er nu i din venneliste.',
                                          'dest': '/samlskrammel/',
                                          'user': u})

def index(request):
  if not request.session.has_key('member_id'):
    return render(request,'userprofile.html',{'user': None})
  if not User.objects.filter(id=request.session["member_id"]).exists():
    return render(request,'userprofile.html',{'user': None, 'error': 'Session afsluttet.'})
  u=User.objects.get(id=request.session["member_id"])
  venner=Friend.objects.filter(myOwner=u).values('myFriend')
  return render(request,'userprofile.html',{'user': u.username,
                                            'friends': Post.objects.filter(myOwner__in=venner).values('myOwner__username').annotate(collected=Sum('myWeight')).order_by('-collected')[:10],
                                            'posts': Post.objects.filter(myOwner=u).order_by('-myWhen')[:5]})
