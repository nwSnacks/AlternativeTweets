$(function () {
    var tweetObj;
    var points;
    var numberLives;

    setUpGame()

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
            setResult("RIGHT!");
        } else {
            --numberLives;
            setLives();
            setResult("WRONG!");
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
                setResult("RIGHT!");
            } else {
                --numberLives;
                setLives();
                setResult("WRONG!");
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
        xmlHttp.open("GET", "http://alternativetweets.us/question", false); // false for synchronous request
        xmlHttp.send();
        console.log("sent request")
        tweetObj = JSON.parse(xmlHttp.responseText);
        console.log(tweetObj.toString())
        console.log("Tweet: " + tweetObj["tweet"])
        $("#tweetBody").html(tweetObj["tweet"]);
    }

    function gameOverDialogue() { 
        setResult("YOU'RE FIRED!!!");

        $("#submitScore")[0].style.display = "block";

        // When the user clicks on (x), close the modal
        $(".close").click(function() {
            $("#submitScore")[0].style.display = "none";
            setUpGame();
        });

        $("#modalText").text("Your final score is " + points);

        $("#submitButton").click(function() {
            sendScoreToLeaderboard($("#name_input")[0].value);
            $("#submitScore")[0].style.display = "none";
            setUpGame();

        });

        // When the user clicks anywhere outside of the modal, close it
        $(window).click(function(event) {
            if (event.target == $("#submitScore")[0]) {
                $("#submitScore")[0].style.display = "none";
                setUpGame();
            }
        });
    }

    // when game starts, should be at 0 points and 3 lives left
    function setUpGame() {
        tweetObj = {}
        points = 0
        setScore()
        numberLives = 3
        setLives()
    }

    function setScore() {
        $("#scoreValue").html(points);
        $("#submitScore").value = points;
    }

    function setLives() {
        if (numberLives == 3) {
            $("#hitPoints").attr("src", "../static/heart3.png");
        } else if (numberLives == 2) {
            $("#hitPoints").attr("src", "../static/heart2.png");
        } else if (numberLives == 1) {
            $("#hitPoints").attr("src", "../static/heart1.png");
        } else if (numberLives == 0) {
            $("#hitPoints").attr("src", "../static/heart0.png");
        }
    }
    function setResult(result) {
        $("#result").html(result);
    }

    function sendScoreToLeaderboard(name) {

        var xmlHttp = new XMLHttpRequest();

        var secondsSinceEpoch = (Date.now() / 1000).toFixed(0)

        var params = "pub_date=" + secondsSinceEpoch + "&username=" + name + "&score=" + points;
        xmlHttp.open("POST", "http://127.0.0.1:5000/leaderboard?" + params, false); // false for synchronous request
        xmlHttp.send();
    }
});
