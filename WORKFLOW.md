# 여행 페이지 만드는 순서

새 여행을 추가할 때 Claude가 따라야 하는 절차. 세토우치 → 나고야 → 가오슝 → 규슈 → 타이베이 → 오사카 순으로 다듬어진 형식이다.

## 0. 원본 읽기

원본은 매번 형식이 다르다. 설치 없이 표준 라이브러리로 읽는다.

| 원본 | 방법 |
|---|---|
| Notion 공개 페이지 | `POST https://www.notion.so/api/v3/loadPageChunk` + `queryCollection` + `syncRecordValues`. WebFetch는 JS 셸만 와서 안 됨 |
| Google Sheets / Drive | Drive MCP (`read_file_content`). 회사 계정(youngjae.park@woowahan.com)만 연결돼 있어 **개인 계정 파일은 안 보임** → 로컬 다운로드로 받기 |
| `.xlsx` | `zipfile` + `xml.etree`로 직접 파싱 (`scratchpad/xlsxread.py`) |
| `.hwp` (5.x) | OLE 복합문서 파서를 직접 구현 (`scratchpad/hwpread.py`). 이미지는 `BinData/`에서 zlib 해제 후 `sips`로 변환 |

## 1. 지역 조사 (생략 금지)

원본 문서만으로 "이야기"를 쓰지 않는다. **각 지역의 역사·지명 유래·음식 배경을 직접 검색해서** 알고 가면 보이는 것을 따로 만든다. 사용자가 명시적으로 요청한 부분이다.

- 지명의 유래, 왜 그 도시가 그렇게 생겼는지
- 대표 음식이 그 지역에서 나온 이유
- 건축·유적의 성립 배경과 연도
- 발상지에 이설이 있으면 "~설이 유력하다"로 적는다

## 2. 페이지 구조 (세토우치 기준, 전부 동일하게)

```
좌측 고정 모드탭: 일정 / 이야기
├─ #view-itinerary
│   ├─ figure.routemap        전체 동선 지도 (SVG, viewBox 840x330)
│   ├─ nav.days               날짜 탭 (grid, 일수에 맞춰 열 수 조정)
│   └─ section.day × N
│        ├─ dayhead(h2 + datebadge) + p.daylead
│        ├─ figure.routemap   하루 곡선 (SVG, viewBox 840x200)
│        ├─ div.summary       요약 카드 3장
│        ├─ div.transit       이동 다이어그램 (이동 있는 날만)
│        ├─ div.plancard      타임라인 표 (시간 / 일정 / 메모)
│        └─ div.tips          체크포인트
└─ #view-guide
    └─ section.region × N
         ├─ dayhead(h2 + datebadge) + figure.routemap (지역 일러스트 840x170)
         ├─ p.gtext           지역 배경
         ├─ gsub "알고 가면 보이는 것" + ul.glist
         └─ gsub "판단의 기록" + ul.glist
```

CSS는 `setouchi-2026/index.html`의 `<style>` 블록을 그대로 재사용한다.

## 3. 지켜야 할 규칙

- **공개 저장소다. 실명을 넣지 않는다.** 동행자는 "가족 여행 · 3인" 처럼 인원으로, 예약자명도 빼기
- **D-day나 "여행 N일차" 같이 날짜로 계산되는 표시를 넣지 않는다.** 시간이 지나면 이상해진다
- **정산 섹션은 넣지 않는다** (요청 시에만)
- 메모에는 일정에 필요한 사실만. 조사 경위나 후일담은 쓰지 않는다
- 한국어 산문에 em-dash(—) 쓰지 않기

## 4. 렌더링 검증 (빼먹지 말 것)

헤드리스 크롬으로 직접 열어서 눈으로 확인한다.

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --window-size=960,1500 \
  --virtual-time-budget=6000 --screenshot=out.png <file>
```

- 탭을 클릭한 상태를 보려면 파일을 복사해 끝에 `<script>`로 `.click()`을 붙여 렌더
- 모바일은 `--window-size`가 최소 500px이라 안 먹는다. **390px iframe에 담아서** 확인
- 자주 나오는 문제: SVG 라벨 겹침, 어두운 배경에 어두운 글씨, 곡선 양 끝 노드 라벨이 지면 밴드에 묻힘(양 끝은 `up` 배치), 표 열 라벨이 모바일에서 깨짐
- 하루 곡선 노드는 6개를 넘기지 않는다. 7개가 되면 오른쪽 끝에서 라벨이 겹친다
- 크롬 정책으로 `file://`이 막히면 `python3 -m http.server 8899`로 띄우고 `127.0.0.1`로 연다

## 5. 마무리

1. `index.html`(목록)에 카드 추가, 최신 여행이 위로
2. 커밋 후 푸시
3. 확인: `https://pjok1122.github.io/trips/<슬러그>/`

## 푸시 참고

이 저장소는 개인 계정(pjok1122) 소유인데 gh 활성 계정이 회사 계정일 때가 있다.
`.git/config`에 아래가 들어 있어 이 저장소만 pjok1122로 인증한다.

```
[credential]
	helper =
	helper = !f() { echo username=pjok1122; echo "password=$(gh auth token -u pjok1122)"; }; f
```

gh에서 pjok1122가 로그아웃되면 다시 막히니, 그때는 `gh auth login` 후 재시도.

## 남은 일

- [ ] 가고시마 2017 (`~/Downloads/가고시마.hwp`) · 본문에 **3·4일차(12/23, 12/24)가 없음**. 다른 파일이 있는지 확인하거나 기억으로 채운 뒤 작업
- [ ] 가오슝 2025 · 7일차(12/16)와 8일차(12/17)는 일정 시트에 상세가 없어 **가계부 순서로 재구성**했다. 실제와 다르면 수정
- [ ] 나고야 · 노션의 준비물·버킷리스트 토글은 아직 반영하지 않음
