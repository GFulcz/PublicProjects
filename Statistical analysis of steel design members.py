from tkinter import filedialog
import os
import csv

import numpy as np

import sqlite3
# https://stackoverflow.com/questions/70937038/group-by-works-with-select-columns-not-in-group-by

def select_file() -> str:
    file_path = filedialog.askdirectory(title="Select the directory with exported .csv files")
    if file_path:
        print("Selected path:", file_path, '\n')
    else:
        print("No path selected.\n")

    return file_path

def parse_range_string(range_string):
    result = []
    ranges = range_string.split(',')

    for r in ranges:
        if '-' in r:
            start = int(r.split('-')[0])
            end = int(r.split('-')[1])
            result.extend(range(start, end + 1))
        else:
            result.append(int(r))

    return result

if __name__=='__main__':

    print('Please select a directory with .csv files exported')
    dir_path = select_file()
    # dir_path = r"C:\\Users\\Grzegorz\Documents\\GitHub\\Test-repo-GF\\GF\\0__OwnRepo\Statistical\Stahlhalle"
    files_list = os.listdir(dir_path)
    member_results_file: str = None
    member_sections_file: str = None
    for item in files_list:
        if item.startswith("Design Ratios on Members by Member ! Steel Design !"):
            member_results_file = item
        if item == "Sections.csv":
            member_sections_file = item

    # Create SQLite db
    db = sqlite3.connect('RFEM_results.db')
    cur = db.cursor()


    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if len(cur.fetchall()) > 1:
        cur.execute('DROP TABLE IF EXISTS Steel_Design')
        cur.execute('DROP TABLE IF EXISTS Sections')
        # TODO maybe use drop schema?



    # TODO add option for member sets
    # Retrieve clear data from Steel_Design CSV file

    # if True segment used to create collapse/expand code sections
    if True:
        member_results_path: str = '{}{}{}'.format(dir_path, os.sep, member_results_file)
        with open(member_results_path, 'r', encoding='utf-8-sig') as f:
            results = csv.reader(f, delimiter=";")

            headline1 = next(results)
            headline2 = next(results)


            col0_Member_no = headline1[0].replace(' ','_').replace('.','')
            col1_Location_x = f'{headline1[1]}_{headline2[1].split(" ")[0]}'
            col2_Stress_Point_no = f"{headline1[2]}_{headline2[2].replace(' ','_').replace('.','')}"
            col3_Design_Situation_name = f'{headline1[3]}_{headline2[3]}'
            col4_Load_Combination_no = f"{headline1[4]}_{headline2[4].replace('.','')}"
            col5_Design_Check_ratio = f"{headline1[5].replace(' ','_')}_{headline2[5].split(' ')[0]}"
            col6_Design_Check_type = f"{headline1[5].replace(' ','_')}_{headline2[6]}"
            col7_Design_Check_description = f"{headline1[5].replace(' ','_')}_{headline2[7]}"

            headlines: [str] = [col0_Member_no,
                                col1_Location_x,
                                col2_Stress_Point_no,
                                col3_Design_Situation_name,
                                col4_Load_Combination_no,
                                col5_Design_Check_ratio,
                                col6_Design_Check_type,
                                col7_Design_Check_description]



            data: [[str]] = []

            members_total = 0
            for i, line in enumerate(results):

                if line[1].find('|') >= 0:
                    continue
                if len(line[1]) == 0:
                    continue

                members_total = int(line[0])
                data.append((line))


    # Create and populate Steel_Design Table
    if True:
        table_columns: str = ''
        for col in headlines:
            table_columns += f'{col} TEXT, \n'
        table_columns = table_columns[:-3]

        sql: str = f'''
            CREATE TABLE Steel_Design (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                {table_columns}
                ) ;'''

        cur.execute(sql)


        table_columns: str = ''
        for col in headlines:
            table_columns += f'{col}, \n'
        table_columns = table_columns[:-3]

        sql = f'''INSERT INTO Steel_Design ({table_columns})
                    VALUES (?,?,?,?,?,?,?,?);'''
        cur.executemany(sql, data)


    # Create Contains_warning column and delete non numeric ratios
    if True:
        cur.execute("SELECT DISTINCT Design_Check_Ratio FROM Steel_Design ORDER BY Design_Check_Ratio DESC;")

        non_numeric_ratio_val = []
        for result in cur:
            result_value = result[0].replace('.','')
            if result_value.isnumeric() == False:
                non_numeric_ratio_val.append(result_value)


        sql_non_numeric_values:str = ''
        for item in non_numeric_ratio_val:
            sql_non_numeric_values += f" \'{item}\',"
        sql_non_numeric_values= sql_non_numeric_values[:-1]


        cur.execute(f"SELECT DISTINCT Member_No FROM Steel_Design WHERE Design_Check_Ratio IN ({sql_non_numeric_values});")
        members_containing_warning_or_error = []
        for i, result in enumerate(cur):
            members_containing_warning_or_error.append((result))


        cur.execute('ALTER TABLE Steel_Design ADD Contains_Warning_or_Error INTEGER DEFAULT 0')


        sql: str = f'''
            UPDATE Steel_Design SET Contains_Warning_or_Error = 1
                WHERE Member_NO = ?'''
        cur.executemany(sql, members_containing_warning_or_error)


        cur.execute(f'DELETE FROM Steel_Design WHERE DESIGN_CHECK_RATIO IN ({sql_non_numeric_values});')


    # Create ratio_max_des_to_stability_des and fillout calculated ratio
    if True:
        cur.execute('ALTER TABLE Steel_Design ADD Ratio_max_Design_Check_to_Stability INTEGER DEFAULT 0')

        cur.execute('SELECT Member_No, max(cast(Design_Check_Ratio as real)), Design_Check_Description FROM Steel_Design WHERE Design_Check_Description LIKE "Stability%" GROUP BY Member_No ORDER BY cast(Member_No as integer)')
        member_stability_max: [[]] = []
        for result in cur:
            result_list = [(result[0]), float(result[1])]
            member_stability_max.append(result_list)


        cur.execute('SELECT Member_No, max(cast(Design_Check_Ratio as real)) FROM Steel_Design GROUP BY Member_No ORDER BY cast(Member_No as integer)')
        member_ratio_max: [[]]  = []
        for result in cur:
            result_list = [(result[0]), float(result[1])]
            member_ratio_max.append(result_list)
            # print(result)

        ratios_list = []
        for max_list in member_ratio_max:
            for stability_list in member_stability_max:
                if max_list[0] == stability_list[0]:
                    if max_list[1] == 0:
                        max_list[1] = 0.001

                    ratios_list.append([round( (stability_list[1]/max_list[1]) , 3), max_list[0]])
                    # print(f'{[max_list[0]]}, {round( (stability_list[1]/max_list[1]) , 3)}')
                    # print(f'{max_list[0]} {max_list[1]} _ {stability_list[0]} {stability_list[1]}: {round((stability_list[1] /max_list[1]),2) }')
                    # break

        sql: str = f'''
            UPDATE Steel_Design SET Ratio_max_Design_Check_to_Stability = ?
                WHERE Member_NO = ?'''
        cur.executemany(sql, ratios_list)



    #=-=-=-=-=-=-=-=-=-=-=-=-=-=#=-=-=-=-=-=-=-=-=-=-=-=-=-=


    # Retrieve clear data from Sections CSV file
    if True:
        member_sections_path: str = '{}{}{}'.format(dir_path, os.sep, member_sections_file)
        with open(member_sections_path, 'r', encoding='utf-8-sig') as f:
            sections = csv.reader(f, delimiter=';')

            headline1 = next(sections)
            headline2 = next(sections)

            col0_Section_No = headline1[0].replace(' ','_').replace('.','')
            col1_Section_Name = f"{headline2[1].replace(' ','_')}"
            col2_Assigned_to_Members = f"{headline2[2].replace(' ','_').replace('.','')}"
            col3_Material = f'{headline2[3]}'

            headlines: [str] = [col0_Section_No,
                                col1_Section_Name,
                                col2_Assigned_to_Members,
                                col3_Material]


            data: [[str]] = []

            for i, row in enumerate(sections):
                line = [row[0], row[1], row[2], row[3]]
                line[2] = parse_range_string(line[2])
                data.append((line))


    # Parse Sections data into SQL Table form
    if True:
        sections_data: [[]] = []
        for member_number in range(1, members_total+1):
            for i in range(len(data)):
                row = []
                if member_number in data[i][2]:
                    row = [member_number, data[i][0], f"{data[i][0]}: {data[i][1]}", data[i][3]]
                if len(row) != 0:
                    sections_data.append(row)


    # Create and populate Sections Table
    if True:
        sql: str = f'''
            CREATE TABLE Sections (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Member_No TEXT,
                {headlines[0]} TEXT,
                {headlines[1]} TEXT,
                {headlines[3]} TEXT
                ) ;'''

        cur.execute(sql)


        sql = f'''INSERT INTO Sections (Member_No, {headlines[0]}, {headlines[1]}, {headlines[3]})
                    VALUES (?,?,?,?);'''
        cur.executemany(sql, sections_data)


    # Extract all of the useful data from db
    if True:
        sql = f'''
        SELECT
            cast(sd.Member_No as integer) as Member_No,
            Section_Name,
            max(cast(sd.Design_Check_Ratio as real)) as Design_Check_Ratio,
            Contains_Warning_or_Error,
            Ratio_max_Design_Check_to_Stability,
            Loading_No,
            Design_Check_Description

        FROM Steel_Design as sd
        JOIN Sections as s on sd.Member_No = s.Member_No
        GROUP BY sd.Member_No
        ORDER BY s.Section_Name, cast(sd.Member_No as integer); '''


    view = f"""CREATE VIEW IF NOT EXISTS Results AS {sql} """
    cur.execute(view)

    print('PRAGMA of Results table')
    cur.execute('PRAGMA table_info(Results)')
    for x in cur:
        print(x)
    print()


    print("SELECT * FROM RESULTS")
    print("M.no, Section Name, Max Des ratio, warning/error, ratio rel stability, Loading No, description, ")
    cur.execute('SELECT * FROM Results LIMIT 30')
    for x in cur:
        print(x)
    print()


    print('STATISTICAL PARAMETERS')
    cur.execute('SELECT round( avg(Design_Check_Ratio), 3) FROM Results')
    average_ratio: float = 0
    for x in cur:
        average_ratio = x[0]

    print(f'Average Design Check Ratio in whole structure: {average_ratio}')


    cur.execute('SELECT Design_Check_Ratio FROM Results')
    # third_moment: [float] = []
    results_ratios: [float] = []
    for x in cur:
        results_ratios.append(x[0])
    #     value = (x[0]-average_ratio)**3
    #     third_moment.append(value)

    # param = sum(third_moment) / len(third_moment)
    # print(param)


    std_val = np.std(results_ratios)
    print(f'Standard Deviation of Design Check Ratio value in whole structure: {std_val}')

    # print(param/(std_val**3))


    # Delete unused files
    db.close()
    db_filepath = "{}{}{}".format(os.getcwd(), os.sep, 'RFEM_results.db')
    os.remove(db_filepath)


    '''

    - Create table steel desing results with the 'data' variable
    DONE
    - bulk insert the data
    DONE
    - in the same way extract info from Sections.csv
    DONE
    - create table sections in the same schema
    DONE
    - bulk insert the data
    DONE

    - create a query for max design ratio of every member number
    DONE
    - generate a column in Steel_Design table that uses max ratio and assigns ULS|SLS|Stability value to each row
    DONE - skipped assignment of uls/sls


    - create view of index-member_number-section-load_combination-max_ratio-max_description
    DONE
    '''

    '''
    - then based on that create a column plot - vertical: max_ratio value, horizontal: sorted bar graph max_ratio, color coded by section
    - then calculate data skewness coefficient and define  if structure is optimal or not
    - then list out (plot) members with max_description != stability and their max_ratio's
    - then list frequency of each load combination and load combination per section
    - create pdf with this data and graphics
    '''



    # Oracle naming scheme
    # sql: str = f'''
    #     CREATE TABLE Steel_Design (
    #         result_id NUMBER,
    #         Member_No VARCHAR2 (10 CHAR) CONSTRAINT Member_No_NN NOT NULL ENABLE,
    #         Location_x NUMBER,
    #         Stress_Point_No VARCHAR2 (10 CHAR),
    #         Design_Situation VARCHAR2 (5 CHAR),
    #         Loading_No VARCHAR2 (10 CHAR),
    #         Design_Check_Ratio VARCHAR2 (10 CHAR) CONSTRAINT Design_Ratio_NN NOT NULL ENABLE,
    #         Design_Check_Type VARCHAR2 (10 CHAR),
    #         Design_Check_Description VARCHAR2 (150 CHAR)
    #         ) ;