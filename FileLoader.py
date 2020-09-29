import pandas as pd
from reference import DATE
class FileLoader:

    def load(self, path):
        new = pd.read_excel(path)
        print(f"Created dataframe for file {path}")
        try:
            new[DATE] = pd.to_datetime(new[DATE], yearfirst=True)
        except:
            print(f"Date format is not correct in file {path} in column {DATE}")
            exit(2)
        return new

    def display(self, df, n):
        if n >= 0:
            print(df.head(n))
        else:
            print(df.tail(-n))
        print("\n[%d rows x %d colums]" % (n, df.shape[1]))