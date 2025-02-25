import streamlit as st
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Set page configuration
st.set_page_config(
    page_title="Sentiment Analysis System",
    page_icon="https://cdn-icons-png.flaticon.com/512/9850/9850903.png",
    layout="wide"
)

st.title("SENTIMENT ANALYSIS SYSTEM")

# Sidebar navigation
choice = st.sidebar.selectbox("My Menu", ("HOME", "ANALYSIS", "RESULTS"))

if choice == "HOME":
    st.image("https://camo.githubusercontent.com/1fa27ef9b772b945093204377c5b4509f15b3f04aba8297863b765aa68571f10/68747470733a2f2f6d656469612e7370726f7574736f6369616c2e636f6d2f75706c6f6164732f323032332f30372f53656e74696d656e742d616e616c797369732d4855422d46696e616c2e6a7067")
    st.write("1. This is a Natural Language Processing application that can analyze sentiment from text data.")
    st.write("2. It categorizes sentiment into Positive, Negative, or Neutral.")
    st.write("3. The application visualizes results based on factors such as age, gender, language, and city.")

elif choice == "ANALYSIS":
    sid = st.text_input("Enter your Google Sheet ID")
    r = st.text_input("Enter Range (e.g., Sheet1!A1:D100)")
    c = st.text_input("Enter column name to be analyzed")
    btn = st.button("Analyze")

    if btn:
        try:
            # Create credentials from your service account key file (named key.json)
            credentials = service_account.Credentials.from_service_account_file(
                "key.json",
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            
            # Build the Google Sheets API service
            service = build("sheets", "v4", credentials=credentials).spreadsheets().values()
            result = service.get(spreadsheetId=sid, range=r).execute()
            data = result.get('values', [])
            
            if not data or len(data) < 2:
                st.error("The provided range does not contain enough data.")
            else:
                # Convert data to a DataFrame
                df = pd.DataFrame(data=data[1:], columns=data[0])
                analyzer = SentimentIntensityAnalyzer()
                sentiments = []
                
                for i in range(len(df)):
                    text = df.at[i, c]
                    scores = analyzer.polarity_scores(text)
                    if scores['compound'] > 0.5:
                        sentiments.append("Positive")
                    elif scores['compound'] < -0.5:
                        sentiments.append("Negative")
                    else:
                        sentiments.append("Neutral")
                        
                df['Sentiment'] = sentiments
                df.to_csv("results.csv", index=False)
                st.success("Analysis complete! Results saved as results.csv.")
                st.dataframe(df)
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

elif choice == "RESULTS":
    try:
        df = pd.read_csv("results.csv")
        st.dataframe(df)
        
        viz_choice = st.selectbox("Choose Visualization", ("NONE", "PIE CHART", "HISTOGRAM", "SCATTER PLOT"))
        
        if viz_choice == "PIE CHART":
            pos_pct = (len(df[df['Sentiment'] == 'Positive']) / len(df)) * 100
            neg_pct = (len(df[df['Sentiment'] == 'Negative']) / len(df)) * 100
            neu_pct = (len(df[df['Sentiment'] == 'Neutral']) / len(df)) * 100
            fig = px.pie(values=[pos_pct, neg_pct, neu_pct], names=['Positive', 'Negative', 'Neutral'],
                         title="Sentiment Distribution")
            st.plotly_chart(fig)

        elif viz_choice == "HISTOGRAM":
            col_choice = st.selectbox("Choose column for histogram", df.columns)
            if col_choice:
                fig = px.histogram(df, x=col_choice, color="Sentiment", title=f"Histogram of {col_choice}")
                st.plotly_chart(fig)

        elif viz_choice == "SCATTER PLOT":
            cont_col = st.text_input("Enter the continuous column name for the scatter plot")
            if cont_col and cont_col in df.columns:
                fig = px.scatter(df, x=cont_col, y="Sentiment", color="Sentiment",
                                 title=f"Scatter Plot using {cont_col}")
                st.plotly_chart(fig)
    except Exception as e:
        st.error(f"An error occurred while displaying results: {e}")




                
                
