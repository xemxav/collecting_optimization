import pandas as pd
from reference import DATE


class FileLoader:
    """
    The Fileloader class enables the cration and display of panda dataframe from a excel file
    """

    @staticmethod
    def load(path):
        """
        Takes an excel file and create a dataframe. It checks if the the date column is in date format or not.
        If not, it prints an error and exit.
        :param path: path to excel file
        :return: a panda dataframe
        """
        new = None
        try:
            new = pd.read_excel(path)
        except FileNotFoundError:
            print(f"No such file :'{path}'")
            exit(2)
        print(f"Created dataframe for file {path}")
        try:
            new[DATE] = pd.to_datetime(new[DATE], yearfirst=True)
        except ValueError:
            print(f"Date format is not correct in file {path} in column {DATE}")
            exit(2)
        return new

    @staticmethod
    def display(df, n):
        """
        Takes a dataframe and displays n lines
        :param df: a panda dataframe
        :param n: the number of line to be displayed
        """
        if n >= 0:
            print(df.head(n))
        else:
            print(df.tail(-n))
        print("\n[%d rows x %d colums]" % (n, df.shape[1]))
