let preguntasContainer = document.querySelectorAll("form > .row > div.col-10 > .form-check");

preguntasContainer.forEach(container => {
    container.addEventListener("mouseover", onHoverQuestion);
    container.addEventListener("mouseout", onHoverOut);
    container.addEventListener("click",onClick);
});

function onHoverQuestion(e) {
    let container = e.currentTarget;
    // container.style
    // container.classList.remove("bg-light");
    // container.classList.add("bg-success", "bg-opacity-25",'text-white');
    // container.addEventListener("click",onClick);

}

function onHoverOut(e) {
    let container = e.currentTarget;
    // container.classList.remove("bg-success", "bg-opacity-25",'text-white');
    // container.classList.add("bg-light");
}

function onClick(e){
    let container = e.currentTarget;
    // if(container.classList.contains("bg-light")){
    //     container.classList.remove("bg-light");
    // }
    // container.classList.toggle("bg-success");
    // container.classList.toggle("bg-opacity-25");
    // container.classList.toggle("text-white");
    // container.classList.toggle("active")
    
}