import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt


def plot2d_graph(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    c = [colors[i % (len(colors))]
         for i in nx.get_node_attributes(graph, 'cluster').values()]
    if c:  # is set
        nx.draw(graph, pos, node_color=c, node_size=0.25)
    else:
        nx.draw(graph, pos, node_size=0.25)
    plt.show(block=False)


def plot2d_data_preview(df):
    if (len(df.columns) > 3):
        print("Plot Waring: more than 2-Dimensions!")
    df.plot(kind='scatter', c=df['cluster'], cmap='gist_rainbow', x=0, y=1)
    plt.show(block=False)
    

def plot2d_data(df):
    if (len(df.columns) > 3):
        print("Plot Waring: more than 2-Dimensions!")
    
    clusters = sorted(df['cluster'].unique())
    markers = ["d", "v", "s", "*", "^", "d", "v", "s", "*", "^"]
    colors = ['red', 'slateblue', 'green', 'hotpink', 'sienna', 'skyblue',
             'darkorange', 'turquoise', 'violet', 'greenyellow', 'steelblue', 'teal', 'lime']
    
    for i in range(len(clusters)+1):
        df_i = df.loc[(df['cluster']==i+1)]
        #plt.scatter(df_i.iloc[:,0], df_i.iloc[:,1], marker=markers[i%len(markers)], 
        #            s=7, c=colors[i%len(colors)])
        plt.scatter(df_i.iloc[:,0], df_i.iloc[:,1], c=colors[i%len(colors)])

    plt.show(block=False)
    
def plot2d_data_sl(df):
    '''Colors to use with comparison using scikit-learn datasets'''
    if (len(df.columns) > 3):
        print("Plot Waring: more than 2-Dimensions!")
    
    clusters = sorted(df['cluster'].unique())
    #markers = ["d", "v", "s", "*", "^", "d", "v", "s", "*", "^"]
    colors = ["#377eb8", "#ff7f00", "#4daf4a", "#f781bf", "#a65628", "#984ea3",
              "#999999","#e41a1c","#dede00"]
    
    for i in range(len(clusters)+1):
        df_i = df.loc[(df['cluster']==i+1)]
        plt.scatter(df_i.iloc[:,0], df_i.iloc[:,1], c=colors[i%len(colors)])

    plt.show(block=False)
