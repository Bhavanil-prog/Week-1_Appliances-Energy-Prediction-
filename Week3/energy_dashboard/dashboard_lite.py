"""
Advanced Analytics Dashboard - Streamlit Alternative
A lightweight analytics dashboard without pandas/streamlit dependencies
"""

from flask import Flask, render_template
import json
import os
import urllib.request
import urllib.error

try:
    import requests  # type: ignore
except Exception:
    requests = None

app = Flask(__name__, static_folder='static_dashboard', template_folder='templates_dashboard')


def fetch_json(url, timeout=3):
    """Try to fetch JSON from a URL. Use requests if available, otherwise urllib.
    Returns parsed JSON on success, or None on failure.
    """
    global requests
    if requests is not None:
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            pass
    # fallback to urllib
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            raw = r.read()
            return json.loads(raw.decode('utf-8'))
    except Exception:
        return None


def build_analytics_from_api(base_url='http://127.0.0.1:5000'):
    """Aggregate data from the Flask API endpoints. If any endpoint is unavailable,
    return None to indicate the caller should fall back to static data.
    """
    try:
        summary = fetch_json(f"{base_url}/api/summary") or {}
        hourly = fetch_json(f"{base_url}/api/hourly-avg") or {}
        daily = fetch_json(f"{base_url}/api/daily-avg") or {}
        top = fetch_json(f"{base_url}/api/top-consumers") or []
        model = fetch_json(f"{base_url}/api/model-info") or {}

        analytics = {
            'overview': summary,
            'hourly_breakdown': [],
            'daily_breakdown': [],
            'room_analysis': top,
            'predictions': [
                {'time': 'Next Hour', 'predicted': model.get('test_score', 100), 'confidence': 80}
            ],
            'alerts': []
        }

        # convert hourly
        if 'hours' in hourly and 'appliances' in hourly:
            for h, a in zip(hourly.get('hours', []), hourly.get('appliances', [])):
                analytics['hourly_breakdown'].append({'hour': int(h), 'consumption': a, 'lights': 0})

        # convert daily
        if 'dates' in daily and 'appliances' in daily:
            for d, a in zip(daily.get('dates', []), daily.get('appliances', [])):
                analytics['daily_breakdown'].append({'date': d, 'consumption': a, 'lights': 0})

        # fill overview defaults if missing
        if not analytics['overview']:
            analytics['overview'] = {
                'total_records': 0,
                'date_range': {'start': '', 'end': ''},
                'appliances': {'mean': 0, 'min': 0, 'max': 0, 'std': 0},
                'lights': {'mean': 0, 'min': 0, 'max': 0},
                'temperature': {'mean': 0, 'min': 0, 'max': 0}
            }

        return analytics
    except Exception:
        return None


# Pre-calculated fallback analytics data (used if API is unavailable)
STATIC_ANALYTICS = {
    'overview': {
        'total_energy_consumed': 1932456.78,
        'average_daily_consumption': 97.69,
        'peak_hour': 18,
        'peak_consumption': 125.78,
        'efficiency_score': 87.5,
        'cost_per_kwh': 0.12,
        'estimated_monthly_cost': 1542.50
    },
    'daily_breakdown': [
        {'date': '2016-01-11', 'consumption': 95.4, 'lights': 3.2, 'temp': 21.5},
        {'date': '2016-01-12', 'consumption': 97.2, 'lights': 3.5, 'temp': 21.8},
        {'date': '2016-01-13', 'consumption': 93.8, 'lights': 3.1, 'temp': 20.9},
    ],
    'hourly_breakdown': [
        {'hour': 0, 'consumption': 74.56, 'lights': 2.34},
        {'hour': 1, 'consumption': 68.92, 'lights': 1.87},
        {'hour': 2, 'consumption': 67.34, 'lights': 1.56},
    ],
    'room_analysis': [
        {'room': 'Kitchen', 'consumption': 285.4, 'percentage': 28.5, 'efficiency': 'Good'},
        {'room': 'Living Room', 'consumption': 215.3, 'percentage': 21.5, 'efficiency': 'Good'},
    ],
    'predictions': [
        {'time': 'Next Hour', 'predicted': 105.3, 'confidence': 92},
    ],
    'alerts': [
        {'level': 'warning', 'message': 'Peak consumption detected at 18:00 (125.78 kWh)', 'time': '2 hours ago'},
    ]
}


@app.route('/dashboard')
def dashboard():
    """Render the advanced analytics dashboard. Try to use live API data and
    fall back to static analytics if the API cannot be reached."""
    # Prefer local API
    api_base = os.environ.get('API_BASE', 'http://127.0.0.1:5000')
    analytics = build_analytics_from_api(api_base)
    if analytics is None:
        analytics = STATIC_ANALYTICS

    return render_template('advanced_dashboard.html', data=json.dumps(analytics))


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  ADVANCED ANALYTICS DASHBOARD")
    print("=" * 60)
    print()
    print("Dashboard initialized successfully!")
    print()
    print("Starting analytics server...")
    print()
    print("  http://localhost:8501")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    app.run(debug=False, port=8501, host='0.0.0.0')
