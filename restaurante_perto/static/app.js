async function buscar() {
    const query = document.getElementById("query").value.trim();
    const resultado = document.getElementById("resultado");

    // LOADING ANIMADO
    resultado.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <div class="loading-text">Buscando restaurantes...</div>
        </div>
    `;

    if (!query) {
        resultado.innerHTML = "Digite algo para buscar.";
        return;
    }

    // pegar localização do usuário
    navigator.geolocation.getCurrentPosition(async (pos) => {

        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        const payload = {
            query: query,
            latitude: lat,
            longitude: lng,
            radius_km: 3,
            min_rating: 0,
            min_reviews: 0,
            open_now: false
        };

        const resp = await fetch("/api/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await resp.json();

        if (!data.items || data.items.length === 0) {
            resultado.innerHTML = "Nenhum restaurante encontrado.";
            return;
        }

        resultado.innerHTML = "";

        data.items.forEach(item => {
            resultado.innerHTML += `
                <div class="card" onclick="abrirPopup(${item.lat}, ${item.lng})">

                    <div class="card-img">
                        ${item.photo_url 
                            ? `<img src="${item.photo_url}">`
                            : `<img src="/static/no-img.png">`
                        }
                    </div>

                    <div class="card-info">
                        <h3>${item.name}</h3>
                        <p>${item.address}</p>
                        <p>⭐ ${item.rating || "?"} (${item.reviews || 0} avaliações)</p>
                        <p>${item.distance_km} km de distância</p>
                    </div>

                </div>
            `;
        });

    }, () => {
        resultado.innerHTML = "Permita acesso à localização.";
    });
}


// ========================================================
//              POPUP + REDIRECIONAMENTO MAPS
// ========================================================

let destinoLat = null;
let destinoLng = null;

// abrir popup
function abrirPopup(lat, lng) {

    // FECHA QUALQUER POPUP ABERTO ANTES DE ABRIR OUTRO
    const popup = document.getElementById("popup");
    popup.classList.remove("show");

    setTimeout(() => {
        destinoLat = lat;
        destinoLng = lng;
        popup.classList.add("show");
    }, 150); // pequeno delay para garantir animação suave
}

// botão SIM → abre o Maps
document.getElementById("btnSim").onclick = function () {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${destinoLat},${destinoLng}`;
    window.open(url, "_blank");
    document.getElementById("popup").classList.remove("show");
};

// botão NÃO → apenas fecha
document.getElementById("btnNao").onclick = function () {
    document.getElementById("popup").classList.remove("show");
};
