from graphtools import *
import itertools
import pandas as pd


def internal_interconnectivity(graph, cluster):
    # Interconnectivity in terms of Edge Cut (sum of weights from connecting edges)
    # of a bisection of the graph (bisected using metis)
    return np.sum(bisection_weights(graph, cluster))


def relative_interconnectivity(graph, cluster_i, cluster_j):
    edges = connecting_edges((cluster_i, cluster_j), graph)
    # Interconnectivity in terms of Edge Cut (sum of weights from connecting edges)
    EC = np.sum(get_weights(graph, edges)) 
    ECci, ECcj = internal_interconnectivity(
        graph, cluster_i), internal_interconnectivity(graph, cluster_j)
    # EC normalized by the EC of cluster i and j
    return EC / ((ECci + ECcj) / 2.0)


def internal_closeness(graph, cluster):
    # Simple sum of the weights of the cluster
    cluster = graph.subgraph(cluster)
    edges = cluster.edges()
    weights = get_weights(cluster, edges)
    return np.sum(weights)


def relative_closeness(graph, cluster_i, cluster_j):
    edges = connecting_edges((cluster_i, cluster_j), graph)
    if not edges:
        return 0.0
    else:
        # Avg weight of connecting edges
        try:
            SEC = np.mean(get_weights(graph, edges))
        except Exception as e:
            print("SEC error", e.message, e.args)
    # Sum of weights within the clusters
    # In the paper, they use |C_i| and |C_j|, which represent the number
    # of data points of the clusters
    Ci, Cj = internal_closeness(
        graph, cluster_i), internal_closeness(graph, cluster_j)
    # Avg weight of the connecting edges of the bisection of ci and cj
    try:
        SECci = np.mean(bisection_weights(graph, cluster_i))
        SECcj = np.mean(bisection_weights(graph, cluster_j))
    except Exception as e:
            print("SEC error", e.message, e.args)
    return SEC / ((Ci / (Ci + Cj) * SECci) + (Cj / (Ci + Cj) * SECcj))


def merge_score(g, ci, cj, a):
    return relative_interconnectivity(
        g, ci, cj) * np.power(relative_closeness(g, ci, cj), a)


def merge_best(graph, df, a, k, verbose=False):
    '''Adjusted to return a list with the mergescores'''
    clusters = np.unique(df['cluster'])
    merge_scores = []
    max_score = 0
    ci, cj = -1, -1
    if len(clusters) <= k:
        return False

    if verbose:
        curr_i_value = -1
    for combination in itertools.combinations(clusters, 2):
        i, j = combination
        if i != j:
            if verbose:
                if (curr_i_value==-1 or curr_i_value != i):
                    print("\nChecking c%d with..." % i)
                    j_values = []
                j_values.append(f"c{j}")
                curr_i_value = i
            gi = get_cluster(graph, [i])
            gj = get_cluster(graph, [j])
            edges = connecting_edges(
                (gi, gj), graph)
            
            if not edges:
                continue
            
            ms = merge_score(graph, gi, gj, a)
            merge_scores.append(ms)
            if verbose:
                j_values.append("...")
                print(*j_values, sep = ", ")
                print(f"Found connecting edges between c{i} and c{j}")
                print("Merge score: %f" % (ms))
                j_values=[]
                j_values.append("...") 
            if ms > max_score:
                if verbose:
                    print("Better than: %f" % (max_score))
                max_score = ms
                ci, cj = i, j

    if max_score > 0:
        if verbose:
            print("Merging c%d and c%d" % (ci, cj))
        df.loc[df['cluster'] == cj, 'cluster'] = ci
        for i, p in enumerate(graph.nodes()):
            if graph.nodes[p]['cluster'] == cj:
                graph.nodes[p]['cluster'] = ci
    return merge_scores


def cluster(df, k, knn=10, m=30, alpha=2.0, verbose=False, plot=False):
    '''Added a record_merge_scores to keep track of this value from all
    iterations, and to also return this'''
    record_merge_scores = []
    graph = knn_graph(df, knn, verbose=True)
    graph = pre_part_graph(graph, m, df, verbose=True)
    iterm = tqdm(enumerate(range(m - k)), total=m-k)
    for i in iterm:
        current_merge_scores = merge_best(graph, df, alpha, k, verbose)
        record_merge_scores.append(sorted(current_merge_scores, reverse=True))
        if plot:
            plot2d_data_preview(df)
    res = rebuild_labels(df)
    return res, record_merge_scores

def rebuild_labels(df):
    ans = df.copy()
    clusters = list(pd.DataFrame(df['cluster'].value_counts()).index)
    c = 1
    for i in clusters:
        ans.loc[df['cluster'] == i, 'cluster'] = c
        c = c + 1
    return ans
