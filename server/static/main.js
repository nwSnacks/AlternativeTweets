$(function () {
    var tweetObj = {}
    var points = 0
    var numberLives = 3

    // when the tweet button is clicked, check if the current tweet is a real tweet.
    // if true, increment points. if not, decrement lives, go to game over screen if at 0 lives.
    // replace tweet
    $('#tweet').click(function () {
        $('#tweet').prop("disabled", true);
        $('#text').prop("disabled", true);
        if (tweetObj["true_or_false"] == "true") {
            ++points
        } else {
            --numberLives
            if (numberLives == 0) {
                gameOverDialogue();
            }
        }
        updateTweet()
        $('#tweet').prop("disabled", false);
        $('#text').prop("disabled", false);
    }

    // when the text button is clicked, check if the current tweet is a fake tweet.
    // if true, increment points. if not, decrement lives, go to game over screen if at 0 lives.
    // replace tweet
    $('#text').click(function () {
        $('#tweet').prop("disabled", true);
        $('#text').prop("disabled", true);
        if (tweetObj["true_or_false"] == "false") {
            ++points
        } else {
            --numberLives
            if (numberLives == 0) {
                gameOverDialogue();
            }
        }
        updateTweet()
        $('#tweet').prop("disabled", false);
        $('#text').prop("disabled", false);
    }


    function updateTweet() {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "http://localhost/question", false); // false for synchronous request
        xmlHttp.send();
        tweetObj = xmlHttp.responseText;
    }

    function gameOverDialogue() {
        // TODO:
        points = 0;
        numberLives = 3;
    }
});