const tokenData = JSON.parse(document.getElementById('token-data').textContent);

console.log("TOKEN DATA: ",tokenData);


function redirigirVerificarToken(){
    window.location.href = `/authentication/verified/${tokenData}`;
}

function contador(){
    let remaining = 5;
    const el = document.getElementById('countdown') || document.getElementById('contador');
    if (el) el.textContent = remaining;
    const iv = setInterval(() => {
        remaining--;
        if (el) el.textContent = remaining;
        console.log('Contador:', remaining);
        if (remaining <= 0) {
            clearInterval(iv);
            redirigirVerificarToken();
        }
    }, 1000);
}

contador();