let canvas = document.getElementById("myChart");
let canvas2 = document.getElementById("myChart2");
let canvas3 = document.getElementById("myChart3");
let ctx = canvas.getContext("2d");
let ctx2 = canvas2.getContext("2d");
let ctx3 = canvas3.getContext("2d");

let myChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: [],
        datasets: [{
            label: "Por promedio de notas",
            data: [],
            backgroundColor: [
                "rgba(255, 99, 132, 0.5)",
                "rgba(54, 162, 235, 0.5)",
                "rgba(255, 206, 86, 0.5)",
                "rgba(75, 192, 192, 0.5)",
                "rgba(153, 102, 255, 0.5)",
                "rgba(255, 159, 64, 0.5)",
                "rgba(255, 99, 132, 0.5)",
                "rgba(54, 162, 235, 0.5)",
                "rgba(255, 206, 86, 0.5)",
                "rgba(75, 192, 192, 0.5)"
            ]
        }]
    },
    options: {
        indexAxis: "y",
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            x: {
                beginAtZero: true
            }
        }
    }
});

let myChart2 = new Chart(ctx2, {
    type: "line",
    data: {
        // labels: [
        //     "enero", "febrero", "marzo", "abril", "mayo", "junio",
        //     "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        // ],
        labels: [],
        datasets: [{
            label: 'Histórico de aciertos',
            data: [],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

let myChart3 = new Chart(ctx3, {
    type: "pie",
    data: {
        // labels: [
        //     "enero", "febrero", "marzo", "abril", "mayo", "junio",
        //     "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        // ],
        labels: ["Aciertos","Fallos"],
        datasets: [{
            label: 'Acertadas vs Falladas',
            data: [],
            backgroundColor:[
              "rgba(54, 162, 235, 0.5)",
              "rgba(255, 99, 132, 0.5)",
            ],
        }]
    },
    options:{
      maintainAspectRatio: false,
      responsive:true
    }
});

async function obtenerEstadisticasGenerales(){
    return fetch("/estadisticas/general").then(data =>{
        return data.json();
    }).catch(error => {
        console.log(error);
        return [];
    });
}

async function obtenerEstadisticasHistorico(mes="",anio="",desde="",hasta=""){
    // mes="",anio="",desde="",hasta=""
    let endpoint = `/estadisticas/historico`;
    if(mes == "1" && anio == "" && desde == "" && hasta == ""){
        endpoint =`/estadisticas/historico?mes=${mes}`;
    }else if(mes == "" && anio == "1" && desde == "" && hasta == ""){
        endpoint =`/estadisticas/historico?anio=${anio}`;
    }else if(desde != "" && hasta != ""){
        endpoint =`/estadisticas/historico?desde=${desde}&hasta=${hasta}`;
    }

    return fetch(endpoint).then(data =>{
        return data.json();
    }).catch(error => {
        console.log(error);
        return [];
    });
}

function cargarNumeroCuestionarios(data){
    let tablaEstadisticasBasicas = document.getElementById("estadisticasBasicas");
    let tbody = tablaEstadisticasBasicas.querySelector("tbody");
    let temas = Object.keys(data);
    temas.forEach(tema => {
        let row = document.createElement("tr");
        row.className = "text-center";
        // Celdas de la tabla
        let cellTema = document.createElement("td");
        cellTema.textContent = tema;
        cellTema.className = "fw-bold fs-6";
        let cellCompletados = document.createElement("td");
        cellCompletados.textContent = data[tema]["cuestionarios_realizados"];
        let cellRespondidas = document.createElement("td");
        cellRespondidas.textContent = data[tema]["preguntas_respondidas"];
        let cellAciertos = document.createElement("td");
        cellAciertos.textContent = data[tema]["respuestas_acertadas"];
        let cellPromedio = document.createElement("td");
        cellPromedio.textContent = data[tema]["nota_promedio"];
        // Guardamos las celdas
        row.appendChild(cellTema);
        row.appendChild(cellCompletados);
        row.appendChild(cellRespondidas);
        row.appendChild(cellAciertos);
        row.appendChild(cellPromedio);
        tbody.appendChild(row);
    });
}

obtenerEstadisticasGenerales().then(data =>{

    // Convertir en funcion
    let temas = Object.keys(data);
    myChart.data.labels = temas;
    
    temas.forEach(tema => {
        let promedio_tema = data[tema]["nota_promedio"];
        myChart.data.datasets[0].data.push(promedio_tema);
    });
    // -----------------------------------------------------
    cargarNumeroCuestionarios(data);

    myChart.update();
});

function cargarDatosHistorico(data){
    myChart2.data.labels = [];
    myChart2.data.datasets[0].data = [];
    myChart2.update();
    let fechas = Object.keys(data);
    console.log("Cargando historico");
    fechas.forEach(fecha => {
        myChart2.data.labels.push(fecha);
        let aciertos = data[fecha];
        myChart2.data.datasets[0].data.push(aciertos);
    });
    myChart2.update();
}

obtenerEstadisticasHistorico("1").then(data => {
    
    cargarDatosHistorico(data);
});

function filtroMes(){
    let desde = document.getElementById("desde").value;
    let hasta = document.getElementById("hasta").value;
    if(desde != "" && hasta != ""){
        obtenerEstadisticasHistorico("","",desde,hasta).then(data => {
            cargarDatosHistorico(data);
        });
    }
}

function cambioMes(){
    console.log("POR MES");
    obtenerEstadisticasHistorico("1","").then(data => {
        cargarDatosHistorico(data);
    });
}

function cambioAnio(){
    console.log("POR AÑO");
    obtenerEstadisticasHistorico("","1").then(data => {
        console.log(data);
        cargarDatosHistorico(data);
    });
}