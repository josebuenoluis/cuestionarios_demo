let usersList = document.getElementById("usersList");
let inputUsername = document.getElementById("id_username");
let inputPassword = document.getElementById("id_password");
let modal = new bootstrap.Modal(document.getElementById('modalUsers'));
function seleccionarUsuario(event){
    let alertUserSelected = event.target;
    if(alertUserSelected.classList.contains("alert")){
        let dataUserSpans = alertUserSelected.querySelectorAll("span");
        let username = dataUserSpans[2].textContent;
        let password = dataUserSpans[5].textContent;
        inputUsername.value = username;
        inputPassword.value = password;
        console.log("Username: "+ username);
        console.log("Password: "+password);
        modal.hide();
    }else{
        let alertUserQuery = alertUserSelected.closest(".alert");
        let dataUserSpans = alertUserQuery.querySelectorAll("span");
        let username = dataUserSpans[2].textContent;
        let password = dataUserSpans[5].textContent;
        inputUsername.value = username;
        inputPassword.value = password;
        console.log("Username: "+ username);
        console.log("Password: "+password);
        modal.hide();
    }
}

