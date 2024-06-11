from transformers import pipeline
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

import os


model = pipeline("text-classification", model="hieudinhpro/BERT_Sentiment_Vietnamese")


def predict_sentiment (dataframe , topic) :
  
    predicted = []
    for x in dataframe[topic]:
        sentiment_lecturer_topic = model(str(x))
        predicted.append(sentiment_lecturer_topic)
    return predicted

def column_names (dataframe):
   
   value_to_remove = "Unnamed: 0"
   list_column_names = dataframe.columns.tolist()
   if value_to_remove in list_column_names :
        list_column_names.remove(value_to_remove)
   return  list_column_names

def create_result_datafream (column_names, df):
    df_pedicted = pd.DataFrame()
    for column_name in column_names:
       df_pedicted[column_name] = predict_sentiment(df,column_name)
    return  df_pedicted


def analysis (df_pedicted, topic) :

  label_predicted = []
  label_POSITIVE = label_NEGATIVE  = 0
  for i in df_pedicted[topic] :
    label_predicted.append(i[0]['label'])
    if i[0]['label'] == "POSITIVE" :
      label_POSITIVE +=1
    elif i[0]['label'] == "NEGATIVE" :
      label_NEGATIVE +=1

  return {
            "pos":label_POSITIVE,
            "Neg":label_NEGATIVE,
            "neu": len(label_predicted) -  label_POSITIVE - label_NEGATIVE
            }

# Function to create a pie chart
def create_pie_chart(label_counts, title):
    labels = label_counts.keys()
    sizes = label_counts.values()
    colors = ['#ff9999','#66b3ff','#99ff99']
    explode = (0.1, 0, 0)  # explode the first slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)  


directory = 'result'
filename = 'output.csv'
filepath = os.path.join(directory, filename)

def title_head ():

    st.title("School Sentiment Analysis App")
    # Set the title of the Streamlit app
    st.title('CSV File Viewer')

title_head()

# File uploader for CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write(df)
        
        st.write("#Lines",len(df))
        
        # Display column names
        st.write("Topic Names:")
        list_column_names = column_names(df)
        st.write(list_column_names)
        df_pedict = create_result_datafream(list_column_names, df)
        df_pedict.to_csv(filepath, index=False)
 

    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
else:
    st.info("Please upload a CSV file.")


# if flat :
#     try: 
#         result_csv = df_pedict
#         st.write(pd.read_csv(filepath))
#         st.title('Pie Chart Generator')
#         column_to_analyze = st.selectbox("Select a column for analysis", result_csv.columns)
        
#         data = analysis(result_csv, column_to_analyze)
#         fig, ax = plt.subplots()
#         ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
#         ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#         # Display chart using Streamlit
#           
#     except Exception as e:
#         st.error(f"")
# else :
#     st.write()
            

try: 
        result_csv = df_pedict
        st.write(pd.read_csv(filepath))
        st.title('Pie Chart Generator')
        column_to_analyze = result_csv.columns
        for topic in column_to_analyze:
            st.header(topic)
            data = analysis(result_csv, topic)
            create_pie_chart(data, topic)
except Exception as e:
        st.error(f"")



          


