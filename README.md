# Google-Form-Sentiment-Analysis

![Logo](https://cdn-icons-png.flaticon.com/512/9850/9850903.png)

## Overview

The **Sentiment Analysis System** is a web application designed to perform sentiment analysis on text data using Natural Language Processing (NLP). It categorizes sentiments into Positive, Negative, and Neutral and visualizes the results using various types of plots. The app is built using Python and leverages libraries like Streamlit, pandas, VADER Sentiment, and Plotly for a seamless data analysis and visualization experience.

## Features

- **Sentiment Analysis**: The system analyzes text data from a Google Spreadsheet and classifies it into three sentiment categories: Positive, Negative, and Neutral.
- **Data Visualization**: The app provides multiple visualization options, including Pie Charts, Histograms, and Scatter Plots, to better understand the sentiment distribution.
- **Interactive User Interface**: The application is built with Streamlit, making it highly interactive and user-friendly.

## Libraries Used

- **Streamlit**: For building the web application interface.
- **pandas**: For data manipulation and analysis.
- **VADER Sentiment**: For performing sentiment analysis on text data.
- **Plotly**: For creating interactive plots and charts.
- **Google Sheets API**: For accessing and retrieving data from Google Spreadsheets.

## How It Works

1. **Home**: Provides an introduction to the application, describing its purpose and functionalities.
2. **Analysis**:
   - Users input their Google Spreadsheet ID and specify the range and column to be analyzed.
   - The app retrieves the data, performs sentiment analysis using VADER Sentiment, and saves the results as a CSV file (`results.csv`).
3. **Results**:
   - Displays the analyzed data in a tabular format.
   - Users can choose between different visualization types (Pie Chart, Histogram, Scatter Plot) to explore the sentiment analysis results.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sentiment-analysis-system.git
   cd sentiment-analysis-system
   ```
2. Install the required Python packages:
   ```bash
   pip install streamlit pandas google-auth-oauthlib google-api-python-client vaderSentiment plotly
   ```
3. Obtain the `key.json` file for Google Sheets API authentication and place it in the project directory.
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

- **Home**: Learn about the app's functionalities.
- **Analysis**: Enter your Google Spreadsheet ID, define the range and column for analysis, and start the sentiment analysis.
- **Results**: View and explore the sentiment analysis results through interactive visualizations.

## Screenshots

- **Home Page**: ![Home](https://media.sproutsocial.com/uploads/2023/07/Sentiment-analysis-HUB-Final.jpg)
- **Results Visualization**:
-  ![image](https://github.com/user-attachments/assets/3506ddfd-79ac-4a69-ab5e-a2ad4f69071c)
- ![image](https://github.com/user-attachments/assets/757012e3-a875-4361-a520-2f85a29425bf)
- ![image](https://github.com/user-attachments/assets/3549e999-85cb-4c7c-bbab-61665782adb2)



## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.
