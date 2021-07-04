
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import re
import time

try:
    print("기상청에서 날씨정보를 가져오는 중입니다. 잠시 기다려주세요.")
    print("크롤링 중..")
    start = time.time()
    with open('C:\\Users\\juho3\\Desktop\\Python\\Fundamental_BigData_programming_course\\20121277_김주호_FinalProject\\Data\\averages_monthly_temperature.txt', 'wt') as fp:
        for year in range(2016, 2019):
            # 입력한 url의 웹페이지의 소스코드를 가져온다. 2016년도, 2017년도, 2018년도의 월평균 기온 정보를 가져온다.
            html = requests.get("https://www.weather.go.kr/weather/climate/past_table.jsp?stn=108&yy=" + str(year) + "&obs=07&x=29&y=5")

            # 소스코드를 tree구조로 parsing한다.
            soup = bs(html.text, 'html.parser')

            # findAll 함수를 사용하여, 'tr' 태그명의 data에 접근한다.
            data1 = soup.findAll('tr')

            # 정규표현식을 이용하여, 원하는 정보를 추출한다. 원하는 정보는 data[-1]에 있다.
            pattern = re.compile("(?<=<td>).+(?=<\/td>)")
            temperatures = pattern.findall(str(data1[-1]))

            # 2016년은 6월달부터의 정보를 text 파일에 입력,
            # 2017년은 모든 달의 정보를 text 파일에 입력,
            # 2018년은 10월달까지의 정보를 text파일에 입력
            if year == 2016:
                fp.write('\n'.join(temperatures[5:]))
                fp.write("\n")
            elif year == 2017:
                fp.write('\n'.join(temperatures))
                fp.write("\n")
            else:
                fp.write('\n'.join(temperatures[:10]))       
                
    print("2016-06 ~ 2018-10 의 월평균 기온 정보가 해당 디렉토리에 text파일로 성공적으로 저장되었습니다.")
    end = time.time()
    
    print("크롤링에 소요된 시간은 %.2f초 입니다.\n\n" %(end- start))
    
except FileNotFoundError:
    print("파일 쓰기 Error!! 해당 디렉토리를 찾을 수 없습니다.")

if __name__ == "__main__":
    print("-----------------------------------------------------------------------------")
    print("해당 웹페이지에서 월평균 기온의 데이터는 아래의 형태로 저장되어 있습니다.")
    pprint(data1[-1])
