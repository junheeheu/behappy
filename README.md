# 가치투자를 위한 가치 평가

## 기업 정보를 받아오자

## 코드 환경

# 개발 환경

## Python 환경
* python: 3.7 이상
* pip3 필요
~~~
apt update
apt -y upgrade
apt-get install -y python3
apt-get install -y python3-pip
~~~
* python3 와 pip3를 기본으로 사용하려면, 아래 파일을 열어 수정
    * Linux: ~/.bashrc 
    * MAC: ~/.bash_profile
~~~
alias python='python3'
alias pip='pip3'
~~~

## 그 외 Lib. Dependencies
~~~
pip install beautifulsoup4 lxml pandas 
~~~

# google sheet 연동
## 인증
* [GCP, Google Cloud Platform 에서 프로젝트 만들기](https://console.cloud.google.com/projectselector2/apis)
![GCP_create_project](./fig/gcp_create_project.png)

## 사용 방법
* [Google Developers 공식 사이트 tutorial](https://developers.google.com/sheets/api/quickstart/python)
    * 인증까지는 이걸 보고 하면 됨.
* [Google Sheet 사용 예제 git](https://github.com/gsuitedevs/python-samples)
* [인증 정보](https://docs.google.com/document/d/1X5YvvzRfTSZ5FUzNDZRmeZh9pi8nLK5o6SamiU_iWbc/edit#)

## 환경 설정
* google api 관련 lib. 설치 필요
~~~
pip install gspread
pip install --upgrade oauth2client

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
~~~


<!--
그림 추가
![ex_screenshot](./img/screenshot.png)

*single asterisks* - 기울임체
_single underscores_ - 기울임체
**double asterisks** - 굵은글씨체
__double underscores__ - 기울임체/굵은글씨체
***triple underscores*** - 기울임체/굵은글씨체
~~cancelline~~ - 취소줄

기본 테이블
| 이름   | 설명  | 나이 |
| ----- | ---- | --- |
| 김태완  | 아빠  | 40 |
| 임선영  | 엄마  | 30 |
| 김민수  | 아들  | 2  |

테이블 정렬
오른쪽 정렬
—-:
왼쪽 정렬
:—-
가운데 정렬
:—-:

| 이름   | 설명  | 나이 |
| :----- | ----: | :---: |
| 김태완  | 아빠  | 40 |
| 임선영  | 엄마  | 30 |
| 김민수  | 아들  | 2  |

링크
[taewan.kim](http://taewan.kim)

참조 링크
[구글][1]
[1]: http://www.google.com

각주
최근 스칼라는 매우 인기가 높은 언어이다.[^scala]
\[^scala]: 스칼라는 마틴 오더시크가 개발한 함수형 언어이다.
-->