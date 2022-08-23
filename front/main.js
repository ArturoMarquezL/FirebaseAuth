function login(token){

    sessionStorage.setItem("token", token)

    var request =  new XMLHttpRequest();
    request.open('GET', 'https://8000-arturomarqu-firebaseaut-ya3gtonts88.ws-us62.gitpod.io/user/');
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept", "application/json")

    request.onload = function () {
        var status = request.status;
        if (status === 202){
            window.location.replace("home.html")
        }
        else{
            console.log(request.responseText)
        }
    }

    request.send();
    
}

function getToken(){
    let email = document.getElementById("email")
    let password = document.getElementById("password")

    var request =  new XMLHttpRequest();
    request.open('GET', 'https://8000-arturomarqu-firebaseaut-ya3gtonts88.ws-us62.gitpod.io/user/validate/');
    request.setRequestHeader("Authorization", "Basic " + btoa(email.value + ":" + password.value));
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept", "application/json")

    request.onload = function () {
        var status = request.status;

        if (status === 202){
            token = request.responseText
            token = JSON.parse(token)
            token = token.token
            login(token)
        }
        else{
            console.log(request.responseText)
        }
    }
    request.send();
}

function singup(){

    let email = document.getElementById("email");
    let password = document.getElementById("password");

    payload = {
        "email": email.value,
        "password": password.value
    }

    var request =  new XMLHttpRequest();
    request.open('POST', 'https://8000-arturomarqu-firebaseaut-ya3gtonts88.ws-us62.gitpod.io/signup/');
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept", "application/json")

    request.onload = function () {
        var status = request.status;

        if (status === 202){
            window.location.replace("home.html")
        }
        else{
            console.log(request.responseText)
        }
    }
    request.send(JSON.stringify(payload));
     
}
