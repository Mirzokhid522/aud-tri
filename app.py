from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trimmed-data')
def get_trimmed_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'trimmed_data.csv')
    
    if not os.path.exists(csv_path):
        return jsonify({"error": "trimmed_data.csv not found. Run downloader first."}), 404

    try:
        df = pd.read_csv(csv_path, skiprows=1)
        
        labels = []
        cpi = []
        trimmed = []
        
        for _, row in df.iterrows():
            if len(row) >= 3 and pd.notna(row.iloc[0]):
                label = str(row.iloc[0]).strip()
                
                # Skip summary, footnotes, or descriptive text rows
                if label.lower() in ['', 'nan', 'data source', 'note'] or label.startswith('(') or len(label) > 10:
                    continue
                
                try:
                    cpi_val = float(row.iloc[1]) if pd.notna(row.iloc[1]) else 0.0
                    trim_val = float(row.iloc[2]) if pd.notna(row.iloc[2]) else 0.0
                    
                    labels.append(label)
                    cpi.append(cpi_val)
                    trimmed.append(trim_val)
                except ValueError:
                    continue

        # Slice the data to the last 1 year (last 12 data points)
        if len(labels) > 12:
            labels = labels[-12:]
            cpi = cpi[-12:]
            trimmed = trimmed[-12:]

        return jsonify({
            "labels": labels,
            "cpi": cpi,
            "trimmed": trimmed
        })

    except Exception as e:
        return jsonify({"error": f"Parsing error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3455)