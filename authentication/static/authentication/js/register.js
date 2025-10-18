let avatar = "";
let containerAvatarSelected = document.getElementById("containerAvatarSelected");
let modalAvatar = new bootstrap.Modal(document.getElementById('staticBackdrop'));
let inputAvatar = document.getElementById("avatar_input");
const user = JSON.parse(document.getElementById('user-data').textContent);
console.log(user);
document.getElementById("id_username").value = user["username"];
document.getElementById("id_password1").value = user["password"];
document.getElementById("id_password2").value = user["password"];
document.getElementById("id_email").value = user["email"];

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

