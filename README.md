# Grouping_Analysis

Grouping_Analysis is a Python script and function for grouping data within a given dataset and calculating simple reference values to their grouped characteristics.

## Installation

Grouping_Analysis is a single file Python script and doesn't require explicit installation. 
Script uses [pandas](https://pypi.org/project/pandas/) library.

```bash
pip install pandas
```

## FAQ

- What does this do?

This program allows to group selected dataset by categories, analyse it and then retrieve this data back into original file structure.
Grouping can be performed by Categorical or Numerical values. Please note that resulting values are only numerical.
User can also import Perform_DataFrame_Analysis() function to other scrips.

- What do the grouping columns mean?

This is a list of columns inside the analysed file, selected by the user to perform grouping and further analysis. This can be either a singular column, or multiple ones.
When defining this, it's recommended to select columns representing categorical information. 
If a column containing very specific data is selected, such as indexing info - Client Numbers, Item id etc. then the program will yield results identical from original file.

- Why would I want to exclude columns?

Some data uses Numerical values for describing categories. For example calculating average results from this column would not yield any useful info. 
In this case, its recommended to exclude this column.

- What do the analysis_type options mean?

This selects which type of analysis is performed by program. User can select from:
TYPE_SUM, TYPE_MEAN, TYPE_MEDIAN, TYPE_STD, TYPE_CONFIDENCE_INTERVAL

NOTE:
The functionality of TYPE_CONFIDENCE_INTERVAL is to be implemented.

- What do the results_type options mean?

This selectes which type of results are returned back. User can select from: 
TYPE_FILL_WITH_GROUPED, TYPE_CALCULATE_RELATIVE_GROUPED

- What for can I use results_type = TYPE_FILL_WITH_GROUPED?

This can be used to compare original values to the direct results of grouping and analysis.
This can be helpful for example, to use direct mean values of every category to fill NaN values in a given dataset.

- What for can I use results_type = TYPE_CALCULATE_RELATIVE_GROUPED?

This can be used to directly inspect a ratio of a given original value to the calculated grouping value.
This can be helpful to quickly generate a lot of comparative data within a given dataset.

- I am using results_type = TYPE_CALCULATE_RELATIVE_GROUPED argument, my resulting dataset contains inf values, why?

This occurs when grouping result for a given column is equal to zero. When defining a ratio of original value to grouped value a division by zero occurs.
In this case, program defines the ratio value to be inf.

- I see that some of my columns have been excluded from analysis, despite my original input, why?

This could have happend due to default value of exclude_recognised_boolean_columns = True. This allows program to select numerical columns containing only [0,1] values across the whole dataset and exclude them from analysis.
This is now considered to be a Boolean type data and is automatically excluded by program.
You can disable this manually when using imported Perform_DataFrame_Analysis() function.

- What does grouping_dropna argument change?

This is a Pandas functionality of pandas.DataFrame.groupby(dropna=False).
If it is enabled then NaN values together with row/column will be dropped during grouping. If false, NaN values will be treated as the key in groups.
You can enable this manually when using imported perform_dataframe_analysis() function.

- What does the fill_NaN_values_of_grouping_columns change?

This is a safety measure which automatically replacec NaN values with "NaN" str value in the columns selected for grouping. This prevents errors when indexing and calculating values for the resultant dataframe.

- Where did you obtain the data for example files?

They are available on kaggle.com for free, upon registration in the service.
https://www.kaggle.com/datasets/vinicius150987/titanic3
https://www.kaggle.com/datasets/abcsds/pokemon

- I see that inside this file there are many #comments or #TODO notes, why?

This file is a result of a private work on a spare time, partly as a hobby, the TODO notes are my own notes for things that in my opinion should be implemeted/fixed at a later date.
In case of suggestions or comments, I invite you to please get in contact on github.
