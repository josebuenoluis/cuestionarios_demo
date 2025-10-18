let containerAvatarSelected = document.getElementById("containerAvatarSelected");
let modalUpdateDates = document.getElementById("modalUpdateDates");
let modalCambiar = new bootstrap.Modal(document.getElementById('modalUpdateDates'));
let modalAvatar = new bootstrap.Modal(document.getElementById('staticBackdrop'));
let btnGuardarModalUpdate = document.getElementById("btnGuardarModalUpdate");

function seleccionarAvatar(event) {
    let avatarSeleccionado = event.currentTarget.querySelector("svg");
    let avatarReemplazar = containerAvatarSelected.querySelector("svg");
    avatarReemplazar.remove();
    containerAvatarSelected.appendChild(avatarSeleccionado.cloneNode(true));
}

function guardarAvatar() {
    let avatarSeleccionado = containerAvatarSelected.querySelector("svg").outerHTML;
    console.log({avatar:avatarSeleccionado});
    postAvatar({avatar:avatarSeleccionado}).then(data => {
        if(data.status == true){
            let userIconNavbar = document.getElementById("user-icon");
            userIconNavbar.querySelector("svg").remove();
            userIconNavbar.appendChild(containerAvatarSelected.querySelector("svg").cloneNode(true));
            let avatarUserContainer = document.getElementById("avatarUserContainer");
            let avatarReemplazar = avatarUserContainer.querySelector("svg");
            avatarReemplazar.remove();
            avatarUserContainer.insertBefore(containerAvatarSelected.querySelector("svg").cloneNode(true), avatarUserContainer.firstChild);
            modalAvatar.hide();
        }else{
            console.log("No se pudo guardar el avatar");
        }
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

async function postAvatar(avatar){
    const csrftoken = getCookie('csrftoken');
    return fetch("/panel/guardar/avatar/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(avatar)
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}

// Funcion para limpiar el modal de Bootstrap
function limpiarModal(){
    let modalBody = modalUpdateDates.querySelector(".modal-body");
    modalBody.innerHTML = "";
}

function modalCambiarUsuario(){
    modalUpdateDates.querySelector(".modal-footer").querySelector(".btn-primary").onclick = guardarUsername;
    console.log("Modal cambio de usuario");
    document.getElementById("staticBackdropLabel2").textContent = "Cambiar Usuario";
    let inpurUsername = document.createElement("input");
    inpurUsername.type = "text";
    inpurUsername.className = "form-control";
    inpurUsername.id = "username-change";
    inpurUsername.name = "username";
    inpurUsername.placeholder = "Nuevo username";
    inpurUsername.value = "";
    inpurUsername.required = true;
    let modalBody = modalUpdateDates.querySelector(".modal-body");
    modalBody.innerHTML = "";
    let labelUsername = document.createElement("label");
    labelUsername.htmlFor = "username-change";
    labelUsername.textContent = "Nuevo username";
    modalBody.appendChild(labelUsername);
    modalBody.appendChild(inpurUsername);
}

function modalInformativo() {
    console.log("Modal informativo - función no disponible en versión demo");

    // Cambiar el título del modal
    document.getElementById("staticBackdropLabel2").textContent = "Función en desarrollo";

    // Obtener el cuerpo del modal
    let modalBody = modalUpdateDates.querySelector(".modal-body");
    modalBody.innerHTML = "";

    // Crear un mensaje informativo
    let mensaje = document.createElement("p");
    mensaje.textContent = "Esta función no está disponible en la versión demo. La versión completa del sistema se encuentra actualmente en desarrollo.";
    mensaje.style.textAlign = "center";
    mensaje.style.fontWeight = "bold";
    mensaje.style.color = "#555";

    // Agregar el mensaje al cuerpo del modal
    modalBody.appendChild(mensaje);
}


function modalGenerarToken(){
    let modalBody = modalUpdateDates.querySelector(".modal-body");
    document.getElementById("staticBackdropLabel2").textContent = "Cambiar Email";
    let container = document.createElement("div");
    container.className = "d-flex flex-column align-items-center justify-content-center";
    container.id = "btnTokenContainer";
    let containerInputs = document.createElement("div");
    containerInputs.className = "d-flex flex-column align-items-start justify-content-center w-100";
    let inputTokenChange = document.createElement("input");
    inputTokenChange.className = "form-control";
    inputTokenChange.type = "text";
    inputTokenChange.id = "token-change";
    inputTokenChange.name = "token";
    inputTokenChange.placeholder = "Token";
    inputTokenChange.required = true;
    inputTokenChange.disabled = true;
    inputTokenChange.maxLength = 36;
    let labelToken = document.createElement("label");
    labelToken.htmlFor = "token-change";
    labelToken.textContent = "Token";
    modalBody.innerHTML = "";
    let btnGenerarToken = document.createElement("button");
    btnGenerarToken.type = "button";
    btnGenerarToken.className = "btn btn-secondary mb-3 mt-3 w-50";
    btnGenerarToken.textContent = "Generar token";
    btnGenerarToken.id = "btnGenerarToken";
    btnGenerarToken.onclick = () => {
        // generarToken("",inputsNewPassword);
    };
    containerInputs.appendChild(labelToken);
    containerInputs.appendChild(inputTokenChange);
    container.appendChild(btnGenerarToken);
    modalBody.appendChild(containerInputs);
    modalBody.appendChild(container);

}

function modalCambiarEmail(){
    // modalUpdateDates
    let modalBody = modalUpdateDates.querySelector(".modal-body");
    document.getElementById("staticBackdropLabel2").textContent = "Cambiar Email";
    let container = document.createElement("div");
    container.className = "d-flex flex-column align-items-center justify-content-center";
    container.id = "btnTokenContainer";
    let containerInputs = document.createElement("div");
    containerInputs.className = "d-flex flex-column align-items-start justify-content-center w-100";
    let inputTokenChange = document.createElement("input");
    inputTokenChange.className = "form-control";
    inputTokenChange.type = "text";
    inputTokenChange.id = "token-change";
    inputTokenChange.name = "token";
    inputTokenChange.placeholder = "Token";
    inputTokenChange.required = true;
    inputTokenChange.disabled = true;
    inputTokenChange.maxLength = 36;
    let labelToken = document.createElement("label");
    labelToken.htmlFor = "token-change";
    labelToken.textContent = "Token";
    modalBody.innerHTML = "";
    let btnGenerarToken = document.createElement("button");
    btnGenerarToken.type = "button";
    btnGenerarToken.className = "btn btn-secondary mb-3 mt-3 w-50";
    btnGenerarToken.textContent = "Generar token";
    btnGenerarToken.id = "btnGenerarToken";
    btnGenerarToken.onclick = () => {
        generarToken("",inputsCambioEmail);
    };
    containerInputs.appendChild(labelToken);
    containerInputs.appendChild(inputTokenChange);
    container.appendChild(btnGenerarToken);
    modalBody.appendChild(containerInputs);
    modalBody.appendChild(container);
    // modalBody.appendChild(labelToken);
    // modalBody.appendChild(inputTokenChange);
    // modalBody.appendChild(btnGenerarToken);
    // limpiarModal();
}

function guardarPassword(){
    let oldPassword = document.getElementById('old-password-change').value;
    let newPassword = document.getElementById('password-change').value;
    let newPasswordRepeat = document.getElementById('password-change-repeat').value;
    if(newPassword === newPasswordRepeat){
        postPassword({old_password:oldPassword,new_password:newPassword}).then(data => {
            if(data.status == true){
                limpiarModal();
                // Cerramos el modal
                modalCambiar.hide();
            }else{
                alert("No se pudo cambiar la contraseña. Verifique que la contraseña actual sea correcta.");
                console.log("No se pudo guardar el username");
            }
        });
    }else{
        alert("Las nuevas contraseñas no coinciden.");
    }
}

function modalCambiarPassword(){
    limpiarModal();
    btnGuardarModalUpdate.onclick = guardarPassword;

    let modalBody = modalUpdateDates.querySelector(".modal-body"); 
    document.getElementById("staticBackdropLabel2").textContent = "Cambiar contraseña";
    
    let labelOldPassword = document.createElement("label");
    labelOldPassword.htmlFor = "old-password-change";
    labelOldPassword.textContent = "Contraseña actual";
    let oldPassword = document.createElement("input");
    oldPassword.type = "password";
    oldPassword.className = "form-control mb-2";
    oldPassword.id = "old-password-change";
    oldPassword.name = "old-password";
    oldPassword.placeholder = "Contraseña actual";
    oldPassword.value = "";
    oldPassword.required = true;
    oldPassword.autofocus = true;
    modalBody.appendChild(labelOldPassword);
    modalBody.appendChild(oldPassword);

    let labelNewPassword = document.createElement("label");
    labelNewPassword.htmlFor = "password-change";
    labelNewPassword.textContent = "Nueva contraseña";
    let newPassword = document.createElement("input");
    newPassword.type = "password";
    newPassword.className = "form-control mb-2";
    newPassword.id = "password-change";
    newPassword.name = "password";
    newPassword.placeholder = "Nueva contraseña";
    newPassword.value = "";
    newPassword.required = true;
    modalBody.appendChild(labelNewPassword);
    modalBody.appendChild(newPassword);

    let labelNewPasswordRepeat = document.createElement("label");
    labelNewPasswordRepeat.htmlFor = "password-change-repeat";
    labelNewPasswordRepeat.textContent = "Repetir nueva contraseña";
    let newPasswordRepeat = document.createElement("input");
    newPasswordRepeat.type = "password";
    newPasswordRepeat.className = "form-control";
    newPasswordRepeat.id = "password-change-repeat";
    newPasswordRepeat.name = "password-repeat";
    newPasswordRepeat.placeholder = "Repetir nueva contraseña";
    newPasswordRepeat.value = "";
    newPasswordRepeat.required = true;

    modalBody.appendChild(labelNewPasswordRepeat);
    modalBody.appendChild(newPasswordRepeat);

}

function guardarUsername(){
    let newUsername = document.getElementById('username-change').value;
    postUsername(newUsername).then(data => {
        if(data.status == true){
            let inputUsername = document.getElementById("username");
            inputUsername.value = newUsername;

            limpiarModal();
            // Cerramos el modal
            
            console.log(modalCambiar);
            modalCambiar.hide();
        }else{
            console.log("No se pudo guardar el username");
        }
    });
}
    

async function postUsername(newUsername){
    const csrftoken = getCookie('csrftoken');
    return fetch("/panel/guardar/username/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({username:newUsername})
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}

async function postPassword(passwordObject){
    const csrftoken = getCookie('csrftoken');
    return fetch("/panel/guardar/password/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(passwordObject)
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}


async function postEmail(newEmail){
    const csrftoken = getCookie('csrftoken');
    return fetch("/panel/guardar/email/", {
        method: "POST",
        credentials: "same-origin",
        headers: {

            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(newEmail)
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log(error);
        return { status: false };
    });
}

function generarToken(email,action){
    let inputToken = document.getElementById("token-change");
    inputToken.disabled = false;
    let btnGenerarToken = document.getElementById("btnGenerarToken");
    let btnVerificarToken = document.createElement("button");
    let containerBtnToken = document.getElementById("btnTokenContainer");
    btnVerificarToken.type = "button";
    btnVerificarToken.className = "btn btn-primary mb-3 mt-3 w-50";
    btnVerificarToken.textContent = "Verificar token";
    btnVerificarToken.id = "btnVerificarToken";
    btnVerificarToken.onclick = () => {
        postVerificarToken().then(data => {
            console.log("Verificar token: ",data); 
            // inputsCambioEmail();
            action();
        })
    };
    containerBtnToken.appendChild(btnVerificarToken);
    btnGenerarToken.style.display = "none";
    postGenerarToken(email).then(data => {
        console.log("Token: ",data);
    });


}

function inputsCambioEmail(){
    let modalBody = modalUpdateDates.querySelector(".modal-body");
    let containerNewEmail = document.createElement("div");
    containerNewEmail.className = "d-flex flex-column align-items-start justify-content-center w-100 mb-2";
    let newEmail = document.createElement("input");
    newEmail.type = "email";
    newEmail.className = "form-control";
    newEmail.id = "email-change";
    newEmail.name = "email";
    newEmail.placeholder = "Nuevo email";
    newEmail.value = "";
    newEmail.required = true;
    newEmail.oninput = validarEmails;
    let labelEmail = document.createElement("label");
    labelEmail.htmlFor = "email-change";
    labelEmail.textContent = "Nuevo email";
    containerNewEmail.appendChild(labelEmail);
    containerNewEmail.appendChild(newEmail);

    let containerNewEmailRepeat = document.createElement("div");
    containerNewEmailRepeat.className = "d-flex flex-column align-items-start justify-content-center w-100 mb-2";
    let newEmailRepeat = document.createElement("input");
    newEmailRepeat.type = "email";
    newEmailRepeat.className = "form-control";
    newEmailRepeat.id = "email-change-repeat";
    newEmailRepeat.name = "email-repeat";
    newEmailRepeat.placeholder = "Repetir nuevo email";
    newEmailRepeat.value = "";
    newEmailRepeat.required = true;
    newEmailRepeat.oninput = validarEmails;
    let labelEmailRepeat = document.createElement("label");
    labelEmailRepeat.htmlFor = "email-change-repeat";
    labelEmailRepeat.textContent = "Repetir nuevo email";

    let containerBtnVerificar = document.createElement("div");
    containerBtnVerificar.className = "d-flex flex-column align-items-center justify-content-center w-100";
    let btnVerificarEmail = document.createElement("input");
    btnVerificarEmail.type = "button";
    btnVerificarEmail.className = "btn btn-primary mb-3 mt-3 w-50";
    btnVerificarEmail.value = "Verificar email";
    btnVerificarEmail.id = "btnVerificarEmail";
    btnVerificarEmail.disabled = true;
    btnVerificarEmail.onclick = () => {
        // generarToken(newEmail.value);
        // alert("Verificar email");   
        postGenerarToken(newEmail.value).then(data => {
            if(data.status == true){
                limpiarModal();
                let inputTokenChange = document.createElement("input");
                inputTokenChange.className = "form-control";
                inputTokenChange.type = "text";
                inputTokenChange.id = "token-change";
                inputTokenChange.name = "token";
                inputTokenChange.placeholder = "Token";
                inputTokenChange.required = true;
                inputTokenChange.maxLength = 36;
                let labelToken = document.createElement("label");
                labelToken.htmlFor ="token-change";
                labelToken.textContent = "Token";
                let containerBtnVerificar = document.createElement("div");
                containerBtnVerificar.className = "d-flex flex-column align-items-center justify-content-center w-100";
                let btnVerificarToken = document.createElement("button");
                btnVerificarToken.type = "button";
                btnVerificarToken.className = "btn btn-primary mb-3 mt-3 w-50";
                btnVerificarToken.textContent = "Verificar token";
                btnVerificarToken.id = "btnVerificarToken";
                btnVerificarToken.onclick = () => {
                    postVerificarToken().then(data => {
                        console.log("Verificar token: ",data); 
                        if(data.status == true){
                            postEmail({email:newEmail.value}).then(data => {
                                if(data.status == true){
                                    document.getElementById("email").value = newEmail.value;
                                    limpiarModal();
                                    modalCambiar.hide();
                                }else{
                                    alert("No se pudo cambiar el email.");
                                }
                            });
                        }else{
                            alert("Token incorrecto.");
                        }

                    });
                }
                containerBtnVerificar.appendChild(btnVerificarToken);
                let containerInputs = document.createElement("div");
                containerInputs.className = "d-flex flex-column align-items-start justify-content-center w-100";
                containerInputs.appendChild(labelToken);
                containerInputs.appendChild(inputTokenChange);
                modalBody.appendChild(containerInputs);
                modalBody.appendChild(containerBtnVerificar);
            }else{
                alert("No se pudo enviar el token de verificación al nuevo email.");
            }
            
            // limpiarModal();
            // modalCambiarEmail();
        });
    }
    containerBtnVerificar.appendChild(btnVerificarEmail);

    containerNewEmailRepeat.appendChild(labelEmailRepeat);
    containerNewEmailRepeat.appendChild(newEmailRepeat);
    containerNewEmailRepeat.appendChild(containerBtnVerificar);
    
    limpiarModal();
    modalBody.appendChild(containerNewEmail);
    modalBody.appendChild(containerNewEmailRepeat);
    
}

function validarEmails(){
    let email = document.getElementById("email-change").value;
    let emailRepeat = document.getElementById("email-change-repeat").value;
    let btnVerificarEmail = document.getElementById("btnVerificarEmail");
    if(email === emailRepeat && email !== "" && emailRepeat !== ""){
        btnVerificarEmail.disabled = false;
    }else{
        btnVerificarEmail.disabled = true;
    }
}


async function postGenerarToken(email){
    return fetch("/panel/token/generar/", {
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

async function postVerificarToken(){
    const token = document.getElementById("token-change").value;
    return fetch("/panel/token/verificar/", {
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