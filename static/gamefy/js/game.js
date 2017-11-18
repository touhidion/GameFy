var tries = 0;
var result_number;
var previous_best_score;

function generateRandom(){
    result_number = Math.floor((Math.random() * 50) + 1);
}

function checkInputAndResponse(previous_score){
    if(tries == 0){
        previous_best_score = previous_score;
        generateRandom();
    }

    var user_input = parseInt(document.getElementById('user_input').value);

    if(!user_input){
        document.getElementById('game_hint').style.color='red';
        document.getElementById('game_hint').innerHTML='Enter number please!';
    }else{
        tries++;
        checkResult(user_input);
    }
}

function checkResult(user_input){

    document.getElementById('game_tries').innerHTML = tries;

    if(result_number == user_input){

        manageNewScore();

    }else if(result_number > user_input){
        document.getElementById('game_hint').style.color='red';
        document.getElementById('game_hint').innerHTML = 'Higher'+result_number;
    }else{
        document.getElementById('game_hint').style.color='red';
        document.getElementById('game_hint').innerHTML = 'Lower';
    }
}

function manageNewScore(){
    document.getElementById('game_notifications').style.color='green';

    if(tries < previous_best_score){
        previous_best_score = tries;

        document.getElementById('success_message').innerHTML =
        'You have found the number.<br> You have tried <strong>'+tries+'</strong> times. And<br> Congratulations! this is new High Score.';

        /*csrfmiddwaretoken not working inside .js file,
        so I had to send json data from .html file to save score.
        That's why calling function inside the html file again*/

        saveBestScore(tries);
    }else{
        document.getElementById('success_message').innerHTML =
         'You have found the number.<br> And you have tried <strong>'+tries+'</strong> times.';
    }

    document.getElementById('user_input').value='';
    document.getElementById('game_hint').innerHTML = '';

    tries = 0;
}

function restartGame(){
    tries = 0;
    document.getElementById('game_tries').innerHTML = tries;
    document.getElementById('game_hint').innerHTML = '';
    document.getElementById('user_input').value = '';
    document.getElementById('game_notifications').style.color='black';
    document.getElementById('success_message').innerHTML = '';
}