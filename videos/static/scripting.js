/*function add_video(content){
    template = Handlebars.compile(document.querySelector('#videoHandlebar').innerHTML)
    document.querySelector('#container').innerHTML += template({'videoid':content.id, 'videoname':content.videoname, 'thumbnail':content.thumbnail.url}) 
}*/



function removeFromHistory(btn){
    const videoid = btn.getAttribute("data-videoid");
    //alert(videoid);
    fetch(`/removeFromHistory?videoid=${videoid}`)
    .then(response => response.json())
    .then(data =>{
        if(data.historystatus == 'removed')
            alert('removed from watch history');
            location.reload();
    })
}

function watchlater(btn){
    
    const videoid = btn.getAttribute("data-videoid");
    //alert(videoid);
    fetch(`/watchlater?videoid=${videoid}`)
    .then(response => response.json())
    .then(data => {
        if(data.status == 'loggedout')
            window.location.replace("/");
        else if(data.status == 'true'){
            document.querySelector('#anim').innerHTML = 'Added to watch later';
            document.querySelector('#anim').style.animationPlayState='running';
        }
    })
}//end of watchlater function

function removeFromWatchLater(btn){
    const videoid = btn.getAttribute("data-videoid");
    const wid = btn.getAttribute("data-Wid");
    fetch(`/removefromwatchlater?videoid=${videoid}&wid=${wid}`)
    .then(response => response.json())
    .then(data =>{
        if(data.status == 'loggedout')
            window.location.replace("/")
        else if(data.status == 'true'){
            location.reload();
            document.querySelector('#anim').innerHTML = 'Removed from watch later';
            document.querySelector('#anim').style.animationPlayState='running';
        }
    })
}

function createNewPlaylist(){
    const playlistname = document.querySelector('#playlistname').value;
    const cbox = document.querySelector('#cbox').checked;
    const channelid = document.querySelector('#curchannelid').innerHTML;
    fetch(`/createplaylist?name=${playlistname}&cbox=${cbox}&channelid=${channelid}`)
    .then(response => response.json())
    .then(data =>{
        if(data.playlist == 'loggedout')
            window.location.replace("/");
        else if(data.playlist == 'true'){
            //document.querySelector('#playlistlist').remove('no');
            const cboxtemplate = Handlebars.compile(document.querySelector('#choicehandlebar').innerHTML);
            document.querySelector('#playlistOptions').innerHTML += cboxtemplate({'playlistid':data.playlistid, 'playlistname':playlistname});
            document.querySelector('#panim').style.animationPlayState = 'running';
        }

    })
}//end of creating new playlist function




document.addEventListener('DOMContentLoaded', ()=>{
/*
    let counter=0
    let quantity=2

    load();

    function load(){
        let start = counter+1
        let end = start+quantity-1
        counter=end+1;

        fetch(`/supply?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            data.videos.forEach(add_video);
        })
    }*/

    //playlist input field
    document.querySelector('#createPlaylist').disabled = true;
    document.querySelector('#playlistname').onkeyup = ()=>{
        if(document.querySelector('#playlistname').value =='')
            document.querySelector('#createPlaylist').disabled = true;
        else
            document.querySelector('#createPlaylist').disabled = false;
    }
})//end of event listener for playlistname btn


function savetoplaylist(btn){
    on(5);
    const videoid = btn.getAttribute("data-videoid");
    //alert(videoid);
    document.querySelector('#videoid').value = videoid;
}//end of save to playlist function

window.addEventListener('popState', function(){
    alert('location changed');
    if(localStorage.getItem('playlistaddmessage'))
        alert('playlist added');
        localStorage.clear();
})

function setinput(anc){
    //alert(anc.innerHTML);
    document.querySelector('#searchinputfield').value = anc.innerHTML;
}

function removeFromPlaylist(btn){
    const videoid = btn.getAttribute('data-videoid');
    const pid = btn.getAttribute('data-pid');
    fetch(`/removeFromPlaylist?videoid=${videoid}&pid=${pid}`)
    .then(response => response.json())
    .then(data =>{
        if(data.status == 'removed'){
            location.reload();
        }
        else if(data.status == 'loggedout'){
            window.replace('/');
        }
    })
}

document.addEventListener('DOMContentLoaded' , ()=>{
    const resulttemplate = Handlebars.compile(document.querySelector('#resultHandlebar').innerHTML);
    var resultsArray = []
    document.querySelector('#searchinputfield').onkeyup = ()=>{
        const text = document.querySelector('#searchinputfield').value;
        if(text=='')   
            resultsArray = []
        //elements = document.getElementsByClassName('.relatedresults');
        
        fetch(`/searchforvideo?text=${text}`)
        .then(response => response.json())
        .then(data =>{
            //alert(data.relatedresults);
            //alert(resultsArray);
            if(data.relatedresults == '[]')
                document.querySelector('#relatedresultsdiv').innerHTML = '';
            else{
                resultsArray.splice(0,resultsArray.length);
                document.querySelector('#relatedresultsdiv').innerHTML = '';
                for (i in data.relatedresults){
                    //if(!resultsArray.includes(i)){
                        resultsArray.push(i);
                        document.querySelector('#relatedresultsdiv').innerHTML += resulttemplate({'name':data.relatedresults[i]});
                    //}
            }
        }
        })
    }
})









function unsubscribe(btn){
    //compile handlebars template
    //alert('hai')
    const subtemplate = Handlebars.compile(document.querySelector('#subhandlebar').innerHTML);
    const channelid = btn.getAttribute('data-channelid');
    //alert(channelid);
    fetch(`/unsubscribe?channelid=${channelid}`)
    .then(response => response.json())
    .then(data =>{
        if(data.unsubscriptionStatus == 'loggedout')
            alert('You need to login to subscribe, login using sign in button');
        else if(data.unsubscriptionStatus){
            document.querySelector('#subdiv').innerHTML='';
            document.querySelector('#subdiv').innerHTML=subtemplate({'channelid':channelid});
    }
    })
}//end of function


//subscriptions
function subscribeUser(btn){
    //compile handlebars template
    const unsubtemplate = Handlebars.compile(document.querySelector('#unsubhandlebar').innerHTML);
    //alert('hai')
    const channelid = btn.getAttribute('data-channelid');
    //const channelid = document.querySelector('#hiddenchannelid').innerHTML;
    //alert(channelid);
    fetch(`/subscribe?channelid=${channelid}`)
    .then(response => response.json())
    .then(data =>{
        if(data.subscriptionStatus == 'loggedout')
            alert('You need to login to subscribe to this channel');
        else if(data.subscriptionStatus){
            document.querySelector('#subdiv').innerHTML='';
            document.querySelector('#subdiv').innerHTML=unsubtemplate({'channelid':channelid});
    }
    })
}//end of funciton