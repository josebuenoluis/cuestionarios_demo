function move(e){
    let enlace = e.target;
    let path = window.location.pathname;
    if(enlace.id == "next"){
        let n_pagina = path[path.length - 1];
        if(!isNaN(path[path.length - 1])){
            n_pagina = parseInt(n_pagina) + 1;
            let newPath = path.substring(0, path.length - 1);
            newPath += n_pagina.toString();
            window.location.href = newPath;
        }else{
            path += "2";
        }
    }else{
        if(!isNaN(path[path.length - 1])){
            n_pagina = parseInt(n_pagina);
            if(n_pagina > 1){
                n_pagina -= 1;
            }
            let newPath = path.substring(0, path.length - 1);
            newPath += n_pagina.toString();
            window.location.href = newPath;
        }
    }
}

function consultaCiclosAsignaturas(e){
    let tema = document.getElementById("tema").value;
    let cuestionarios = document.getElementById("container-cuestionarios");
    let busqueda = document.getElementById("busqueda").value;
    let data = {"tema":"","asignatura":"","busqueda":"","filtros":""};
    data.filtros = "true";
    if(busqueda != ""){
        data.busqueda = busqueda;
    }
    if(tema != ""){
        data.tema = tema;
    }
    let endpoint = `/cuestionarios/?tema=${encodeURIComponent(data.tema)}&busqueda=${encodeURIComponent(data.busqueda)}&filtros=${encodeURIComponent(data.filtros)}`; 
    fetch(endpoint, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.text()).then(data =>{
        // const newCuestionarios = document.createElement('div');
        // newCuestionarios.innerHTML = data;
        cuestionarios.replaceWith(document.createRange().createContextualFragment(data));
        // newCuestionarios.id = "container-cuestionarios";
    });

}

function flipped(e){
    let button = e.target;
    let containerCuestionario = button.closest('.container-cuestionario');
    containerCuestionario.classList.toggle('flipped');
}

function tipoPrompt(){
    // alert(input);
    let inputPrompt = document.getElementById("typePrompt");
    let inputArchivo = document.getElementById("typeFile");
    let containerArchivo = document.getElementById("container-archivo");
    let containerPrompt = document.getElementById("container-prompt");
    if (inputPrompt.checked) {
        console.log("Tipo Prompt está activo");
        containerPrompt.style.display = "";
        containerArchivo.style.display = "none";
    } else if (inputArchivo.checked) {
        console.log("Tipo Archivo está activo");
        containerPrompt.style.display = "none";
        containerArchivo.style.display = "";
    } else {
        console.log("Ninguna opción está activa");
    }
}