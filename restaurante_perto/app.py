import os
import time
import math
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response, abort

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Defina GOOGLE_MAPS_API_KEY no arquivo .env")

# --------- Utilidades ---------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def to_price_signs(price_level):
    try:
        lvl = int(price_level)
        if lvl <= 0:
            return "R$"
        return "R$" * min(lvl + 1, 5)
    except Exception:
        return ""


def fetch_places_nearby(lat, lng, query, radius=3000, max_pages=2, open_now=None):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    results = []
    next_token = None

    for _ in range(max_pages):
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": "restaurant",
            "keyword": query,
            "key": GOOGLE_API_KEY,
            "language": "pt-BR",
        }
        if open_now:
            params["opennow"] = "true"
        if next_token:
            params["pagetoken"] = next_token

        try:
            resp = requests.get(base_url, params=params, timeout=10)
        except requests.RequestException as e:
            raise RuntimeError(f"Erro de conexão com Google Places: {e}") from e

        if resp.status_code != 200:
            raise RuntimeError(f"Google Places retornou HTTP {resp.status_code}")

        data = resp.json()
        status = data.get("status")
        if status == "OK":
            items = data.get("results", [])
            results.extend(items)
            next_token = data.get("next_page_token")
            if next_token:
                time.sleep(2.0)
            else:
                break
        elif status == "ZERO_RESULTS":
            break
        elif status in ("OVER_QUERY_LIMIT", "REQUEST_DENIED", "INVALID_REQUEST"):
            msg = data.get("error_message", status)
            raise RuntimeError(f"Erro da API do Google Places: {msg}")
        else:
            msg = data.get("error_message", status)
            raise RuntimeError(f"Falha na busca: {msg}")

    unique = {}
    for r in results:
        pid = r.get("place_id")
        if pid and pid not in unique:
            unique[pid] = r
    return list(unique.values())


def transform_place(place, origin_lat, origin_lng):
    loc = place.get("geometry", {}).get("location", {})
    plat, plng = loc.get("lat"), loc.get("lng")
    dist_km = None
    if isinstance(plat, (int, float)) and isinstance(plng, (int, float)):
        dist_km = round(haversine_km(origin_lat, origin_lng, plat, plng), 2)

    photo_ref = None
    photos = place.get("photos") or []
    if photos:
        photo_ref = photos[0].get("photo_reference")

    open_now = None
    if "opening_hours" in place:
        open_now = place["opening_hours"].get("open_now")

    return {
        "place_id": place.get("place_id"),
        "name": place.get("name"),
        "address": place.get("vicinity") or place.get("formatted_address"),
        "rating": place.get("rating"),
        "reviews": place.get("user_ratings_total"),
        "open_now": open_now,
        "price_level": place.get("price_level"),
        "price_signs": to_price_signs(place.get("price_level")),
        "lat": plat,
        "lng": plng,
        "distance_km": dist_km,
        "photo_url": f"/api/photo?ref={photo_ref}&maxwidth=400" if photo_ref else None,
        "business_status": place.get("business_status"),
    }


# ---------------- ROTAS ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json(silent=True) or {}

    query = (data.get("query") or "").strip()
    lat = data.get("latitude")
    lng = data.get("longitude")
    radius_km = float(data.get("radius_km") or 3.0)
    open_now = bool(data.get("open_now")) if data.get("open_now") is not None else None

    # 🔥 NOVO PARÂMETRO
    sort_by = data.get("sort_by", "distance").strip().lower()

    if not query:
        return jsonify({"error": "O campo 'query' é obrigatório."}), 400
    if lat is None or lng is None:
        return jsonify({"error": "Latitude e longitude são obrigatórios."}), 400

    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({"error": "Coordenadas inválidas."}), 400

    radius_m = max(200, min(int(radius_km * 1000), 10000))

    try:
        raw_places = fetch_places_nearby(
            lat, lng, query, radius=radius_m, max_pages=2, open_now=open_now
        )
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 502

    items = [transform_place(p, lat, lng) for p in raw_places]

    def passes_filters(item):
        if open_now and item.get("open_now") is False:
            return False
        return True

    filtered = list(filter(passes_filters, items))

    # -------- 🔥 NOVO SISTEMA DE ORDENAÇÃO ----------
    if sort_by == "rating":
        # ordenar por nota (maior para menor)
        filtered.sort(key=lambda x: float(x.get("rating") or 0), reverse=True)
    else:
        # padrão: ordenar por distância
        filtered.sort(key=lambda x: float(x.get("distance_km") or 9999))
    # ------------------------------------------------

    limited = filtered[:40]

    return jsonify(
        {
            "total_found": len(filtered),
            "returned": len(limited),
            "items": limited,
        }
    )


@app.route("/api/photo")
def api_photo():
    ref = request.args.get("ref")
    maxwidth = request.args.get("maxwidth", "400")
    if not ref:
        return abort(400, "Parâmetro 'ref' é obrigatório.")

    photo_url = "https://maps.googleapis.com/maps/api/place/photo"
    params = {
        "photo_reference": ref,
        "maxwidth": maxwidth,
        "key": GOOGLE_API_KEY,
    }

    try:
        resp = requests.get(photo_url, params=params, stream=True, timeout=10)
    except requests.RequestException:
        return abort(502, "Falha ao carregar foto do Google.")

    if resp.status_code != 200:
        return abort(resp.status_code)

    return Response(
        resp.iter_content(chunk_size=4096),
        content_type=resp.headers.get("Content-Type")
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
