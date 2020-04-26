import networkx as nx
import pandas as pd
import csv
import pprint as pp
import numpy as np
import random

def readCSV(filename):
    rows = []
    with open(filename, encoding="UTF-8") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
            for i, r in enumerate(row):
                if r.isdigit():
                    row[i]= int(r)
            rows.append(row)
    return rows


if __name__ == "__main__":
    studenci = readCSV("studenci.csv")
    promotorzy = readCSV("promotorzy.csv")



    G = nx.DiGraph()

    studenci = studenci[1:]

    random.shuffle(studenci)

    G.add_node("start")
    G.add_node("meta", demand=-(len(studenci)))

    
    
    for nazwisko, pojemnosc in promotorzy:
        G.add_node(nazwisko)
        G.add_edge(nazwisko, "meta", capacity=pojemnosc, weight=0)

    for imie, nazwisko, *_ in studenci:
        nazwa_wezla = imie + nazwisko
        G.add_node(nazwa_wezla, demand=0)
        G.add_edge("start", nazwa_wezla, capacity=1, weight=0)

    for imie, nazwisko, *preferencje in studenci: 
        nazwa_wezla = imie + nazwisko
        for index, (nazwisko, _) in enumerate(promotorzy):
            #jakiś komentarz żeby ogarnać te indeksy
            G.add_edge(nazwa_wezla, nazwisko, capacity=1, weight=preferencje[index])




    result = nx.max_flow_min_cost(G, "start", "meta")

    for imie, nazwisko, *_ in studenci:
        for k,v in result[imie+nazwisko].items():
            if(v == 1):
                print(imie, nazwisko, k)
                break
            
    