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
            // document.getElementById("mood_buttons").style.display = 'None'
            alert("Thank you!");
        }
        // async: false
    });

}

window.onload = function () {

    let video = document.getElementById('video_annotation')

    document.getElementById("emotion_blue").onclick = function () {
        emotion = 'blue';
        time_seconds = video.currentTime
        behaviours = {
            'jump': 1,
            'laugh': 0,
            'head_movement': 0,
            'other': 'Sending data by JS'
        }
        make_request('video_test_again.avi', emotion, time_seconds, behaviours);
    }
}
