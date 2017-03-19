$(function () {
    var tweetObj = {}
    var points = 0
    var numberLives = 3

    window.onload = function () {
        $("#tweet").prop("disabled", true);
        $("#text").prop("disabled", true);
        updateTweet();
        $("#tweet").prop("disabled", false);
        $("#text").prop("disabled", false);
        setScore();
        setLives();
    };

    // when the tweet button is clicked, check if the current tweet is a real tweet.
    // if true, increment points. if not, decrement lives, go to game over screen if at 0 lives.
    // replace tweet
    $("#tweet").click(function () {
        $("#tweet").prop("disabled", true);
        $("#text").prop("disabled", true);
        if (tweetObj["true_or_false"] == "true") {
            ++points;
            setScore();
        } else {
            --numberLives;
            if (numberLives == 0) {
                gameOverDialogue();
            }
        }
        updateTweet()
        $("#tweet").prop("disabled", false);
        $("#text").prop("disabled", false);
    })

    // when the text button is clicked, check if the current tweet is a fake tweet.
    // if true, increment points. if not, decrement lives, go to game over screen if at 0 lives.
    // replace tweet
    $("#text").click(function () {
        console.log("text button clicked");
            $("#tweet").prop("disabled", true);
            $("#text").prop("disabled", true);
            if (tweetObj["true_or_false"] == "false") {
                ++points;
                setScore();
            } else {
                --numberLives;
                if (numberLives == 0) {
                    gameOverDialogue();
                }
            }
            updateTweet()
            $("#tweet").prop("disabled", false);
            $("#text").prop("disabled", false);
        }
    )


    function updateTweet() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "http://localhost:5000/question", false); // false for synchronous request
        xmlHttp.send();
        console.log("sent request")
        tweetObj = JSON.parse(xmlHttp.responseText);
        console.log(tweetObj.toString())
        console.log("Tweet: " + tweetObj["tweet"])
        $("#tweetBody").html(tweetObj["tweet"]);
    }

    function gameOverDialogue() {
        var myForm = document.getElementById('submit');
        formData = new FormData(myForm);
        formData.set('score', points);
        points = 0;
        numberLives = 3;
    }
    function setScore(){
        $("#scoreValue").html(points);
    }
    function setLives(){
        if(numberLives==3){
            $('#hitPoints').attr("src","../static/heart3.png");
        } else if(numberLives==2){
            $('#hitPoints').attr("src","../static/heart2.png");
        } else if(numberLives==1){
            $('#hitPoints').attr("src","../static/heart1.png");
        } else if(numberLives==0){
            $('#hitPoints').attr("src","../static/heart0.png");
        }
    }
});