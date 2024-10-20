# 定义要写入的列表
import time
def write_data(data):
    # 定义文件名
    file_name = './data/'+str(time.time().__int__())+".txt"
    # 写入数据
    with open(file_name, 'w', encoding='utf-8') as file:
        # 使用join方法将列表中的元素用逗号连接，并写入文件
        file.write(','.join([str(i) for i in data]))

