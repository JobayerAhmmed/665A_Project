# sankey.py
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("param_classification.csv")

px4_cats = []
all_cats = []

px4_dict = {}
for index, row in df.iterrows():
    cats = []
    px4_cat = row['PX4_category']
    px4_cats.append(px4_cat)
    cat1 = row['Category1']
    if cat1 not in all_cats:
    	all_cats.append(cat1)
    cat2 = row['Category2']
    if cat2 not in all_cats:
    	all_cats.append(cat2)
    cat3 = row['Category3']
    if cat3 not in all_cats:
    	all_cats.append(cat3)

    cats.append(cat1)
    cats.append(cat2)
    cats.append(cat3)
    cats = [x for x in cats if x == x]
    px4_dict[px4_cat] = cats


all_cats = [x for x in all_cats if x == x]
# for elem in all_cats:
# 	print(elem)

nodes = []
for source in px4_cats:
	new_dict = {"label": source}
	nodes.append(new_dict)
for process in all_cats:
	new_dict = {"label": process}
	nodes.append(new_dict)
sink = {"label": "Parameters"}
nodes.append(sink)

node_labels = [node["label"] for node in nodes]
# print(node_labels)

links = []
for pcat in node_labels:
	if pcat in px4_dict:
		for mcat in px4_dict[pcat]:
			new_dict = {"source": node_labels.index(pcat), "target": node_labels.index(mcat), "value": 1}
			links.append(new_dict)
			sink_dict = {"source": node_labels.index(mcat), "target": node_labels.index("Parameters"), "value": 1}
			links.append(sink_dict)
# print(links)

fig = go.Figure(go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                                   label=node_labels),
                           link=dict(source=[link["source"] for link in links],
                                     target=[link["target"] for link in links],
                                     value=[link["value"] for link in links])))


fig.update_layout(title_text="PX4 Parameter Categorization", font_size=10)

fig.show()

