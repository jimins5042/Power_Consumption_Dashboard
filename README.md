구현 중...

# 프로젝트 소개

- 인공지능 기반의 주간 전력수급현황 예측 및 관리 시스템
- 민간 발전 전력 거래 플랫폼

</br>

# 프로젝트 개요

국내 전력계통 운영을 담당하는 한국전력거래소는 SMP(계통한계가격)의 결정, 발전 계획 수립, 장·단기 전력 수급 분석 등을 위해 전력수요예측 업무를 수행하고 있다.
발전기 예방 정비 계획, 송·변전 설비 유지 보수 계획 및 예비력 운용 등 안정적인 전력계통 운영을 위해 전국 단위의 240시간 전력수요예측이 필수적이다.

기존 지수이동가중평균법을 이용한 주간전력 수요예측 프로그램(KMLF)은 전력수요의 시계열적 특성을 반영할 수 있지만 다양한 변동 요인을 체계적으로 반영하기에는 한계가 있다. 
최근 기후변화와 탄소중립 실천을 위한 재생에너지 확대 보급, 신재생 발전설비의 급격한 증가 등으로 전력계통 운영의 어려움이 가중되고 있다.

본 프로젝트에서는 기상관측 데이터를 반영한 인공지능 기반의 주간전력 수요예측 기법을 제안하여 기존 예측 모형 대비 정확도 개선 효과를 정량적으로 분석하였고, 이를 통해 전력계통 운영의 안정성을 높이는 데 기여하고자 한다.  

나아가, 전력 수요량 예측값을 시각적으로 나타낸 대시보드와 전력 거래 자료에 특화된 LLM을 구축하여 전력 거래 입문 난이도를 낮추고, 전력 거래 플랫폼을 구현하여 민간 발전 전력 수급이 원활해지는 것을 목표로 한다.

</br>

# 핵심 기능

- LSTM, Prophet 기반 전력 수요량 예측 알고리즘
- 전력 예측 수요량 시각화 대시보드
- 전력 거래 정보 특화 LLM 모델 (RAG 모델)
- 전력 거래 플랫폼

</br>

# 화면 구성 (임시)

## 주간전력 수요예측 대시보드

![포스트 2](https://github.com/jimins5042/Power_Consumption_Dashboard/assets/28335699/53a1cc7c-c13f-434f-a49e-f39feb0f0abd)

## 전력 거래 특화 LLM

![포스트 3 (6)](https://github.com/jimins5042/Power_Consumption_Dashboard/assets/28335699/bd17cab4-82fe-4de6-8457-b81d9baff57f)

# 구현 과정

[![Velog's GitHub stats](https://velog-readme-stats.vercel.app/api?name=2jooin1207&slug=전력수급현황-예측-및-관리-시스템-만들기-개요)](https://velog.io/@2jooin1207/series/%EC%A0%84%EB%A0%A5%EC%88%98%EA%B8%89%ED%98%84%ED%99%A9-%EC%98%88%EC%B8%A1-%EB%B0%8F-%EA%B4%80%EB%A6%AC-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EB%A7%8C%EB%93%A4%EA%B8%B0)


