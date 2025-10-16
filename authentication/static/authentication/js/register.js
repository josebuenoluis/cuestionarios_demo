let avatar = "";
let containerAvatarSelected = document.getElementById("containerAvatarSelected");
let modalAvatar = new bootstrap.Modal(document.getElementById('staticBackdrop'));
let inputAvatar = document.getElementById("avatar_input");

document.getElementById("id_password1").value = "pruebausuario12345678";
document.getElementById("id_password2").value = "pruebausuario12345678";

inputAvatar.value = containerAvatarSelected.querySelector("svg").outerHTML;
function seleccionarAvatar(event) {
    let avatarSeleccionado = event.currentTarget.querySelector("svg");
    let avatarReemplazar = containerAvatarSelected.querySelector("svg");
    avatarReemplazar.remove();
    containerAvatarSelected.appendChild(avatarSeleccionado.cloneNode(true));
}

function guardarAvatar(){
    let avatarSeleccionado = containerAvatarSelected.querySelector("svg").outerHTML;
    // let inputAvatar = document.getElementById("avatar_input");
    inputAvatar.value = avatarSeleccionado;
    let avatarUserContainer = document.getElementById("avatarUserContainer");
    let avatarReemplazar = avatarUserContainer.querySelector("svg");
    avatarReemplazar.remove();
    avatarUserContainer.insertBefore(containerAvatarSelected.querySelector("svg").cloneNode(true), avatarUserContainer.firstChild);
    modalAvatar.hide();
}

