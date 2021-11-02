global index
from typing import List

from gensim.models import Word2Vec
from networkx import Graph
from networkx_viewer import Viewer
from pandas import DataFrame
from seaborn import set_style, regplot
from sklearn.decomposition import PCA

from src.loader.DataManager import DataManager
import plotly.graph_objects as go


def plot_graph(vectors: List[List[int]], labels: List[str], colours: List[str] = None) -> None:
    """
    a labelled 2D plot of graph embeddings
    (pca used to reduce vector dimensions)
    """

    pca = PCA(n_components = 2)
    set_style("whitegrid")

    data = DataFrame(
        data = pca.fit_transform(vectors),
        columns = ['x_coordinate', 'y_coordinate']
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = data.x_coordinate,
        y = data.y_coordinate,
        mode = "markers+text",
        name = "File Graph",
        text = labels,
        textposition = "top center"
    ))
    fig.show()


def createFilePathGraph():
    data_manager = DataManager(None)
    data_manager.load_data_from_file("../src/git-test/data")
    # %%
    from src.utils.Constants import name_index
    from tqdm import tqdm
    labeldict = {}
    file_graph = Graph()
    file_graph.add_node(node_for_adding = 'root')
    for backup_date, backed_up_files in tqdm(list(data_manager.getData())[:10]):
        for file in backed_up_files:
            path = file[name_index].split('/')

            if len(path[0]) == 0:
                path.pop(0)

            file_graph.add_node(path[0])
            file_graph.add_edge('root', path[0])

            for index in range(1, len(path)):
                next_node_id = '/'.join(path[:index])
                labeldict[next_node_id] = path[index]
                file_graph.add_node(next_node_id)
                file_graph.add_edge('/'.join(path[:index - 1]), next_node_id)
    # %%
    app = Viewer(file_graph)
    app.mainloop()


def create_path_lists():
    data_manager = DataManager(None)
    data_manager.load_data_from_file("../src/git-test/data")
    # %%
    from src.utils.Constants import name_index
    from tqdm import tqdm
    training_data = []
    gramer = []
    file_graph = Graph()
    file_graph.add_node(node_for_adding = 'root')
    for backup_date, backed_up_files in tqdm(list(data_manager.getData())[:10]):
        for file in backed_up_files:
            path = file[name_index].lower().split('/')
            for element in path:
                if element not in gramer:
                    if element == 'annotations':
                        print(element)
                    gramer.append(element)
            training_data.append(path)

    return training_data, gramer


def create_vectors_from_random_walks() -> List[List[float]]:
    skipgram_model = Word2Vec(window = 4, sg = 1, hs = 0, negative = 10, alpha = .03, min_alpha = .0007, seed = 14, min_count=1)
    training_data, grammer = create_path_lists()
    skipgram_model.build_vocab(training_data, progress_per = 2)
    skipgram_model.train(
        training_data,
        total_examples = skipgram_model.corpus_count,
        epochs = 20,
        report_delay = 1
    )

    plot_graph(
        vectors = skipgram_model.wv[grammer],
        labels = grammer
    )


if __name__ == '__main__':
    # createFilePathGraph()
    create_vectors_from_random_walks()
