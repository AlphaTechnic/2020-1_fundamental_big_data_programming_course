
import pandas as pd
import re
# path에 있는 text파일을 가져와서 DataFrame을 생성하는 유틸리티.

def build_DataFrame_from_text(path):
# path 에 있는 데이터를 가져와 DataFrame을 생성하여 돌려준다.

    data_list = []    

    # 해당 파일을 읽어오는 것을 실패했을 경우에 대한 예외처리를 해준다.
    try:
        with open(path, 'rt' ,encoding = 'utf-8') as fp:

            # cafehero_sales.txt 파일의 첫번째 line이 DataFrame의 column이 될 것이다.
            column_name = fp.readline().split()

            while True:
                line = fp.readline()
                if line == '':
                    break

                # 텍스트파일 속 원본 데이터가 1,000,000 처럼 쉼표가 있어서, 이를 제거하는 작업을 정규표현식을 이용해 해주며,
                # refined된 data를 split으로 리스트화 한다.
                line = re.sub(r"[,]", "", line)
                data = line.split()

                # 각 line별 첫번 째 단어인 '2016-09' 같은 날짜는 DataFrame의 index의 역할을 할 것이므로, 문자열 형태로 그대로 담는다.
                # 그 뒤에 오는 n번 째 단어들은 int의 형태로 바꿔 line_refined 리스트에 담고, 
                # 이 완성된 line_refined 리스트를 data_list에 담는다.
                line_refined = []
                for ind, content in enumerate(data):
                    if ind == 0:
                        line_refined.append(content)
                    else:
                        line_refined.append(int(content))

                data_list.append(line_refined)
        
        # data_list의 원소로 있는 line_refined 리스트의 첫 번째원소(=날짜)가 DataFrame의 index가 된다.
        ind = [data_list[i][0] for i in range(len(data_list))]
        cafehero = pd.DataFrame(data = data_list, columns = column_name, index = ind)

        print("해당 파일의 Data를 정상적으로 가져왔습니다.")
        
        return cafehero

    except FileNotFoundError:
        print("파일 읽기 Error!! 해당 파일을 찾을 수 없습니다.")
        
        return None

def add_TextData_to_DataFrame(path, DataFrame, column_name):
    # text파일 에 있는 데이터를 가져와 입력한 DataFrame에 column으로 추가한다.
    with open(path) as fp:
        data_list = list(map(float, fp.readlines()))
        DataFrame[column_name] = data_list
    
    return DataFrame
