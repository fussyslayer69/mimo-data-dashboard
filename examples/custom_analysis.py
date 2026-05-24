# Example: Custom Dataset Analysis
from dashboard import DataDashboard, generate_sample_data

def example_custom_analysis():
    """Analyze a custom dataset."""
    dashboard = DataDashboard()

    # Generate custom data
    data = generate_sample_data(500)

    # Analyze
    result = dashboard.analyze(data=data, name="custom_dataset")

    # Generate dashboard
    dashboard.generate_dashboard(result, output="custom_dashboard.html")

    print(f"Dashboard generated with {len(result.insights)} insights")

if __name__ == "__main__":
    example_custom_analysis()
