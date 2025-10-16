let respuestasSeleccionadas = {};
const cuestionario = JSON.parse(document.getElementById('cuestionario-data').textContent);
function editarPregunta(e){
    let boton = e.target.closest("button");
    let nPregunta = boton.id.split("-").at(1);
    let idContainerRespuestas = "respuestas-pregunta-"+nPregunta;
    console.log(idContainerRespuestas);
    let containerPregunta = document.getElementById(idContainerRespuestas);
    let respuestasPregunta = containerPregunta.querySelectorAll(".form-check");
    if(boton.classList.contains("button-edit")){ 
        console.log("Container respuestas: ",containerPregunta);
        console.log("Respuestas pregunta: ",respuestasPregunta);
        respuestasSeleccionadas[nPregunta] = {};
        respuestasSeleccionadas[nPregunta]["pregunta"] = containerPregunta.children[0].querySelector("h2").textContent;
        let preguntaTitulo = document.createElement("input");
        preguntaTitulo.type = "text";
        preguntaTitulo.className = "form-control";
        preguntaTitulo.value = respuestasSeleccionadas[nPregunta]["pregunta"];
        // Inserta el input antes del h2 existente
        containerPregunta.children[0].insertBefore(preguntaTitulo, containerPregunta.children[0].querySelector("h2"));
        // containerPregunta.children[0].appendChild(preguntaTitulo);
        containerPregunta.children[0].querySelector("h2").remove();
        respuestasPregunta.forEach(element => {
            let idRespuesta = element.querySelector("input").id;
            let valorRespuesta = element.querySelector("label").textContent;
            respuestasSeleccionadas[nPregunta][idRespuesta] = valorRespuesta;
        });
        console.log("Respuestas seleccionadas: ",respuestasSeleccionadas);
        respuestasPregunta.forEach(element => {
            // Elimina el label existente
            let label = element.querySelector("label");
            if (label) {
                label.remove();
            }
            // Crea un input de texto con el valor anterior
            let inputEdit = document.createElement("input");
            inputEdit.type = "text";
            inputEdit.className = "form-control mb-2";
            inputEdit.id = element.querySelector("input").id;
            // Opcional: coloca el valor anterior en el input
            let valorAnterior = respuestasSeleccionadas[nPregunta][element.querySelector("input").id];
            inputEdit.value = (valorAnterior || "").trim().replace(/\n/g, "");
            let inputRadio = element.querySelector("input");
            inputRadio.remove();
            element.classList.remove("save");
            let container = element.querySelector("div");
            container.remove();
            element.appendChild(inputEdit);
        });
        console.log("Respuestas preguntas edit: ",respuestasPregunta);
        boton.classList.remove("button-edit");
        boton.classList.add("button-save");
        let icono = boton.querySelector("i");
        icono.className = "bi bi-floppy2-fill";
    }else if(boton.classList.contains("button-save")){
        boton.classList.remove("button-save");
        boton.classList.add("button-edit");
        let icono = boton.querySelector("i");
        icono.className = "bi bi-pencil-fill";
        let respuestasSeleccionadasEditadas = {};
        let tituloPreguntaEditado = containerPregunta.children[0].querySelector("input").value;
        let tituloPregunta = document.createElement("h2");
        tituloPregunta.className = "fs-3 mb-3";
        tituloPregunta.textContent = tituloPreguntaEditado;
        let inputTitulo = containerPregunta.children[0].querySelector("input");
        inputTitulo.remove();
        containerPregunta.children[0].insertBefore(tituloPregunta, containerPregunta.children[0].firstChild);
        respuestasPregunta.forEach(element => {
            let idRespuesta = element.querySelector("input").id;
            let valorRespuesta = element.querySelector("input").value;
            respuestasSeleccionadasEditadas[idRespuesta] = valorRespuesta;
        });
        console.log("Editadas: ",respuestasSeleccionadasEditadas);
        Object.keys(respuestasSeleccionadas).forEach(key => {
            // key es el idRespuesta
            // respuestasSeleccionadasEditadas[key] es el valor editado
            if(respuestasSeleccionadas[nPregunta][key] != respuestasSeleccionadasEditadas[key] && key != "pregunta"){
                respuestasSeleccionadas[nPregunta][key] = respuestasSeleccionadasEditadas[key];
            }
        });
        respuestasPregunta.forEach(element => {
            let container = document.createElement("div");
            container.className = "d-flex flex-row justify-content-center align-items-center px-2";
            let idRespuesta = element.querySelector("input").id;
            let valorRespuesta = element.querySelector("input").value;
            // respuestasSeleccionadasEditadas[idRespuesta] = valorRespuesta;
            element.querySelector("input").remove();
            let inputRadio = document.createElement("input");
            inputRadio.type = "radio";
            inputRadio.name = nPregunta;
            inputRadio.value = idRespuesta;
            inputRadio.id = idRespuesta;
            inputRadio.className = "form-check-input";
            let labelInput = document.createElement("label");
            labelInput.className = "form-check-label fs-6 ms-1 w-100 h-100 py-2";
            labelInput.htmlFor = idRespuesta;
            labelInput.textContent = valorRespuesta;
            element.classList.add("save");
            container.appendChild(inputRadio);
            container.appendChild(labelInput);
            element.appendChild(container);
        });
        
        delete respuestasSeleccionadas[nPregunta];
        console.log("Respuestas editadas: ",respuestasSeleccionadas);
    }
}

function guardarFormulario(e){
    e.preventDefault();
    let formulario = document.querySelector("form");
    let preguntasCols = formulario.querySelectorAll(".row > div");
    cuestionario["cuestionario_preguntas"] = [];
    for(let col = 0; col < preguntasCols.length-1; col++){
        let preguntaCol = preguntasCols[col];
        let preguntaObject = {};
        let hijos = preguntaCol.children;
        // Obtenemos la pregunta que siempre es el primer hijo de cada col
        let pregunta = hijos[0].querySelector("h2").textContent;
        preguntaObject["pregunta"] = pregunta;
        // Iteramos en las respuestas
        preguntaObject["opciones"] = [];
        let respuesta_correcta = 0;
        for (let i = 1; i < hijos.length; i++) {
            let hijo = hijos[i]; // Este es el div.form-check, que contiene input y label
            let opcion = hijo.querySelector("label").textContent;
            let input = hijo.querySelector("input");
            if(input.checked){
                respuesta_correcta = i - 1;
            }
            preguntaObject["opciones"].push(opcion);
        }
        // Solo de prueba, luego corregir
        preguntaObject["respuesta_correcta"] = respuesta_correcta;
        cuestionario["cuestionario_preguntas"].push(preguntaObject);
    }
    console.log(cuestionario);
    postCuestionario().then(data => {
        console.log("Respuesta: ",data);
        if(data.success == true){
            window.location.href = `/cuestionarios/contestar/${data.idCuestionario}`;
        }
    })
}

async function postCuestionario(){
    let endpoint = "/cuestionarios/crear";
    return await fetch(endpoint,{
       method:"POST" ,
       headers:{
        "Content-Type":"application/json",
        'X-CSRFToken': getCookie('csrftoken')
       },
       body:JSON.stringify({
        "nombre":cuestionario["nombre"],
        "tema":cuestionario["tema"],
        "descripcion":cuestionario["descripcion"],
        "cuestionario":cuestionario["cuestionario_preguntas"],
        "enlace":"guardar"
       })
    }).then(response => {
        return response.json();
    }).catch(error => {
        console.log("Error: ",error);
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Verifica si esta cookie es la que queremos
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}