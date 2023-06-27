import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu



conn=psycopg2.connect(host="localhost",
                      user="postgres",
                      password="Nlgangster@7",
                      port=4540,
                      database="phonepe")
cursor=conn.cursor()
conn.commit()


def format_indian_number(number):
    if number >= 10000000:  # If number is equal to or greater than 1 crore
        return f"{number // 10000000} Cr"
    elif number >= 100000:  # If number is equal to or greater than 1 lakh
        return f"{number // 100000} L"
    else:
        return number

st.set_page_config(layout= "wide",initial_sidebar_state= "expanded")               


st.sidebar.header(":violet[Phonepe_pulse]")
with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data","About"], 
                    icons=["house","bar-chart-line", "exclamation-circle"],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "13px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#6F36AD"}})
    
if selected == "Home":
    
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    st.write(" ")
    st.write(" ")
    st.markdown("### :violet[Domain :] Fintech")
    st.markdown("### :violet[Technologies used :] Github Cloning, Python, SQL, Streamlit, and Plotly.")
    st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

    
                                        
if selected == "Explore Data":
    explore_data = st.sidebar.selectbox("#### select type", ["overall_stats","state_stats"])
    if explore_data == "overall_stats":
        st.markdown("## :violet[Overall Statistics]")
        cat =["Transcation", "User"]    
        select_box = st.sidebar.selectbox('#### Select the categories :',cat )
        year = [2018,2019,2020,2021,2022]
        select_year = st.sidebar.selectbox("#### Select the year :",year)   
        quater = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
        select_quater =st.sidebar.selectbox("#### Select the quater :", quater)        
        
        if select_box == "Transcation":
            tab1, tab2 = st.tabs(["Total_Transcation", "Total_Amount"])
            
            with tab1:          
                col1, col2 = st.columns([2,1])
                cursor.execute(f"( select categories, sum(total_count) as total_counts, sum(amount) as total_amount from agg_trans_state where year = {select_year} and quater = '{select_quater}' group by categories order by categories)")
                a = pd.DataFrame(cursor.fetchall(),columns=["categories","total_counts","total_amount"])
                with col2:
                    col2.markdown("## :violet[Transaction]")
                    trans = a['total_counts'].sum()
                    col2.markdown("#### :violet[All PhonePe transactions (UPI + Cards + Wallets)]")
                    col2.markdown(f"#### :white[{format(trans,',')}]")
                    col3,col4 =st.columns([1,1])
                    amount = a['total_amount'].sum()
                    col3.markdown("#### :violet[Total payment value]")
                    col3.markdown(f"#### :white[₹ {format_indian_number(amount)}]")
                    avg = round(amount/trans)
                    col4.markdown("#### :violet[Avg. transaction value]")
                    col4.markdown(f"#### :white[₹ {avg}]")
                    
                    #for showing categories
                    
                    col2.markdown("### :violet[Categories]")
                    col5,col6 =st.columns([2,1])
                    col5.markdown(f"##### :violet[{a['categories'][1]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][1]}]")
                    col5.markdown(f"##### :violet[{a['categories'][3]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][3]}]")
                    col5.markdown(f"##### :violet[{a['categories'][4]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][4]}]") 
                    col5.markdown(f"##### :violet[{a['categories'][0]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][0]}]")
                    col5.markdown(f"##### :violet[{a['categories'][2]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][2]}]")
                    
                with col1:
                    #for showing bar plot   
                    
                    a["total_transcation_value"] = a["total_counts"].apply(format_indian_number)
                    fig = px.bar(a,
                                 y="categories",
                                 x= "total_counts",
                                 color = "total_counts",
                                 orientation="h",
                                 text ="total_transcation_value",
                                 labels = {"y":"Categories","x":"Total counts"},
                                 title = "Total no transcation",
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(title_x = 0.4)
                    col1.plotly_chart(fig)
                    
                    #for showing geo visualization
                    
                    cursor.execute(f"select state_name, sum(total_count) as Total_Transactions, sum(amount) as Total_amount from map_trans_state where year = {select_year} and quater = '{select_quater}' group by state_name order by state_name")
                    df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])                
                    df2 = pd.read_csv('C:/Users/Gowtham/Statenames.csv')
                    df1.State = df2
                    
                    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',
                              locations='State',
                              color='Total_Transactions',
                              color_continuous_scale='sunset',
                              fitbounds="locations")
                    fig.update_geos(visible= False)
                    col1.plotly_chart(fig,use_container_width=True)
                    
                col3, col4 = st.columns([2,1])
                
                with col4:                    
                    col4.markdown("## :violet[Top 10 Transaction ]")
                    col5,col6,col7 =st.columns([1,1,1])
                    b1 = col5.button("State")
                    b2 = col6.button("Districts")
                    b3 = col7.button("Pincode")
                    if b1:
                        cursor.execute(f"select state_name, state_total_count  from top_trans_overall where year = {select_year} and quater = '{select_quater}' ")
                        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count'])
                        st.dataframe(df,hide_index=True)
                        fig = px.pie(df, values='Transactions_Count',
                                         names='State',
                                         title='Top 10 State',
                                         color_discrete_sequence=px.colors.sequential.Agsunset
                                         )
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif b2:
                        cursor.execute(f"select districts_name, districts_total_count  from top_trans_overall where year = {select_year} and quater = '{select_quater}' ")
                        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count'])
                        st.dataframe(df,hide_index=True)
                        fig = px.pie(df, values='Transactions_Count',
                                         names='State',
                                         title='Top 10 Districts',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif b3:
                       cursor.execute(f"select pincode, pincode_total_count  from top_trans_overall where year = {select_year} and quater = '{select_quater}' ")
                       df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count'])
                       st.dataframe(df,hide_index=True)
                       fig = px.pie(df, values='Transactions_Count',
                                        names='State',
                                        title='Top 10 pincode',
                                        color_discrete_sequence=px.colors.sequential.Agsunset)
           
                       fig.update_traces(textposition='inside', textinfo='percent+label')
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.plotly_chart(fig,use_container_width=True) 
   
            with tab2:
                col1, col2 = st.columns([2,1])
                with col2:
                    
                    col2.markdown("## :violet[Transaction]")
                    trans = a['total_counts'].sum()
                    col2.markdown("#### :violet[All PhonePe transactions (UPI + Cards + Wallets)]")
                    col2.markdown(f"#### :white[{format(trans,',')}]")
                    col3,col4 =st.columns([1,1])
                    amount = a['total_amount'].sum()
                    col3.markdown("#### :violet[Total payment value]")
                    col3.markdown(f"#### :white[₹ {format_indian_number(amount)}]")
                    avg = round(amount/trans)
                    col4.markdown("#### :violet[Avg. transaction value]")
                    col4.markdown(f"#### :white[₹ {avg}]")
                    
                    #for showing categories
                    
                    col2.markdown("### :violet[Categories]")
                    col5,col6 =st.columns([2,1])
                    col5.markdown(f"##### :violet[{a['categories'][1]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][1]}]")
                    col5.markdown(f"##### :violet[{a['categories'][3]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][3]}]")
                    col5.markdown(f"##### :violet[{a['categories'][4]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][4]}]")
                    col5.markdown(f"##### :violet[{a['categories'][0]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][0]}]")
                    col5.markdown(f"##### :violet[{a['categories'][2]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][2]}]")

                with col1:    
                    #for showing bar plot   
                    
                    a["total_amount_value"] = a["total_amount"].apply(format_indian_number)
                    fig1 = px.bar(y=a["categories"],
                                  x= a["total_amount"],
                                  color = a["total_amount"],
                                  orientation="h",
                                  text = a["total_amount_value"],
                                  labels = {"y":"Categories","x":"Total Amount"},
                                  title = "Total Amount",
                                  color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig1.update_layout(title_x = 0.4)
                    col1.plotly_chart(fig1,use_container_width=True)
                    
                    #for showing geo visualization
                    
                    cursor.execute(f"select state_name, sum(total_count) as Total_Transactions, sum(amount) as Total_amount from map_trans_state where year = {select_year} and quater = '{select_quater}' group by state_name order by state_name")
                    df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])                
                    df2 = pd.read_csv('C:/Users/Gowtham/Statenames.csv')
                    df1.State = df2
                    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',
                              locations='State',
                              color='Total_amount',
                              color_continuous_scale='sunset',
                              fitbounds="locations")              
                    fig.update_geos(visible= False)
                    col1.plotly_chart(fig,use_container_width=True)
                col3, col4 = st.columns([2,1])
                
                with col4:                    
                    col4.markdown("## :violet[Top 10 Transaction Amount ]")
                    col11,col12,col13 =st.columns([1,1,1])
                    a1 = col11.button("State", key="state_button")
                    a2 = col12.button("Districts", key="districts_button")
                    a3 = col13.button("Pincode", key="pincode_button")
                    
                    if a1:
                        cursor.execute(f"select state_name, state_amount from top_trans_overall where year = {select_year} and quater = '{select_quater}' ")
                        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Amount'])
                        st.dataframe(df,hide_index=True)
                        fig = px.pie(df, values='Transactions_Amount',
                                         names='State',
                                         title='Top 10 State',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)                                        
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif a2:
                        cursor.execute(f"select districts_name, districts_amount  from top_trans_overall where year = {select_year} and quater = '{select_quater}' ")
                        df = pd.DataFrame(cursor.fetchall(), columns=['Districts', 'Transactions_Amount'])
                        st.dataframe(df,hide_index=True)
                        fig = px.pie(df, values='Transactions_Amount',
                                         names='Districts',
                                         title='Top 10 Districts',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif a3:
                       cursor.execute(f"select pincode, pincode_amount  from top_trans_overall where year = {select_year} and quater = '{select_quater}' ")
                       df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Amount'])
                       st.dataframe(df,hide_index=True)
                       fig = px.pie(df, values='Transactions_Amount',
                                        names='Pincode',
                                        title='Top 10 pincode',
                                        color_discrete_sequence=px.colors.sequential.Agsunset)
                                       
           
                       fig.update_traces(textposition='inside', textinfo='percent+label')
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.plotly_chart(fig,use_container_width=True)         
                
            
        
            
        if select_box == "User":
            tab1, tab2 = st.tabs(["Total Registered User", "Total App opener"])
            with tab1:
                col1, col2 = st.columns([2,1])
                cursor.execute(f"(select state_name, round(avg(app_open)) as app_opener, sum(total_count) as total_reg from agg_user_state where year = {select_year} and quater ='{select_quater}' group by state_name order by state_name)")
                a = pd.DataFrame(cursor.fetchall(),columns =["state_name","app_opener","total_reg"])
                with col2:
                    col2.markdown("## :violet[Users]")
                    users = a['total_reg'].sum()
                    col2.markdown(f"#### :violet[Registered PhonePe users till {select_quater[:2]} {select_year}]")
                    col2.markdown(f"#### :white[{users}]")
                    
                    col2.markdown(f"#### :violet[PhonePe app opens in {select_quater[:2]} {select_year}]")
                    col2.markdown(f"#### :white[{a['app_opener'].sum()}]")
                                    
                with col1:
                    #for showing geo visualization
                    
                    cursor.execute(f"(select state_name, round(avg(appopen)) as app_opener, sum(reg) as total_reg from map_user_state where year = {select_year} and quater ='{select_quater}' group by state_name order by state_name)")
                    df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_App_openers', 'Total_Reg_user'])                
                    df2 = pd.read_csv('C:/Users/Gowtham/Statenames.csv')
                    df1.State = df2
                    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',
                              locations='State',
                              color='Total_Reg_user',
                              color_continuous_scale='sunset',
                              fitbounds="locations")
                    fig.update_geos(visible= False)
                    col1.plotly_chart(fig,use_container_width=True)
                    
                    #for showing bar plot   
                    
                a["total_user_reg"] = a["total_reg"].apply(format_indian_number)
                fig = px.bar(a,
                    y= "total_reg",
                    x="state_name",
                    orientation='v',
                             
                             color = a["total_reg"],
                             text = a["total_user_reg"],
                             labels = {"x":"State","y":"Total Registered User"},
                             title = "State VS Total Registered User",
                             color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_layout(title_x = 0.4)
                st.plotly_chart(fig,use_container_width=True)
                
                
                
                col3, col4 = st.columns([2,1])
                with col4:
                    col4.markdown(f"## :violet[Top 10 Total Registered Users till {select_quater[:2]} {select_year} ]")
                    col5,col6,col7,col8 =st.columns([1,1,1,1])
                    c1 = col5.button("State", key="state_button")
                    c2 = col6.button("Districts", key="districts_button")
                    c3 = col7.button("Pincode", key="pincode_button")
                    c4 = col8.button("Brand", key="brand_button")
                    if c1:
                        cursor.execute(f"select state_name,state_reg from top_user_overall where year ={select_year} and quater ='{select_quater}'")
                        df = pd.DataFrame(cursor.fetchall(),columns = ["State","Total_Registered_user"])
                        st.dataframe(df,hide_index = True)
                        fig = px.pie(df, values='Total_Registered_user',
                                         names='State',
                                         title='Top 10 State',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)                                        
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif c2:
                        cursor.execute(f"select districts_name,districts_reg from top_user_overall where year ={select_year} and quater ='{select_quater}'")
                        df = pd.DataFrame(cursor.fetchall(),columns = ["Districts","Total_Registered_user"])
                        st.dataframe(df,hide_index = True)
                        fig = px.pie(df, values='Total_Registered_user',
                                         names='Districts',
                                         title='Top 10 Districts',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)                                        
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif c3:
                        cursor.execute(f"select pincode,pincode_reg from top_user_overall where year ={select_year} and quater ='{select_quater}'")
                        df = pd.DataFrame(cursor.fetchall(),columns = ["Pincode","Total_Registered_user"])
                        st.dataframe(df,hide_index = True)
                        fig = px.pie(df, values='Total_Registered_user',
                                         names='Pincode',
                                         title='Top 10 pincodes',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)                                        
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                    elif c4: 
                        cursor.execute(f"select brand,total_count from agg_user_overall where year ={select_year} and quater ='{select_quater}'")
                        df = pd.DataFrame(cursor.fetchall(),columns = ["Brand","Total_Registered_user"])
                        st.dataframe(df,hide_index = True)
                        fig = px.pie(df, values='Total_Registered_user',
                                         names='Brand',
                                         title='User registered brand',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)                                        
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                    else:
                        pass
                                
            with tab2:
                col1, col2 = st.columns([2,1])
               
                cursor.execute(f"(select state_name, round(avg(app_open)) as app_opener, sum(total_count) as total_reg from agg_user_state where year = {select_year} and quater ='{select_quater}' group by state_name order by state_name)")
                a = pd.DataFrame(cursor.fetchall(),columns= ['state_name', 'app_opener', 'total_reg'])
                
                with col2:
                    col2.markdown("## :violet[Users]")
                    users = a['total_reg'].sum()
                    col2.markdown(f"#### :violet[Registered PhonePe users till {select_quater[:2]} {select_year}]")
                    col2.markdown(f"#### :white[{users}]")
                    
                    col2.markdown(f"#### :violet[PhonePe app opens in {select_quater[:2]} {select_year}]")
                    col2.markdown(f"#### :white[{a['app_opener'].sum()}]")
                                    
                with col1:
                    #for showing geo visualization
                    
                    cursor.execute(f"(select state_name, round(avg(appopen)) as app_opener, sum(reg) as total_reg from map_user_state where year = {select_year} and quater ='{select_quater}' group by state_name order by state_name)")
                    df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_App_openers', 'Total_Reg_user'])                
                    df2 = pd.read_csv('C:/Users/Gowtham/Statenames.csv')
                    df1.State = df2
                    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',
                              locations='State',
                              color='Total_App_openers',
                              color_continuous_scale='sunset',
                              fitbounds="locations")
                    fig.update_geos(visible= False)
                    col1.plotly_chart(fig,use_container_width=True)
                    
                    #for showing bar plot   
                    
                a["total_app_opener"] = a["app_opener"].apply(format_indian_number)
                fig = px.bar(a,
                             y= "app_opener",
                             x="state_name",
                             orientation='v',                             
                             color = 'app_opener',
                             text = "total_app_opener",
                             labels = {"x":"State","y":"Total App opener"},
                             title = "State VS Total App Opener",
                             color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_layout(title_x = 0.4)
                st.plotly_chart(fig,use_container_width=True)
            
    #for creating state wise
    else:
        st.markdown("## :violet[State Statistics]")
        cat =["Transcation", "User"] 
        select_box = st.sidebar.selectbox('#### Select the categories :',cat )
        year = [2018,2019,2020,2021,2022]
        select_year = st.sidebar.selectbox("#### Select the year :",year)
        quater = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
        select_quater =st.sidebar.selectbox("#### Select the quater :", quater)
        
        cursor.execute(f"select state_name from map_trans_state where year = {select_year} and quater = '{select_quater}' group by state_name order by state_name")
        state = pd.DataFrame(cursor.fetchall(),columns= ['State'])
        select_state = st.selectbox("#### Select the State :", state)

   
        if select_box == "Transcation":
            tab1, tab2 = st.tabs(["Total_Transcation", "Total_Amount"])
            
            with tab1:          
                col1, col2 = st.columns([2,1])
                agg_trans = cursor.execute(f"( select categories, sum(total_count) as total_counts, sum(amount) as total_amount from agg_trans_state where state_name = '{select_state}' and year = {select_year} and quater = '{select_quater}' group by categories order by categories);")
                a = pd.DataFrame(cursor.fetchall(), columns = ["categories", 'total_counts', 'total_amount'])
                
                with col2:
                    col2.markdown("## :violet[Transaction]")
                    trans = a['total_counts'].sum()
                    col2.markdown("#### :violet[All PhonePe transactions (UPI + Cards + Wallets)]")
                    col2.markdown(f"#### :white[{trans}]")
                    col3,col4 =st.columns([1,1])
                    amount = a['total_amount'].sum()
                    col3.markdown("#### :violet[Total payment value]")
                    col3.markdown(f"#### :white[₹ {format_indian_number(amount)}]")
                    avg = round(amount/trans)
                    col4.markdown("#### :violet[Avg. transaction value]")
                    col4.markdown(f"#### :white[₹ {avg}]")
                    
                    #for showing categories
                    
                    col2.markdown("### :violet[Categories]")
                    col5,col6 =st.columns([2,1])
                    col5.markdown(f"##### :violet[{a['categories'][1]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][1]}]")
                    col5.markdown(f"##### :violet[{a['categories'][3]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][3]}]")
                    col5.markdown(f"##### :violet[{a['categories'][4]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][4]}]") 
                    col5.markdown(f"##### :violet[{a['categories'][0]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][0]}]")
                    col5.markdown(f"##### :violet[{a['categories'][2]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][2]}]")
                    
                with col1:
                    #for showing bar plot   
                    
                    a["total_transcation_value"] = a["total_counts"].apply(format_indian_number)
                    fig = px.bar(y=a["categories"],
                                 x= a["total_counts"],
                                 color = a["total_counts"],
                                 orientation="h",
                                 text = a["total_transcation_value"],
                                 labels = {"y":"Categories","x":"Total counts"},
                                 title = "Total no transcation",
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(title_x = 0.4)
                    col1.plotly_chart(fig,use_container_width=True)
                    
                agg_trans = cursor.execute(f"(select district_name,total_count,amount from map_trans_state where state_name = '{select_state}' and year = {select_year} and quater = '{select_quater}');")
                b = pd.DataFrame(cursor.fetchall(), columns = ["District_name", 'total_counts', 'total_amount'])
                b["total_transcation_value"] = b["total_counts"].apply(format_indian_number)
                fig = px.bar(x=b["District_name"],
                             y= b["total_counts"],
                             color = b["total_counts"],
                             orientation="v",
                             text = b["total_transcation_value"],
                             labels = {"x":"District","y":"Total counts"},
                             title = "Total no transcation",
                             color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_layout(title_x = 0.4)
                st.plotly_chart(fig,use_container_width=True)
                
                col3, col4 = st.columns([2,1])
                
                with col4:                    
                    col4.markdown("## :violet[Top 10 Transaction ]")
                    col5,col6 =st.columns([1,1])
                    b1 = col5.button("Districts")
                    b2 = col6.button("Pincode")                    
                        
                    if b1:
                        cursor.execute(f"select districts_name, districts_total_count  from top_trans_state where state_name ='{select_state}' and year = {select_year} and quater = '{select_quater}' ")
                        df = pd.DataFrame(cursor.fetchall(), columns=['Districts', 'Transactions_Count'])
                        st.dataframe(df,hide_index=True)
                        fig = px.pie(df, values='Transactions_Count',
                                         names='Districts',
                                         title='Top 10 Districts',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif b2:
                       cursor.execute(f"select pincode, pincode_total_count  from top_trans_state where state_name ='{select_state}' and year = {select_year} and quater = '{select_quater}' ")
                       df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count'])
                       st.dataframe(df,hide_index=True)
                       fig = px.pie(df, values='Transactions_Count',
                                        names='Pincode',
                                        title='Top 10 pincode',
                                        color_discrete_sequence=px.colors.sequential.Agsunset)
           
                       fig.update_traces(textposition='inside', textinfo='percent+label')
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.plotly_chart(fig,use_container_width=True) 
                
            with tab2:          
                col1, col2 = st.columns([2,1])
                col3, col4 = st.columns([2,1])
                agg_trans = cursor.execute(f"( select categories, sum(total_count) as total_counts, sum(amount) as total_amount from agg_trans_state where state_name = '{select_state}' and year = {select_year} and quater = '{select_quater}' group by categories order by categories);")
                a = pd.DataFrame(cursor.fetchall(), columns = ["categories", 'total_counts', 'total_amount'])
                
                with col2:
                    col2.markdown("## :violet[Transaction]")
                    trans = a['total_counts'].sum()
                    col2.markdown("#### :violet[All PhonePe transactions (UPI + Cards + Wallets)]")
                    col2.markdown(f"#### :white[{trans}]")
                    col3,col4 =st.columns([1,1])
                    amount = a['total_amount'].sum()
                    col3.markdown("#### :violet[Total payment value]")
                    col3.markdown(f"#### :white[₹ {format_indian_number(amount)}]")
                    avg = round(amount/trans)
                    col4.markdown("#### :violet[Avg. transaction value]")
                    col4.markdown(f"#### :white[₹ {avg}]")
                    
                    #for showing categories
                    
                    col2.markdown("### :violet[Categories]")
                    col5,col6 =st.columns([2,1])
                    col5.markdown(f"##### :violet[{a['categories'][1]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][1]}]")
                    col5.markdown(f"##### :violet[{a['categories'][3]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][3]}]")
                    col5.markdown(f"##### :violet[{a['categories'][4]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][4]}]") 
                    col5.markdown(f"##### :violet[{a['categories'][0]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][0]}]")
                    col5.markdown(f"##### :violet[{a['categories'][2]}]")
                    col6.markdown(f"##### :white[{a['total_amount'][2]}]")
                    
                with col1:
                    #for showing bar plot   
                    
                    a["total_transcation_value"] = a["total_amount"].apply(format_indian_number)
                    fig = px.bar(y=a["categories"],
                                 x= a["total_amount"],
                                 color = a["total_amount"],
                                 orientation="h",
                                 text = a["total_transcation_value"],
                                 labels = {"y":"Categories","x":"Total Amount"},
                                 title = "Total No transcation Amount",
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(title_x = 0.4)
                    col1.plotly_chart(fig,use_container_width=True)
                    
                agg_trans = cursor.execute(f"(select district_name,total_count,amount from map_trans_state where state_name = '{select_state}' and year = {select_year} and quater = '{select_quater}');")
                b = pd.DataFrame(cursor.fetchall(), columns = ["District_name", 'total_counts', 'total_amount'])
                b["total_transcation_value"] = b["total_amount"].apply(format_indian_number)
                fig = px.bar(x=b["District_name"],
                             y= b["total_amount"],
                             color = b["total_amount"],
                             orientation="v",
                             text = b["total_transcation_value"],
                             labels = {"x":"District","y":"Total Amount"},
                             title = "Total No Transcation Amount",
                             color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_layout(title_x = 0.4)
                st.plotly_chart(fig,use_container_width=True)
                
                col3, col4 = st.columns([2,1])
                
                with col4:                    
                    col4.markdown("## :violet[Top 10 Transaction Amount]")
                    col5,col6 =st.columns([1,1])
                    b1 = col5.button("Districts", key= 'district_name')
                    b2 = col6.button("Pincode", key = 'pincode')                    
                        
                    if b1:
                        cursor.execute(f"select districts_name, districts_amount  from top_trans_state where state_name ='{select_state}' and year = {select_year} and quater = '{select_quater}' ")
                        df = pd.DataFrame(cursor.fetchall(), columns=['Districts', 'Transactions_Amount'])
                        st.dataframe(df,hide_index=True)
                        fig = px.pie(df, values='Transactions_Amount',
                                         names='Districts',
                                         title='Top 10 Districts',
                                         color_discrete_sequence=px.colors.sequential.Agsunset)
            
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.write(" ")
                        col3.plotly_chart(fig,use_container_width=True)
                        
                    elif b2:
                       cursor.execute(f"select pincode, pincode_amount  from top_trans_state where state_name ='{select_state}' and year = '{select_year}' and quater = '{select_quater}' ")
                       df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Amount'])
                       st.dataframe(df,hide_index=True)
                       fig = px.pie(df, values='Transactions_Amount',
                                        names='Pincode',
                                        title='Top 10 pincode',
                                        color_discrete_sequence=px.colors.sequential.Agsunset)
           
                       fig.update_traces(textposition='inside', textinfo='percent+label')
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.write(" ")
                       col3.plotly_chart(fig,use_container_width=True)

        else:           
            col1, col2 = st.columns([2,1])
            
            cursor.execute(f"(select round(avg(app_open)) as app_opener, sum(total_count) as total_reg from agg_user_state where state_name= '{select_state}' and year = '{select_year}' and quater ='{select_quater}' group by state_name order by state_name)")
            a = pd.DataFrame(cursor.fetchall(),columns= ['app_opener', 'total_reg'])
            
            with col2:
                col2.markdown("## :violet[Users]")
                users = a['total_reg'].sum()
                col2.markdown(f"#### :violet[Registered PhonePe users till {select_quater[:2]} {select_year}]")
                col2.markdown(f"#### :white[{users}]")
                
                col2.markdown(f"#### :violet[PhonePe app opens in {select_quater[:2]} {select_year}]")
                col2.markdown(f"#### :white[{a['app_opener'].sum()}]")
                
            with col1:
                cursor.execute(f"select district_name,reg, appopen from map_user_state where state_name= '{select_state}' and  year ='{select_year}' and quater ='{select_quater}'")
                df = pd.DataFrame(cursor.fetchall(),columns = ["Districts","Total_Registered_user","Total_App_openers"])
                col2.dataframe(df,hide_index=True)
                fig =px.bar(df,
                            x ='Districts',
                            y='Total_Registered_user',
                            color = 'Total_Registered_user',
                            orientation="v",
                            text = 'Total_Registered_user',
                            labels = {"x":"District","y":'Total Registered user'},
                            title = "Total No Registered user",
                            color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_layout(title_x = 0.4)
                col1.plotly_chart(fig,use_container_width=True)
                
                fig =px.bar(df,
                            x ='Districts',
                            y="Total_App_openers",
                            color = "Total_App_openers",
                            orientation="v",
                            text = "Total_App_openers",
                            labels = {"x":"District","y":"Total App openers"},
                            title = "Total No App_openers",
                            color_discrete_sequence=px.colors.sequential.Agsunset)
                fig.update_layout(title_x = 0.4)
                col1.plotly_chart(fig,use_container_width=True)
            col3, col4 = st.columns([2,1])
            
            with col4:
                col4.markdown(f"## :violet[Top 10 Total Registered Users till {select_quater[:2]} {select_year} ]")
                col5,col6,col7 =st.columns([1,1,1])                    
                c1 = col5.button("Districts", key="districts_button")
                c2 = col6.button("Pincode", key="pincode_button")
                c3 = col7.button("Brand", key="brand_button")                   
                    
                if c1:
                    cursor.execute(f"select districts_name,districts_reg from top_user_state where state_name= '{select_state}' and  year ='{select_year}' and quater ='{select_quater}'")
                    df = pd.DataFrame(cursor.fetchall(),columns = ["Districts","Total_Registered_user"])
                    st.dataframe(df,hide_index = True)
                    fig = px.pie(df, values='Total_Registered_user',
                                     names='Districts',
                                     title='Top 10 Districts',
                                     color_discrete_sequence=px.colors.sequential.Agsunset)                                        
        
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.plotly_chart(fig,use_container_width=True)
                    
                elif c2:
                    cursor.execute(f"select pincode,pincode_reg from top_user_state where state_name= '{select_state}' and year ='{select_year}' and quater ='{select_quater}'")
                    df = pd.DataFrame(cursor.fetchall(),columns = ["Pincode","Total_Registered_user"])
                    st.dataframe(df,hide_index = True)
                    fig = px.pie(df, values='Total_Registered_user',
                                     names='Pincode',
                                     title='Top 10 pincodes',
                                     color_discrete_sequence=px.colors.sequential.Agsunset)                                        
        
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.plotly_chart(fig,use_container_width=True)
                elif c3: 
                    cursor.execute(f"select brand,total_count from agg_user_state where state_name= '{select_state}' and  year ='{select_year}' and quater ='{select_quater}'")
                    df = pd.DataFrame(cursor.fetchall(),columns = ["Brand","Total_Registered_user"])
                    st.dataframe(df,hide_index = True)
                    fig = px.pie(df, values='Total_Registered_user',
                                     names='Brand',
                                     title='User registered brand',
                                     color_discrete_sequence=px.colors.sequential.Agsunset)                                        
        
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.write(" ")
                    col3.plotly_chart(fig,use_container_width=True)
                else:
                    pass

if selected == "About":
    st.write(" ")
    st.write(" ")
    st.markdown("### :violet[About PhonePe Pulse:] ")
    st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
    
    st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
    
    st.markdown("### :violet[About PhonePe:] ")
    st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
    
    st.write("**:violet[My Project GitHub link]** ⬇️")
    st.write("https://github.com/IamJafar/Phonepe_Pulse_Data_Visualization")
    
    
    
