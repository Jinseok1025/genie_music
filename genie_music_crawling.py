import requests
from bs4 import BeautifulSoup
import pandas as pd

# 지니 차트 정보를 가져오는 함수
def fetch_genie_chart_data(url):
    # 웹 요청 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # URL에 요청 보내기
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 노래 제목과 아티스트 추출
        song_titles = [title.get_text().strip() for title in soup.select('a.title.ellipsis')]
        song_artists = [artist.get_text().strip() for artist in soup.select('a.artist.ellipsis')]

        # 제목과 아티스트를 결합하여 차트 데이터 생성
        chart_data = list(zip(song_titles, song_artists))
        return chart_data
    else:
        return None

# 지니 차트 페이지 URL 리스트
genie_chart_urls = [
    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20240520&hh=12&rtm=Y&pg=1",
    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20240520&hh=12&rtm=Y&pg=2"
]

# 모든 URL에서 차트 데이터 가져오기
all_chart_data = []
for url in genie_chart_urls:
    chart_data = fetch_genie_chart_data(url)
    if chart_data:
        all_chart_data.extend(chart_data)

# 데이터프레임으로 변환
chart_df = pd.DataFrame(all_chart_data, columns=['Title', 'Artist'])
chart_df['Rank'] = range(1, len(chart_df) + 1)

# 제목과 아티스트를 결합하여 출력용 문자열 생성
chart_df['Title'] = chart_df['Title'] + ' - ' + chart_df['Artist']

# 불필요한 열 제거
chart_df = chart_df[['Rank', 'Title']]

# pandas 출력 옵션 설정 (최대 100행 출력)
pd.set_option('display.max_rows', 100)

# 차트 데이터 출력
for index, row in chart_df.iterrows():
    print(f"{row['Rank']}. {row['Title']}")
