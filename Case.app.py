#!/usr/bin/env python
# coding: utf-8

# # Case 2 - naam

# * Joey van Alphen
# * Mohamed Garad
# * Nusret Kaya
# * Shereen Macnack

# # 1. Data inladen

# ### Dataset 1: Maandcijfers Nederlandse luchthavens van nationaal belang

# In[1]:


#pip install cbsodata


# In[2]:


import cbsodata
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import statsmodels.api as sm


# In[3]:


data1 = pd.DataFrame(cbsodata.get_data('37478hvv'))


# In[4]:


#data1.shape


# In[5]:


data1.info(verbose=True, show_counts=True)


# In[6]:


data1.head()


# ### Dataset 2: Emissies naar lucht door de Nederlandse economie; nationale rekeningen

# In[7]:


data2 = pd.DataFrame(cbsodata.get_data('83300NED'))


# In[8]:


# data2.shape


# In[9]:


data2.info()


# In[10]:


data2.head()


# # 2. Data filteren

# ### 1. Aviation data filteren

# In[11]:


aviation_data = data1[['ID', 'Luchthavens', 'Perioden', 'Overlandbewegingen_1', 'Terreinbewegingen_2','TotaalAlleVluchten_3', 'TotaalVertrokkenVluchten_9', 'TotaalAantalPassagiers_12','EuropaTotaal_22','EULanden_54','OverigEuropa_55', 'Afrika_57','Amerika_63', 'Azie_67', 'Oceanie_71', 'TotaalGoederenvervoer_43', 'TotalePostvervoer_74']]


# In[ ]:





# In[12]:


#aviation_data die is gefilterd op alleen het totaal van alle luchhavens van nationaal belang
alle_luchthavens = aviation_data[aviation_data['Luchthavens']=='Totaal luchthavens van nationaal belang']


# In[13]:


alle_luchthavens.head(50)


# In[14]:


# alle_luchthavens filteren op volledige jaren ipv maanden voor totaal 
value_list = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
boolean_series = alle_luchthavens.Perioden.isin(value_list)
alle_luchthavens = alle_luchthavens[boolean_series]
alle_luchthavens_index = alle_luchthavens.reset_index(drop = True)
alle_luchthavens_index.head(50)


# In[ ]:





# In[15]:


#aviation_data die de individuele luchthavens bevat
individuele_luchthavens = aviation_data[aviation_data['Luchthavens']!='Totaal luchthavens van nationaal belang']
individuele_luchthavens_index = individuele_luchthavens.reset_index(drop = True)


# In[ ]:





# In[16]:


#individuele_luchthavens_index gefilterd op volledige jaren ipv maanden voor individuele luchthavens
value_list = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005','2006', '2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016','2017', '2018', '2019','2020']
boolean_series = individuele_luchthavens_index.Perioden.isin(value_list)
individuele_luchthavens_index = individuele_luchthavens_index[boolean_series]
individuele_luchthavens_index.head()


# ### 2. Emissies data filteren

# In[17]:


data2.head()


# In[18]:


co2_emissies = data2[['ID','NederlandseEconomie','Perioden', 'CO2_1']]


# In[19]:


co2_emissies_luchtvaart = co2_emissies[co2_emissies['NederlandseEconomie']=='51 Vervoer door de lucht']


# In[20]:


co2_emissies_luchtvaart.head(50)


# In[21]:


#Filteren vanaf 1997 om de andere dataset te matchen
co2_emissies_luchtvaart = co2_emissies_luchtvaart[co2_emissies_luchtvaart['Perioden']>='1997'].reset_index(drop=True)
co2_emissies_luchtvaart = co2_emissies_luchtvaart.drop(['ID'], axis=1) 


# In[22]:


co2_emissies_luchtvaart.head(50)


# In[23]:


co2_emissies_luchtvaart.columns = [ 'Emissie categorie', 'Perioden', 'CO2 uitstoot (mln kg)']
co2_emissies_luchtvaart.head(30)


# In[24]:


# Dataframes combineren
samengestelde_tabel = alle_luchthavens_index.merge(co2_emissies_luchtvaart, on='Perioden', how='left')

samengestelde_tabel = samengestelde_tabel.drop(['ID', 'Emissie categorie'], axis = 1)


# In[25]:


# Kolom namen veranderen van samengestelde tabel
samengestelde_tabel = samengestelde_tabel.rename ({'Perioden': 'Jaar', 'Overlandbewegingen_1':'Overlandbewegingen' , 'Terreinbewegingen_2':'Terreinbewegingen', 'TotaalAlleVluchten_3': 'Totaal aantal vluchten', 'TotaalVertrokkenVluchten_9':'Totaal vertrokken vluchten','TotaalAantalPassagiers_12': 'Totaal aantal passagiers', 'EuropaTotaal_22':'Europa totaal','EULanden_54': 'EU landen', 'OverigEuropa_55':'Overig Europa', 'Afrika_57':'Afrika','Amerika_63': 'Amerika','Azie_67': 'Azie', 'Oceanie_71':'Oceanie', 'TotaalGoederenvervoer_43':'Totaal goederenvervoer','TotalePostvervoer_74':'Totaal postvervoer', 'CO2_1': 'CO2 emissies in jaar'}, axis = 1)
samengestelde_tabel.head(30)


# In[26]:


corr = np.corrcoef(samengestelde_tabel['Totaal aantal vluchten'], samengestelde_tabel['CO2 uitstoot (mln kg)'])


# In[27]:


fig = px.scatter(samengestelde_tabel, x='Totaal aantal vluchten', y ='CO2 uitstoot (mln kg)', trendline="ols", )


# In[28]:


fig1 = px.histogram(individuele_luchthavens_index, x='Perioden', y='TotaalAlleVluchten_3', color = 'Luchthavens')


# In[29]:


fig2 = px.line(samengestelde_tabel, x='Jaar', y='CO2 uitstoot (mln kg)')


# # 3. Maken van de Streamlit app

# In[30]:


header = st.container()


# In[31]:


with header:
    st.title('Aviaition data blog')
    st.text('In deze blog gebruiken we data van het CBS over de maandelijkse cijfers van Nederlandse luchthavens. Wij willen inzicht krijgen hoe deze cijfers gerelateerd zijn tot de jaarlijkse uitstoot van de luchtvaart')


# In[32]:


aviation_data_streamlit_table = aviation_data[['Luchthavens', 'Perioden', 'TotaalAlleVluchten_3', 'TotaalAantalPassagiers_12','TotaalGoederenvervoer_43', 'TotalePostvervoer_74']]
aviation_data_streamlit_table.columns = ['Luchthavens', 'Perioden', 'Totaal aantal vluchten', 'Totaal aantal passagiers', 'Totale goederenvervoer', 'Totale postvervoer']
value_list = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005','2006', '2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016','2017', '2018', '2019','2020']
boolean_series = aviation_data_streamlit_table.Perioden.isin(value_list)
aviation_data_streamlit_table = aviation_data_streamlit_table[boolean_series]
aviation_data_streamlit_table.head(30)


# In[33]:


st.header('Een eerste kijk in de data')
st.text("Deze eerste dataset is gefilterd op de belangrijke informatie per luchthaven en alle luchthavens in totaal")


# In[34]:


InputAirport = st.sidebar.selectbox("Select Airport", ("Totaal luchthavens van nationaal belang", "Amsterdam Airport Schiphol", "Rotterdam The Hague Airport", "Eindhoven Airport", "Maastricht Aachen Airport", "Groningen Airport Eelde"))


# In[35]:


AirportSelect = aviation_data_streamlit_table[aviation_data_streamlit_table["Luchthavens"] == InputAirport]


# In[36]:


st.dataframe(AirportSelect)


# ### tweede tabel

# In[37]:


st.subheader('Tweede dataset met emmissies')
st.text("Deze dataset bevat de totale emmissies van vervoer door de lucht")


# In[38]:


st.dataframe(co2_emissies_luchtvaart)


# In[39]:


st.subheader("De samengestelde dataset")
st.markdown('Nu kunnen we variabelen toevoegen')


# In[40]:


aviation_data_streamlit_table = aviation_data_streamlit_table[aviation_data_streamlit_table['Luchthavens']=='Totaal luchthavens van nationaal belang']
samengestelde_tabel_streamlit = aviation_data_streamlit_table.merge(co2_emissies_luchtvaart, on='Perioden', how='left')
samengestelde_tabel_streamlit = samengestelde_tabel_streamlit.drop(['Emissie categorie'], axis = 1)
samengestelde_tabel_streamlit.head(50)


# In[41]:


st.dataframe(samengestelde_tabel_streamlit)


# In[53]:


samengestelde_tabel_streamlit['Totale uitstoot sinds meting'] = samengestelde_tabel_streamlit['CO2 uitstoot (mln kg)'].cumsum()
samengestelde_tabel_streamlit


# ## Plots

# In[43]:


fig1 = px.line(samengestelde_tabel_streamlit, x='Perioden', y = 'Totale uitstoot sinds meting')


# In[44]:


fig2 = px.scatter(samengestelde_tabel_streamlit, x='Totaal aantal vluchten', y ='CO2 uitstoot (mln kg)', trendline="ols", )


# In[45]:


fig3 = px.histogram(individuele_luchthavens_index, x='Luchthavens', y='TotaalAlleVluchten_3', color = 'Luchthavens', animation_frame = 'Perioden', animation_group = 'Luchthavens' )


# In[46]:


fig4 = px.line(samengestelde_tabel_streamlit, x='Perioden', y='CO2 uitstoot (mln kg)', title = 'CO2 emissie verloop')  
fig4['layout'].pop('updatemenus')


# In[47]:


fig5 = go.Figure(data=[go.Scatter(
    x=samengestelde_tabel_streamlit['Perioden'],
    y=samengestelde_tabel_streamlit['CO2 uitstoot (mln kg)'],
    mode='markers',)
])
  
# Add dropdown
fig5.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "scatter"],
                    label="Scatter Plot",
                    method="restyle"
                ),
                dict(
                    args=["type", "bar"],
                    label="Bar Chart",
                    method="restyle"
                )
            ]),
            direction="down",
        ),
    ]
)

fig5.update_xaxes(title_text = 'Jaar')
fig5.update_yaxes(title_text = 'CO2 emissie')


# In[48]:


st.plotly_chart(fig1)


# In[49]:


st.plotly_chart(fig2)


# In[50]:


st.plotly_chart(fig3)


# In[51]:


st.plotly_chart(fig4)


# In[52]:


st.plotly_chart(fig5)

