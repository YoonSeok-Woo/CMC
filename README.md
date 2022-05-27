# Cyber Maxlevel Coach


<h3> 인공지능 기반 자세 교정 서비스</h3>

> PT를 받고 싶지만 상황적 여건이 안되는 사람들을 위한
> 홈 트레이닝 지원 서비스
>
> > 유튜브 영상을 가져와 나의 웹캠을 통해 동작을 비교하고, <br/>
> > 실시간으로 사이버코치의 피드백을 받아 동작을 교정!

## 📎  프로젝트 목차

---

- [Cyber Maxlevel Coach](#Cyber Maxlevel Coach)<br/>
- [프로젝트 목차](#프로젝트-목차)
  - [1️⃣ 프로젝트 소개](#1️⃣-프로젝트-소개)
    - [기술 스택](#기술-스택)
  - [2️⃣ 프로젝트 파일 구조](#2️⃣-프로젝트-파일-구조)
  - [3️⃣ 프로젝트 산출물](#3️⃣-프로젝트-산출물)
  - [4️⃣ 프로젝트 빌드](#4️⃣-프로젝트-빌드)

## 1️⃣ 프로젝트 소개

---

1. 일정 : 22.02.21 - 22.04.08 (총 6주)
   - Sub1 : 22.02.21 - 22.03.04
   - Sub2 : 22.03.05 - 22.03.18
   - Sub3 : 22.03.19 - 22.04.08
   - [세부 일정](https://important-leopon-e7f.notion.site/e4ab857bff8843f6bbb5c802593dc98a?v=158d7df35c3f4ed398c58b0278de6ec0)
2. 인원 (총 6인)
   - 김승현 : Front-end, 팀장
   - 김영진 : Back-end
   - 노태현 : AI
   - 박세진 : AI
   - 박소율 : Back-end
   - 우윤석 : AI

### 기술 스택

1. 이슈관리 : Jira
2. 형상관리 : Gitlab
3. 커뮤니케이션 : Mattermost, Notion
4. 개발환경
   - OS : Windows 10
   - IDE
     - Visual Studio Code
   - Frontend
     - Vue 3.0.0
     - Vuex 4.0.0-0
   - Backend
     - Django 3.2.12
   - Database : SQLite3
   - CI/CD
     - Jenkins
     - nginx
     - aws ec2
     - Docker

## 2️⃣ 프로젝트 폴더 구조

---

- Back

  ```bash
  C:.
  ├─accounts			// accouts app
  ├─cmc				// django project
  ├─exercises			// exercises app
  ├─reports			// reports app
  │  ├─management
  │  │  └─commands
  └─schedules			// schedules app
       └─management
            └─commands
  ```

- Front
  ```bash
  .root
  ├─node_modules
  ├─public
  └─src
      ├─api           // 비동기 api
      ├─assets
      ├─components    // 컴포넌트
      ├─config        // 설정파일
      ├─router        // 라우터
      ├─store         // 상태 관리
      │  └─modules
      └─views         // 뷰 페이지
  ```

## 3️⃣ 프로젝트 산출물

---

- 프로젝트 관리 : [Notion](https://important-leopon-e7f.notion.site/71b33081c3244e59a28ae814f53a67e1)
- [서비스 흐름도](https://lab.ssafy.com/s06-ai-image-sub2/S06P22A502/-/blob/master/%EC%82%B0%EC%B6%9C%EB%AC%BC/%EC%84%9C%EB%B9%84%EC%8A%A4%20%ED%9D%90%EB%A6%84%EB%8F%84/%EC%84%9C%EB%B9%84%EC%8A%A4%20%ED%9D%90%EB%A6%84%EB%8F%84.PNG)
- [ERD](https://lab.ssafy.com/s06-ai-image-sub2/S06P22A502/-/blob/master/%EC%82%B0%EC%B6%9C%EB%AC%BC/ERD/ERD.png)
- [서비스 아키텍처](https://lab.ssafy.com/s06-ai-image-sub2/S06P22A502/-/blob/master/%EC%82%B0%EC%B6%9C%EB%AC%BC/%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90.PNG)
- [API 문서](https://lab.ssafy.com/s06-ai-image-sub2/S06P22A502/-/blob/master/%EC%82%B0%EC%B6%9C%EB%AC%BC/API%20%EB%AC%B8%EC%84%9C/API%20%EB%AC%B8%EC%84%9C.pdf)
## 4️⃣ 프로젝트 빌드

---

- [포팅 메뉴얼](https://lab.ssafy.com/s06-ai-image-sub2/S06P22A502/-/tree/master/exec)
