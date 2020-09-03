# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:53:28 2020

@author: wingkwong
"""


def df_writer(
    data_frame, file_path, header=True, mode="overwrite", separator=",",
):
    """
        Writing data frame to external storage systems

        data_frame: the dataframe to be written
        file_path: the directory in where the files will be generated
        header (default true): writes the names of columns as the first line.
        mode (default overwrite): specifies the behavior when data or table already exists
        separator (default ,): sets a single character as a separator for each field and value

    """

    data_frame.repartition(32).write.csv(
        file_path, header=header, mode=mode, sep=separator
    )
