import numpy as np
import pandas as pd
from multiprocess import Pool
from scipy.sparse import csr_matrix
import sys

MAX_SIZE = 1000000  # sys.maxsize throws an error when transforming the data


class Hasher():
    def __init__(self, data=None, size=MAX_SIZE, hash=None):
        """
        Constructor
        :param data: pd.DataFrame | dataframe to sparsify
        :param size: int | size of each sparse vector
        :param hash : function | hash function (optional)
        """
        self.data = data
        self.size = size
        self.hash = hash

    def fit(self, data):
        """
        Fit the instance to data
        :param data: pd.DataFrame | data to fit
        :return: None | set self.data
        """
        self.data = data

    def hash_row(self, row):
        """
        Hashes the values of row mapping it to integers
        Those values will be used as the positions of active features (all set at 1.0)
        in the training sparse matrix
        :param row: list, array | a given row of self.data
        :return: list | list of hash-values/positions
        """
        if self.hash is None:
            # Use python built-in hash function
            hashed_values = list(
                map(lambda x: hash(str(x)) % self.size, list(row)))
        else:
            hashed_values = list(
                map(lambda x: self.hash(str(x)) % self.size, list(row)))
        return hashed_values

    def sparsify(self, row):
        """
        "Sparsify" a given row of data
        :param row: list, array | a given row of self.data
        :return: 2-tuple | tuple containing (positions_active_vales, active_values)
        """
        # TODO: change if you want to take into account continuous values
        return (self.hash_row(row), [1.0] * len(row))

    def transform(self, data, cores=1):
        """
        Creates a sparse matrix from data
        data MUST NOT contain the labels
        :param data: pd.DataFrame | dataframe to sparsify
        :return: scipy.csr_matrix | sparse matrix of shape (data.shape[0], self.size)
        """
        curr_csr_matrix = csr_matrix((data.shape[0], self.size))

        if cores > 1:
            # Multithreaded computing
            def _get_crs_mat(row):
                i, row = row[0], row[1:]
                sparse_row = self.sparsify(row)
                row_csr_matrix = csr_matrix(
                    (sparse_row[1], ([i] * len(row), sparse_row[0])),
                    shape=curr_csr_matrix.shape)
                return row_csr_matrix

            matrix_list = Pool(cores).map(lambda row: _get_crs_mat(row),
                                          data.itertuples())
            curr_csr_matrix = sum(matrix_list)

        else:
            for row in data.itertuples():
                i, row = row[0], row[1:]
                sparse_row = self.sparsify(row)
                curr_csr_matrix = curr_csr_matrix + csr_matrix(
                    (sparse_row[1], ([i] * len(row), sparse_row[0])),
                    shape=curr_csr_matrix.shape)

        return curr_csr_matrix

    def fit_transform(self, data, cores=1):
        self.fit(data)
        return self.transform(self.data, cores=cores)


if __name__ ==  "__main__":
    """
    Here is how to make use of a Hash instance
    """

    # Load your data
    data = pd.read_csv("./data/train.csv")

    # Process your data
    """
     /!\ Important : In order to make sure to have one hash-value per value for each feature
                     you should transform your data to concatenate "feature_name" and "value"
    """
     # transforms
    data_processed = data # to change here

    # Instanciate Hasher
    hash = Hasher(size=10000) # carefully choose "size" parameter no to have collisions when hashing

    # Fit to Data
    data_sparse = hash.fit_transform(data_processed)

    # Now use data_sparse as an entry to your learning model
