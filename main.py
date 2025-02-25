import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Sentiment Analysis System",page_icon="https://cdn-icons-png.flaticon.com/512/9850/9850903.png")
st.title("SENTIMENT ANALYSIS SYSTEM")


choice=st.sidebar.selectbox("My Menu",("HOME","ANALYSIS","RESULTS"))

if(choice=='HOME'):
    st.image("https://cdn.dribbble.com/userupload/21162478/file/original-e2fb97f5400edfc0cf5e39bbee823576.gif")
    st.write("1. This is a Natural Language Processing application that can analyze sentiment from text data.")
    st.write("2. It categorizes sentiment into Positive, Negative, or Neutral.")
    st.write("3. The application visualizes results based on factors such as age, gender, language, and city.")


elif choice == "ANALYSIS":
    sid = st.text_input("Enter your Google Sheet ID")
    r = st.text_input("Enter Range between first column and last column (e.g., Sheet1!A1:D100)")
    c = st.text_input("Enter column name to be analyzed")
    btn=st.button("Analyze")

    if btn:
        if 'cred' not in st.session_state:
            # Initialize OAuth flow
            f=InstalledAppFlow.from_client_secrets_file("key.json",["https://www.googleapis.com/auth/spreadsheets"])
            # Run local server for authentication            
            st.session_state['cred']=f.run_local_server(port=0)


        mymodel=SentimentIntensityAnalyzer()
        
        # Build the Google Sheets API service
        service=build("Sheets","v4",credentials=st.session_state['cred']).spreadsheets().values()
        result=service.get(spreadsheetId=sid ,range=r).execute()
        data=result['values']
        df=pd.DataFrame(data=data[1:],columns=data[0])
        l=[]


        for i in range(len(df)):


            t=df._get_value(i,c)
            pred=mymodel.polarity_scores(t)
            if(pred['compound']>0.5):
                l.append("Positive")
            elif(pred['compound']<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
            
        df['Sentiment']=l
        df.to_csv("results.csv",index=False) #To save the excel on firefox to computer in csv form
        st.subheader("The Analysis results are saved by the name of a results.csv file")

elif(choice=="RESULTS"):
    df=pd.read_csv("results.csv")
    choice2=st.selectbox("Choose Visualization",("NONE","PIE CHART","HISTOGRAM","SCATTER PLOT"))
    st.dataframe(df)
    if(choice2=="PIE CHART"):
        posper=(len(df[df['Sentiment']=='Positive'])/len(df))*100
        negper=(len(df[df['Sentiment']=='Negative'])/len(df))*100
        neuper=(len(df[df['Sentiment']=='Neutral'])/len(df))*100
        fig=px.pie(values=[posper,negper,neuper],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)

    elif(choice2=="HISTOGRAM"):
        k=st.selectbox("CHoose column",df.columns)
        if k:
            fig=px.histogram(x=df[k],color=df['Sentiment'])
            st.plotly_chart(fig)
    elif(choice2=="SCATTER PLOT"):
        k=st.text_input("Enter the continous column name")
        if k:
            fig=px.scatter(x=df[k],y=df['Sentiment'],color=df['Sentiment'],size=df[k])
            st.plotly_chart(fig)




                
                