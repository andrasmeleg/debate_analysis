#source:   https://www.geeksforgeeks.org/python-textinput-widget-in-kivy/
#source: https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#
#source: Tech with Tim
# the code scrapes the top results from google scholar, and prints it out in kivy  
USER_AGENTS = [
    # Chrome
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    # Firefox
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
    # Opera
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    # Safari
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    # Internet Explorer, probably a good idea to leave this one out...
    'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
import pandas as pd
from bs4 import BeautifulSoup
import requests
import random
from lxml.html import fromstring
from itertools import cycle
import traceback

import kivy      
from kivy.app import App  
kivy.require('1.11.1')    
from kivy.uix.label import Label  
from kivy.uix.textinput import TextInput  
from kivy.uix.boxlayout import BoxLayout 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.widget import Widget

def get_header(agents):
    return {'User-agent': random.choice(agents)}

Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        
''')
  
# Create the App class 
def searchsource(searchword, startyear: int=0, resultsnum: int=5):
    if len(searchword.split())>1:
        searchword=("+".join(searchword.split()))
    url = 'https://scholar.google.com/scholar?hl=en&q='
    listone = []
    listtwo = []
    for i in range(resultsnum):
        response = requests.get(url+searchword+f'&as_ylo={startyear}'+ f'&start={(i-1)*10}', headers=get_header(USER_AGENTS))
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_results = soup.find_all('h3', class_='gs_rt')
        quotecount_results = soup.find_all('a')
        for text in headline_results:
            a = text.get_text()        
            try:
                if ']'in a:
                    listone.append(a.split('] ')[1])
                else: listone.append(a) 
            except:
                listone.append(a)
        for res in quotecount_results:
            if 'Cited by' in res.get_text():
                listtwo.append(int(res.get_text().split()[2]))
    mylist = sorted(list(set(zip(listone, listtwo))),key = lambda x: x[1], reverse= True)
    return(mylist[0:resultsnum])

class BeszamolApp(App): 
      
    def build(self): 
  
        self.b = BoxLayout(orientation ='vertical') 
  
        # Adding the text input 
        self.t = TextInput(font_size = 30, 
                      size_hint_y = None, 
                      height = 60,
                      multiline=False,
                      hint_text = 'search expression')
        self.y = TextInput(font_size = 30, 
                      size_hint_y = None, 
                      height = 60,
                      multiline=False,
                      hint_text = 'start year')
        self.u = TextInput(font_size = 30, 
                      size_hint_y = None, 
                      height = 50,
                      multiline=False,
                      hint_text = 'number of results')
        self.h = Button(text = 'submit', font_size = 40, size_hint=(1, .25))
        self.h.bind(on_press = self.pressed)
        self.b.add_widget(self.t) 
        self.b.add_widget(self.y) 
        self.b.add_widget(self.u)

        class RV(RecycleView):
            def __init__(self, **kwargs):
                super(RV, self).__init__(**kwargs)
                #self.data = [{'text': str(x)} for x in list(name)]
        self.b.add_widget(self.h) 
        self.b.add_widget(RV())
                 
        return self.b

    def pressed(self, instance):
        mytext = searchsource(self.t.text, int(self.y.text), int(self.u.text))
        class RV(RecycleView):
            def __init__(self, **kwargs):
                super(RV, self).__init__(**kwargs)
                self.data = [{'text': str(x)} for x in list(mytext)]

        self.b.remove_widget(self.b.children[0])
        self.b.add_widget(RV())
        return self.b


if __name__ == "__main__": 
    BeszamolApp().run() 