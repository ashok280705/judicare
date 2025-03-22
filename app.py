from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Case duration and cost estimation logic
CASE_DURATIONS = {
    "Civil": {"District": 365, "High Court": 730, "Supreme Court": 1095},
    "Criminal": {"District": 540, "High Court": 1080, "Supreme Court": 1825},
    "Family": {"District": 400, "High Court": 800, "Supreme Court": 1200},
    "Property": {"District": 600, "High Court": 900, "Supreme Court": 1800},
    "Business": {"District": 500, "High Court": 1000, "Supreme Court": 1500}
}

CASE_COSTS = {
    "Civil": {"District": 20000, "High Court": 50000, "Supreme Court": 100000},
    "Criminal": {"District": 30000, "High Court": 70000, "Supreme Court": 150000},
    "Family": {"District": 25000, "High Court": 60000, "Supreme Court": 110000},
    "Property": {"District": 40000, "High Court": 90000, "Supreme Court": 160000},
    "Business": {"District": 35000, "High Court": 80000, "Supreme Court": 140000}
}

def calculate_predicted_date(case_type, court_level, filing_date):
    """Calculate case resolution date based on case type and court level."""
    try:
        filing_date_obj = datetime.strptime(filing_date, "%Y-%m-%d")
        duration_days = CASE_DURATIONS[case_type][court_level]
        predicted_date = filing_date_obj + timedelta(days=duration_days)
        return predicted_date.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error calculating date: {e}")
        return "Invalid Date"

def calculate_case_cost(case_type, court_level):
    """Calculate estimated case cost based on case type and court level."""
    try:
        return CASE_COSTS[case_type][court_level]
    except Exception as e:
        print(f"Error calculating cost: {e}")
        return "Invalid Cost"

@app.route('/')
def home():
    """Render the home page with the form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission and display predicted results."""
    case_type = request.form.get('case_type')
    court_level = request.form.get('court_level')
    filing_date = request.form.get('filing_date')

    if not (case_type and court_level and filing_date):
        return render_template('index.html', error="Please fill all fields.")

    # Calculate results
    predicted_date = calculate_predicted_date(case_type, court_level, filing_date)
    predicted_cost = calculate_case_cost(case_type, court_level)

    return render_template('index.html', predicted_date=predicted_date, predicted_cost=predicted_cost)

if __name__ == "__main__":
    app.run(debug=True)
