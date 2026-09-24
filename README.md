# trips

직접 짠 여행 일정들을 모아두는 정적 사이트입니다.

- 목록: https://pjok1122.github.io/trips/
- 세토우치 2026: https://pjok1122.github.io/trips/setouchi-2026/

## 구조

```
.
├── index.html            # 여행 목록 (랜딩 페이지)
├── setouchi-2026/
│   └── index.html        # 여행 하나 = 폴더 하나
├── _archive/             # 작업 원본·중간본 (gitignore, 로컬 전용)
│   └── setouchi-2026/
└── .nojekyll             # Jekyll 처리 비활성화
```

빌드 없이 GitHub Pages가 `main` 브랜치 루트를 그대로 서빙합니다.

`_archive/` 는 일정을 만들면서 나온 원본·중간본을 모아두는 곳입니다. gitignore 되어 있어
공개 사이트에는 노출되지 않고, 대신 GitHub에 백업되지도 않습니다. 백업까지 원하면
`.gitignore` 에서 `_archive/` 줄을 지우면 됩니다.

## 새 여행 추가하기

1. 슬러그 폴더를 만들고 HTML을 `index.html` 이름으로 넣습니다. 원본은 `_archive/` 로 옮겨 둡니다.
   ```sh
   mkdir -p kyushu-2027 _archive/kyushu-2027
   cp ~/Downloads/규슈여행.html kyushu-2027/index.html
   mv ~/Downloads/규슈여행.html _archive/kyushu-2027/
   ```
   폴더명은 영문 소문자 + 하이픈으로 (`지역-연도` 권장). 한글 폴더명은 URL이 지저분해지니 피합니다.

2. `index.html` 의 `<div class="trips">` 안에 카드 한 블록을 복사해 맨 위에 추가합니다.
   ```html
   <a class="trip" href="./kyushu-2027/">
     <div class="trip-meta">Japan · 규슈</div>
     <div class="trip-title">여행 제목</div>
     <div class="trip-route">A → B → C</div>
     <div class="trip-dates">N박 N일 · 2027. 1. 1(금) – 1. 5(화)</div>
   </a>
   ```

3. 커밋 후 푸시하면 1~2분 내 반영됩니다.
   ```sh
   git add . && git commit -m "add kyushu-2027" && git push
   ```

## 메모

- 각 여행 HTML은 외부 의존성이 Google Fonts / Google Maps 링크 정도인 단일 파일이라 그대로 두면 됩니다.
- 이미지를 따로 쓰게 되면 해당 여행 폴더 안에 `assets/` 를 만들어 상대 경로로 참조하세요.
- **public 저장소입니다.** 숙소 예약번호, 여권번호, 연락처 같은 개인정보는 일정 HTML에 넣지 마세요.
