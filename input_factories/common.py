from input_factories.data_factory.datasets.artists import Artists
from input_factories.data_factory.datasets.collaboration_songs import CollaborationSongs
from input_factories.data_factory.datasets.scientists import Scientists

mapping_category_to_class = {
    'artists': Artists,
    'collaboration_songs': CollaborationSongs,
    'scientists': Scientists
}
