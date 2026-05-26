# ML Car Price Predictor — Multi-Source Web App

A car-price prediction web app trained on scraped data from multiple Moroccan/regional used-car marketplaces. Combines web-scraping pipelines (Avito, Kifal, Moteur, Autocaz) with a regression model exposed through a Django front-end.

## How it works

1. **Scrape** listings from each source into CSVs:
   - `Avito.py` → `Avito_data.csv`
   - `Kifal.py` → `Kifal_data.csv`
   - `autocaz.py` → `autocaz.csv`
   - `Moteur_data.csv` from a separate pipeline
2. **Train** a regression model over the combined dataset using label-encoded categorical features (brand, fuel, transmission, body type — `*_encoder.pkl`).
3. **Predict** prices through the Django web UI.

## Stack

- **Scraping:** Selenium + ChromeDriver
- **ML:** scikit-learn (encoders persisted as `.pkl`)
- **Web:** Django (`core/` app, SQLite during development)

## Quick start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> and submit a car spec to get a predicted price.

### Re-scrape data

```bash
python Avito.py
python Kifal.py
python autocaz.py
```

> ⚠️ Selenium needs a matching ChromeDriver. The bundled `chromedriver.exe` may be outdated — replace with the version that matches your installed Chrome.

## Files

```
ML_Web_CarPricePredictor/
├── Avito.py / Avito_data.csv
├── Kifal.py / Kifal_data.csv
├── autocaz.py / autocaz.csv
├── Moteur_data.csv
├── *_encoder.pkl              # Persisted label encoders
├── car_ads/                   # Django app
├── core/                      # Django project
└── manage.py
```

## License

Educational / portfolio project. Respect each source site's terms of service when running the scrapers.
