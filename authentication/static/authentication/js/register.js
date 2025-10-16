let avatar = "";
let containerAvatarSelected = document.getElementById("containerAvatarSelected");
let modalAvatar = new bootstrap.Modal(document.getElementById('staticBackdrop'));
function seleccionarAvatar(event) {
    let avatarSeleccionado = event.currentTarget.querySelector("svg");
    let avatarReemplazar = containerAvatarSelected.querySelector("svg");
    avatarReemplazar.remove();
    containerAvatarSelected.appendChild(avatarSeleccionado.cloneNode(true));
}

function guardarAvatar(){
    let avatarSeleccionado = containerAvatarSelected.querySelector("svg").outerHTML;
    let inputAvatar = document.getElementById("avatar_input");
    inputAvatar.value = avatarSeleccionado;
    let avatarUserContainer = document.getElementById("avatarUserContainer");
    let avatarReemplazar = avatarUserContainer.querySelector("svg");
    avatarReemplazar.remove();
    avatarUserContainer.insertBefore(containerAvatarSelected.querySelector("svg").cloneNode(true), avatarUserContainer.firstChild);
    modalAvatar.hide();
}

// Para consultar el SVG seleccion y convertirlo en string
// let avatarSeleccionado = containerAvatarSelected.querySelector("svg").outerHTML;
