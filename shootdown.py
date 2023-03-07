# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 10:27:06 2023

@author: bloomberg
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pickle
import time
import plotly.graph_objects as go
import plotly.io as pio
import plotly.graph_objs as go
pio.renderers.default = 'browser'

options = webdriver.ChromeOptions()
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(options=options)
driver.get('https://shoot-down.site/users/login/')

id_field = driver.find_element(By.NAME,"username")
id_field.send_keys('henryma26@gmail.com')

pw_field = driver.find_element(By.NAME,"password")
pw_field.send_keys('sbidealing')

submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
submit_button.click()

link_element = driver.find_element(By.LINK_TEXT, 'LIVE CBBC FE')
link_element.click()

time.sleep(5)


while True:
    livedata = driver.page_source
    start = '<svg class="table_area" id="table_area">'
    end = 'Bear Shot Range</text></svg>'
    findstart = livedata.find(start)
    findend = livedata.find(end)
    livedata = driver.page_source
    start = '<svg class="table_area" id="table_area">'
    end = 'Bear Shot Range</text></svg>'
    findstart = livedata.find(start)
    findend = livedata.find(end)
    cbbcchart = livedata[findstart:findend]
    
    soup = BeautifulSoup(cbbcchart, 'html.parser')
    # texts = soup.find_all('text', {'id':True})
    bulldis = []
    beardis = []
    bulldisfe = []
    beardisfe = []
    bulldisturn = []
    beardisturn = []
    
    bull_texts = soup.find_all('text', {'id': lambda x: x and 'BullRange' in x})
    bull_texts2 = soup.find_all('text', {'id': lambda x: x and 'BullbarTextPos' in x})
    bull_texts3 = soup.find_all('text', {'id': lambda x: x and 'BullCbbCTextVol' in x})
    bear_texts = soup.find_all('text', {'id': lambda x: x and 'BearRange' in x})
    bear_texts2 = soup.find_all('text', {'id': lambda x: x and 'BearbarTextPos' in x})
    bear_texts3 = soup.find_all('text', {'id': lambda x: x and 'BearCbbCTextVol' in x})

    
    for text in bull_texts:
        bulldis.append(text.text)
    for text in bull_texts2:
        if text.text.strip():  # check if the text is not an empty string
            bulldisfe.append(int(text.text))
        else:
            bulldisfe.append(0)
    for text in bull_texts3:
        bulldisturn.append(text.text)
    for text in bear_texts:
        beardis.append(text.text)
    for text in bear_texts2:
        if text.text.strip():  # check if the text is not an empty string
            beardisfe.append(int(text.text))
        else:
            beardisfe.append(0)
    for text in bear_texts3:
        beardisturn.append(text.text)
    
    print(beardis)
    print(beardisfe)
    # Data
    # x = ['20,600 - 20,699', '20,700 - 20,799', '20,800 - 20,899', '20,900 - 20,999', '21,000 - 21,099', '21,100 - 21,199']
    # y = [32, 1315, 10113, 3672, 4283, 764]
    
    # Create trace
    trace = go.Bar(
        x=bulldisfe,
        y=bulldis,
        orientation='h',
        text=bulldisfe,
        name='Bull FE',
        textposition='auto',
        marker=dict(color='blue')
    )
    
   
    trace2 = go.Bar(
        x=beardisfe,
        y=beardis,
        orientation='h',
        name='Bear FE',
        text=beardisfe,
        textposition='auto',
        marker=dict(color='red')
    )
    
    
    # Create layout
    layout = go.Layout(
        title='Histogram',
        xaxis=dict(title='Count'),
        yaxis=dict(title='Range'),
        height=900,
    )
    
    # Create figure
    fig = go.Figure(data=[trace, trace2], layout=layout)
    
    # Change color of specific bars
    # color_list = ['grey' if i in [0, 2, 4] else 'blue' for i in range(len(bulldisfe))]
    # fig.data[0].marker.color = color_list
        
    # Show plot
    plotly_html = pio.to_html(fig, full_html=False)

    # Create the HTML string with the JavaScript code to reload the page
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="refresh" content="30">
        </head>
        <body>
            {plotly_html}
        </body>
    </html>
    """
    
    # Write the HTML file to disk using utf-8 encoding
    with open('testing.html', 'w', encoding='utf-8') as f:
        f.write(html)    
    
    time.sleep(30)


    
# bear_texts = soup.find_all('text', {'id': lambda x: x and ('BearRange' in x or 'BearbarTextPos' in x or 'BearCbbCTextVol' in x)})

# for text in bear_texts :
#     print(text.text)
    
        
# link_element2 = driver.find_element(By.LINK_TEXT, 'HISTORICAL TRADING HOUR CBBC FE')
# link_element2.click()

# # select_menu = Select(driver.find_element)
# soup = driver.page_source
# getdates = soup.find('select', {'id': 'range_select'})

# for option in getdates.find_all('option'):
#     print(option['value'])
