import datetime
from datetime import datetime
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium.plugins import HeatMap, HeatMapWithTime

def main():
    st.set_page_config(page_title='SCEB Dashboard', layout="wide")
    st.title('SCEB Dashboard :customs:')
    st.caption('Monitoring offences caught islandwide by SCEB officers')
    
        
if __name__ == "__main__":
    main()

# Read in CSV file
df = pd.read_csv('C:/Users/Admin/Desktop/fakescebdata.csv')

# Data pre-processing (Change to datetime format, Extract Year and Month)
df['datetime'] = df['date'] + ' ' + df['case time']
df['datetime'] = df['datetime'].apply(lambda x:datetime.strptime(x, '%d/%m/%Y %I:%M %p'))
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month_name()

year_list = list(df['datetime'].dt.year.unique())
month_list = list(df['datetime'].dt.month_name().unique())

st.sidebar.write('This sidebar is used to filter the dashboard')
st.sidebar.date_input('Start date:  :clock9:', df['datetime'].min())
st.sidebar.date_input('End date:  :clock330:', df['datetime'].max())
st.sidebar.multiselect(label='Select officer(s):  :male-police-officer: :female-police-officer:', options=list(df['officer'].unique()))
st.sidebar.multiselect(label='Select nationalities', options=list(df['nationality'].unique()))


tab0, tab1, tab2 = st.tabs(['Overview', 'Heatmap', 'Choropleth'])

with tab0:
    
    df_countOffence = df.groupby(['year', 'month','date'])['nationality'].count().reset_index(name='count')
    
    st.write('Volume of cases over the past X months')
    st.line_chart(df_countOffence, x='date', y='count')
    st.write(df_countOffence)   
    

with tab1:
    # Create a basic map centered in Singapore
    m = folium.Map(location=[1.3521, 103.8198],
                   tiles='cartodbpositron',
                   zoom_start=11)   
    
    for i, row in df.iterrows():
        
        # Setup content of the popup
        iframe = folium.IFrame('Postal Code: ' + str(row['postal']))
        
        # Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        
        # Add each row to the map
        folium.Marker(location=(row['latitude'],row['longitude']), popup=popup, tooltip='Address: ' + str(row['address'])).add_to(m)
    
    # Add a heatmap layer
    df_count = df.groupby(['postal','latitude','longitude','date'])['officer'].count().reset_index(name='count')
    HeatMap(data=df_count[['latitude', 'longitude', 'count']], name='Heat Map').add_to(m)
    

    
    st.write(st.file_uploader(label = 'Upload CSV file here'))
    
    c1, c2 = st.columns(2)
    with c1:
        # folium.LayerControl().add_to(m)
        m.add_child(folium.LayerControl())
        st_map = st_folium(m, width=1050, height=675) # This is the st_folium object that give s bidriectional...
        
    
        if st_map['last_object_clicked']:
            fil_lat = st_map['last_object_clicked']['lat']
            fil_lng = st_map['last_object_clicked']['lng']
            df2 = df[(df['latitude'] == fil_lat) & (df['longitude'] == fil_lng)]
        else:
            df2 = df
        
    with c2:
        st.dataframe(df2)

with tab2:
    st.write('For choropleth')
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
# https://folium.streamlit.app/
# OneMap API token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjk4MTksInVzZXJfaWQiOjk4MTksImVtYWlsIjoiam9yZGFuaGFuQGhvdG1haWwuc2ciLCJmb3JldmVyIjpmYWxzZSwiaXNzIjoiaHR0cDpcL1wvb20yLmRmZS5vbmVtYXAuc2dcL2FwaVwvdjJcL3VzZXJcL3Nlc3Npb24iLCJpYXQiOjE2NzU0MjA5MjYsImV4cCI6MTY3NTg1MjkyNiwibmJmIjoxNjc1NDIwOTI2LCJqdGkiOiJkNDg0MDE1ZDU5ZWE0NDM2YWFjNGJkZTJkNWViZDcyYiJ9.ndDmAL_fgbgBLWMG0cT8_j_fJytARIaOhiJ2u3OdkTo
