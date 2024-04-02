# Assuming that you have data in your folder. 
import numpy as np 
import pandas as pd
import random
import matplotlib.pyplot as plt
import networkx as nx



with open('reporting_carrier_ontimeperformance.csv') as cp:
    ontime = pd.read_csv(cp)

ontime = ontime[['Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek', 'FlightDate', 'Reporting_Airline', 'DOT_ID_Reporting_Airline', 'IATA_CODE_Reporting_Airline', 'Tail_Number', 'Flight_Number_Reporting_Airline', 'OriginAirportID', 'OriginAirportSeqID', 'OriginCityMarketID', 'Origin', 'OriginCityName', 'OriginState', 'OriginStateName', 'DestAirportID', 'DestAirportSeqID', 'DestCityMarketID', 'Dest', 'DestCityName', 'DestState', 'DestStateName', 'CRSDepTime', 'DepTime', 'CRSArrTime', 'ArrTime', 'Cancelled', 'CRSElapsedTime', 'ActualElapsedTime', 'AirTime', 'Flights', 'Distance', 'DistanceGroup']]
print(list(ontime.columns.values))

ontime.head()

# This describes the number of airports that are in this dataset. 
unique_values = ontime['Origin'].unique()
print(f"Unique values in column: {unique_values}")
print(f"There are {len(unique_values)} airports.")

# AIRPORT TAGS
airports = ontime['Origin'].unique()
print(f"There are {len(unique_values)} airports.")

# NUMBER OF FLIGHTS
number_of_flights = ontime.shape
print(number_of_flights[0])

# Flight connections and frequencies


flight_frequencies = ontime.groupby(['Origin', 'Dest']).size().reset_index(name='Frequency') # Used to group => look at pd documentation for more information
flight_dictionary = dict(zip(flight_frequencies[['Origin', 'Dest']].apply(tuple, axis=1), flight_frequencies['Frequency'])) # this is the list of connections and frequencies which we can now put into a entwork


print(flight_dictionary)

# Creating the network graph 
G = nx.Graph()

for (origin, dest), frequency in flight_dictionary.items():
    G.add_edge(origin, dest, weight=frequency)

weights = [G[u][v]['weight'] for u, v in G.edges()]
max_weight = max(weights)
# normalized_weights = [w / max_weight * 10 for w in weights]  # Scale weights for visibility
# pos = nx.spring_layout(G)
pos = nx.spring_layout(G, k=1.5, iterations=30)  # adjust k for more space

plt.figure(figsize=(35, 35), dpi=80)
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightgreen")
nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

plt.title("Flight Network", size=15)
plt.savefig("Flight Network visualized.jpeg")
# plt.show()
