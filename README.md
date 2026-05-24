# MiMo Data Dashboard

> 📊 Real-time data analysis and visualization powered by MiMo v2.5

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5)
![MiMo](https://img.shields.io/badge/MiMo-v2.5-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

An intelligent data analysis system that processes datasets, generates insights, and creates interactive dashboards. Uses MiMo v2.5's reasoning to identify patterns, anomalies, and actionable insights.

**Key capabilities:**
- Automated data profiling and quality assessment
- Statistical analysis with AI-powered insights
- Anomaly detection and trend identification
- Interactive HTML dashboard generation
- Natural language insights and recommendations

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              Data Dashboard Engine                     │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Profiler │  │ Analyzer │  │  Dashboard Gen   │   │
│  │  Agent   │  │  (MiMo)  │  │    (HTML)        │   │
│  └─────┬────┘  └─────┬────┘  └────────┬─────────┘   │
│        │              │                 │              │
│  ┌─────▼──────────────▼─────────────────▼────────┐   │
│  │              Data Pipeline                      │   │
│  │  [Ingest] → [Profile] → [Analyze] → [Visualize]│  │
│  └───────────────────────────────────────────────┘   │
│        │              │                 │              │
│  ┌─────▼──┐    ┌─────▼──┐    ┌────────▼────────┐   │
│  │  CSV/  │    │  Stats │    │   HTML/CSS/JS   │   │
│  │  JSON  │    │ Engine │    │   Dashboard     │   │
│  └────────┘    └────────┘    └─────────────────┘   │
└──────────────────────────────────────────────────────┘
```

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/mimo-data-dashboard.git
cd mimo-data-dashboard

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export MIMO_API_KEY="your-api-key"  # Optional

python main.py --demo
```

## Usage

```python
from dashboard import DataDashboard

dashboard = DataDashboard()

# Load and analyze data
result = dashboard.analyze("data/sales.csv")

# Generate dashboard
dashboard.generate_dashboard(result, output="dashboard.html")

# Access insights
for insight in result.insights:
    print(f"💡 {insight}")
```

## Demo

```bash
python main.py --demo
```

Expected output:

```
[Profiler] Loading dataset: sample_sales.csv
[Profiler] 1,000 rows × 8 columns detected
[Profiler] Data quality: 94.2% complete
[Analyzer] Running statistical analysis...
[Analyzer] MiMo v2.5 identified 3 key trends
[Analyzer] Detected 12 anomalies (1.2% of data)
[Dashboard] Generating interactive HTML dashboard...
[Dashboard] ✅ Dashboard saved to demo/dashboard.html

📊 Key Insights:
  1. Revenue increased 23% QoQ — strongest in Enterprise segment
  2. Customer churn rate dropped to 4.2% (industry avg: 6.8%)
  3. Peak sales occur on Tuesdays, 2-4 PM
```

## Demo Output

<!-- ![Dashboard](demo/dashboard_screenshot.png) -->

## Roadmap

- [ ] Real-time streaming data support
- [ ] More chart types (scatter, heatmap, treemap)
- [ ] Export to PDF reports
- [ ] Database connector plugins

## License

MIT License — see [LICENSE](LICENSE).

---

*Powered by [Xiaomi MiMo v2.5](https://github.com/XiaomiMiMo)*
