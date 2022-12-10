import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
import chart_studio
chart_studio.tools.set_credentials_file(username='Manuu254', api_key='iep00eGu5fmUTmt82ZdD')
import chart_studio.plotly as save2cs

import statsmodels.api as sm
import statsmodels.formula.api as smf

from scipy import stats
import inequality

import wbgapi as wb


wb.series.info(db = 12) # Series in the Education Statistics Database


wb.economy.info(wb.income.members('HIC'))      # high-income economies


wb.data.DataFrame('SP.POP.TOTL', wb.region.members('AFR'), range(2010, 2020, 2))


wb.series.info(db = 6) # Series in the Debt Statistics database


wb.series.info(topic = 3) # Series in the topic Economy & Growth


wb.series.metadata.get('NY.GNS.ICTR.GN.ZS')

wb.series.metadata.get('NY.GDP.PCAP.PP.KD')


wb.data.DataFrame('SP.POP.TOTL', time=range(2010,2015), labels=True)  # 5 years of population data (with economy names) from 2010 to 2014

wb.data.DataFrame(['SI.POV.NAHC', 'NY.GDP.PCAP.CD'], 
                    economy = wb.region.members('LAC'),
                    mrnev = 1, # Most recent non-empty most values (time period varies)
                    timeColumns = True, # Show the time dimension for each series/economy
                    labels = True
                    )   # Most recent poverty and income data for Latin American countries (LAC)

wb.series.metadata.get('SI.POV.NAHC') # Note: National poverty rates lines are not necessarily comparable across contries

wb.series.metadata.get('EN.ATM.CO2E.PC')

wb.data.DataFrame('EN.ATM.CO2E.PC', mrnev=1, labels = True).join(wb.economy.DataFrame()['incomeLevel'])  # Most recent CO2 emissions per capita for each country and merge its income group

wb.data.DataFrame('EN.ATM.CO2E.PC',mrnev=1,labels=True).sort_values('EN.ATM.CO2E.PC',ascending=False).head(10)   # Top 10 emitters per capita

GDPpc_long = wb.data.DataFrame(['NY.GDP.PCAP.PP.CD'], 
                                time=range(2000, 2021),
                                labels=True,
                                skipAggs=True, 
                                skipBlanks=True, 
                                columns='series').reset_index() # Import GDP per capita (PPP Constant international $)
GDPpc_long

GDPpc_wide = pd.pivot_table(GDPpc_long, 
                            values='NY.GDP.PCAP.PP.CD', 
                            index = 'economy', columns='time').dropna()
GDPpc_wide # Rearrange data in wide form and drop countries for which data for all years are not available

wb.data.DataFrame('NY.GDP.PCAP.CD', wb.region.members('EMU'), time=range(1960, 2020))

wb.data.DataFrame('NY.GDP.PCAP.CD', wb.region.members('EMU'), time=range(1960, 2020)).dropna()


ren = wb.data.DataFrame('EG.ELC.RNEW.ZS',
                      ['DEU','FRA','ESP','GBR','USA'],
                      time=range(2000,2016,5))
ren

regionalIndentifiers = wb.economy.DataFrame(skipAggs=True).reset_index()
regionalIndentifiers

GDPpc_longWITHri = pd.merge(GDPpc_long, regionalIndentifiers, how="left", left_on= "economy", right_on= "index")
GDPpc_longWITHri # Merge regional intifiers with long-form panel data (merge one to many)

px.line(GDPpc_longWITHri, 
        x= 'Time', 
        y= 'NY.GDP.PCAP.PP.CD',
        #log_y= True,
        color='Country',
        #facet_col = 'incomeLevel',
        #facet_col_wrap= 2,
        labels={'NY.GDP.PCAP.PP.CD': 'GDP per capita'}
        )

px.line(GDPpc_longWITHri, 
        x= 'Time', 
        y= 'NY.GDP.PCAP.PP.CD',
        log_y= True,
        color='Country',
        facet_col = 'incomeLevel',
        facet_col_wrap= 2,
        labels={'NY.GDP.PCAP.PP.CD': 'GDP per capita'}
        )

figPlotly20220520 = px.line(GDPpc_longWITHri, 
        x= 'Time', 
        y= 'NY.GDP.PCAP.PP.CD',
        log_y= True,
        color='Country',
        facet_col = 'incomeLevel',
        facet_col_wrap= 2,
        labels={'NY.GDP.PCAP.PP.CD': 'GDP per capita'}
        )  #save to chart studio.plot(figPlotly20220520, filename = 'figPlotly20220520', auto_open=True)

wb.series.metadata.get('EG.ELC.RNEW.ZS')

wb.data.DataFrame('EG.ELC.RNEW.ZS',
                      ['DEU','FRA','ESP','GBR','USA'],
                      time=range(2000,2016,5)).plot.bar();


wb.series.metadata.get('NY.GDP.PCAP.PP.KD')


wb.data.DataFrame('NY.GDP.PCAP.PP.KD', 
                    economy = wb.region.members('SAS'), 
                    time = range(2000, 2021), numericTimeKeys = True,
                    labels = True).set_index('Country').transpose().plot(title='GDP per capita in South Asia');


wb.data.DataFrame('NY.GDP.PCAP.PP.KD', 
                    economy = wb.region.members('SAS'), 
                    time = range(2000, 2016), numericTimeKeys = True,
                    labels = True)

GDPpc_long_SAS = wb.data.DataFrame(['NY.GDP.PCAP.PP.KD'], 
                                economy = wb.region.members('SAS'),
                                time=range(2000, 2021),
                                labels=True,
                                skipAggs=True, 
                                #skipBlanks=True, 
                                columns='series').reset_index().sort_values(['economy', 'Time'])

GDPpc_long_SAS


px.line(GDPpc_long_SAS, 
        x= 'Time', 
        y= 'NY.GDP.PCAP.PP.KD',
        color='Country',
        labels={"NY.GDP.PCAP.PP.KD": "GDP per capita"}
        )

df2017_2019 = wb.data.DataFrame(['NY.GDP.PCAP.PP.KD', 'SE.SEC.NENR'], 
                                time=range(2017, 2019),
                                labels=True,
                                skipAggs=True, 
                                skipBlanks=True, 
                                columns='series').reset_index()
df2017_2019


px.scatter(df2017_2019.query("Time == '2017'"),
           x="SE.SEC.NENR",
           y="NY.GDP.PCAP.PP.KD",
           log_y = True, # log scale for the y axis
           trendline="ols", trendline_options=dict(log_y=True),
           #color="region",
           #size="pop", size_max=60,
           hover_name="Country",
           labels={"SE.SEC.NENR": "School enrollment, secondary (% net)",
                   "NY.GDP.PCAP.PP.KD": "GDP per capita"
                   }
           )

px.choropleth(
    df2017_2019.query("Time == '2017'"),
    locations = "economy",
    color = "NY.GDP.PCAP.PP.KD",
    hover_name = "Country",
    color_continuous_scale = px.colors.sequential.Plasma,
    projection = "natural earth",
    labels = {"NY.GDP.PCAP.PP.KD": "GDP per capita"}
     )
