from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.emptyview),
    path("youtube/", views.index, name='index'),

    path("youtube/watch/video=<int:vid>",views.watch,name='watch'),
    path("youtube/watch/video=<int:vid>&playlist=<int:pid>",views.watch,name='watchPlaylist'),
    path("youtube/watch/video=<int:vid>&watchlater=<int:wid>", views.watch, name='watchlater'),

    path("youtube/feed/history", views.watchhistory, name='watchhistory'),
    path("youtube/profile/<str:username>", views.viewprofile, name='profile'),
    path('accounts/profile/', views.profile),
    path("trending/<str:category>", views.category, name='category'),
    path("youtube/channel/<int:channelid>", views.channel, name='channel'),
    path("youtube/mychannel", views.mychannel, name='mychannel'),
    path("youtube/create_channel", views.createChannel, name='createchannel'),
    path("youtube/new_channel_setup", views.channelSetup, name='channelsetup'),
    path("youtube/addvideo", views.addvideo, name='addvideo'),
    path("youtube/uploadvideo", views.uploadvideo, name='uploadvideo'),
    path('comment', views.addcomment, name='comment'),
    path("subscribe", views.subscribe, name='subscribe'),   
    path("unsubscribe", views.unsubscribe, name='unsubscribe'),
    path("like", views.likevideo, name='like'),
    path("dislike", views.dislikevideo, name='dislike'),
    path('createplaylist', views.createPlaylist, name="createplaylist"),
    path("youtube/playlist/<int:id>", views.showplaylist, name='showplaylist'),
    path("youtube/playlist/<str:List>", views.showplaylist, name='watchlaterPlaylist'),

    path("savetoplaylists", views.savetoplaylists, name='savetoplaylists'),
    path("searchforvideo", views.searchforvideo),
    path("youtube/search_results", views.search, name='searchsomething'),

    path("youtube/customize_channel/<int:channelid>", views.customize, name='customize'),
    path("removeFromHistory", views.removeFromHistory, name='removeFromHistory'),
    path("removeFromPlaylist", views.removeFromPlaylist, name='removeFromPlaylist'),
    path("supply", views.supplyVideos, name='supplyvideos'),
    path("watchlater", views.watchlater),
    path("removefromwatchlater", views.removefromwatchlater, name='removefromwatchlater'),
    path("youtube/subscriptions", views.subscriptions, name='subscriptions')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)