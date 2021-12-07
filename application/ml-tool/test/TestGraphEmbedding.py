from test.TestUtils import create_path_lists

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
        # text = labels,
        textposition = "top center"
    ))
    fig.show()


def createFilePathGraph():
    data_manager = DataManager(None)
    data_manager.load_data_from_file("../src/git-test/data")
    # %%
    from src.utils.Constants import name_index
    from tqdm import tqdm
    file_graph = Graph()
    file_graph.add_node(node_for_adding = 'root')
    for backup_date, backed_up_files in tqdm(list(data_manager.getData())[:10]):
        for file in backed_up_files:
            path = file[name_index].split('/')

            if len(path[0]) == 0:
                path.pop(0)

            prev_node = path[0]
            file_graph.add_node(prev_node)
            file_graph.add_edge('root', prev_node)

            for index in range(2, len(path) + 1):
                next_node_id = '/'.join(path[:index])
                file_graph.add_node(next_node_id)
                file_graph.add_edge(prev_node, next_node_id)
                prev_node = next_node_id
    # %%
    app = Viewer(file_graph)
    app.mainloop()


# Todo mention path embeddings from random walks using RNN or LSTM or Transformere
def create_vectors_from_random_walks():
    skipgram_model = Word2Vec(window = 4, sg = 1, hs = 0, negative = 10, alpha = .03, min_alpha = .0007, seed = 14, min_count=1)
    training_data, grammer = create_path_lists(300)
    skipgram_model.build_vocab(training_data, progress_per = 2)
    skipgram_model.train(
        training_data,
        total_examples = skipgram_model.corpus_count,
        epochs = 10,
        report_delay = 1
    )

    plot_graph(
        vectors = skipgram_model.wv[grammer],
        labels = grammer
    )


if __name__ == '__main__':
    createFilePathGraph()
    # create_vectors_from_random_walks()
