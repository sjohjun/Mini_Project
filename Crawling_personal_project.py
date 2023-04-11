# requests는 Python에서 HTTP 요청을 보내는 라이브러리이며,
# BeautifulSoup는 HTML을 파싱하여 데이터를 추출하는 라이브러리입니다.
# 파싱이란? 문자열데이터를 분석하고 분해하여 목적한 패턴에 맞게 문자열의 구조를 결정하는 것
import requests
from bs4 import BeautifulSoup




# 일부 웹 사이트에서 스크래핑 요청을 거부하는 경우가 있기 때문에 이를 우회하기 위해
# 일반적인 브라우저에서 요청하는 것과 같은 값을 가지게 하는것
# 그 다음, 가져온 HTML 문서를 BeautifulSoup 객체로 변환하여 반환
# 이때 'html.parser'를 사용하여 HTML 문서를 파싱하도록 지정

def create_soup(url):
    headers={'User-Agent':'Mozilla/5.0 '} #뒷부분 삭제
    res=requests.get(url,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    return soup
 

# 네이버 날씨 크롤링

# create_soup 함수를 사용하여, 해당 URL의 HTML 문서를 BeautifulSoup 객체로 변환
# 각각의 날씨 정보(최저 기온, 최고 기온, 강수 확률, 현재 온도)는 HTML 문서 내에서
# CSS class를 가진 요소로 표시되어 있는데 soup 객체에서 이를 추출하여,각각의 변수에 저장한다.
#이 때 get_text() 메서드를 사용하여, 해당 요소의 텍스트 값을 가져온다.

def get_weather(city):
    url = f"https://search.naver.com/search.naver?where=\
        nexearch&sm=top_hty&fbm=1&ie=utf8&query={city}날씨"
    soup=create_soup(url)
    min_temp=soup.find('span',{'class':'lowest'}).get_text()
    max_temp=soup.find('span',{'class':'highest'}).get_text()
    rain=soup.find('div',{'class':'cell_weather'}).get_text().strip()
    curr_temp=soup.find('div',{'class':'temperature_text'}).get_text().strip()
    print("---------------------------------------")
    print("현재온도 : ", curr_temp)
    print("최저 기온 : ", min_temp)
    print("최고 기온 : ", max_temp)
    print("강수 확률 : ", rain)
    print("---------------------------------------")
    return "이상입니다."


# 네이버 뉴스 크롤링

# 네이버 뉴스에서는 ul 태그의 class 이름이 "cluster_list"인 태그 내에,
# li 태그의 하위 요소인 a 태그에 뉴스 제목이 포함
# 이를 select 메서드를 사용하여 추출하고, 뉴스 제목을 리스트 형태로 저장

def get_news(category):
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={category}"
    soup = create_soup(url)
    news_list = soup.select("ul.cluster_list li a") 
    news_titles = [news.text for news in news_list]
    return news_titles

#네이버 금융 주식종목 크롤링

# select_one 메서드를 사용하여 추출하고, 각 정보를 저장
# 각 정보에 대해, 문자열에서 탭 문자와 개행 문자를 제거하는 replace 메서드를 적용

def get_stock(code):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    soup = create_soup(url)
    name = soup.select_one('h2 a').text.strip() #종목이름
    name = name.replace('\t','').replace('\n','') 
    marketcap = soup.select_one('#_market_sum').text.strip() #시가총액
    marketcap = marketcap.replace('\t','').replace('\n','')
    per = soup.select_one('#_per').text.strip()
    per = per.replace('\t','').replace('\n','')
    divedends = soup.select_one('#_dvr').text.strip() #배당 수익률
    divedends = divedends.replace('\t','').replace('\n','')
    prof= soup.select_one('.rwidth .f_up').text.strip() #전문가 투자의견
    prof = prof.replace('\t','').replace('\n','')
    s_per = soup.select_one('div~ div+ .gray .strong em').text.strip() #동일 업종 평균 per
    s_per = s_per.replace('\t','').replace('\n','')
    print("----------------------------------------------------------------------------------")
    
    print(f"해당 종목의 이름은 {name}입니다.\n")
    print(f"시가 총액 정보입니다. 현재 {name}의 시가총액은 {marketcap}억원입니다.\n")
    print(f"PER 정보입니다. 현재 {name}의 PER은 {per}배 입니다.\n")
    print(f"배당 정보입니다. 현재 {name}의 배당수익률은 2022.12 기준 {divedends}%입니다.\n")
    print(f"현재 전문가들의 투자의견은 {prof}입니다.\n")
    
    if per > s_per:
        print(f"동일 업종 평균 PER는 {s_per}이므로 동일 업종 평균보다 높습니다.\n")
    elif per < s_per:
        print(f"동일 업종 평균 PER는 {s_per}이므로 동일 업종 평균보다 낮습니다.\n")
    elif per == s_per:
        print(f"동일 업종 평균 PER는 {s_per}이므로 동일 업종 평균과 일치합니다.\n")
        
    print("----------------------------------------------------------------------------------")
    return "이상입니다."


# 사용자와 상호작용하는 함수
def personal_assistant():
    print("----------------------------")
    print("안녕하세요! 개인 비서입니다.")
    print("----------------------------")
    while True:
        try:
            command = input("무엇을 도와드릴까요? (날씨, 뉴스, 주식 / 종료): \n\n")
            if command == "종료":
                print("감사합니다. 다음에 또 만나요!")
                break
                
            elif command == "날씨":
                city = input("어떤 도시의 날씨를 알고 싶으세요? ")
                print(get_weather(city))
                
            elif command == "뉴스":
                category = input("어떤 카테고리의 뉴스를 알고 싶으세요? (정치(100), 경제(101), 사회(102), 문화(103), 세계(104)): ")
                idx = 1;
                for i in get_news(category):
                    if i == "\n\n":
                        continue
                    elif i == "\n\n동영상기사\n":
                        continue
                    print(idx,"  ", i)
                    print("-" * 100)
                    idx+=1
                    
            elif command == "주식":
                code = input("주식 코드 번호를 입력해주세요. (예 : 삼성전자(005930))")
                print(get_stock(code))
                
            else:
                print("잘못된 명령어입니다.")
        except:
            print("오류가 발생했습니다. 다시 입력해주세요.")

# 개인 비서 실행
personal_assistant()