from django.http import Http404
from django.shortcuts import render
#from django.template import loader
from .models import Album, Song
# Create your views here.
#################

from django.http import HttpResponse

def index(request):
    all_albums = Album.objects.all()
    #template =  loader.get_template('music/index.html')
    context = {'all_albums' :all_albums}
    #return HttpResponse(template.render(context, request))
    return render(request, 'music/index.html', context)

def detail(request, album_id):
    #return HttpResponse("<h2>Details for Album id: " + str(album_id) + "</h2>")
    #album = get_obect_or_404(Album, pk=album_id)

    try:
        album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist")
    return render(request, 'music/details.html', {'album' :album})

def favorite(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist")
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except(KeyError, Song.DoesNotExist):
        return render(request, 'music/details.html', {'album' :album,
        'error_message': "You did not selet a valid song",})
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/details.html', {'album' :album})
