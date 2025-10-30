# 설치 및 설정 가이드

이 문서는 Coupang MCP Server를 처음 설치하고 사용하는 방법을 단계별로 안내합니다.

## 목차

1. [사전 요구사항](#사전-요구사항)
2. [쿠팡 파트너스 API 키 발급](#쿠팡-파트너스-api-키-발급)
3. [프로젝트 설치](#프로젝트-설치)
4. [환경 변수 설정](#환경-변수-설정)
5. [Claude Desktop 설정](#claude-desktop-설정)
6. [테스트 및 확인](#테스트-및-확인)
7. [문제 해결](#문제-해결)

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
sudo apt install python3.13 python3.13-venv
python3 --version
```

### 2. UV 패키지 매니저 설치

UV는 빠른 Python 패키지 관리자입니다.

#### Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 확인:
```bash
uv --version
```

### 3. Git 설치

#### Windows
[Git for Windows](https://git-scm.com/download/win) 다운로드 및 설치

#### macOS
```bash
brew install git
```

#### Linux
```bash
sudo apt install git
```

### 4. Claude Desktop 설치

1. [Claude Desktop](https://claude.ai/download) 페이지에서 다운로드
2. 운영체제에 맞는 버전 설치
3. Claude 계정으로 로그인

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

## 프로젝트 설치

### 1. 저장소 클론

원하는 폴더에서 터미널/명령 프롬프트를 열고:

```bash
git clone https://github.com/space-cap/mcp-coupang-server.git
cd mcp-coupang-server
```

### 2. 의존성 설치

프로젝트 폴더에서:

```bash
uv sync
```

이 명령은 다음을 자동으로 수행합니다:
- Python 가상환경 생성
- 필요한 패키지 설치 (aiohttp, pydantic, python-dotenv 등)

---

## 환경 변수 설정

### 1. .env 파일 생성

프로젝트 루트 폴더에 `.env` 파일을 생성합니다.

#### Windows (PowerShell)
```powershell
New-Item -Path .env -ItemType File
notepad .env
```

#### macOS/Linux
```bash
touch .env
nano .env
# 또는
code .env  # VS Code가 설치되어 있다면
```

### 2. API 키 입력

`.env` 파일에 다음 내용을 입력합니다:

```env
# 쿠팡 파트너스 API 자격증명
COUPANG_ACCESS_KEY=여기에_Access_Key_입력
COUPANG_SECRET_KEY=여기에_Secret_Key_입력
COUPANG_PARTNER_ID=여기에_Partner_ID_입력

# (선택사항) 딥링크 기본 트래킹 ID
COUPANG_SUB_ID=mytracker
```

**예제:**
```env
COUPANG_ACCESS_KEY=AKXXXXXXXXXXXXXXXXXXX
COUPANG_SECRET_KEY=abcd1234567890efghijklmnopqrstuvwxyz
COUPANG_PARTNER_ID=AF1234567
COUPANG_SUB_ID=desktop_app
```

⚠️ **주의사항:**
- 따옴표(`"` 또는 `'`) 사용하지 않기
- 공백 없이 입력
- `.env` 파일은 Git에 커밋하지 않기 (이미 `.gitignore`에 등록됨)

### 3. 환경 변수 확인

설정이 올바른지 테스트:

```bash
uv run python -c "from src.utils.config import config; print(f'Partner ID: {config.partner_id}')"
```

Partner ID가 출력되면 성공입니다!

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

### 중요: 환경 변수가 필요합니다

Claude Desktop 설정 전에 **반드시** 환경 변수를 설정해야 합니다.
위의 [환경 변수 설정](#환경-변수-설정) 섹션을 먼저 완료하세요.

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

**Windows:**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\사용자이름\\경로\\mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/사용자이름/경로/mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

⚠️ **중요**:
- `C:\\Users\\사용자이름\\경로\\mcp-coupang-server` 부분을 실제 프로젝트 경로로 변경
- Windows는 백슬래시 두 개(`\\`) 사용
- macOS/Linux는 슬래시(`/`) 사용

#### 3. 경로 확인 방법

**Windows:**
```powershell
cd mcp-coupang-server
pwd
```

**macOS/Linux:**
```bash
cd mcp-coupang-server
pwd
```

출력된 경로를 복사하여 설정 파일에 붙여넣습니다.

#### 4. 기존 설정이 있는 경우

다른 MCP 서버가 이미 설정되어 있다면:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": [...]
    },
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "프로젝트_경로",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

### Claude Desktop 재시작

1. Claude Desktop 완전히 종료
2. 작업 관리자(Windows) 또는 활성 상태 보기(macOS)에서 Claude 프로세스 확인 후 종료
3. Claude Desktop 다시 실행

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

Claude Desktop 없이 직접 테스트하려면 playground 스크립트를 사용하세요:

```bash
# 상품 검색 테스트
uv run python playground/1_simple_search.py

# 카테고리 베스트 상품 테스트
uv run python playground/6_category_best.py

# 딥링크 생성 테스트
uv run python playground/7_create_deeplinks.py
```

### 3. 사용 가능한 도구

현재 활성화된 MCP 도구:

1. **search_products** - 키워드로 상품 검색
2. **get_best_products_by_category** - 카테고리별 베스트 상품 (18개 카테고리)
3. **create_deeplinks** - URL을 트래킹 단축 URL로 변환

---

## 문제 해결

### 1. "ModuleNotFoundError" 오류

**증상:**
```
ModuleNotFoundError: No module named 'src'
```

**해결:**
```bash
cd mcp-coupang-server
uv sync
```

### 2. API 인증 실패 (401 Unauthorized)

**증상:**
```
Error: Failed to fetch data from Coupang API. API request failed with status 401
```

**해결:**
1. `.env` 파일의 API 키 확인
2. 쿠팡 파트너스에서 키가 활성화되어 있는지 확인
3. 공백이나 따옴표가 없는지 확인

### 3. Claude Desktop에서 도구가 보이지 않음

**원인:**
- 설정 파일 경로가 잘못됨
- JSON 형식 오류
- Claude Desktop이 완전히 재시작되지 않음

**해결:**
1. `claude_desktop_config.json` 파일 경로 확인
2. JSON 유효성 검사 ([JSONLint](https://jsonlint.com/)에서 확인)
3. Claude Desktop 완전 종료 후 재시작
4. Claude Desktop 개발자 도구에서 로그 확인 (View > Toggle Developer Tools)

### 4. Windows에서 한글 깨짐

**증상:**
Playground 스크립트 실행 시 한글이 `???`로 표시

**해결:**
```powershell
# PowerShell에서 UTF-8 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

또는 **Windows Terminal** 사용 권장

### 5. UV 명령을 찾을 수 없음

**증상:**
```
'uv' is not recognized as an internal or external command
```

**해결:**
1. UV 재설치
2. 터미널 재시작
3. PATH 환경 변수 확인

**Windows (수동 PATH 추가):**
```powershell
$env:Path += ";$env:USERPROFILE\.cargo\bin"
```

### 6. 권한 오류 (Permission Denied)

**macOS/Linux:**
```bash
chmod +x main.py
```

### 7. 로그 확인

서버 로그 확인:

```bash
# 프로젝트 폴더에서
uv run python main.py
```

로그 출력을 확인하여 오류 메시지를 파악할 수 있습니다.

### 8. Claude Desktop 로그 확인

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

---

## 고급 설정

### 1. 환경 변수 추가 옵션

`.env` 파일에 추가 가능한 옵션:

```env
# API 기본값 (선택사항)
COUPANG_API_BASE_URL=https://api-gateway.coupang.com

# 로깅 레벨 (선택사항)
LOG_LEVEL=INFO
```

### 2. 여러 Sub ID 사용

딥링크 생성 시 다양한 트래킹 ID를 사용하려면:

```
이 URL을 딥링크로 변환하되, Sub ID는 "campaign2024"로 설정해줘:
https://www.coupang.com/vp/products/184614775
```

### 3. 테스트 자동화

모든 playground 스크립트를 한 번에 실행:

**Windows (PowerShell):**
```powershell
Get-ChildItem playground\*.py | ForEach-Object { uv run python $_.FullName }
```

**macOS/Linux:**
```bash
for script in playground/*.py; do
    echo "Testing $script..."
    uv run python "$script"
done
```

---

## 다음 단계

1. [사용 예제](usage-examples.md) 문서 확인
2. [개발 가이드](development-guide.md)로 커스터마이징
3. [Playground 스크립트](../playground/README.md)로 API 테스트

---

## 지원

문제가 계속되면:

1. [GitHub Issues](https://github.com/space-cap/mcp-coupang-server/issues) 등록
2. 쿠팡 파트너스 고객센터 문의 (API 관련)
3. [Claude 지원](https://support.anthropic.com/) 문의 (Claude Desktop 관련)

---

**마지막 업데이트**: 2025-10-30
