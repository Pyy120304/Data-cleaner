import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler


# edit
def drop_duplicates(data):
    '''
    Xóa các dòng bị lặp
    '''
    return data.drop_duplicates()


def handle_missing_data(data):
    '''
    Hàm này xử lý các giá trị NaN
    Nếu số lượng NaN nhỏ hơn mức cho phép thì ta có thể drop
    Nếu không, ta thay giá trị mới cho NaN
    '''
    num_missing_rows = data.isnull().any(axis=1).sum()

    if num_missing_rows <= len(data) / 10:
        data = data.dropna()
    else:
        for col in data.columns:
            if data[col].dtype in ['int64', 'float64']:
                # Thay thế NaN bằng mean() cho giá trị định lượng
                data[col] = data[col].fillna(data[col].mean())
            else:
                # Thay thế NaN bằng ffill() cho giá trị định tính
                data[col] = data[col].fillna(method='ffill')
                data[col] = data[col].fillna(method='bfill')
    return data


def adjust_data(data, lst=[], method='Min-Max'):
    if lst == []:
        columns = data.columns
    else:
        columns = lst

    if method == 'Min-Max':
        scaler = MinMaxScaler()
    elif method == 'Z-score':
        scaler = StandardScaler()
    elif method == 'Robust':
        scaler = RobustScaler()
    else:
        raise ValueError("Unknown method: {}".format(method))

    data[columns] = scaler.fit_transform(data[columns])
    return data



# transform
def change_data_type(data, col, type):
    """
    Hàm thay đổi kiểu dữ liệu của một cột trong Data
    """
    if type == 'string':
        data[col] = data[col].astype(str)
    elif type == 'float':
        data[col] = data[col].astype(float)
    elif type == 'datetime':
        data[col] = pd.to_datetime(data[col], errors='coerce')  
    else:
        data[col] = data[col].astype(int)
    return data


def merge_column(data, lst, char):
    """
    Hàm hợp nhất các cột trong DataFrame thành một cột mới dựa trên 
    giá trị char được nhập
    """
    new_col_name = lst[0]
    for i in range(1,len(lst)) :
        new_col_name += (char + lst[i])
    # new_col_name = lst[0] + char + lst[1]
    data[new_col_name] = data[lst].apply(lambda row: char.join(row.astype(str)), axis=1)
    return data


def split_column(data, col, char):
  """
  Hàm tách một cột trong DataFrame thành nhiều cột mới
  """
  split_values = data[col[0]].str.split(char, expand=True)
  new_col_names = [col[0] + '_' + str(i + 1) for i in range(split_values.shape[1])]
  data[new_col_names] = split_values
  return data




# view
def entire_dataset(data):
    info = f"Number of Rows: {data.shape[0]}\n"
    info += f"Number of Columns: {data.shape[1]}\n\n"
    info += "Columns and Data Types:\n"
    info += "-"*30 + "\n"
    for col in data.columns:
        info += f"{col}: {data[col].dtype}\n"
    return info

def frequency_distribution(data, column):
    """
    Trả về bảng phân phối tần số của một cột được chọn từ một DataFrame.
    """
    frequency_data = data[column].value_counts().reset_index()
    frequency_data.columns = [column, 'Frequency']
    
    return frequency_data