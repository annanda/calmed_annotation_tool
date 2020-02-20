function make_request(video_name, emotion, time_seconds, behaviors, method = "post") {
    $.ajax({
        url: '/store_annotation',
        type: 'POST',
        data: JSON.stringify({
            video_file_name: video_name,
            emotional_zone: emotion,
            time_seconds: time_seconds,
            behaviours: behaviors
        }),
        contentType: 'application/json',
        processData: false,
        success: function (msg) {
            document.getElementById("behaviours").style.display = 'none';
            document.getElementById("wrapper").style.display = 'block';

            document.getElementById('video_annotation').currentTime = time_seconds;
            document.getElementById('video_annotation').play()
        }
        // async: false
    });

}

function collect_behaviours(video_file, emotion, time_seconds) {
    behaviours = {}

    var behaviour = document.getElementById("behaviours_checkbox")
    var txt = "";
    var i;
    for (i = 0; i < behaviour.length - 1; i++) {
        if (behaviour[i].checked) {
            behaviours[behaviour[i].value] = 1
        } else {
            behaviours[behaviour[i].value] = 0
        }
    }
    var typed_behaviour = document.getElementById('typed_text').value
    behaviours['Other'] = typed_behaviour;
    $('input[type=checkbox]').prop('checked', false);
    document.getElementById('typed_text').value = "";
    return behaviours
}

window.onload = function () {

    let video = document.getElementById('video_annotation');
    let emotion = '';
    let time_seconds = '';
    let video_name = ''
    let behaviours = {}


    document.getElementById("emotion_blue").onclick = function () {
        emotion = 'blue';
        time_seconds = video.currentTime;
        video.pause();
        document.getElementById("behaviours").style.display = 'block';
        document.getElementById("wrapper").style.display = 'none';
        video_name = document.getElementById("source_video").getAttribute('src');
    }

    document.getElementById("emotion_green").onclick = function () {
        emotion = 'green';
        time_seconds = video.currentTime;
        video.pause();
        document.getElementById("behaviours").style.display = 'block';
        document.getElementById("wrapper").style.display = 'none';
        video_name = document.getElementById("source_video").getAttribute('src');
    }

    document.getElementById("emotion_red").onclick = function () {
        emotion = 'red';
        time_seconds = video.currentTime;
        video.pause();
        document.getElementById("behaviours").style.display = 'block';
        document.getElementById("wrapper").style.display = 'none';
        video_name = document.getElementById("source_video").getAttribute('src');
    }

    document.getElementById("emotion_yellow").onclick = function () {
        emotion = 'yellow';
        time_seconds = video.currentTime;
        video.pause();
        document.getElementById("behaviours").style.display = 'block';
        document.getElementById("wrapper").style.display = 'none';
        video_name = document.getElementById("source_video").getAttribute('src');
    }

    document.getElementById("send_behaviours").onclick = function () {
        behaviours = collect_behaviours();
        make_request(video_name, emotion, time_seconds, behaviours);
    }
}
