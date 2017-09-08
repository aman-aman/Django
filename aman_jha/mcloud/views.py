from mcloud.models import Album
from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import View
from django.views import generic
from mcloud.models import Album,Song
from django.contrib.auth import authenticate,login,logout
from mcloud.form import UserForm


class IndexView(generic.ListView):
    template_name = 'mcloud/index.html'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'mcloud/detail.html'

class Albumcreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('mcloud:index')



def favorite(request,album_id):
    album = get_object_or_404(Album,pk=album_id)
    try:
         selected_song = album.song_set.get(pk=request.POST['song'])
    except(KeyError,Song.DoesNotExist()):
        return render(request,'mcloud/detail.html',{'album':album,'error_message':"you did not enter correct choice",})
    else:
        selected_song.is_favorite=True
        selected_song.save()
        return render(request,'mcloud/detail.html',{'album':album})

class UserFormView(View):
    form_class=UserForm
    template_name='mcloud/registrationform.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('mcloud:index')
        return render(request,self.template_name,{'form':form})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'mcloud/login.html', context)

def login_user(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    albums = Album.objects.filter(user=request.user)
                    return render(request, 'mcloud/index.html', {'albums': albums})
                else:
                    return render(request, 'mcloud/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'mcloud/login.html', {'error_message': 'Invalid login'})
        return render(request, 'mcloud/login.html')

def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'mcloud/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'mcloud/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
    })

#def index(request):
   # all_albums=Album.objects.all()
    #return render(request,'mcloud/index.html',{'all_albums':all_albums})

#22
#def detail(request,album_id):
 #   album=get_object_or_404(Album,pk=album_id)
  #  return render(request,'mcloud/detail.html',{'album':album})