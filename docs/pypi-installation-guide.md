# PyPI 패키지로 Claude Desktop에서 사용하기

이 문서는 PyPI에 배포된 `mcp-coupang-server` 패키지를 설치하고 Claude Desktop에서 사용하는 방법을 설명합니다.

## 목차

1. [Git Clone 방식과의 차이점](#git-clone-방식과의-차이점)
2. [사전 요구사항](#사전-요구사항)
3. [패키지 설치](#패키지-설치)
4. [쿠팡 파트너스 API 키 발급](#쿠팡-파트너스-api-키-발급)
5. [Claude Desktop 설정](#claude-desktop-설정)
6. [환경 변수 설정 방법](#환경 변수-설정-방법)
7. [테스트 및 확인](#테스트-및-확인)
8. [문제 해결](#문제-해결)
9. [패키지 업데이트](#패키지-업데이트)

---

## Git Clone 방식과의 차이점

### Git Clone 방식 (개발자용)
```bash
git clone https://github.com/space-cap/mcp-coupang-server.git
cd mcp-coupang-server
uv sync
```
- 소스 코드 직접 관리
- 커스터마이징 가능
- 개발 및 기여에 적합

### PyPI 패키지 방식 (사용자용) ⭐ 권장
```bash
pip install mcp-coupang-server
```
- 간단한 설치 (한 줄)
- 업데이트 간편
- 일반 사용자에게 적합
- **이 문서는 PyPI 패키지 방식을 설명합니다**

---

## 사전 요구사항

### 1. Python 설치

**Python 3.13 이상**이 필요합니다.

#### Windows
1. [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.13+ 다운로드
2. 설치 시 **"Add Python to PATH"** 체크박스 반드시 선택
3. 설치 완료 후 확인:
   ```powershell
   python --version
   ```

#### macOS
```bash
# Homebrew로 설치
brew install python@3.13
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip
python3 --version
```

### 2. pip 확인

Python 설치 시 pip도 함께 설치됩니다. 확인:

```bash
pip --version
# 또는
python -m pip --version
```

### 3. Claude Desktop 설치

1. [Claude Desktop](https://claude.ai/download) 페이지에서 다운로드
2. 운영체제에 맞는 버전 설치
3. Claude 계정으로 로그인

---

## 패키지 설치

### 기본 설치

터미널 또는 명령 프롬프트에서:

```bash
pip install mcp-coupang-server
```

### 설치 확인

```bash
pip show mcp-coupang-server
```

출력 예시:
```
Name: mcp-coupang-server
Version: 1.0.0
Summary: MCP Server for Coupang Partners API integration with Claude Desktop
Home-page: https://github.com/space-cap/mcp-coupang-server
Author: steve
Author-email: mobilenjoy@naver.com
License: MIT
Location: ...
Requires: aiohttp, mcp, pydantic, python-dotenv
```

### 설치 위치 확인

패키지가 설치된 경로 확인:

```bash
pip show -f mcp-coupang-server | grep Location
```

---

## 쿠팡 파트너스 API 키 발급

### 1. 쿠팡 파트너스 가입

1. [쿠팡 파트너스](https://partners.coupang.com) 접속
2. 회원가입 (개인 또는 사업자)
3. 약관 동의 및 기본 정보 입력

### 2. API 키 신청

1. 쿠팡 파트너스 로그인
2. 상단 메뉴에서 **"도구" > "API 사용 신청"** 클릭
3. API 사용 목적 및 서비스 설명 작성
4. 승인 대기 (보통 1-3 영업일 소요)

### 3. API 키 확인

승인 후:

1. **"도구" > "API 키 관리"** 메뉴 접속
2. 다음 정보 확인 및 복사:
   - **Access Key** (예: `AKXXX...`)
   - **Secret Key** (예: `abcd1234...`)
   - **Partner ID** (예: `AF1234567`)

⚠️ **중요**: 이 정보는 절대 공개하면 안 됩니다!

---

## Claude Desktop 설정

### 설정 파일 위치

운영체제별 Claude Desktop 설정 파일 위치:

#### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

전체 경로:
```
C:\Users\사용자이름\AppData\Roaming\Claude\claude_desktop_config.json
```

#### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Linux
```
~/.config/Claude/claude_desktop_config.json
```

### 설정 파일 수정

#### 1. 설정 파일 열기

**Windows (PowerShell):**
```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

#### 2. MCP 서버 추가

설정 파일에 다음 내용을 추가합니다:

**✨ 방법 1: 환경 변수를 Claude Desktop 설정에 직접 입력 (권장)**

```json
{
  "mcpServers": {
    "coupang": {
      "command": "coupang-mcp-server",
      "env": {
        "COUPANG_ACCESS_KEY": "여기에_Access_Key_입력",
        "COUPANG_SECRET_KEY": "여기에_Secret_Key_입력",
        "COUPANG_PARTNER_ID": "여기에_Partner_ID_입력",
        "COUPANG_SUB_ID": "여기에_Sub_ID_입력"
      }
    }
  }
}
```

**예제:**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "coupang-mcp-server",
      "env": {
        "COUPANG_ACCESS_KEY": "AKXXXXXXXXXXXXXXXXXXX",
        "COUPANG_SECRET_KEY": "abcd1234567890efghijklmnopqrstuvwxyz",
        "COUPANG_PARTNER_ID": "AF1234567",
        "COUPANG_SUB_ID": "desktop_app"
      }
    }
  }
}
```

**방법 2: 시스템 환경 변수 사용**

시스템 환경 변수를 먼저 설정한 후:

```json
{
  "mcpServers": {
    "coupang": {
      "command": "coupang-mcp-server"
    }
  }
}
```

시스템 환경 변수 설정 방법은 [환경 변수 설정 방법](#환경-변수-설정-방법) 참조.

#### 3. 기존 설정이 있는 경우

다른 MCP 서버가 이미 설정되어 있다면:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": [...]
    },
    "coupang": {
      "command": "coupang-mcp-server",
      "env": {
        "COUPANG_ACCESS_KEY": "...",
        "COUPANG_SECRET_KEY": "...",
        "COUPANG_PARTNER_ID": "...",
        "COUPANG_SUB_ID": "..."
      }
    }
  }
}
```

### Claude Desktop 재시작

1. Claude Desktop 완전히 종료
2. 작업 관리자(Windows) 또는 활성 상태 보기(macOS)에서 Claude 프로세스 확인 후 종료
3. Claude Desktop 다시 실행

---

## 환경 변수 설정 방법

### 방법 1: Claude Desktop 설정 파일에 직접 입력 (권장) ⭐

위의 [Claude Desktop 설정](#claude-desktop-설정) 섹션 참조.

**장점:**
- 가장 간단하고 직관적
- Claude Desktop에서만 사용되므로 안전
- 설정이 한 곳에 모여 있어 관리 용이

**단점:**
- 설정 파일에 API 키가 저장됨 (파일 권한 관리 필요)

### 방법 2: 시스템 환경 변수 설정

#### Windows (시스템 전역 설정)

**GUI 방식:**
1. "시스템 환경 변수 편집" 검색
2. "환경 변수" 버튼 클릭
3. "사용자 변수" 또는 "시스템 변수"에서 "새로 만들기" 클릭
4. 다음 변수들 추가:
   - 변수 이름: `COUPANG_ACCESS_KEY`, 값: `여기에_Access_Key_입력`
   - 변수 이름: `COUPANG_SECRET_KEY`, 값: `여기에_Secret_Key_입력`
   - 변수 이름: `COUPANG_PARTNER_ID`, 값: `여기에_Partner_ID_입력`
   - 변수 이름: `COUPANG_SUB_ID`, 값: `여기에_Sub_ID_입력`

**PowerShell 방식 (임시, 세션 종료 시 사라짐):**
```powershell
$env:COUPANG_ACCESS_KEY = "여기에_Access_Key_입력"
$env:COUPANG_SECRET_KEY = "여기에_Secret_Key_입력"
$env:COUPANG_PARTNER_ID = "여기에_Partner_ID_입력"
$env:COUPANG_SUB_ID = "여기에_Sub_ID_입력"
```

**PowerShell 방식 (영구 설정):**
```powershell
[System.Environment]::SetEnvironmentVariable('COUPANG_ACCESS_KEY', '여기에_Access_Key_입력', 'User')
[System.Environment]::SetEnvironmentVariable('COUPANG_SECRET_KEY', '여기에_Secret_Key_입력', 'User')
[System.Environment]::SetEnvironmentVariable('COUPANG_PARTNER_ID', '여기에_Partner_ID_입력', 'User')
[System.Environment]::SetEnvironmentVariable('COUPANG_SUB_ID', '여기에_Sub_ID_입력', 'User')
```

#### macOS/Linux (영구 설정)

**Bash:**
```bash
# ~/.bashrc 또는 ~/.bash_profile에 추가
export COUPANG_ACCESS_KEY="여기에_Access_Key_입력"
export COUPANG_SECRET_KEY="여기에_Secret_Key_입력"
export COUPANG_PARTNER_ID="여기에_Partner_ID_입력"
export COUPANG_SUB_ID="여기에_Sub_ID_입력"

# 적용
source ~/.bashrc
```

**Zsh (macOS 기본):**
```bash
# ~/.zshrc에 추가
export COUPANG_ACCESS_KEY="여기에_Access_Key_입력"
export COUPANG_SECRET_KEY="여기에_Secret_Key_입력"
export COUPANG_PARTNER_ID="여기에_Partner_ID_입력"
export COUPANG_SUB_ID="여기에_Sub_ID_입력"

# 적용
source ~/.zshrc
```

**장점:**
- 모든 애플리케이션에서 사용 가능
- 설정 파일에 API 키를 저장하지 않음

**단점:**
- 설정이 복잡
- 시스템 재시작 또는 쉘 재로드 필요

---

## 테스트 및 확인

### 1. Claude Desktop에서 확인

Claude Desktop을 실행하고 새 대화를 시작합니다.

#### MCP 서버 연결 확인

화면 하단에 🔧 아이콘이나 "Tools" 표시가 있는지 확인합니다.

#### 테스트 명령

다음 중 하나를 입력해보세요:

```
쿠팡에서 "무선 이어폰"을 검색해줘
```

```
가전디지털 카테고리(1016)의 베스트 상품을 보여줘
```

```
쿠팡에서 "노트북"을 검색하고, 상위 3개 상품을 딥링크로 변환해줘
```

### 2. 명령줄에서 직접 테스트

Claude Desktop 없이 MCP 서버를 직접 실행하려면:

```bash
coupang-mcp-server
```

이 명령은 MCP 서버를 stdio 모드로 실행합니다. Claude Desktop이나 다른 MCP 클라이언트가 연결할 수 있습니다.

### 3. 사용 가능한 도구

현재 활성화된 MCP 도구:

1. **search_products** - 키워드로 상품 검색
2. **get_best_products_by_category** - 카테고리별 베스트 상품 (18개 카테고리)
3. **create_deeplinks** - URL을 트래킹 단축 URL로 변환

---

## 문제 해결

### 1. "command not found: coupang-mcp-server"

**증상:**
```
'coupang-mcp-server' is not recognized as an internal or external command
```

**원인:**
- pip 설치 경로가 PATH에 없음

**해결:**

**Windows:**
```powershell
# Python Scripts 폴더를 PATH에 추가
$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
```

**macOS/Linux:**
```bash
# pip가 설치한 바이너리 위치 확인
python3 -m pip show -f mcp-coupang-server | grep Location

# ~/.bashrc 또는 ~/.zshrc에 추가
export PATH="$PATH:$HOME/.local/bin"
source ~/.bashrc  # 또는 source ~/.zshrc
```

**대안:**
Python 모듈로 직접 실행:
```bash
python -m src.server
```

### 2. API 인증 실패 (401 Unauthorized)

**증상:**
```
Error: Failed to fetch data from Coupang API. API request failed with status 401
```

**해결:**
1. 환경 변수가 올바르게 설정되었는지 확인
2. Claude Desktop 설정 파일의 `env` 필드 확인
3. 쿠팡 파트너스에서 API 키가 활성화되어 있는지 확인
4. 공백이나 따옴표가 없는지 확인

### 3. Claude Desktop에서 도구가 보이지 않음

**원인:**
- 설정 파일 JSON 형식 오류
- 환경 변수 누락
- Claude Desktop이 완전히 재시작되지 않음

**해결:**
1. `claude_desktop_config.json` 파일의 JSON 유효성 검사 ([JSONLint](https://jsonlint.com/)에서 확인)
2. 환경 변수가 모두 설정되었는지 확인
3. Claude Desktop 완전 종료 후 재시작
4. Claude Desktop 개발자 도구에서 로그 확인 (View > Toggle Developer Tools)

### 4. 패키지 설치 실패

**증상:**
```
ERROR: Could not find a version that satisfies the requirement mcp-coupang-server
```

**해결:**
1. Python 버전 확인 (3.13 이상 필요):
   ```bash
   python --version
   ```
2. pip 업그레이드:
   ```bash
   python -m pip install --upgrade pip
   ```
3. 다시 설치:
   ```bash
   pip install mcp-coupang-server
   ```

### 5. 환경 변수가 인식되지 않음

**확인 방법:**

**Windows:**
```powershell
echo $env:COUPANG_ACCESS_KEY
```

**macOS/Linux:**
```bash
echo $COUPANG_ACCESS_KEY
```

값이 출력되지 않으면 환경 변수가 설정되지 않은 것입니다.

**해결:**
- Claude Desktop 설정 파일의 `env` 필드 사용 (권장)
- 시스템 환경 변수 재설정 후 시스템 재시작

### 6. Claude Desktop 로그 확인

**Windows:**
```
%APPDATA%\Claude\logs
```

**macOS:**
```
~/Library/Logs/Claude/
```

**Linux:**
```
~/.config/Claude/logs/
```

로그 파일에서 MCP 서버 연결 오류를 확인할 수 있습니다.

---

## 패키지 업데이트

### 최신 버전으로 업데이트

```bash
pip install --upgrade mcp-coupang-server
```

### 현재 설치된 버전 확인

```bash
pip show mcp-coupang-server | grep Version
```

### 특정 버전 설치

```bash
pip install mcp-coupang-server==1.0.0
```

### 업데이트 후 확인

1. Claude Desktop 재시작
2. 새 대화에서 테스트 명령 실행

---

## 추가 정보

### PyPI 패키지 페이지

- [https://pypi.org/project/mcp-coupang-server/](https://pypi.org/project/mcp-coupang-server/)

### GitHub 저장소

- [https://github.com/space-cap/mcp-coupang-server](https://github.com/space-cap/mcp-coupang-server)

### 사용 예제 및 고급 기능

- [사용 예제](usage-examples.md)
- [개발 가이드](development-guide.md)

---

## 지원

문제가 계속되면:

1. [GitHub Issues](https://github.com/space-cap/mcp-coupang-server/issues) 등록
2. 쿠팡 파트너스 고객센터 문의 (API 관련)
3. [Claude 지원](https://support.anthropic.com/) 문의 (Claude Desktop 관련)

---

## 비교: Git Clone vs PyPI 패키지

| 항목 | Git Clone | PyPI 패키지 |
|------|-----------|-------------|
| **설치 방법** | `git clone` + `uv sync` | `pip install` |
| **설치 시간** | 느림 (의존성 설치) | 빠름 |
| **업데이트** | `git pull` + `uv sync` | `pip install --upgrade` |
| **커스터마이징** | 가능 (소스 수정) | 불가능 |
| **Claude Desktop 설정** | `uv --directory` 필요 | `coupang-mcp-server` 명령만 필요 |
| **환경 변수** | `.env` 파일 또는 시스템 | Claude Desktop `env` 필드 권장 |
| **적합한 사용자** | 개발자, 기여자 | 일반 사용자 |

**권장 사항:**
- 일반 사용자: **PyPI 패키지** 방식 (이 문서)
- 개발자/기여자: **Git Clone** 방식 ([설치 및 설정 가이드](installation-guide.md))

---

**마지막 업데이트**: 2025-10-31
