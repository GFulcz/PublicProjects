
import os
from math import inf
from tkinter import filedialog
import pandas as pd
from enum import Enum





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

class AnalysisType(Enum):
    '''
    Possible types of statistical analysis within perform_dataframe_analysis function
    '''
    TYPE_MAX, TYPE_MIN, TYPE_SUM, TYPE_MEAN, TYPE_STD, TYPE_CONFIDENCE_INTERVAL = range(6) 
    # ['max', 'min', 'sum', 'mean', 'median', 'std', 'Confidence_interval']

class ResultsType(Enum):
    '''
    Possible types of results representation after using perform_dataframe_analysis function
    '''
    TYPE_FILL_WITH_GROUPED, TYPE_CALCULATE_RELATIVE_GROUPED = range(2)
    # ['fill_with_grouped', 'calculate_relative_grouped']


def perform_dataframe_analysis(user_dataframe: pd.DataFrame, grouping_columns: list[str], 
                               exclude_columns: list[str], analysis_type: str = AnalysisType.TYPE_MEAN, 
                               results_type: str = ResultsType.TYPE_CALCULATE_RELATIVE_GROUPED, precision: int = 3,
                               exclude_recognised_boolean_columns: bool = True,
                               grouping_dropna: bool = False) -> pd.DataFrame:
    '''
    TODO

    '''
    if True:
        # # TODO analysis type 'all'
        # # for analysis type "all" add logic to exclude earlier analysed columns 
        # # function to regex out columns containing '* _rel(*)' '* _abs[*]' into exclude columns

        # # TODO
        # std_Confidence_interval: 1 #default 1
        # # TODO 
        # # DataFrame_presentation: 'str' = 'merged' #or 'separate_files'
        # # TODO convert original/grouped/compared_row_dict to numpy arrays to speed up the program 

        # TODO
        # pokemon example
        # columns for grouping: Type 1, Type 2
        # columns to be excluded: Legendary, Generation
        # causes Pandas errors - possibly due to some pokemons not having Type 2 property and those values are deleted by drop_na.
        # needed to add some logic around this, probably addivng values to nan fields in grouping columns


        if exclude_recognised_boolean_columns:
            boolean_columns = _list_detected_boolean_columns(user_dataframe)
            exclude_columns += boolean_columns

        groups_dataframe = user_dataframe.groupby(by=grouping_columns, dropna=grouping_dropna)

    Analysistype_valid = ['max', 'min', 'sum', 'mean', 'median', 'std', 'Confidence_interval']        



    match analysis_type:
        # https://stackoverflow.com/questions/69854421/python-match-case-using-global-variables-in-the-cases-solvable-by-use-of-classe




        case AnalysisType.TYPE_MAX :
            Grouped_results = pd.DataFrame(groups_dataframe.max(numeric_only = True).round(precision))
        case 'min':
            Grouped_results = pd.DataFrame(groups_dataframe.min(numeric_only = True).round(precision))
        case 'sum':
            Grouped_results = pd.DataFrame(groups_dataframe.sum(numeric_only = True).round(precision))
        case 'mean':
            Grouped_results = pd.DataFrame(groups_dataframe.mean(numeric_only = True).round(precision))
        case 'median':
            Grouped_results = pd.DataFrame(groups_dataframe.median(numeric_only = True).round(precision))
        case 'std':
            Grouped_results = pd.DataFrame(groups_dataframe.std(numeric_only = True).round(precision))
        # TODO - implement analysis if values are within confidence interval
        # https://en.wikipedia.org/wiki/Standard_deviation#Rules_for_normally_distributed_data
        case 'Confidence_interval':
            raise NotImplementedError('Not yet implemented')
        case _ :
            raise ValueError(f'Analysistype: Analysistype must be one of {analysis_type_valid}') 


    
    


    match results_type:
        case 'fill_with_grouped':
            df_range = range(user_dataframe.shape[0])
            Dataframe_grouped = pd.DataFrame(data=None, columns=user_dataframe.columns)
            for i, row in enumerate(df_range):
                original_row = user_dataframe.iloc[row]
                original_row_dict = original_row.to_dict()
                original_row_index = tuple(original_row[grouping_columns].values)
                grouped_row_dict = Grouped_results.loc[original_row_index].to_dict()


                grouped_values_dict = _fill_grouped_rows(original_row_dict, grouped_row_dict, exclude_columns)
                last_index = Dataframe_grouped.shape[0]
                Dataframe_grouped.loc[last_index] = grouped_values_dict


        case 'calculate_relative_grouped':
            df_range = range(user_dataframe.shape[0])
            Dataframe_compared = pd.DataFrame(data=None, columns=user_dataframe.columns)
            for i, row in enumerate(df_range):
                original_row = user_dataframe.iloc[row]
                original_row_dict = original_row.to_dict()
                original_row_index = tuple(original_row[grouping_columns].values)
                grouped_row_dict = Grouped_results.loc[original_row_index].to_dict()


                compared_row_dict = _compare_rows_relative(original_row_dict, grouped_row_dict, exclude_columns, precision)
                last_index = Dataframe_compared.shape[0]
                Dataframe_compared.loc[last_index] = compared_row_dict


        case _ :
            raise ValueError(f'Resultstype: Resultstype must be one of {ResultsType}') 


    if Dataframe_grouped.size != 0:
        changed_columns = _list_changed_columns(Grouped_results, exclude_columns, grouping_columns)
        new_column_names = _list_new_column_names(changed_columns, analysis_type, grouping_columns, name='abs')
        rename_dict = dict(zip(changed_columns, new_column_names))
        Dataframe_grouped.rename(columns=rename_dict, inplace=True)

        return Dataframe_grouped

    if Dataframe_compared.size != 0:
        changed_columns = _list_changed_columns(Grouped_results, exclude_columns, grouping_columns)
        new_column_names = _list_new_column_names(changed_columns, analysis_type, grouping_columns, name='rel')
        rename_dict = dict(zip(changed_columns, new_column_names))
        Dataframe_compared.rename(columns=rename_dict, inplace=True)

        return Dataframe_compared



def select_file() -> str:
    file_path = filedialog.askopenfilename(title="Select a .csv file")
    if file_path:
        print("Selected file:", file_path)
    else:
        print("No file selected.")
    
    return file_path



if __name__ == '__main__':
    filetype_valid = ['.csv', '.xls', '.xlsx']
    Analysistype_valid = ['max', 'min', 'sum', 'mean', 'median', 'std', 'Confidence_interval']
    Resultstype_valid = ['fill_with_grouped', 'calculate_relative_grouped', 'both']


    print("Please select a file to analyse")
    file_path = select_file()
    basename = os.path.basename(file_path)
    basename_ext_only = os.path.splitext(basename)[1]
    basename_no_ext = os.path.splitext(basename)[0]
    dirname = os.path.dirname(file_path)
  
    match basename_ext_only:
        case '.csv':
            df = pd.read_csv(file_path)
            if len(df.columns.to_list()) == 1:
                df = pd.read_csv(file_path, sep=';')    
        case '.xls':
            df = pd.read_excel(file_path)
        case '.xlsx':
            df = pd.read_excel(file_path)
        case _ :
            raise ValueError(f'Value error: selected file has unknown extension. Following file extensions are supported: {filetype_valid}')


    print("The file contains followint columns:")
    print(df.columns.tolist())


    user_input = str(input('Please select columns for grouping from the above, separated by a "," comma:\n'))
    user_input = user_input.split(sep=',')
    Grouping_columns = []
    for col in user_input:
            Grouping_columns.append(str(col).strip())
    print(f'The input is interpreted as: {Grouping_columns}')
    for col in Grouping_columns:
        if col not in (df.columns.tolist()):
            print(f'Column "{col}" not recognised in the original file. Please try again\n')



    #TODO
    # while iter < limit:
    #     grouping = str(input('Please select columns for grouping from the above, separated by a "," comma:\n'))
    #     grouping = grouping.split(sep=',')
    #     Grouping_columns = []
    #     for col in grouping:
    #          Grouping_columns.append(str(col).strip())
        
    #     correct_columns = 0
    #     for col in Grouping_columns:
    #         if col not in (df.columns.tolist()):
    #             print(f'Column "{col}" not recognised in the original file. Please try again\n\n')
    #             continue
    #         else:
    #             correct_columns += 1
    #         if correct_columns == (len(Grouping_columns)-1):
    #             iter = limit+1
                
    #     if iter == limit:
    #         print('Limit of tries exceeded, please try again')
    

    user_input = str(input('\nPlease select columns to be excluded from the analysis, separated by a "," comma:\n'))
    user_input = user_input.split(sep=',')
    Exclude_columns = []
    for col in user_input:
            Exclude_columns.append(str(col).strip())
    print(f'The input is interpreted as: {Exclude_columns}\n')
    for col in Exclude_columns:
        if col not in (df.columns.tolist()):
            print(f'Column "{col}" not recognised in the original file. Please try again\n')
        


    print(f'Please choose Analysis type from: {Analysistype_valid}')
    user_input = str(input())
    Analysistype = str(user_input).strip()
    print(f'The input is interpreted as: {Analysistype}\n')


 
    print(f'Please choose Result type from: {Resultstype_valid}')
    user_input = str(input())
    Resultstype = str(user_input).strip()
    print(f'The input is interpreted as: {Resultstype}\n')

            
    print('The rest of the parameters has ben set as:')
    print('Precision = 3')
    print('Exclude_recognised_boolean_columns = True')
    print('Grouping_dropna = False')
    print('If you\'d like to change them, please use perform_dataframe_analysis() function from this file\n')

    if Resultstype == 'both':
        df_result = perform_dataframe_analysis(df, Grouping_columns, Exclude_columns, Analysistype, Resultstype_valid[0])
        file_path = '{}{}{}'.format(dirname, os.sep, f'{basename_no_ext}_results_{Resultstype_valid[0]}_{Analysistype}')
        df_result.to_csv(file_path +'.csv')
        df_result.to_excel(file_path + '.xlsx')

        df_result = perform_dataframe_analysis(df, Grouping_columns, Exclude_columns, Analysistype, Resultstype_valid[1])
        file_path = '{}{}{}'.format(dirname, os.sep, f'{basename_no_ext}_results_{Resultstype_valid[1]}_{Analysistype}')
        df_result.to_csv(file_path +'.csv')
        df_result.to_excel(file_path + '.xlsx')

    else:
        df_result = perform_dataframe_analysis(df, Grouping_columns, Exclude_columns, Analysistype, Resultstype)
        file_path = '{}{}{}'.format(dirname, os.sep, f'{basename_no_ext}_results_{Resultstype}_{Analysistype}')
        df_result.to_csv(file_path + '.csv')
        df_result.to_excel(file_path + '.xlsx')
    
    print(f'Result files have been saved to:\n{dirname}')

