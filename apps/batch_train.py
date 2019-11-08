from datetime import datetime
import os

from trainer.utils.util import *

EXAMPLE_NAME = 'learning_rate'

NUM_TESTS = 5
EPOCH_NUM = 500

MODEL_NAMES = [
    'simple'
]

HEAD_TYPES = [
    # 'de',
    'vector',
    # 'scalar'
]

FILTERS = [
    '16_32'
]

KERNELS = [
    '7_7'
]

FEATURE_NAMES = [
    # 'boundary_edge_surface',
    # 'boundary_surface',
    # 'boundary_edge',
    # 'surface_edge',
    'boundary',
    # 'surface',
    # 'edge'
]

LEARNING_RATES = [
    1e-2,
    1e-3,
    1e-4
]

TRAIN_DATA_PERCENTAGES = [
    # 0.25,
    # 0.5,
    # 0.75,
    1.0
]


def make_job_name():
    return "cnn_" + datetime.now().strftime('%Y%m%d_%H%M%S')


def make_data(features, train_data_pct):
    if not isinstance(features, list):
        features = [features]

    command = (
        'python -m trainer.preprocess' 
        ' --features={}'
        ' --train-data-percentage={}'
    ).format(','.join(features), train_data_pct)

    os.system(command)


def train(job_name, feature_name, model_name, head_type, filter, kernel, learning_rate, path_output, path_tfrecords):
    feature_name = '_'.join(sorted(feature_name.split('_')))

    command = (
        'python -m trainer.train'
        ' --model-name={}'
        ' --head-type={}'
        ' --job-name={}'
        ' --feature-name={}'
        ' --filters={}'
        ' --kernels={}'
        ' --path-tfrecords={}'
        ' --learning-rate={}'
        ' --ex-path={}'
        ' --epoch-num={}'
    ).format(model_name, head_type, job_name, feature_name, filter, kernel, path_tfrecords, learning_rate, path_output, EPOCH_NUM)

    os.system(command)


def main():
    for feature_name in FEATURE_NAMES:
        for train_data_pct in TRAIN_DATA_PERCENTAGES:
            make_data(feature_name, train_data_pct)
            for model_name in MODEL_NAMES:
                for head_type in HEAD_TYPES:
                    for learning_rate in LEARNING_RATES:
                        for filter in FILTERS:
                            for kernel in KERNELS:
                                for num_test in range(NUM_TESTS):
                                    print('running ', model_name, ' test number ', num_test)
                                    job_name = make_job_name()

                                    dir_tfrecords = feature_name + '_' + str(train_data_pct)
                                    path_tfrecords = os.path.join('data', 'processed', dir_tfrecords, 'tfrecords')
                                    path_output = os.path.join(
                                        'output', EXAMPLE_NAME, str(train_data_pct),
                                        str(learning_rate), model_name, feature_name)

                                    print(f'tfrecords are at: {path_tfrecords}')
                                    print(f'outputs are at: {path_output}')

                                    train(job_name, feature_name, model_name, head_type, filter, kernel,
                                          learning_rate, path_output, path_tfrecords)


if __name__ == '__main__':
    main()
