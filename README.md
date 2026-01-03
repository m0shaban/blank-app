# 🔌 Elkatamy Executive Dashboard - Denyo Generator Fleet Management

**Professional Industrial IoT Dashboard for Real-time Fleet Monitoring & Analytics**

## 📋 Overview

A comprehensive Streamlit-based executive dashboard designed for the CEO of Elkatamy, the exclusive agent for Denyo generators in Egypt. The dashboard provides real-time visibility into the fleet's operational and financial metrics, enabling data-driven decision-making for generator rental and maintenance operations.

## ✨ Key Features

### 🎛️ **Interactive Sidebar Controls**
- **Region Filter**: Multi-select filter for Egyptian governorates (Cairo, Giza, Alexandria, Aswan, Red Sea, Suez)
- **Status Filter**: Track Active, Idle, and Maintenance statuses
- **Capacity Range**: Dynamic slider for filtering by generator capacity (15-350 kVA)

### 📊 **Executive KPI Dashboard** (Top Row)
- **💰 Total Monthly Revenue**: Aggregated rental income with YoY trends
- **⚙️ Fleet Utilization Rate**: Real-time percentage of active generators
- **🚨 Critical Alerts Count**: Immediate identification of issues requiring attention
- **⛽ Average Fuel Efficiency**: Fleet-wide fuel level tracking

### 📍 **Geospatial Intelligence**
- Interactive map showing live generator locations across Egypt
- GPS coordinates with jitter for realistic positioning
- Real-time telemetry visualization

### 📈 **Financial Analytics**
- Revenue by Project Site (Top 10 ranking)
- Dynamic bar charts with color-coded gradient
- Drill-down capability through filters

### 🤖 **AI Insights & Predictive Maintenance**
- Automated maintenance alerts based on vibration/performance patterns
- Risk scoring for critical assets
- Actionable recommendations for technician dispatch

### ⚠️ **Active Alerts Table**
- Color-coded severity indicators (Red for critical)
- Filters for: Low Fuel, Overheating, Service Due
- Dynamic styling with real-time updates

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.0+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express
- **Styling**: Custom CSS + Streamlit Theme
- **Color Scheme**: Corporate Blue (#00a8e8) & Dark Grey (#1f2937)

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/m0shaban/blank-app.git
cd blank-app

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

The app will start on `http://localhost:8501`

## 🚀 Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and main file (`streamlit_app.py`)
6. Wait for deployment to complete

## 📊 Mock Data Features

The dashboard includes **50 realistic generator records** with:

| Property | Range | Details |
|----------|-------|---------|
| **Models** | 5 types | DCA-18ESX, DCA-25USI, DCA-45USI, DCA-150ESK, DCA-400ESK |
| **Capacity** | 15-350 kVA | Correlated with model type |
| **Locations** | 6 cities | Distributed across Egypt |
| **Revenue** | EGP 5K-500K | Monthly rental income |
| **Fuel Level** | 10-100% | Real-time consumption tracking |
| **Temperature** | 70-110°C | Engine health monitoring |

## 🎯 Business Value

### For CEO/Executive Level:
- ✅ Unified command center for fleet operations
- ✅ Instant visibility into revenue generation
- ✅ Predictive maintenance reduces unexpected downtime
- ✅ Resource optimization across regions
- ✅ Risk management through real-time alerts

### Decision-Making Insights:
1. **Operational**: Fleet utilization trending and capacity planning
2. **Financial**: Revenue by region and profitability analysis
3. **Maintenance**: Predictive alerts prevent costly failures
4. **Strategic**: Regional performance benchmarking

## 📝 Code Structure

```
streamlit_app.py
├── Page Configuration & Styling (Dark Theme)
├── Mock Data Generation (50 Generators)
├── Sidebar Controls (Filters)
├── KPI Dashboard Header
├── Geospatial Visualization (Map)
├── Financial Analytics (Revenue Charts)
├── AI Insights Section
├── Active Alerts Table
└── Footer
```

## 🔐 Security Notes

- Mock data is for demonstration purposes
- All revenue figures are simulated
- Connect to real databases by modifying `get_fleet_data()` function
- Implement authentication via Streamlit Secrets for production

## 📞 Support

For questions or customizations, please refer to:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)

## 📄 License

MIT License - See LICENSE file

---

**Built with ❤️ for Elkatamy Power Systems**

*Last Updated: January 2026*
