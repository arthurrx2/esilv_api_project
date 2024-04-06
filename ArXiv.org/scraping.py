#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 16:14:07 2024

@author: arthur
"""


import requests
import xml.etree.ElementTree as ET

def fetch_articles(query=None):
    base_url = 'http://export.arxiv.org/api/query?'
    # Si une requête est spécifiée, formater la requête pour l'URL
    if query:
        query_formatted = query.replace(' ', '+')
        search_query = f'search_query=all:{query_formatted}'
    else:
        search_query = 'search_query=all'  # Cela va chercher sans filtre spécifique
    
    # Vous pouvez également ajuster le nombre de résultats que vous souhaitez récupérer
    max_results = 'max_results=100'
    url = f'{base_url}{search_query}&{max_results}'
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to get data: {response.status_code}")
        return []
    
    response_xml = ET.fromstring(response.content)
    
    articles = []
    for entry in response_xml.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        links = entry.findall('{http://www.w3.org/2005/Atom}link')
        link = next((l.attrib['href'] for l in links if l.attrib.get('type') == 'text/html'), 'No URL')
        
        articles.append({
            'title': title.strip(),
            'summary': summary.strip(),
            'url': link
        })
    
    return articles





# articles = fetch_articles()
# for article in articles:
#       print(article['title'], article['url'])

