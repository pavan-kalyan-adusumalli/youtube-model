from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount
from .models import *
from django import forms
from .forms import AddChannelForm, AddVideoForm
from datetime import date
import re
# Create your views here.
def emptyview(request):
    return HttpResponseRedirect(reverse("index"))

def supplyVideos(request):
    videos = Video.objects.all()
    videolist = []
    start = int(request.GET.get("start")) or 0
    end = int(request.GET.get('end')) or start+9

    for i in range(start-1, end):
        videolist.append(videos[i])
    
    return JsonResponse({"videos":videolist})

def index(request):
    videos = Video.objects.all()
    if(request.user.is_authenticated):
        usersobjects = ytusers.objects.all()
        userslist = [user.username for user in usersobjects]
        '''print(userslist)
        print(type(request.user.username))  
        print(request.user.username in userslist)'''
        social_info = SocialAccount.objects.filter(user=request.user)
        '''print(social_info)
        print(social_info[0].extra_data)
        print(social_info[0].extra_data['name'])'''
        userpic = social_info[0].extra_data['picture']
        #print(userpic)
        if(request.user.username not in userslist):
        #create a user object if he is authenticating for the first  time
            newuser = ytusers(username=request.user, userpicture=userpic)
            #print(newuser.username)
            newuser.save()

            likedPlaylist = Playlist(playlistname='Liked videos', private=True, owner = newuser)
            likedPlaylist.save()

        
        cur_user_obj = ytusers.objects.get(username=request.user.username)
        user_channel = cur_user_obj.userchannels.all().first()
        #user_channel = Channel.objects.filter(owner=cur_user_obj).first()
        #print('userchannel is',user_channel)
        

        #data=SocialAccount.objects.get(user=request.user).uid
        #print(data.get("id"))
        #print(users.objects.all())
        #print(request.provider)
        #print(request.user.socialaccount_set.all.extra_data.username)
        userplaylists = Playlist.objects.filter(owner=cur_user_obj)
        return render(request, 'videos/index.html', {'userplaylists':userplaylists, 'extradata':social_info[0].extra_data, 'userchannel':user_channel, 'videos':reversed(videos)})
    else:
        return render(request, "videos/index.html", {'videos': reversed(videos)})

def subscriptions(request):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        subscription_videos = []
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        subs = cur_user_obj.subscriptions.all()
        for channel in subs:
            for video in channel.videos.all():
                subscription_videos.append(video)
        return render(request, 'videos/index.html', {'videos':subscription_videos, 'extradata':social_info[0].extra_data, 'userchannel':cur_user_obj.userchannels.first()})

    else:
        return render(request, 'videos/error.html', {'message': 'You need to login to see this', 'info':'Use the login button to login'})

def watch(request, vid, pid=0, wid=0):
    playlistobj = None
    if(pid):
        playlistobj = Playlist.objects.filter(id=pid).first()
        #print('playlist videos', playlistobj.videoname.all())
        playlistvideos = playlistobj.videoname.all()
    #watchlater
    elif(wid):
        playlistobj = WatchLater.objects.filter(id=wid).first()
        #print('playlist videos', playlistobj.videos.all())
        playlistvideos = playlistobj.videos.all()
    else:
        playlistvideos = []

    video = Video.objects.get(id=vid)
    likes = video.like.count()
    dislike = video.dislikes.count()
    comments = video.comment.all()
    if(request.user.is_authenticated):
        video.views += 1
        video.save()
        #get the user
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        subscribedchannels = cur_user_obj.subscriptions.all()
        suggestedlist = [videoobj for videoobj in Video.objects.exclude(id=video.id) if(videoobj.uploadedchannel in subscribedchannels)]
        
        #print('subscriptions',cur_user_obj.subscriptions.all())
        user_channel = cur_user_obj.userchannels.first()
        #  subscription check  #
        subscribed=False #let initially subscribe=False
        #cur_channel_obj = video.uploadedchannel
        #channelsubs = cur_channel_obj.subs (lets write it in direct method)
        channelsubs = video.uploadedchannel.subs.all()
        if(cur_user_obj in channelsubs):
            subscribed = True
        #   end of subscription check   #

        watchedvideos = cur_user_obj.watchedVideos.all()
        if(video in watchedvideos):
            cur_user_obj.watchedVideos.remove(video)
        video.watchHistory.set([cur_user_obj])
        video.save()
        social_info = SocialAccount.objects.filter(user=request.user)
        userplaylists = Playlist.objects.filter(owner=cur_user_obj)
        return render(request, "videos/watch.html", {'channelinfo':video.uploadedchannel, 'userplaylists':userplaylists, 'playlistobj':playlistobj, 'playlistvideos':playlistvideos, 'subvideos':suggestedlist, 'suggestions':Video.objects.exclude(id=vid), 'userchannel':user_channel, 'liked': cur_user_obj in video.like.all(), 'disliked':cur_user_obj in video.dislikes.all(), 'likescount':likes, 'dislikescount':dislike, "video":video, "comments":comments, "extradata":social_info[0].extra_data, 'noofcomments':len(comments), 'subscribed':subscribed})
    return render(request, "videos/watch.html", {'playlistobj':playlistobj, 'playlistvideos':playlistvideos, 'suggestions':Video.objects.exclude(id=vid), 'likescount':likes, 'dislikescount':dislike, "video":video, "comments":comments, 'noofcomments':len(comments)})

    
def watchhistory(request):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        
        cur_user_obj = ytusers.objects.get(username=request.user.username)
        feed=cur_user_obj.watchedVideos.all()
        reversedfeed = reversed(feed)
        return render(request, 'videos/history.html', {'extradata':social_info[0].extra_data, 'feed':reversedfeed, 'userchannel':cur_user_obj.userchannels.first()})
    return render(request, 'videos/history.html')

def removeFromHistory(request):
    if(request.user.is_authenticated):
        videoid = request.GET.get('videoid')
        videoobj = Video.objects.filter(id=videoid).first()
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        videoobj.watchHistory.remove(cur_user_obj)
        videoobj.save()
        return JsonResponse({"historystatus":'removed'})
    else:
        return render(request, 'videos/error.html', {'message':'You should login to do this', "info":'Use signin button to login'})

def viewprofile(request, username):
    return(render(request, "videos/userprofile.html"))

def profile(request):
    return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    return HttpResponseRedirect(reverse("logout"))


def category(request, category):
    videos = Video.objects.filter(category=category)
    if(request.user.is_authenticated):
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        social_info = SocialAccount.objects.filter(user=request.user)
        return render(request, 'videos/more.html', {'videos':videos,     'extradata':social_info[0].extra_data, 'category':category, 'userchannel':cur_user_obj.userchannels.first()})
    
    return(render(request, 'videos/more.html',{'category':category, 'videos':videos}))

def channel(request, channelid):
    cur_channel_obj = Channel.objects.filter(id=channelid).first()
    subscount = len(cur_channel_obj.subs.all())
    channelvideos = cur_channel_obj.videos.all()
    channelplaylists = Playlist.objects.filter(channelname = cur_channel_obj)
    subscribed = False

    totalviews = 0
    for video in list(channelvideos):
        totalviews += video.views
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        
        if(cur_user_obj in cur_channel_obj.subs.all()):
            subscribed = True
        return render(request, 'videos/channel.html', {'userchannel':cur_user_obj, 'subscribed':subscribed, 'totalviews':totalviews, 'extradata': social_info[0].extra_data, 'playlists':channelplaylists, 'channelinfo':cur_channel_obj, 'subscount':subscount, 'channelvideos':channelvideos})
    return render(request, 'videos/channel.html', {'subscribed':subscribed, 'totalviews':totalviews,'playlists':channelplaylists, 'channelinfo':cur_channel_obj, 'subscount':subscount, 'channelvideos':channelvideos})

def showplaylist(request,id=None, List=None):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        userchannel = cur_user_obj.userchannels.first()
    if(id is None and List=='wl'):#wl for watchlater
        if(request.user.is_authenticated):
            requestedPlaylist = WatchLater.objects.filter(owner=cur_user_obj).first()
            if(requestedPlaylist):
                playlistvideos = requestedPlaylist.videos.all()
                playlistvideoscount = requestedPlaylist.videos.count()
                return render(request, 'videos/playlist.html', {'extradata': social_info[0].extra_data, 'watchlaterid':requestedPlaylist.id, 'playlist':requestedPlaylist, 'playlistvideos':playlistvideos, 'videoscount':playlistvideoscount, 'firstvideo':playlistvideos[0], 'userchannel' : cur_user_obj.userchannels.first(), 'userchannel':userchannel})
            return render(request, 'videos/error.html', {'message':'You have no videos in your watch later', 'info':'Try to add some'})
        else:
            return render(request, 'videos/error.html', {'message':'You should login to see this'})

    if(id is None and List=='likedvideos'):
        if(request.user.is_authenticated):
            requestedPlaylist = Playlist.objects.filter(playlistname='Liked videos', owner = cur_user_obj).first()
            playlistvideos = requestedPlaylist.videoname.all()
            playlistvideoscount = requestedPlaylist.videoname.count()
            if(playlistvideos):
                return render(request, 'videos/playlist.html', {'extradata': social_info[0].extra_data, 'playlist':requestedPlaylist, 'playlistvideos':playlistvideos, 'videoscount':playlistvideoscount, 'firstvideo':playlistvideos[0], 'userchannel' : cur_user_obj.userchannels.first(), 'userchannel':userchannel})
            else:
                return render(request, 'videos/playlist.html', {'extradata': social_info[0].extra_data, 'playlist':requestedPlaylist, 'videoscount':playlistvideoscount, 'userchannel':userchannel})
        else:
            return render(request, 'videos/error.html', {'message':'You should login to see this'})
    #get the playlist info
    #print(id)
    requestedPlaylist = Playlist.objects.filter(id=id).first()
    if( not requestedPlaylist):
        return HttpResponse('<h2>No such playlist exists</h2>')
    #print(requestedPlaylist)
    playlistvideos = list(requestedPlaylist.videoname.all())
    #print(playlistvideos)
    playlistvideoscount = requestedPlaylist.videoname.count()
    
    if(request.user.is_authenticated):
        print(requestedPlaylist in cur_user_obj.playlists.all())
        #if(requestedPlaylist.owner is cur_user_obj):
        if(requestedPlaylist in cur_user_obj.playlists.all()):
            return render(request, 'videos/playlist.html', {'userplaylists':cur_user_obj.playlists.all(), 'owner':'true', 'playlist':requestedPlaylist, 'playlistvideos':playlistvideos, 'videoscount':playlistvideoscount, 'firstvideo':playlistvideos[0], 'extradata': social_info[0].extra_data, 'userchannel':userchannel})
        return render(request, 'videos/playlist.html', {'userplaylists':cur_user_obj.playlists.all(), 'playlist':requestedPlaylist, 'playlistvideos':playlistvideos, 'videoscount':playlistvideoscount, 'firstvideo':playlistvideos[0], 'extradata': social_info[0].extra_data, 'userchannel':userchannel})
    else:
        return render(request, 'videos/playlist.html', {'playlist':requestedPlaylist, 'playlistvideos':playlistvideos, 'videoscount':playlistvideoscount, 'firstvideo':playlistvideos[0]})

def createChannel(request):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        return render(request, 'videos/createChannel.html', {'extradata':social_info[0].extra_data})

def channelSetup(request):
    #get the post data
    channelname = request.POST.get('customChannelName')
    user = ytusers.objects.filter(username=request.user.username).first()
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        form = AddChannelForm()
        if(channelname):
            return render(request, 'videos/channelsetup.html', {'extradata':social_info[0].extra_data, 'form':form, 'ChannelName':channelname, 'curuser':user})
        return render(request, 'videos/channelsetup.html', {'extradata':social_info[0].extra_data, 'form':form, 'ChannelName':social_info[0].extra_data.get('name'), 'curuser':user})

def mychannel(request):
    if(not request.user.is_authenticated):
        return(render(request, 'videos/error.html', {'message':"You should sign in to see this", 'info':'Use signin Button to login'}))
    if(request.method=='POST'):
        channelname = request.POST.get('channelname')
        #print(request.POST.get('channelpicture'))
        form = AddChannelForm(request.POST, request.FILES)
        print(form.errors)

        if(form.is_valid()):
            form.save()
        
    #channel object is saved now get the channel object and return it to template
    social_info = SocialAccount.objects.filter(user=request.user)
    cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
    cur_channel_obj = cur_user_obj.userchannels.all().first()
    subscount = len(cur_channel_obj.subs.all())
    channelvideos = cur_channel_obj.videos.all()
    totalviews = 0
    for video in list(channelvideos):
        totalviews += video.views
    channelplaylists = Playlist.objects.filter(channelname = cur_channel_obj)
    return render(request, 'videos/mychannel1.html', { 'totalviews':totalviews, 'extradata': social_info[0].extra_data, 'channelinfo':cur_channel_obj, 'subscount':subscount,'playlists':channelplaylists,'userplaylists':channelplaylists, 'channelvideos':channelvideos, 'userchannel':cur_channel_obj})

def addvideo(request):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        form = AddVideoForm()
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        channel = cur_user_obj.userchannels.all().first()
        playlists = Playlist.objects.filter(channelname=channel)
        #print(channel)
        if(channel is None):
            return render(request, 'videos/error.html', {'message': 'You need to create a channel to see this'})
        return render(request, 'videos/addvideo.html', {'extradata':social_info[0].extra_data, 'videoform':form, 'channel':channel, 'playlists':playlists, 'userchannel':channel})
    return render(request, 'videos/error.html', {'message':'You should signin to see this', 'info':'Use signin Button to login'})

def uploadvideo(request):
    if(request.method=='POST'):
        #print(request.POST.get('recording'))
        form = AddVideoForm(request.POST, request.FILES)
        
        if(form.is_valid()):
            #print('form is valid')
            form.save()
            playlistid = request.POST.get("playlist")
            if(playlistid):
                #print('uploaded channel and videoname',form.data['uploadedchannel'], form.data['videoname'])
                uploadedchannelid = form.data['uploadedchannel']
                uploadedchannel = Channel.objects.get(id=uploadedchannelid)
                videos = uploadedchannel.videos.all()
                #print(videos.last())
                playlist = Playlist.objects.get(id=playlistid)
                playlist.videoname.add(videos.last())
                playlist.save()
            return HttpResponseRedirect(reverse('index'))
        print(form.data)
        print(form.errors)
        return HttpResponse('form is not valid')



def subscribe(request):
    if(request.user.is_authenticated):
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        channelid = int(request.GET.get('channelid')) or None
        #print('channelid', channelid)
        if(channelid):
            channel_obj = Channel.objects.get(id=channelid)
            channel_obj.subs.add(cur_user_obj)
            channel_obj.save()
            return JsonResponse({"subscriptionStatus":'true'})
        return JsonResponse({"subscriptionStatus":'false'})
    return JsonResponse({"subscriptionStatus":'loggedout'})

def unsubscribe(request):
    if(request.user.is_authenticated):
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        channelid = int(request.GET.get('channelid')) or None
        #print('channelid', channelid)
        if(channelid):
            channel_obj = Channel.objects.get(id=channelid)
            channel_obj.subs.remove(cur_user_obj)
            channel_obj.save()
            return JsonResponse({"unsubscriptionStatus":'true'})
        return JsonResponse({"unsubscriptionStatus":'false'})
    return JsonResponse({"unsubscriptionStatus":'loggedout'})

def addcomment(request):
    if(request.user.is_authenticated):
        vid = int(request.GET.get('videoid'))
        user = ytusers.objects.filter(username=request.user.username).first()
        video = Video.objects.filter(id=vid).first()
        
        #create comment and save
        comment = request.GET.get("content")
        d=date.today()
        cmnt = Comment(content=comment, owner=user, videoname=video, date=d)
        cmnt.save()
        #print(user.username, user.userpicture, comment, d)
        return JsonResponse({'commentStatus':'true', "commentatorname":user.username, 'commentatorpic':user.userpicture, 'commentcontent':comment, 'commenteddate':d})
    else:
        return JsonResponse({"commentStatus":'loggedout'})

def likevideo(request):
    if(request.user.is_authenticated):
        vid = int(request.GET.get("videoid"))
        video = Video.objects.filter(id=vid).first()
        user = ytusers.objects.filter(username=request.user.username).first()
        likedvideosPlaylist = Playlist.objects.filter(owner=user, playlistname='Liked videos').first()
        likedusers = video.like.all()
        dislikedusers = video.dislikes.all()
        if(user in dislikedusers):
            video.dislikes.remove(user)
            video.save()
        
        if(user in likedusers):
            video.like.remove(user)
            video.save()
            return JsonResponse({"likestatus":'removedlike', 'likescount':video.like.count()})
        else:
            video.like.add(user)
            video.save()
            likedvideosPlaylist.videoname.add(video)#add to liked video playlist
            likedvideosPlaylist.save()
            

            return JsonResponse({"likestatus":"addedlike", 'likescount':video.like.count(), "dislikescount":video.dislikes.count()})
    return JsonResponse({"likestatus":'loggedout'})

def dislikevideo(request):
    if(request.user.is_authenticated):
        vid = int(request.GET.get("videoid"))
        video = Video.objects.filter(id=vid).first()
        user = ytusers.objects.filter(username=request.user.username).first()
        likedvideosPlaylist = Playlist.objects.filter(owner=user, playlistname='Liked videos').first()
        dislikedusers = video.dislikes.all()
        likedusers = video.like.all()
        if(user in likedusers):
            video.like.remove(user)
            video.save()
        
        if(user in dislikedusers):
            video.dislikes.remove(user)
            video.save()
            return JsonResponse({"likestatus":'removeddislike', "dislikescount":video.dislikes.count()})
        else:
            video.dislikes.add(user)
            video.save()    
            likedvideosPlaylist.videoname.remove(video)#remove from liked videos
            likedvideosPlaylist.save()
            return JsonResponse({"dislikestatus":"addeddislike", "dislikescount":video.dislikes.count(), 'likescount':video.like.count()})
    return JsonResponse({"dislikestatus":'loggedout'})

def createPlaylist(request):
    if(request.user.is_authenticated):
        
        playlistname = request.GET.get("name")
        cbox = request.GET.get("cbox")
        privacy = False
        if(cbox == 'true'):
            privacy = True
        channelid = request.GET.get('channelid')
        if(channelid and playlistname):
            channel = Channel.objects.get(id=channelid)
            owner = ytusers.objects.filter(username=request.user.username).first()
            newplaylist = Playlist(playlistname=playlistname, private=privacy, owner = owner, channelname = channel)
            newplaylist.save()
            return JsonResponse({"playlist":'true', 'playlistid':newplaylist.id})
        else:
            return JsonResponse({"playlist":'false'})
    else:
        return JsonResponse({"playlist":'loggedout'})

def watchlater(request):
    if(request.user.is_authenticated):
        videoid = request.GET.get("videoid")
        if(not videoid):
            return JsonResponse({'status':'false'})
        cur_video_obj = Video.objects.filter(id=videoid).first()
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        watchlaterobj = WatchLater.objects.filter(owner = cur_user_obj).first()
        if(watchlaterobj is None):
            newwatchlaterobj = WatchLater(owner = cur_user_obj)
            newwatchlaterobj.save()
            if(cur_video_obj in newwatchlaterobj.videos.all()):
                return JsonResponse({'status':'true'})
            else:
                newwatchlaterobj.videos.add(cur_video_obj)
                newwatchlaterobj.save()
                return JsonResponse({"status":'true'})
        else:
            watchlaterobj.videos.add(cur_video_obj)
            watchlaterobj.save()
            return JsonResponse({"status":'true'})
    else:
        return JsonResponse({"status":'loggedout'})

def removefromwatchlater(request):
    if(request.user.is_authenticated):
        vid = request.GET.get('videoid')
        wid = request.GET.get("wid")
        videoobj = Video.objects.get(id=vid)
        watchlaterobj = WatchLater.objects.get(id=wid)
        if(videoobj in watchlaterobj.videos.all()):
            watchlaterobj.videos.remove(videoobj)
            watchlaterobj.save()
            return JsonResponse({'status':'true'})
    else:
        return JsonResponse({"status":'loggedout'})

def savetoplaylists(request):
    if(request.method == 'POST'):
        checkedones = request.POST.getlist('playlists')
        videoid = request.POST.get("videoid")
        #print('videoid is', videoid)
        for id in checkedones:
            #print(id)
            playlistobj = Playlist.objects.filter(id=id).first()
            #print(playlistobj)
            playlistobj.videoname.add(videoid)
            playlistobj.save()
        return render(request, 'videos/playlistadd.html')

def searchforvideo(request):
    text = request.GET.get('text')
    if(text):
        relatedlist = [i.videoname for i in Video.objects.all() if re.search(f"\A{text.lower()}",i.videoname.lower())]
        #print(relatedlist)
        return JsonResponse({"relatedresults":relatedlist})
    return JsonResponse({"relatedresults":'[]'})
    return HttpResponse(relatedlist)

def search(request):
    searchedText = request.POST.get('searchedtext')
    relatedvideos = list(Video.objects.filter(videoname=searchedText))
    relatedchannels = list(Channel.objects.filter(channelname=searchedText))
    morerelatedvideos = [i for i in Video.objects.all() if i not in relatedvideos and searchedText.lower() in i.videoname.lower()]
    morerelatedchannels = [i for i in Channel.objects.all() if i not in relatedchannels and searchedText.lower() in i.channelname.lower()]
    relatedvideos += morerelatedvideos
    relatedchannels += morerelatedchannels
    #print(relatedvideos)
    if(request.user.is_authenticated):
        cur_user_obj = ytusers.objects.filter(username=request.user.username).first()
        userplaylists = list(Playlist.objects.filter(owner=cur_user_obj))
        return render(request, 'videos/search.html', {'searchedtext':searchedText, 'videos':relatedvideos, 'channels':relatedchannels, 'userplaylists':userplaylists, 'userchannel':cur_user_obj.userchannels.first()})
        
    return render(request, 'videos/search.html', {'searchedtext':searchedText, 'videos':relatedvideos, 'channels':relatedchannels,})

def customize(request, channelid):
    if(request.user.is_authenticated):
        channel_obj = Channel.objects.get(id=channelid)
        if(request.method == 'POST'):
            #channelpic = request.POST.get('channelpicture')
            #coverpic = request.POST.get('coverpic')
            desc = request.POST.get('description')    
            form = AddChannelForm(request.POST, request.FILES, instance=channel_obj)
            if(form.is_valid):
                #print(form.data)
                form.save()
                #print(request.FILES)
            return HttpResponseRedirect(reverse('mychannel'))
        else:
            user = ytusers.objects.filter(username=request.user.username).first()
            social_info = SocialAccount.objects.filter(user=request.user)
            
            channelname = channel_obj.channelname
            form = AddChannelForm(instance = channel_obj)
            if(channelname):
                return render(request, 'videos/channelsetup.html', {'customizing':True, 'extradata':social_info[0].extra_data, 'form':form, 'ChannelName':channelname, 'channelobj':channel_obj, 'curuser':user})
            #return render(request, 'videos/channelsetup.html', {'extradata':social_info[0].extra_data, 'form':form, 'ChannelName':social_info[0].extra_data.get('name'), 'curuser':user})
    else:
        return render(request, 'videos/error.html', {'message':'You should log in to see this'})

def removeFromPlaylist(request):
    if(request.user.is_authenticated):
        pid = request.GET.get("pid")
        videoid = request.GET.get('videoid')
        if(pid and videoid):
            cur_playlist = Playlist.objects.get(id=pid)
            cur_video_obj = Video.objects.get(id=videoid)

            cur_playlist.videoname.remove(cur_video_obj)
            cur_playlist.save()
            return JsonResponse({"status":'removed'})
        return JsonResponse({"status":'false'})
    return JsonResponse({"status": 'loggedout'})