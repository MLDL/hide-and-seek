import os
import pickle
import zipfile 

import wget

from libs.tiny_imagenet_utils import read_tiny_imagenet, save_with_tfrecord
from libs.various_utils import makedirs
from configs.project_config import project_path


# ==============================================================================
# Path
tiny_imagenet_dir_path = "{}/data".format(project_path)
tiny_imagenet_path = "{}/tiny-imagenet-200".format(tiny_imagenet_dir_path)
tiny_imagenet_zip_path = "{}.zip".format(tiny_imagenet_path)

tfrecord_train_dir = "{}/tfrecord/train".format(tiny_imagenet_path)
tfrecord_valid_dir = "{}/tfrecord/valid".format(tiny_imagenet_path)
tfrecord_test_dir = "{}/tfrecord/test".format(tiny_imagenet_path)

pickle_save_path = "{}/pickle/tiny_imagenet.pickle".format(tiny_imagenet_path)


# ==============================================================================
# Download dataset and unzip.

# Download tiny imagenet
print("*"*30)
print("Downlaod dataset start")
print("path: {}".format(tiny_imagenet_zip_path))
makedirs(tiny_imagenet_dir_path)
wget.download("http://cs231n.stanford.edu/tiny-imagenet-200.zip",
              tiny_imagenet_zip_path)

# Unzip the dataset
print("-"*30)
print("unzip dataset")
print("path: {}".format(tiny_imagenet_path))
zip_ref = zipfile.ZipFile(tiny_imagenet_zip_path, 'r')
zip_ref.extractall(tiny_imagenet_dir_path)
zip_ref.close()


# ======================================
# Make Dataset
d = read_tiny_imagenet(tiny_imagenet_path, train_ratio=0.8)


# ======================================
# Tranform the dataset into tfrecords for training.
print("-"*30)
print("Transfrom dataset into tfrecords")
print("tfrecord_train_dir: {}".format(tfrecord_train_dir))
print("tfrecord_valid_dir: {}".format(tfrecord_valid_dir))
print("tfrecord_test_dir: {}".format(tfrecord_test_dir))
save_with_tfrecord(tfrecord_train_dir,
                   X=d['X_train'],
                   Y=d['Y_train'],
                   Y_one_hot=d['Y_train_one_hot'],
                   P=d['P_train'],
                   label_depth=200,
                   shard_size=2000,
                   prefix='train')


save_with_tfrecord(tfrecord_valid_dir,
                   X=d['X_valid'],
                   Y=d['Y_valid'],
                   Y_one_hot=d['Y_valid_one_hot'],
                   P=d['P_valid'],
                   label_depth=200,
                   shard_size=2000,
                   prefix='valid')


save_with_tfrecord(tfrecord_test_dir,
                   X=d['X_test'],
                   Y=d['Y_test'],
                   Y_one_hot=d['Y_test_one_hot'],
                   P=d['P_test'],
                   label_depth=200,
                   shard_size=2000,
                   prefix='test')

# Save the dataset into pickle for evalutation.
print("-"*30)
print("Save the dataset into pickle")
print("pickle_save_path: {}".format(pickle_save_path))
makedirs(os.path.dirname(pickle_save_path))
with open(pickle_save_path, "wb") as f:
    pickle.dump(d, f)
