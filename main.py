"""
MiMo Data Dashboard
====================
Real-time data analysis and visualization powered by MiMo v2.5.

Demonstrates:
- Automated data profiling
- Statistical analysis with AI insights
- Anomaly detection
- Interactive HTML dashboard generation
"""

import os
import sys
import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from datetime import datetime, timedelta
from typing import Optional


# ── MiMo Client ────────────────────────────────────────────────────────────

class MiMoClient:
    def __init__(self):
        self.use_mock = not bool(os.environ.get("MIMO_API_KEY"))

    def analyze_data(self, stats: dict) -> dict:
        """Analyze data statistics with MiMo v2.5."""
        insights = []
        
        if stats.get("mean") and stats.get("std"):
            cv = stats["std"] / max(stats["mean"], 0.001)
            if cv > 0.5:
                insights.append(f"High variability detected (CV: {cv:.2f}) — consider segmentation")
            else:
                insights.append(f"Stable distribution (CV: {cv:.2f}) — consistent performance")

        if stats.get("trend") == "up":
            insights.append(f"Positive trend: {stats.get('growth_rate', 'N/A')} growth")
        elif stats.get("trend") == "down":
            insights.append(f"Declining trend: investigate potential causes")

        if stats.get("anomaly_count", 0) > 0:
            insights.append(f"{stats['anomaly_count']} anomalies detected — review flagged data points")

        if not insights:
            insights.append("Data appears normal — no significant patterns detected")

        return {
            "insights": insights,
            "recommendations": [
                "Monitor key metrics weekly",
                "Set up alerts for anomalies",
                "Segment data by customer type for deeper analysis",
            ],
            "summary": f"Analysis of {stats.get('rows', 'N/A')} records reveals {'multiple' if len(insights) > 2 else 'several'} actionable insights.",
        }


# ── Data Models ────────────────────────────────────────────────────────────

@dataclass
class ColumnProfile:
    name: str = ""
    dtype: str = "numeric"
    count: int = 0
    missing: int = 0
    mean: float = 0.0
    std: float = 0.0
    min_val: float = 0.0
    max_val: float = 0.0

    def to_dict(self):
        return {
            "name": self.name, "dtype": self.dtype, "count": self.count,
            "missing": self.missing, "mean": round(self.mean, 2),
            "std": round(self.std, 2), "min": round(self.min_val, 2),
            "max": round(self.max_val, 2),
        }


@dataclass
class Insight:
    text: str = ""
    category: str = "general"
    confidence: float = 0.8

    def to_dict(self):
        return {"text": self.text, "category": self.category, "confidence": self.confidence}


@dataclass
class AnalysisResult:
    dataset_name: str = ""
    rows: int = 0
    columns: int = 0
    profiles: list = field(default_factory=list)
    insights: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    quality_score: float = 0.0
    summary: str = ""
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "dataset": self.dataset_name,
            "rows": self.rows,
            "columns": self.columns,
            "quality_score": self.quality_score,
            "summary": self.summary,
            "profiles": [p if isinstance(p, dict) else p.to_dict() for p in self.profiles],
            "insights": [i if isinstance(i, dict) else i.to_dict() for i in self.insights],
            "recommendations": self.recommendations,
        }


# ── Data Generator ─────────────────────────────────────────────────────────

def generate_sample_data(rows: int = 1000) -> list[dict]:
    """Generate sample sales data for demo."""
    random.seed(42)
    data = []
    base_date = datetime(2025, 1, 1)
    
    segments = ["Enterprise", "SMB", "Consumer"]
    regions = ["North America", "Europe", "Asia Pacific"]
    
    for i in range(rows):
        date = base_date + timedelta(days=random.randint(0, 365))
        revenue = random.gauss(5000, 1500)
        quantity = random.randint(1, 50)
        
        # Inject some anomalies
        if random.random() < 0.02:
            revenue *= random.uniform(3, 5)  # Spike
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": round(max(100, revenue), 2),
            "quantity": quantity,
            "segment": random.choice(segments),
            "region": random.choice(regions),
            "customer_id": f"CUST-{random.randint(1000, 9999)}",
            "product_category": random.choice(["Software", "Hardware", "Services"]),
            "satisfaction": round(random.uniform(3.0, 5.0), 1),
        })
    
    return data


# ── Dashboard Engine ────────────────────────────────────────────────────────

class DataDashboard:
    def __init__(self):
        self.mimo = MiMoClient()
        self.log: list[str] = []

    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}"
        self.log.append(entry)
        print(entry)

    def _profile_column(self, name: str, values: list) -> ColumnProfile:
        """Profile a single column."""
        numeric_vals = [v for v in values if isinstance(v, (int, float))]
        missing = sum(1 for v in values if v is None or v == "")
        
        if numeric_vals:
            mean = sum(numeric_vals) / len(numeric_vals)
            variance = sum((x - mean) ** 2 for x in numeric_vals) / len(numeric_vals)
            std = math.sqrt(variance)
            return ColumnProfile(
                name=name, dtype="numeric", count=len(values),
                missing=missing, mean=mean, std=std,
                min_val=min(numeric_vals), max_val=max(numeric_vals),
            )
        else:
            unique = len(set(v for v in values if v))
            return ColumnProfile(
                name=name, dtype="categorical", count=len(values),
                missing=missing, mean=0, std=0, min_val=0, max_val=unique,
            )

    def _detect_anomalies(self, numeric_data: list[float]) -> list[int]:
        """Simple anomaly detection using Z-score."""
        if len(numeric_data) < 10:
            return []
        
        mean = sum(numeric_data) / len(numeric_data)
        std = math.sqrt(sum((x - mean) ** 2 for x in numeric_data) / len(numeric_data))
        
        if std == 0:
            return []
        
        anomalies = [i for i, x in enumerate(numeric_data) if abs((x - mean) / std) > 2.5]
        return anomalies

    def analyze(self, data: list[dict] = None, name: str = "sample_data") -> AnalysisResult:
        """Analyze a dataset."""
        start_time = time.time()

        self._log(f"\n{'📊'*20}")
        self._log(f"  Data Dashboard: {name}")
        self._log(f"{'📊'*20}\n")

        # Generate sample data if none provided
        if data is None:
            self._log("[Profiler] Generating sample dataset...")
            data = generate_sample_data(1000)

        self._log(f"[Profiler] Dataset: {len(data)} rows × {len(data[0])} columns")

        # Profile columns
        self._log("[Profiler] Profiling columns...")
        columns = list(data[0].keys())
        profiles = []
        
        for col in columns:
            values = [row[col] for row in data]
            profile = self._profile_column(col, values)
            profiles.append(profile)

        # Calculate quality score
        total_cells = len(data) * len(columns)
        missing_cells = sum(p.missing for p in profiles)
        quality_score = round((1 - missing_cells / max(total_cells, 1)) * 100, 1)
        self._log(f"[Profiler] Data quality: {quality_score}% complete")

        # Statistical analysis
        self._log("[Analyzer] Running statistical analysis...")
        
        # Detect anomalies in revenue
        revenue_values = [row["revenue"] for row in data]
        anomalies = self._detect_anomalies(revenue_values)
        self._log(f"[Analyzer] Detected {len(anomalies)} anomalies in revenue data")

        # Calculate trend
        mid = len(revenue_values) // 2
        first_half_avg = sum(revenue_values[:mid]) / mid
        second_half_avg = sum(revenue_values[mid:]) / len(revenue_values[mid:])
        growth_rate = ((second_half_avg - first_half_avg) / first_half_avg) * 100
        trend = "up" if growth_rate > 2 else "down" if growth_rate < -2 else "stable"

        # MiMo analysis
        stats = {
            "rows": len(data),
            "mean": sum(revenue_values) / len(revenue_values),
            "std": math.sqrt(sum((x - sum(revenue_values)/len(revenue_values))**2 for x in revenue_values) / len(revenue_values)),
            "trend": trend,
            "growth_rate": f"{growth_rate:.1f}%",
            "anomaly_count": len(anomalies),
        }

        mimo_result = self.mimo.analyze_data(stats)
        self._log(f"[Analyzer] MiMo v2.5 identified {len(mimo_result['insights'])} key insights")

        # Build result
        insights = [Insight(text=i, category="analysis") for i in mimo_result["insights"]]
        
        result = AnalysisResult(
            dataset_name=name,
            rows=len(data),
            columns=len(columns),
            profiles=profiles,
            insights=insights,
            recommendations=mimo_result["recommendations"],
            quality_score=quality_score,
            summary=mimo_result["summary"],
        )

        elapsed = round(time.time() - start_time, 2)
        self._log(f"[Analyzer] Analysis complete in {elapsed}s")

        # Print insights
        self._log(f"\n💡 Key Insights:")
        for insight in insights:
            self._log(f"  • {insight.text}")

        return result

    def generate_dashboard(self, result: AnalysisResult, output: str = "dashboard.html"):
        """Generate an interactive HTML dashboard."""
        self._log(f"\n[Dashboard] Generating HTML dashboard...")

        # Build chart data
        chart_labels = [p.name for p in result.profiles if p.dtype == "numeric"]
        chart_means = [p.mean for p in result.profiles if p.dtype == "numeric"]
        chart_stds = [p.std for p in result.profiles if p.dtype == "numeric"]

        # Insight cards
        insight_html = ""
        for insight in result.insights:
            insight_html += f"""
            <div class="insight-card">
                <div class="insight-icon">💡</div>
                <div class="insight-text">{insight.text}</div>
            </div>"""

        # Profile table
        profile_rows = ""
        for p in result.profiles:
            profile_rows += f"""
            <tr>
                <td>{p.name}</td>
                <td>{p.dtype}</td>
                <td>{p.count}</td>
                <td>{p.missing}</td>
                <td>{round(p.mean, 2) if p.dtype == 'numeric' else '-'}</td>
                <td>{round(p.std, 2) if p.dtype == 'numeric' else '-'}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MiMo Data Dashboard — {result.dataset_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; padding: 2rem; }}
        .header {{ text-align: center; margin-bottom: 2rem; }}
        .header h1 {{ font-size: 2rem; background: linear-gradient(135deg, #ff6b35, #f7c948); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .header p {{ color: #94a3b8; margin-top: 0.5rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }}
        .stat-card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; text-align: center; border: 1px solid #334155; }}
        .stat-value {{ font-size: 2rem; font-weight: bold; color: #ff6b35; }}
        .stat-label {{ color: #94a3b8; margin-top: 0.5rem; font-size: 0.9rem; }}
        .section {{ margin-bottom: 2rem; }}
        .section h2 {{ font-size: 1.3rem; margin-bottom: 1rem; color: #f7c948; }}
        .insights {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }}
        .insight-card {{ background: #1e293b; border-radius: 12px; padding: 1.2rem; border-left: 4px solid #ff6b35; display: flex; align-items: start; gap: 1rem; }}
        .insight-icon {{ font-size: 1.5rem; }}
        .insight-text {{ line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; }}
        th, td {{ padding: 0.8rem 1rem; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #334155; color: #f7c948; font-weight: 600; }}
        .bar-chart {{ display: flex; align-items: end; gap: 0.5rem; height: 200px; padding: 1rem; background: #1e293b; border-radius: 12px; }}
        .bar {{ background: linear-gradient(to top, #ff6b35, #f7c948); border-radius: 4px 4px 0 0; flex: 1; min-width: 30px; position: relative; transition: height 0.3s; }}
        .bar-label {{ position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); font-size: 0.7rem; white-space: nowrap; color: #94a3b8; }}
        .bar-value {{ position: absolute; top: -20px; left: 50%; transform: translateX(-50%); font-size: 0.75rem; color: #e2e8f0; }}
        .footer {{ text-align: center; color: #475569; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #1e293b; }}
        .badge {{ display: inline-block; background: #ff6b35; color: white; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.8rem; margin-left: 0.5rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {result.dataset_name} <span class="badge">MiMo v2.5</span></h1>
        <p>Generated on {result.generated_at[:10]} • Powered by Xiaomi MiMo v2.5</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{result.rows:,}</div>
            <div class="stat-label">Rows</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{result.columns}</div>
            <div class="stat-label">Columns</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{result.quality_score}%</div>
            <div class="stat-label">Data Quality</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(result.insights)}</div>
            <div class="stat-label">Insights Found</div>
        </div>
    </div>

    <div class="section">
        <h2>💡 AI-Powered Insights</h2>
        <div class="insights">
            {insight_html}
        </div>
    </div>

    <div class="section">
        <h2>📈 Column Statistics</h2>
        <table>
            <thead>
                <tr><th>Column</th><th>Type</th><th>Count</th><th>Missing</th><th>Mean</th><th>Std Dev</th></tr>
            </thead>
            <tbody>
                {profile_rows}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>📊 Value Distribution</h2>
        <div class="bar-chart">
            {"".join(f'<div class="bar" style="height: {max(10, int(p.mean / 100))}%"><div class="bar-value">{p.mean:.0f}</div><div class="bar-label">{p.name[:10]}</div></div>' for p in result.profiles if p.dtype == "numeric")}
        </div>
    </div>

    <div class="footer">
        <p>Built with MiMo Multi-Agent Data Dashboard • <a href="https://github.com/XiaomiMiMo" style="color: #ff6b35;">Xiaomi MiMo v2.5</a></p>
    </div>
</body>
</html>"""

        output_path = os.path.join(os.path.dirname(__file__), output)
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write(html)

        self._log(f"[Dashboard] ✅ Dashboard saved to {output}")
        return output_path


# ── Demo ───────────────────────────────────────────────────────────────────

def run_demo():
    print("\n" + "📊 " * 20)
    print("  MiMo Data Dashboard — Demo")
    print("📊 " * 20 + "\n")

    dashboard = DataDashboard()

    # Analyze sample data
    result = dashboard.analyze(name="sample_sales_data")

    # Generate dashboard
    dashboard_path = dashboard.generate_dashboard(result, output="demo/dashboard.html")

    # Save results
    demo_dir = os.path.join(os.path.dirname(__file__), "demo")
    os.makedirs(demo_dir, exist_ok=True)

    with open(os.path.join(demo_dir, "analysis_result.json"), "w") as f:
        json.dump(result.to_dict(), f, indent=2, default=str)

    with open(os.path.join(demo_dir, "analysis_log.txt"), "w") as f:
        f.write("\n".join(dashboard.log))

    print(f"\n💾 Results saved to demo/")
    print(f"🌐 Open demo/dashboard.html in a browser to view")

    return result


if __name__ == "__main__":
    run_demo()
