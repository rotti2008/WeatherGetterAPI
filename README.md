# WeatherGetterAPI

Kleine Wetter-App mit Fenster (tkinter), entstanden im Schulfach FSST (4BHEL).
Man gibt einen Ort ein und bekommt das aktuelle Wetter mit Emoji, Temperatur, Luftfeuchtigkeit und einer Karte mit rotem Punkt.

## Funktionen
- Ortssuche über die Geocoding-API von OpenWeatherMap
- Aktuelles Wetter in Celsius mit deutscher Beschreibung
- Wetter-Emoji (Tag und Nacht) und Hintergrundfarbe passend zum Wetter
- Kartenausschnitt mit rotem Punkt am Ort
- Fehlermeldungen im Fenster (Ort nicht gefunden, kein Internet, falscher API-Key)

## Voraussetzungen
- Python 3
- Tk für Python (unter Arch Linux: `sudo pacman -S tk`)
- Ein kostenloser API-Key von [OpenWeatherMap](https://openweathermap.org/api)

## Installation
```bash
python -m venv --system-site-packages .venv
source .venv/bin/activate
pip install requests tkintermapview
```

Danach in `API.py` bei `MY_API_KEY` den eigenen Key eintragen.

## Starten
```bash
source .venv/bin/activate
python API.py
```

## Bedienung
Ort ins Eingabefeld schreiben und auf „Wetter anzeigen" klicken oder Enter drücken.

## Aufbau
| Teil | Aufgabe |
|---|---|
| `get_cords(city_name)` | holt die Koordinaten eines Ortes |
| `get_data(lat, lon)` | holt das aktuelle Wetter |
| `show_weather()` | aktualisiert das Fenster |
| `EMOJIS`, `FARBEN` | ordnen dem Wetter Emoji und Hintergrundfarbe zu |

## Quellen
- Wetterdaten: [OpenWeatherMap](https://openweathermap.org/)
- Karte: Esri World Street Map (Esri, HERE, Garmin, OpenStreetMap-Mitwirkende), über [tkintermapview](https://github.com/TomSchimansky/TkinterMapView)
