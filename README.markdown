# AI-Based Threat Intelligence Platform

## Overview
The AI-Based Threat Intelligence Platform is a web-based application that aggregates, analyzes, and visualizes real-time threat intelligence data from the AlienVault Open Threat Exchange (OTX) API. Built using Python and Streamlit, this platform provides security analysts and organizations with actionable insights through interactive dashboards, anomaly detection, and search capabilities. The project was developed as part of the VIT AI Project (Team ID: PNT2022TMIDxxxxxx) and completed on September 22, 2025, at 10:00 PM IST.

## Features
- **Real-Time Data Fetching**: Pulls threat intelligence data from the OTX API.
- **Interactive Visualizations**: Displays top indicators, country heatmaps, threat trends, and type distributions using Plotly.
- **Anomaly Detection**: Identifies unusual threat patterns using scikit-learn's IsolationForest algorithm.
- **Search Functionality**: Allows users to search for specific Indicators of Compromise (IoCs) like IPs, domains, and URLs.
- **Data Export**: Exports threat data as a CSV file for further analysis.
- **Customizable Filters**: Supports date range filtering (Last 24h, 7 Days, 30 Days, All).

## Prerequisites
- Python 3.8 or higher
- Required Python packages: `streamlit`, `requests`, `pandas`, `plotly`, `scikit-learn`, `sqlite3`
- An AlienVault OTX API key (obtainable from https://otx.alienvault.com/)

## Installation

1. **Clone the Repository**
   ```bash
   git clone github link
   cd ai-threat-intelligence-platform
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Note: Create a `requirements.txt` file with the following content if not already present:
   ```
   streamlit==1.28.0
   requests==2.31.0
   pandas==2.1.4
   plotly==5.18.0
   scikit-learn==1.3.2
   ```

4. **Configure the OTX API Key**
   - Set the API key as an environment variable:
     ```bash
     export OTX_API_KEY="your_api_key_here"
     ```
   - Alternatively, replace the default key in `threat_dashboard.py` (line 13) with your own.

5. **Run the Application**
   ```bash
   streamlit run threat_dashboard.py
   ```
   Open your browser and navigate to the URL provided (e.g., `http://localhost:8501`).

## Usage
1. **Fetch Data**: Click "Fetch Latest Threat Data" to pull real-time threat intelligence from OTX.
2. **Load Sample Data**: Use "Load Sample Threat Data" (if implemented) to test with mock data.
3. **Explore Visualizations**: View charts under "Top 10 Malicious Indicators," "Threats by Country," "Threat Trends," and "Indicator Type Distribution."
4. **Search Indicators**: Enter an IP, domain, or URL (e.g., `http://185.196.8.175/login.php`) in the search bar.
5. **Export Data**: Click "Download Threat Data as CSV" to save the current dataset.
6. **Filter Data**: Use the date range radio buttons to adjust the time scope.

## Project Structure
- `threat_dashboard.py`: Main application file containing the Streamlit dashboard logic.
- `threat_data.db`: SQLite database storing fetched threat data (auto-generated).
- `README.md`: This file.
- `requirements.txt`: List of Python dependencies (create if missing).

## Development Timeline
- **Planning**: October 2022 (Sprints 1-4 completed by November 19, 2022).
- **Development**: Ongoing refinements leading to completion on September 22, 2025.
- **Sprints**:
  - Sprint-1: Data Collection (24-29 Oct 2022)
  - Sprint-2: Data Analysis (31 Oct-05 Nov 2022)
  - Sprint-3: User Interface (07-12 Nov 2022)
  - Sprint-4: Export Functionality (14-19 Nov 2022)

## Contributing
We welcome contributions to enhance this platform! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request with a detailed description of your changes.

Please adhere to the following guidelines:
- Follow PEP 8 style guidelines for Python code.
- Include tests for new features.
- Update documentation as needed.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details (create a `LICENSE` file with MIT terms if not present).

## Acknowledgments
- AlienVault for providing the OTX API.
- Streamlit, Plotly, and scikit-learn communities for open-source tools.
- VIT AI Project Team for guidance and support.

---

Last updated: September 22, 2025, 10:00 PM IST