
import os
from math import inf
from tkinter import filedialog
from enum import Enum
import pandas as pd

class AnalysisType(Enum):
    '''
    Possible types of statistical analysis within perform_dataframe_analysis function.
    '''
    TYPE_MAX, TYPE_MIN, TYPE_SUM, TYPE_MEAN, TYPE_MEDIAN, TYPE_STD, TYPE_CONFIDENCE_INTERVAL = range(7)

    @classmethod
    def valid_name(cls) -> list:
        '''
        Returns a list of valid elements included in this Enum.
        '''
        values = []
        for enum in cls:
            values.append(enum.name)
        return values
        # TODO change this from iterative process to a map() function maybe
        # that would require calling .name attribute of Enum class as a
        # function for every object in list created by list(AnalysisType)
        # ['max', 'min', 'sum', 'mean', 'median', 'std', 'Confidence_interval']

class ResultsType(Enum):
    '''
    Possible types of results representation after using perform_dataframe_analysis function.
    '''
    TYPE_FILL_WITH_GROUPED, TYPE_CALCULATE_RELATIVE_GROUPED = range(2)
    # ['fill_with_grouped', 'calculate_relative_grouped']

    @classmethod
    def valid_name(cls) -> list:
        '''
        Returns a list of valid elements included in this Enum.
        '''
        values = []
        for enum in cls:
            values.append(enum.name)
        return values
        # TODO change this from iterative process to a map() function maybe
        # that would require calling .name attribute of Enum class as a
        # function for every object in list created by list(AnalysisType)
        # ['max', 'min', 'sum', 'mean', 'median', 'std', 'Confidence_interval']


def perform_dataframe_analysis(user_dataframe: pd.DataFrame,
                               grouping_columns: list[str],
                               exclude_columns: list[str],
                               analysis_type: str = AnalysisType.TYPE_MEAN.name,
                               results_type: str = ResultsType.TYPE_CALCULATE_RELATIVE_GROUPED,
                               precision: int = 3,
                               exclude_recognised_boolean_columns: bool = True,
                               grouping_dropna: bool = False,
                               fill_NaN_values_of_grouping_columns: bool = True) -> pd.DataFrame:
    '''
    Perform analysis on a given DataFrame by grouping and aggregating data.

    This function allows the user to group a dataset by specified columns and perform 
    analysis on the grouped data. It returns the analyzed data in dataframe format, with renamed columns.

    Parameters:
    user_dataframe (pd.DataFrame): The dataframe to analyze.
    grouping_columns (list[str]): Columns to group the data by. These should be columns 
                                  representing categorical information.
    exclude_columns (list[str]): Columns to exclude from analysis to avoid.
    analysis_type (str): The type of analysis to perform. Options include TYPE_MAX, TYPE_MIN, 
                         TYPE_SUM, TYPE_MEAN, TYPE_MEDIAN, TYPE_STD, TYPE_CONFIDENCE_INTERVAL. 
                         Default is 'TYPE_MEAN'.
    results_type (str): The type of results to return. Options include TYPE_FILL_WITH_GROUPED, 
                        TYPE_CALCULATE_RELATIVE_GROUPED. Default is 'TYPE_CALCULATE_RELATIVE_GROUPED'.
    precision (int): The number of decimal places to round the results to. Default is 3.
    exclude_recognised_boolean_columns (bool): Whether to exclude columns containing only values of [0,1],
                                               considered as Boolean data. Default is True.
    grouping_dropna (bool): Whether to drop NA values during grouping. Default is False.
    fill_NaN_values_of_grouping_columns (bool): Whether to fill NaN values with a 'NaN' str in grouping columns 
                                                before analysis. Default is True.

    Returns:
    pd.DataFrame: The DataFrame with the analysis results.
    '''

    if fill_NaN_values_of_grouping_columns:
        user_dataframe[grouping_columns] = user_dataframe[grouping_columns].fillna(value='NaN')

    if exclude_recognised_boolean_columns:
        boolean_columns = _list_detected_boolean_columns(user_dataframe)
        exclude_columns += boolean_columns

    groups_dataframe = user_dataframe.groupby(by=grouping_columns, dropna=grouping_dropna)

    match analysis_type:
        # https://stackoverflow.com/questions/69854421/python-match-case-using-global-variables-in-the-cases-solvable-by-use-of-classe
        case AnalysisType.TYPE_MAX.name :
            grouped_results = pd.DataFrame(groups_dataframe.max(numeric_only = True).round(precision))
        case AnalysisType.TYPE_MIN.name:
            grouped_results = pd.DataFrame(groups_dataframe.min(numeric_only = True).round(precision))
        case AnalysisType.TYPE_SUM.name:
            grouped_results = pd.DataFrame(groups_dataframe.sum(numeric_only = True).round(precision))
        case AnalysisType.TYPE_MEAN.name:
            grouped_results = pd.DataFrame(groups_dataframe.mean(numeric_only = True).round(precision))
        case AnalysisType.TYPE_MEDIAN.name:
            grouped_results = pd.DataFrame(groups_dataframe.median(numeric_only = True).round(precision))
        case AnalysisType.TYPE_STD.name:
            grouped_results = pd.DataFrame(groups_dataframe.std(numeric_only = True).round(precision))
        # TODO - implement analysis if values are within confidence interval
        # https://en.wikipedia.org/wiki/Standard_deviation#Rules_for_normally_distributed_data
        case AnalysisType.TYPE_CONFIDENCE_INTERVAL.name:
            raise NotImplementedError('Not yet implemented')
        case _ :
            raise ValueError(f'analysis_type: Must be one of {AnalysisType.valid_name()}')


    match results_type:
        case ResultsType.TYPE_FILL_WITH_GROUPED.name :
            df_range = range(user_dataframe.shape[0])
            dataframe_grouped = pd.DataFrame(data=None, columns=user_dataframe.columns)
            for row in df_range:
                original_row = user_dataframe.iloc[row]
                original_row_dict = original_row.to_dict()
                original_row_index = tuple(original_row[grouping_columns].values)
                grouped_row_dict = grouped_results.loc[original_row_index].to_dict()

                grouped_values_dict = _fill_grouped_rows(original_row_dict, grouped_row_dict, exclude_columns)
                last_index = dataframe_grouped.shape[0]
                dataframe_grouped.loc[last_index] = grouped_values_dict

            assert dataframe_grouped.size != 0, 'The result dataframe is empty. Analysis has failed.'

            changed_columns = _list_changed_columns(grouped_results, exclude_columns, grouping_columns)
            new_column_names = _list_new_column_names(changed_columns, analysis_type, grouping_columns, name='abs')
            rename_dict = dict(zip(changed_columns, new_column_names))
            dataframe_grouped.rename(columns=rename_dict, inplace=True)

            return dataframe_grouped


        case ResultsType.TYPE_CALCULATE_RELATIVE_GROUPED.name:
            df_range = range(user_dataframe.shape[0])
            dataframe_compared = pd.DataFrame(data=None, columns=user_dataframe.columns)
            for row in df_range:
                original_row = user_dataframe.iloc[row]
                original_row_dict = original_row.to_dict()
                original_row_index = tuple(original_row[grouping_columns].values)
                grouped_row_dict = grouped_results.loc[original_row_index].to_dict()

                compared_row_dict = _compare_rows_relative(original_row_dict, grouped_row_dict, exclude_columns, precision)
                last_index = dataframe_compared.shape[0]
                dataframe_compared.loc[last_index] = compared_row_dict

            assert dataframe_compared.size != 0, 'The result dataframe is empty. Analysis has failed.'

            changed_columns = _list_changed_columns(grouped_results, exclude_columns, grouping_columns)
            new_column_names = _list_new_column_names(changed_columns, analysis_type, grouping_columns, name='rel')
            rename_dict = dict(zip(changed_columns, new_column_names))
            dataframe_compared.rename(columns=rename_dict, inplace=True)

            return dataframe_compared


        case _ :
            raise ValueError(f'Resultstype: Resultstype must be one of {ResultsType.valid_name()}')




def _list_detected_boolean_columns(_df) -> list:
    boolean_columns = []
    for _col in _df.columns:
        if _df[_col].unique().tolist() == ([1,0] or [0,1]):
            boolean_columns.append(_col)

    return boolean_columns

def _list_changed_columns(grouped_df, excluded_columns: list, grouped_columns: list) -> list:
    changed_columns = grouped_df.columns.tolist()
    changed_columns = list(set(changed_columns) - set(excluded_columns))
    changed_columns += grouped_columns

    return changed_columns

def _list_new_column_names(changed_columns: list, analysistype: str,
                           grouped_columns: list, name: str) -> list:
    columns_changed = changed_columns.copy()
    for i, column in enumerate(columns_changed):
        if column in grouped_columns:
            columns_changed[i] = f'{column}_group'
            continue
        columns_changed[i] = f'{column}_{name}({analysistype})'

    return columns_changed

def _fill_grouped_rows(original_dict: dict, grouped_dict: dict, excluded_columns: list) -> dict:
    result_dict = original_dict.copy()
    for key in grouped_dict:
        if key in excluded_columns:
            continue
        result_dict[key] = grouped_dict[key]

    return result_dict

def _compare_rows_relative(original_dict: dict, grouped_dict: dict,
                           excluded_columns: list, precision: int = 3) -> dict:
    result_dict = original_dict.copy()
    for key in grouped_dict:
        if key in excluded_columns:
            continue
        # TODO - how to treat division by 0?
        if grouped_dict[key] == 0:
            result_dict[key] = inf
            continue
        ratio = round(original_dict[key]/grouped_dict[key], precision)
        result_dict[key] = ratio

    return result_dict






def select_file() -> str:
    '''
    This function opens a prompt window to select a file to be used in analysis. 
    '''
    file_path = filedialog.askopenfilename(title="Select a file containing a dataset")
    assert len(file_path) != 0, 'No file was chosen'
    return file_path

class FileType(Enum):
    '''
    Possible types of filetypes able to be opened by included interface.
    '''
    FILE_CSV = '.csv'
    FILE_XLS = '.xls'
    FILE_XLSX = '.xlsx'

    @classmethod
    def valid_value(cls) -> list:
        '''
        Returns a list of valid elements included in this Enum.
        '''
        values = []
        for enum in cls:
            values.append(enum.value)
        return values
        # TODO change this from iterative process to a map() function maybe
        # that would require calling .name attribute of Enum class as a
        # function for every object in list created by list(AnalysisType)
        # ['max', 'min', 'sum', 'mean', 'median', 'std', 'Confidence_interval']

def validate_textinput(text_input: str, valid_options: list, separator: str = ',') -> list | None:
    '''
    This function accepts text_input coming from the user and compares it with possible predefined valid_options.
    '''
    text_input = text_input.split(separator)
    if len(text_input) == 0:
        print('Text input contains no data. Please try again.')
        return None
    text_input_list = []
    for item in text_input:
        item = item.strip()
        text_input_list.append((item))
    invalid_inputs = []
    for item in text_input_list:
        if item not in valid_options:
            invalid_inputs.append(item)
    if len(invalid_inputs) != 0:
        print(f'''
                Value(s):
                {invalid_inputs}
                not recognised within valid options:
                {valid_options}
                Please try again.\n''')
        return None
    return text_input_list




if __name__ == '__main__':
    INPUT_LIMIT = 5

    # Text interface
    # Select file with dataset
    print("Please select a file to analyse")
    user_file_path = select_file()
    basename = os.path.basename(user_file_path)
    basename_extension_only = os.path.splitext(basename)[1]
    basename_no_extension = os.path.splitext(basename)[0]
    dirname = os.path.dirname(user_file_path)

    match basename_extension_only:
        case FileType.FILE_CSV.value :
            df = pd.read_csv(user_file_path)
            if len(df.columns.to_list()) == 1:
                df = pd.read_csv(user_file_path, sep=';')
        case FileType.FILE_XLS.value :
            df = pd.read_excel(user_file_path)
        case FileType.FILE_XLSX.value :
            df = pd.read_excel(user_file_path)
        case _ :
            raise ValueError(f'''Value error: selected file has unknown extension.
                             Following file extensions are supported: {FileType.valid_value()}''')
        

    
    print("The dataset contains following columns:")
    print(df.columns.tolist())
    valid_columns = df.columns.tolist()


    # User input validation and loops
    iterator = 0
    while iterator < INPUT_LIMIT:
        user_input = str(input('Please select columns for grouping from the above, separated by a "," comma:\n'))
        user_grouping_columns = validate_textinput(user_input, valid_columns)
        print(user_grouping_columns)
        if user_grouping_columns is not None:
            break
        iterator += 1
        assert iterator < INPUT_LIMIT, f'Loop limit of {INPUT_LIMIT} has been reached. Please restart the program.'

    iterator = 0
    while iterator < INPUT_LIMIT:
        user_input = str(input('\nPlease select columns to be excluded from the analysis, separated by a "," comma:\n'))
        user_exclude_columns = validate_textinput(user_input, valid_columns)
        if user_exclude_columns is not None:
            break
        iterator += 1
        assert iterator < INPUT_LIMIT, f'Loop limit of {INPUT_LIMIT} has been reached. Please restart the program.'

    iterator = 0
    while iterator < INPUT_LIMIT:
        user_input = str(input(f'\nPlease choose Analysis type from: {AnalysisType.valid_name()}\n'))
        user_analysistype = validate_textinput(user_input, AnalysisType.valid_name())
        if len(user_analysistype) > 1:
            print('Only one analisyis_type can be performed at a time. Please select only one valid option.')
            user_analysistype = None
        if user_analysistype is not None:
            user_analysistype = user_analysistype[0]
            break
        iterator += 1
        assert iterator < INPUT_LIMIT, f'Loop limit of {INPUT_LIMIT} has been reached. Please restart the program.'

    iterator = 0
    while iterator < INPUT_LIMIT:
        user_input = str(input(f'\nPlease choose Result type from: {ResultsType.valid_name()}\n'))
        user_resultstype = validate_textinput(user_input, ResultsType.valid_name())
        if len(user_resultstype) > 1:
            print('Only one results_type can be selected at a time. Please select only one valid option.')
            user_resultstype = None
        if user_resultstype is not None:
            user_resultstype = user_resultstype[0]
            break
        iterator += 1
        assert iterator < INPUT_LIMIT, f'Loop limit of {INPUT_LIMIT} has been reached. Please restart the program.'

    print('The rest of the parameters has ben set as:')
    print('precision = 3')
    print('exclude_recognised_boolean_columns = True')
    print('grouping_dropna = False')
    print('fill_NaN_values_of_grouping_columns = True')
    print('In order to change them, please use perform_dataframe_analysis() function from this file\n')

    df_result = perform_dataframe_analysis(df, user_grouping_columns, user_exclude_columns, user_analysistype, user_resultstype)
    user_file_path = '{}{}{}'.format(dirname, os.sep, f'{basename_no_extension}_results_{user_resultstype}_{user_analysistype}')
    df_result.to_csv(user_file_path + '.csv')
    df_result.to_excel(user_file_path + '.xlsx')
    
    print(f'Result files have been saved to:\n{dirname}')
