import streamlit as st
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import webbrowser

#https://media.sproutsocial.com/uploads/2023/07/Sentiment-analysis-HUB-Final.jpg

# Set Firefox as the browser on Mac
firefox_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

st.set_page_config(page_title="Sentiment Analysis System", page_icon="https://cdn-icons-png.flaticon.com/512/9850/9850903.png")
st.title("SENTIMENT ANALYSIS SYSTEM")

# Sidebar navigation
choice = st.sidebar.selectbox("My Menu", ("HOME", "ANALYSIS", "RESULTS"))

if choice == "HOME":
    st.image("https://i0.wp.com/turbolab.in/wp-content/uploads/2021/09/sentiment.png?fit=698%2C400&ssl=1")
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
            # Authenticate using OAuth 2.0
            flow = InstalledAppFlow.from_client_secrets_file(
                "key.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            creds = flow.run_local_server(port=0, browser='firefox')
            
            service = build("sheets", "v4", credentials=creds).spreadsheets().values()
            st.write("Authentication successful. Fetching data...")
            
            # Fetch data efficiently
            result = service.get(spreadsheetId=sid, range=r).execute()
            data = result.get('values', [])
            
            if not data or len(data) < 2:
                st.error("The provided range does not contain enough data.")
            else:
                df = pd.DataFrame(data[1:], columns=data[0])
                if c not in df.columns:
                    st.error(f"Column '{c}' not found in the data.")
                else:
                    st.write("Data fetched successfully. Performing Sentiment Analysis...")
                    analyzer = SentimentIntensityAnalyzer()
                    
                    # Optimized sentiment analysis using apply
                    df['Sentiment'] = df[c].apply(lambda x: "Positive" if analyzer.polarity_scores(str(x))['compound'] > 0.5 else
                                                            "Negative" if analyzer.polarity_scores(str(x))['compound'] < -0.5 else "Neutral")
                    df.to_csv("results.csv", index=False)
                    st.success("Analysis results saved to 'results.csv'")
                    
                    # Write back to Google Sheets
                    update_range = f"{r.split('!')[0]}!A1"  # Update from the start of the sheet
                    service.update(spreadsheetId=sid, range=update_range, valueInputOption="RAW", 
                                   body={"values": [df.columns.tolist()] + df.values.tolist()}).execute()
                    st.success("Data successfully updated in Google Sheets!")
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

elif choice == "RESULTS":
    if not os.path.exists("results.csv"):
        st.error("No results file found. Please run the analysis first.")
    else:
        try:
            df = pd.read_csv("results.csv")
            st.dataframe(df)
            viz_choice = st.selectbox("Choose Visualization", ("NONE", "PIE CHART", "HISTOGRAM", "SCATTER PLOT"))

            if viz_choice == "PIE CHART":
                sentiment_counts = df['Sentiment'].value_counts()
                fig = px.pie(values=sentiment_counts, names=sentiment_counts.index, title="Sentiment Distribution")
                st.plotly_chart(fig)

            elif viz_choice == "HISTOGRAM":
                col_choice = st.selectbox("Choose column for histogram", df.columns)
                if col_choice:
                    fig = px.histogram(df, x=col_choice, color="Sentiment", title=f"Histogram of {col_choice}")
                    st.plotly_chart(fig)

            elif viz_choice == "SCATTER PLOT":
                cont_col = st.text_input("Enter the continuous column name for the scatter plot")
                if cont_col and cont_col in df.columns:
                    fig = px.scatter(df, x=cont_col, y="Sentiment", color="Sentiment", title=f"Scatter Plot using {cont_col}")
                    st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred while displaying results: {e}")






# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# import os
# import webbrowser

# # Set Firefox as the browser on Mac
# firefox_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
# webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

# st.set_page_config(page_title="Sentiment Analysis System", page_icon="https://cdn-icons-png.flaticon.com/512/9850/9850903.png")
# st.title("SENTIMENT ANALYSIS SYSTEM")

# # Sidebar navigation
# choice = st.sidebar.selectbox("My Menu", ("HOME", "ANALYSIS", "RESULTS"))

# if choice == "HOME":
#     st.image("https://media.sproutsocial.com/uploads/2023/07/Sentiment-analysis-HUB-Final.jpg")
#     st.write("1. This is a Natural Language Processing application that can analyze sentiment from text data.")
#     st.write("2. It categorizes sentiment into Positive, Negative, or Neutral.")
#     st.write("3. The application visualizes results based on factors such as age, gender, language, and city.")

# elif choice == "ANALYSIS":
#     sid = st.text_input("Enter your Google Sheet ID")
#     r = st.text_input("Enter Range (e.g., Sheet1!A1:D100)")
#     c = st.text_input("Enter column name to be analyzed")
#     btn = st.button("Analyze")

#     if btn:
#         try:
#             # Use Streamlit secrets for authentication
#             creds = Credentials.from_authorized_user_info(
#                 {
#                     "client_id": st.secrets["google"]["client_id"],
#                     "client_secret": st.secrets["google"]["client_secret"],
#                     "refresh_token": st.secrets["google"]["refresh_token"],
#                     "token": ""
#                 }
#             )
            
#             service = build("sheets", "v4", credentials=creds).spreadsheets().values()
#             st.write("✅ Authentication successful. Fetching data...")
            
#             # Fetch data efficiently
#             result = service.get(spreadsheetId=sid, range=r).execute()
#             data = result.get('values', [])
            
#             if not data or len(data) < 2:
#                 st.error("The provided range does not contain enough data.")
#             else:
#                 df = pd.DataFrame(data[1:], columns=data[0])
#                 if c not in df.columns:
#                     st.error(f"Column '{c}' not found in the data.")
#                 else:
#                     st.write("✅ Data fetched successfully. Performing Sentiment Analysis...")
#                     analyzer = SentimentIntensityAnalyzer()
                    
#                     # Optimized sentiment analysis using apply
#                     df['Sentiment'] = df[c].apply(lambda x: "Positive" if analyzer.polarity_scores(str(x))['compound'] > 0.5 else
#                                                                 "Negative" if analyzer.polarity_scores(str(x))['compound'] < -0.5 else "Neutral")
#                     df.to_csv("results.csv", index=False)
#                     st.success("Analysis results saved to 'results.csv'")
                    
#                     # Write back to Google Sheets
#                     update_range = f"{r.split('!')[0]}!A1"  # Update from the start of the sheet
#                     service.update(spreadsheetId=sid, range=update_range, valueInputOption="RAW", 
#                                    body={"values": [df.columns.tolist()] + df.values.tolist()}).execute()
#                     st.success("Data successfully updated in Google Sheets!")
#         except Exception as e:
#             st.error(f"An error occurred during analysis: {e}")

# elif choice == "RESULTS":
#     if not os.path.exists("results.csv"):
#         st.error("No results file found. Please run the analysis first.")
#     else:
#         try:
#             df = pd.read_csv("results.csv")
#             st.dataframe(df)
#             viz_choice = st.selectbox("Choose Visualization", ("NONE", "PIE CHART", "HISTOGRAM", "SCATTER PLOT"))

#             if viz_choice == "PIE CHART":
#                 sentiment_counts = df['Sentiment'].value_counts()
#                 fig = px.pie(values=sentiment_counts, names=sentiment_counts.index, title="Sentiment Distribution")
#                 st.plotly_chart(fig)

#             elif viz_choice == "HISTOGRAM":
#                 col_choice = st.selectbox("Choose column for histogram", df.columns)
#                 if col_choice:
#                     fig = px.histogram(df, x=col_choice, color="Sentiment", title=f"Histogram of {col_choice}")
#                     st.plotly_chart(fig)

#             elif viz_choice == "SCATTER PLOT":
#                 cont_col = st.text_input("Enter the continuous column name for the scatter plot")
#                 if cont_col and cont_col in df.columns:
#                     fig = px.scatter(df, x=cont_col, y="Sentiment", color="Sentiment", title=f"Scatter Plot using {cont_col}")
#                     st.plotly_chart(fig)
#         except Exception as e:
#             st.error(f"An error occurred while displaying results: {e}")
