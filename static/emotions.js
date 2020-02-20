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
            // document.getElementById("answer_mood").style.display = 'block';
            // let text =  'Thank you! <br>';
            // document.getElementById("answer_mood").innerHTML= text + '<a id="continue_mood_link" href="/'+ next_page + '" > Let\'s CONTINUE!';
            document.getElementById("behaviours").style.display = 'block';
            document.getElementById('video_annotation').play()
            // alert("Thank you!");
            // setTimeout(function () {
            //     document.getElementById('video_annotation').play()
            // }, 2000);
        }
        // async: false
    });

}

function collect_behaviours(video_file, emotion, time_seconds) {
    behaviours = {
        'jump': 1,
        'laugh': 0,
        'head_movement': 0,
        'other': 'Sending data by JS'
    }

    // document.getElementById("emotion_blue").onclick =
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
        video_name = document.getElementById("source_video").getAttribute('src');
        // behaviours = {
        //     'jump': 1,
        //     'laugh': 0,
        //     'head_movement': 0,
        //     'other': 'Sending data by JS'
        // }
    }

    document.getElementById("send_behaviours").onclick = function () {
        behaviours = collect_behaviours();
        make_request(video_name, emotion, time_seconds, behaviours);

    }
}
