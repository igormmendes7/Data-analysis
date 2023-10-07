'''The function first creates a subset of the DataFrame df containing only the columns specified in columns. Then, it applies a lambda function to each row of the subset. The lambda function takes the row as input and returns a string containing the unique values of the columns in columns, separated by hyphens. The unique values are sorted in ascending order and any NaN values are dropped. The string is then left-stripped to remove any leading hyphens.
The lambda function is applied to each row of the subset using the apply() method. The axis argument specifies that the function should be applied to each row individually. The result of the apply() method is a Series of strings.
The Series of strings is then converted to a column in the DataFrame df using the [] operator. The new column is named new_col.
The function then repeats the same process to create a new column named new_col_all. However, the lambda function for this column does not drop any NaN values. This results in a column containing all of the values of the columns in columns, separated by hyphens, even if some of the values are NaN.
Finally, the function returns the DataFrame df with the two new columns added.
Here is an example of how to use the process_columns() function:'''

import pandas as pd

df = pd.DataFrame({'A': ['a', 'b', 'c', 'd'],
                   'B': ['b', 'c', 'd', 'e'],
                   'C': ['c', 'd', 'e', 'f']})

def process_columns(df, columns, new_col, new_col_all):
  subset = df[columns].copy()
  df[new_col] = subset.apply(lambda x: '-'.join(sorted(x.dropna().unique())), axis=1).str.lstrip('-')
  df[new_col_all] = subset.apply(lambda x: '-'.join(x.dropna()), axis=1).str.lstrip('-')
  return df

df = process_columns(df.copy(), ['A', 'B','C'], 'ABC', 'ABC_all')
print(df)

'''U gonna get something like:
         A  B  C    ABC  ABC_all
      0  a  b  b  a-b    a-b-b
      1  b  c  d  b-c-d  b-c-d
      2  c  d  e  c-d-e  c-d-e 
      3  d  e  f  d-e-f  d-e-f'''

