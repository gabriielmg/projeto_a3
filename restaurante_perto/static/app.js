// ---------------------------
// MENU HAMBÚRGUER → FILTROS
// ---------------------------
const icon = document.getElementById("menuIcon");
const popupFiltros = document.getElementById("popupFiltros");

// Abrir popup
icon.onclick = () => {
    popupFiltros.classList.add("show");
};

// Fechar popup
function fecharFiltros() {
    popupFiltros.classList.remove("show");
}

// FECHAR POPUP AO CLICAR FORA
document.addEventListener("click", function (event) {
    // Se o popup não estiver aberto → não faz nada
    if (!popupFiltros.classList.contains("show")) return;

    // Se clicou fora do conteúdo e fora do ícone do menu
    if (!event.target.closest(".popup-content") && event.target !== icon) {
        fecharFiltros();
    }
});

// --------------------------
// FUNÇÃO PRINCIPAL DE BUSCA
// --------------------------
async function buscar(filtro = null) {
    const query = document.getElementById("query").value.trim();
    const resultado = document.getElementById("resultado");

    resultado.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <div class="loading-text">Buscando restaurantes...</div>
        </div>
    `;

    navigator.geolocation.getCurrentPosition(async (pos) => {

        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        const payload = {
            query,
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

        let items = data.items;

        // ⭐ Melhor avaliados
        if (filtro === "avaliados") {
            items.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        }

        // 🔥 Mais populares
        if (filtro === "reviews") {
            items.sort((a, b) => (b.reviews || 0) - (a.reviews || 0));
        }

        // Fecha o popup após aplicar o filtro
        fecharFiltros();

        resultado.innerHTML = "";

        items.forEach(item => {
            resultado.innerHTML += `
                <div class="card" onclick="abrirPopup(${item.lat}, ${item.lng})">
                    <div class="card-img">
                        ${item.photo_url 
                            ? `<img src="${item.photo_url}">`
                            : `<img src="/static/no-img.png">`
                        }
                    </div>

                    <h3>${item.name}</h3>
                    <p>${item.address}</p>

                    <p>⭐ ${item.rating || "?"} (${item.reviews || 0} avaliações)</p>
                    <p>${item.distance_km} km de distância</p>
                </div>
            `;
        });

    }, () => {
        resultado.innerHTML = "Permita acesso à localização.";
    });
}

// BOTÕES DOS FILTROS
function buscarAvaliados() {
    buscar("avaliados");
}

function buscarPopulares() {
    buscar("reviews");
}

// ------------------------------------
// POPUP DE CONFIRMAÇÃO
// ------------------------------------
let destinoLat = null;
let destinoLng = null;

function abrirPopup(lat, lng) {
    const popup = document.getElementById("popupConfirmar");
    popup.classList.remove("show");

    setTimeout(() => {
        destinoLat = lat;
        destinoLng = lng;
        popup.classList.add("show");
    }, 150);
}

document.getElementById("btnSim").onclick = function () {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${destinoLat},${destinoLng}`;
    window.open(url, "_blank");
    document.getElementById("popupConfirmar").classList.remove("show");
};

document.getElementById("btnNao").onclick = function () {
    document.getElementById("popupConfirmar").classList.remove("show");
};
