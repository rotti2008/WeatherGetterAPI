import requests as r
import tkinter as tk
import tkintermapview

MY_API_KEY = "16baa08414d20342aea624b4ef474cd2"



def get_cords(city_name):
    url_cords = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={MY_API_KEY}"
    response=r.get(url_cords,timeout=10)
    response.raise_for_status()
    data=response.json() # ist eine Liste
    if len(data)==0:
        raise ValueError("Diesen Ort gibt es nicht, wurde nicht gefunden!")
    lat=data[0]["lat"]
    lon=data[0]["lon"]
    return lat,lon

def get_data(lat,lon):
    url_data = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=de&appid={MY_API_KEY}"
    response=r.get(url_data,timeout=10)
    response.raise_for_status() # löst bei Fehlercode (4xx/5xx) einen HTTPError aus
    data=response.json()# ist ein Dictionary
    himmel=data["weather"][0]["main"]
    beschreibung=data["weather"][0]["description"]
    temperatur=data["main"]["temp"]
    luftfeuchtigkeit=data["main"]["humidity"]
    icon=data["weather"][0]["icon"]
    return himmel,beschreibung,temperatur,luftfeuchtigkeit,icon
      





# Hintergrundfarbe je nach Himmel ("main" aus der API)
FARBEN = {
    "Clear": "#f6c453",
    "Clouds": "#9aa5b1",
    "Rain": "#5b7fa6",
    "Drizzle": "#7a9cc0",
    "Thunderstorm": "#4a4e69",
    "Snow": "#dce8f0",
    "Mist": "#b8c4cc",
    "Fog": "#b8c4cc",
}
STANDARD_FARBE = "#8fb8de"

# Icon-Code der API (d = Tag, n = Nacht) -> Emoji
EMOJIS = {
    "01d": "☀️", "01n": "🌙",
    "02d": "⛅", "02n": "☁️",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️",
    "10d": "🌦️", "10n": "🌧️",
    "11d": "⛈️", "11n": "⛈️",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️",
}
STANDARD_EMOJI = "🌡️"  # falls der Code nicht im Dictionary steht


def show_weather():
    city = entry.get()  # Text aus dem Eingabefeld
    try:
        lat, lon = get_cords(city)
        sky, description, temp, humidity, icon = get_data(lat, lon)
    except ValueError as e:
        fehler.config(text=str(e))  # Meldung im Fenster statt print
        return  # Funktion hier beenden, nichts anzeigen
    except r.RequestException as e:
        fehler.config(text="Verbindungsproblem, bitte Internet und API-Key prüfen")
        return

    fehler.config(text="")  # alte Fehlermeldung löschen
    farbe = FARBEN.get(sky, STANDARD_FARBE)  # .get = Standardfarbe, falls unbekannt
    root.config(bg=farbe)
    for widget in (titel, ort_label, icon_label, temp_label, text_label, feucht_label, fehler):
        widget.config(bg=farbe)
    ort_label.config(text=city.title())
    temp_label.config(text=f"{round(temp,1)} °C")
    text_label.config(text=description.capitalize())
    feucht_label.config(text=f"Luftfeuchtigkeit: {humidity} %")
    icon_label.config(text=EMOJIS.get(icon, STANDARD_EMOJI))

    karte.delete_all_marker()  # alten Punkt entfernen
    karte.set_position(lat, lon)  # Karte auf den Ort zentrieren
    karte.set_zoom(11)
    karte.set_marker(lat, lon, marker_color_circle="red", marker_color_outside="red")  # roter Punkt


# --- Fenster aufbauen ---
root = tk.Tk()
root.title("Wetter")
root.geometry("400x760")
root.config(bg=STANDARD_FARBE)

titel = tk.Label(root, text="Wo soll es sein?", font=("Helvetica", 14), bg=STANDARD_FARBE)
titel.pack(pady=(25, 5))

entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
entry.pack(pady=5)
entry.bind("<Return>", lambda event: show_weather())  # Enter-Taste wie Button

button = tk.Button(root, text="Wetter anzeigen", font=("Helvetica", 12), command=show_weather)
button.pack(pady=10)

fehler = tk.Label(root, text="", fg="#b00020", bg=STANDARD_FARBE, wraplength=300)
fehler.pack()

ort_label = tk.Label(root, text="", font=("Helvetica", 22, "bold"), bg=STANDARD_FARBE)
ort_label.pack(pady=(20, 0))

icon_label = tk.Label(root, text="", font=("Noto Color Emoji", 48), bg=STANDARD_FARBE)
icon_label.pack()

temp_label = tk.Label(root, text="", font=("Helvetica", 48, "bold"), bg=STANDARD_FARBE)
temp_label.pack()

text_label = tk.Label(root, text="", font=("Helvetica", 16), bg=STANDARD_FARBE)
text_label.pack()

feucht_label = tk.Label(root, text="", font=("Helvetica", 12), bg=STANDARD_FARBE)
feucht_label.pack(pady=10)

karte = tkintermapview.TkinterMapView(root, width=360, height=250, corner_radius=0)
# OpenStreetMap blockiert den Standard-User-Agent von tkintermapview, CARTO will einen Key -> Esri-Kartenserver (ohne Key)
# Achtung: bei Esri steht {y} vor {x}
karte.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}")
karte.set_position(48.2, 16.37)  # Startansicht: Wien
karte.set_zoom(5)
karte.pack(pady=10)

root.mainloop()  # Fenster bleibt offen und wartet auf Klicks
