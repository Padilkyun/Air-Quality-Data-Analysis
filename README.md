# Air Pollution Analysis Dashboard

This Streamlit app visualizes air quality data based on multiple pollutants like PM2.5, PM10, SO2, NO2, CO, O3, and weather-related parameters such as temperature, humidity, pressure, rain, and wind speed. The dataset spans from **March 2013 to February 2017**.

## Features:
- **Date Range Filtering**: Filter the data by selecting a custom range for analysis.
- **City/Station Selection**: Allows users to select specific cities or stations for detailed analysis.
- **Trend Analysis**: View the trend of air pollutants (PM2.5, PM10) over time.
- **Pollution Distribution**: Display histograms and box plots of pollutant concentrations.
- **Correlation Analysis**: View how various pollutants are correlated with weather conditions.
- **RFM Analysis**: Evaluate cities' pollution levels based on Recency, Frequency, and Monetary scores.

## How to Run Locally

1. Clone this repository or download the files.
2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Streamlit app:
    ```bash
    streamlit run streamlit.py
    ```

## Requirements:
- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Numpy
- Babel

## Author:
- **Fadhillah Rahmad Kurnia**
- **MC184D5Y0386 || DBS Cooding Camp @ 2024 All Rights Reserved4**

