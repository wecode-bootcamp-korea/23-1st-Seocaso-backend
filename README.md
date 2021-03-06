# Wecode 1st project Seocaso
- 한국의 영화 추천 서비스 [왓챠피디아(WATCHAPEDIA)](https://pedia.watcha.com/ko-KR/) 클론 프로젝트
- 기존과 다르게 기획을 영화 추천 서비스가 아닌 서울 카페 추천 서비스로 변경하였습니다.

## 개발 인원 및 기간
- 개발 기간 : 2021/08/02 - 2021/08/13
- 프론트엔드 : [김다슬](https://github.com/cocacollllla/), [문주영](https://github.com/moonjuyoung1), [소진수](https://github.com/joshhhso)
- 백엔드 : [장호준](https://github.com/bigfanoftim), [최혜림](https://github.com/rimi0108)
- [프론트엔드 github 링크](https://github.com/wecode-bootcamp-korea/23-1st-Seocaso-frontend)

## 프로젝트 선정 이유
- 평소에 본인이 자주 사용하는 사이트이며, 현재 저희의 수준에서 배운 기술들을 적용하기에 난이도가 적합하다고 판단했습니다.

## [데모 영상](https://youtu.be/V38oqwMjnoI)

## 적용 기술 및 구현 기능
### 적용 기술
- Front-End : Javascript, React.js, sass, react-modal
- Back-End : Python, Django web framework, Bcrypt, My SQL, pyjwt
- Common : RESTful API, POSTMAN

### 구현 기능
#### 회원가입 / 로그인
- bcrypt 암호화
- 정규표현식을 이용한 이메일, 패스워드 유효성 검사
- 로그인 시 jwt 토큰 발급

#### 메인 페이지 
- 카페 평점 랭킹
- 카페 리뷰 랭킹

#### 카페 상세 페이지
- 좋아요 기능
- 점수 평가 기능
- 별점 그래프 기능
- 리뷰, 코멘트(대댓글) 기능
- 리뷰 좋아요 기능
- 같은 지역 내 카페 추천 기능

#### 마이 페이지
- 해당 유저가 '좋아요' 누른 카페 목록
- 해당 유저가 점수 평가한 카페 목록
- 각 카페 목록 필터링 기능 (평점 순, 평점 역순)

#### 검색 페이지
- 카페명 검색 결과 목록
- 카페 주소 검색 결과 목록

## Reference

- 이 프로젝트는 [왓챠피디아(WATCHAPEDIA)](https://pedia.watcha.com/ko-KR/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.


