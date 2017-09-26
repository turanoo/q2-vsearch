# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin

import q2_vsearch._cluster_features
import q2_vsearch._cluster_sequences
from q2_types.feature_data import FeatureData, Sequence
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import Sequences

plugin = qiime2.plugin.Plugin(
    name='vsearch',
    version=q2_vsearch.__version__,
    website='https://github.com/qiime2/q2-vsearch',
    package='q2_vsearch',
    user_support_text=None,
    short_description='Plugin for clustering and dereplicating with vsearch.',
    description=('This plugin wraps the vsearch application, and provides '
                 'methods for clustering and dereplicating features and '
                 'sequences.'),
    citation_text=("Rognes T, Flouri T, Nichols B, Quince C, Mahé F. (2016) "
                   "VSEARCH: a versatile open source tool for metagenomics. "
                   "PeerJ 4:e2584. doi: 10.7717/peerj.2584")
)

plugin.methods.register_function(
    function=q2_vsearch._cluster_features.cluster_features_de_novo,
    inputs={
        'table': FeatureTable[Frequency],
        'sequences': FeatureData[Sequence]},
    parameters={
        'perc_identity': qiime2.plugin.Float % qiime2.plugin.Range(
                          0, 1, inclusive_start=False, inclusive_end=True),
        'threads': qiime2.plugin.Int % qiime2.plugin.Range(
                          0, 256, inclusive_start=True, inclusive_end=True)
    },
    outputs=[
        ('clustered_table', FeatureTable[Frequency]),
        ('clustered_sequences', FeatureData[Sequence]),
    ],
    input_descriptions={
        'table': 'The feature table to be clustered.',
        'sequences': 'The sequences corresponding to the features in table.',
    },
    parameter_descriptions={
        'perc_identity': ('The percent identity at which clustering should be '
                          'performed. This parameter maps to vsearch\'s --id '
                          'parameter.'),
        'threads': ('The number of threads to use for computation. Passing 0 '
                    'will launch one thread per CPU core.')
    },
    output_descriptions={
        'clustered_table': 'The table following clustering of features.',
        'clustered_sequences': 'Sequences representing clustered features.',
    },
    name='De novo clustering of features.',
    description=('Given a feature table and the associated feature '
                 'sequences, cluster the features based on user-specified '
                 'percent identity threshold of their sequences. This is not '
                 'a general-purpose de novo clustering method, but rather is '
                 'intended to be used for clustering the results of '
                 'quality-filtering/dereplication methods, such as DADA2, or '
                 'for re-clustering a FeatureTable at a lower percent '
                 'identity than it was originally clustered at. When a group '
                 'of features in the input table are clustered into a single '
                 'feature, the frequency of that single feature in a given '
                 'sample is the sum of the frequencies of the features that '
                 'were clustered in that sample. Feature identifiers and '
                 'sequences will be inherited from the centroid feature '
                 'of each cluster. See the vsearch documentation for details '
                 'on how sequence clustering is performed.')
)

plugin.methods.register_function(
    function=q2_vsearch._cluster_features.cluster_features_closed_reference,
    inputs={
        'table': FeatureTable[Frequency],
        'sequences': FeatureData[Sequence],
        'reference_sequences': FeatureData[Sequence]
    },
    parameters={
        'perc_identity': qiime2.plugin.Float % qiime2.plugin.Range(
                          0, 1, inclusive_start=False, inclusive_end=True),
        'strand': qiime2.plugin.Str % qiime2.plugin.Choices(['plus', 'both']),
        'threads': qiime2.plugin.Int % qiime2.plugin.Range(
                0, 256, inclusive_start=True, inclusive_end=True)
    },
    outputs=[
        ('clustered_table', FeatureTable[Frequency]),
        ('unmatched_sequences', FeatureData[Sequence]),
    ],
    input_descriptions={
        'table': 'The feature table to be clustered.',
        'sequences': 'The sequences corresponding to the features in table.',
        'reference_sequences': 'The sequences to use as cluster centroids.',
    },
    parameter_descriptions={
        'perc_identity': ('The percent identity at which clustering should be '
                          'performed. This parameter maps to vsearch\'s --id '
                          'parameter.'),
        'strand': ('Search plus (i.e., forward) or both (i.e., forward and '
                   'reverse complement) strands.'),
        'threads': ('The number of threads to use for computation. Passing 0 '
                    'will launch one thread per CPU core.')
    },
    output_descriptions={
        'clustered_table': 'The table following clustering of features.',
        'unmatched_sequences': ('The sequences which failed to match any '
                                'reference sequences. This output maps to '
                                'vsearch\'s --notmatched parameter.')
    },
    name='Closed-reference clustering of features.',
    description=('Given a feature table and the associated feature '
                 'sequences, cluster the features against a reference '
                 'database based on user-specified '
                 'percent identity threshold of their sequences. This is not '
                 'a general-purpose closed-reference clustering method, but '
                 'rather is intended to be used for clustering the results of '
                 'quality-filtering/dereplication methods, such as DADA2, or '
                 'for re-clustering a FeatureTable at a lower percent '
                 'identity than it was originally clustered at. When a group '
                 'of features in the input table are clustered into a single '
                 'feature, the frequency of that single feature in a given '
                 'sample is the sum of the frequencies of the features that '
                 'were clustered in that sample. Feature identifiers '
                 'will be inherited from the centroid feature '
                 'of each cluster. See the vsearch documentation for details '
                 'on how sequence clustering is performed.')
)

plugin.methods.register_function(
    function=q2_vsearch._cluster_sequences.dereplicate_sequences,
    inputs={
        'sequences': SampleData[Sequences]
    },
    parameters={},
    outputs=[
        ('dereplicated_table', FeatureTable[Frequency]),
        ('dereplicated_sequences', FeatureData[Sequence]),
    ],
    input_descriptions={
        'sequences': 'The sequences to be dereplicated.',
    },
    parameter_descriptions={},
    output_descriptions={
        'dereplicated_table': 'The table of dereplicated sequences.',
        'dereplicated_sequences': 'The dereplicated sequences.',
    },
    name='Dereplicate sequences.',
    description=('Dereplicate sequence data and create a feature table and '
                 'feature representative sequences. Feature identfiers '
                 'in the resulting artifacts will be the sha1 hash '
                 'of the sequence defining each feature. If clustering of '
                 'features into OTUs is desired, the resulting artifacts '
                 'can be passed to the cluster_features_* methods in this '
                 'plugin.')
)
