# Claude Desktop 설정 가이드

이 가이드는 Coupang MCP 서버를 Claude Desktop에 연동하는 방법을 안내합니다.

## 사전 요구사항

1. **Claude Desktop 설치**
   - [Claude Desktop](https://claude.ai/desktop) 다운로드 및 설치
   - 최신 버전 사용 권장

2. **UV 설치**
   - Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

3. **MCP 서버 설치**
   - 이 저장소 클론 및 의존성 설치 완료

## 설정 파일 위치

Claude Desktop 설정 파일 위치:

### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```
또는
```
C:\Users\<사용자명>\AppData\Roaming\Claude\claude_desktop_config.json
```

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux
```
~/.config/Claude/claude_desktop_config.json
```

## 설정 방법

### 1. 설정 파일 열기

설정 파일이 없으면 새로 생성합니다.

**Windows PowerShell:**
```powershell
# 디렉토리 생성 (없는 경우)
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"

# 파일 열기 (메모장)
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

**macOS/Linux:**
```bash
# 디렉토리 생성 (없는 경우)
mkdir -p ~/Library/Application\ Support/Claude

# 파일 열기
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 2. MCP 서버 설정 추가

#### Windows 설정 예시

```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourUsername\\Projects\\mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**주의사항:**
- 경로에서 백슬래시(`\`)를 두 번 사용 (`\\`)
- `YourUsername`과 경로를 실제 경로로 변경

#### macOS/Linux 설정 예시

```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourname/Projects/mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

### 3. 기존 MCP 서버가 있는 경우

이미 다른 MCP 서버를 사용 중이라면 `mcpServers` 객체에 추가:

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
        "/path/to/mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

### 4. 환경 변수 설정 (선택사항)

환경 변수를 설정 파일에 직접 포함할 수도 있습니다:

```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ],
      "env": {
        "COUPANG_ACCESS_KEY": "your_access_key",
        "COUPANG_SECRET_KEY": "your_secret_key",
        "COUPANG_PARTNER_ID": "your_partner_id"
      }
    }
  }
}
```

**보안 참고:**
- `.env` 파일 사용을 권장합니다
- 설정 파일에 직접 키를 넣는 것은 권장하지 않습니다

## 설정 확인

### 1. Claude Desktop 재시작

설정 파일을 저장한 후 Claude Desktop을 완전히 종료하고 다시 시작합니다.

### 2. MCP 서버 연결 확인

Claude Desktop에서 다음을 확인:
- 왼쪽 하단 또는 설정에서 MCP 서버 상태 확인
- "coupang" 서버가 연결되어 있는지 확인

### 3. 도구 사용 테스트

Claude에게 다음과 같이 질문:

```
쿠팡에서 "노트북"을 검색해줘
```

또는

```
Can you search for "laptop" on Coupang?
```

## 문제 해결

### MCP 서버가 연결되지 않는 경우

1. **경로 확인**
   - 설정 파일의 `--directory` 경로가 정확한지 확인
   - 절대 경로 사용 권장

2. **UV 설치 확인**
   ```bash
   uv --version
   ```

3. **의존성 설치 확인**
   ```bash
   cd /path/to/mcp-coupang-server
   uv sync
   ```

4. **환경 변수 확인**
   - `.env` 파일이 프로젝트 루트에 있는지 확인
   - API 키가 올바르게 설정되어 있는지 확인

5. **수동 테스트**
   ```bash
   cd /path/to/mcp-coupang-server
   uv run python main.py
   ```
   - 오류가 발생하면 로그 확인

### JSON 형식 오류

설정 파일의 JSON 형식이 올바른지 확인:
- [JSONLint](https://jsonlint.com/)에서 검증
- 쉼표, 중괄호, 대괄호 확인

### 로그 확인

Claude Desktop 로그 위치:

**Windows:**
```
%APPDATA%\Claude\logs\
```

**macOS:**
```
~/Library/Logs/Claude/
```

**Linux:**
```
~/.config/Claude/logs/
```

## 고급 설정

### 타임아웃 설정

```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [...],
      "timeout": 30000
    }
  }
}
```

### 여러 환경 설정

개발/프로덕션 환경을 분리하려면:

```json
{
  "mcpServers": {
    "coupang-dev": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-coupang-server-dev",
        "run",
        "python",
        "main.py"
      ]
    },
    "coupang-prod": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

## 추가 리소스

- [MCP 공식 문서](https://modelcontextprotocol.io)
- [Claude Desktop 문서](https://claude.ai/desktop)
- [UV 문서](https://docs.astral.sh/uv/)

## 지원

문제가 계속되면 [이슈](../../issues)를 생성해주세요.
