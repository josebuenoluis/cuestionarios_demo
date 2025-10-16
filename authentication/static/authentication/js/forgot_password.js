
let card = document.querySelector(".card");
let emailUser = "";

function inputsVerificarToken(){
    let email = document.getElementById("email").value;
    emailUser = email;
    let btnGenerarToken = document.getElementById("btnGenerarToken");
    btnGenerarToken.disabled = true;
    let tokenInput = document.getElementById("token");
    postGenerarToken(email).then(data => {
        if(data.status == true){
            tokenInput.disabled = false;
            btnGenerarToken.disabled = false;
            btnGenerarToken.textContent = "Verificar token";
            btnGenerarToken.className = "btn btn-primary";
            btnGenerarToken.onclick = () => {
                postVerificarToken(tokenInput.value).then(data => {
                    if(data.status){
                        inputsNewPassword();
                    }else{
                        alert("El Token ingresado no es valido.");
                    }
                });
            }
        }else{
            alert("El correo electronico no existe.");
        }
    });
}

function limpiarCard(){
    const form = card.querySelector(".card-body form");
    if(!form) return;
    const children = Array.from(form.children);
    children.forEach(child => {
        // conservar inputs ocultos (por ejemplo CSRF), eliminar el resto
        if(child.tagName == "INPUT" && child.type != "hidden" || child.tagName == "LABEL"){
            console.log(child);
            child.remove();
        }
    });
}

function inputsNewPassword(){
    limpiarCard();
    let btnGenerarToken = document.getElementById("btnGenerarToken");
    let containerInputPassword1 = document.createElement("div");
    let labelInputPassword1 = document.createElement("label");
    labelInputPassword1.htmlFor = "password1";
    labelInputPassword1.textContent = "Contraseña";
    let inputPassword1 = document.createElement("input");
    inputPassword1.type = "password";
    inputPassword1.id = "password1";
    inputPassword1.name = "password1";
    inputPassword1.placeholder = "Ingrese nueva contraseña";
    inputPassword1.className = "form-control mb-2";
    containerInputPassword1.appendChild(labelInputPassword1);
    containerInputPassword1.appendChild(inputPassword1);

    let containerInputPassword2 = document.createElement("div");
    let labelInputPassword2 = document.createElement("label");
    labelInputPassword2.htmlFor = "password2";
    labelInputPassword2.textContent = "Repetir contraseña";
    labelInputPassword2.className = "form-label";
    let inputPassword2 = document.createElement("input");
    inputPassword2.type = "password";
    inputPassword2.id = "password2";
    inputPassword2.name = "password2";
    inputPassword2.placeholder = "Repetir contraseña";
    inputPassword2.className = "form-control mb-2";
    containerInputPassword2.appendChild(labelInputPassword2);
    containerInputPassword2.appendChild(inputPassword2);

    const form = card.querySelector(".card-body form");
    form.insertBefore(containerInputPassword2,form.firstChild);
    form.insertBefore(containerInputPassword1,form.firstChild);
    btnGenerarToken.textContent = "Guardar contraseña";
    btnGenerarToken.value = "Guardar contraseña";
    btnGenerarToken.className = "btn btn-success";
    btnGenerarToken.onclick = () => {
        if(validarPassword(inputPassword1.value,inputPassword2.value) == true){
            postPassword(emailUser,inputPassword1.value).then(data => {
                if(data.status){
                    alert("Contraseña cambiada");
                }else{
                    alert("Error");
                }
            });
        }
    };
}

function validarPassword(password1,password2){
    if(password1 === password2){
        return true;
    }
    return false;
}

async function postPassword(email,passwordNew){
// new_password
    return fetch("/authentication/forgot/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body:JSON.stringify({email:email,new_password:passwordNew})
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}

async function postGenerarToken(email){
    return fetch("/authentication/token/generar/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({email:email})
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}

async function postVerificarToken(token){
    return fetch("/authentication/token/verificar/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({token:token})
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}

function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
}