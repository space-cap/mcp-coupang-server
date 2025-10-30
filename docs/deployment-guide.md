# 배포 가이드

이 문서는 Coupang MCP Server를 다른 사람들이 사용할 수 있도록 배포하는 방법을 안내합니다.

## 목차

1. [배포 방식 개요](#배포-방식-개요)
2. [방식 1: GitHub 공개 저장소 (권장)](#방식-1-github-공개-저장소-권장)
3. [방식 2: PyPI 패키지 배포](#방식-2-pypi-패키지-배포)
4. [방식 3: Docker 컨테이너](#방식-3-docker-컨테이너)
5. [방식 4: MCP Registry 등록](#방식-4-mcp-registry-등록)
6. [사용자 가이드 제공](#사용자-가이드-제공)
7. [유지보수 및 업데이트](#유지보수-및-업데이트)

---

## 배포 방식 개요

MCP 서버는 로컬에서 실행되는 프로그램이므로, 중앙 서버에 배포하는 것이 아니라 **사용자가 각자의 PC에 설치**하도록 합니다.

### MCP 서버의 특징

- ✅ 로컬 실행: Claude Desktop과 동일한 PC에서 실행
- ✅ API 키 보안: 각 사용자가 자신의 쿠팡 API 키 사용
- ✅ 설치형 소프트웨어: 중앙 서버 불필요
- ✅ 오픈소스: 코드 공개 가능

### 배포 방식 비교

| 방식 | 난이도 | 관리 | 권장도 |
|------|--------|------|--------|
| GitHub 저장소 | ⭐ 쉬움 | 쉬움 | ⭐⭐⭐⭐⭐ |
| PyPI 패키지 | ⭐⭐ 보통 | 보통 | ⭐⭐⭐⭐ |
| Docker | ⭐⭐⭐ 어려움 | 복잡 | ⭐⭐⭐ |
| MCP Registry | ⭐⭐⭐⭐ 매우 어려움 | 매우 복잡 | ⭐⭐ |

---

## 방식 1: GitHub 공개 저장소 (권장)

가장 간단하고 일반적인 방법입니다.

### 1.1 저장소 준비

#### 현재 상태 확인
```bash
git status
git log --oneline -5
```

#### 필수 파일 확인
- ✅ `README.md` - 프로젝트 설명
- ✅ `LICENSE` - 라이선스 (MIT 권장)
- ✅ `.gitignore` - 민감 정보 제외
- ✅ `pyproject.toml` - 의존성 정의
- ✅ `docs/installation-guide.md` - 설치 가이드

#### 민감 정보 제거 확인
```bash
# .env 파일이 커밋되지 않았는지 확인
git log --all --full-history --source --name-only -- .env

# 혹시 커밋되었다면 히스토리에서 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### 1.2 라이선스 추가

프로젝트 루트에 `LICENSE` 파일 생성:

**MIT License (권장):**
```text
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 1.3 README 개선

README.md에 다음 섹션 추가:

```markdown
## 🚀 빠른 시작

### 사전 요구사항
- Python 3.13+
- UV 패키지 매니저
- 쿠팡 파트너스 API 키

### 설치
```bash
git clone https://github.com/your-username/mcp-coupang-server.git
cd mcp-coupang-server
uv sync
```

상세한 설치 방법은 [📖 설치 가이드](docs/installation-guide.md)를 참조하세요.

## 💬 커뮤니티 및 지원

- 🐛 버그 리포트: [Issues](https://github.com/your-username/mcp-coupang-server/issues)
- 💡 기능 제안: [Discussions](https://github.com/your-username/mcp-coupang-server/discussions)
- ⭐ 도움이 되셨다면 Star를 눌러주세요!

## 📜 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 참조
```

### 1.4 저장소 공개 설정

#### GitHub에서:
1. 저장소 페이지 → **Settings**
2. **Danger Zone** → **Change repository visibility**
3. **Make public** 선택
4. 확인 메시지 입력 후 공개

#### 주의사항:
- `.env` 파일이 커밋에 포함되지 않았는지 다시 확인
- API 키나 민감 정보가 코드에 하드코딩되지 않았는지 확인

### 1.5 릴리스 생성

#### GitHub Releases 사용:
1. 저장소 페이지 → **Releases** → **Create a new release**
2. 태그 생성: `v1.0.0`
3. 릴리스 제목: `v1.0.0 - Initial Release`
4. 설명 작성:

```markdown
## 🎉 Coupang MCP Server v1.0.0

쿠팡 파트너스 API를 Claude Desktop에서 사용할 수 있는 MCP 서버입니다.

### ✨ 기능
- 상품 검색
- 카테고리별 베스트 상품 조회 (18개 카테고리)
- 딥링크 생성 (단축 URL 변환)

### 📦 설치 방법
[설치 가이드](docs/installation-guide.md)를 참조하세요.

### 🔧 요구사항
- Python 3.13+
- UV 패키지 매니저
- 쿠팡 파트너스 API 키

### 📝 변경사항
- 초기 릴리스
```

5. **Publish release** 클릭

### 1.6 사용자 설치 방법

이제 사용자들은 다음과 같이 설치할 수 있습니다:

```bash
# 최신 릴리스 설치
git clone https://github.com/your-username/mcp-coupang-server.git
cd mcp-coupang-server

# 또는 특정 버전 설치
git clone -b v1.0.0 https://github.com/your-username/mcp-coupang-server.git
```

---

## 방식 2: PyPI 패키지 배포

Python 패키지로 배포하여 `pip` 또는 `uv`로 설치 가능하게 합니다.

### 2.1 패키지 구조 준비

#### pyproject.toml 업데이트

현재 `pyproject.toml`에 다음 섹션 추가:

```toml
[project]
name = "coupang-mcp-server"
version = "1.0.0"
description = "MCP Server for Coupang Partners API integration with Claude Desktop"
readme = "README.md"
requires-python = ">=3.13"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["mcp", "coupang", "claude", "ai", "assistant"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
]

[project.urls]
Homepage = "https://github.com/your-username/mcp-coupang-server"
Documentation = "https://github.com/your-username/mcp-coupang-server/tree/main/docs"
Repository = "https://github.com/your-username/mcp-coupang-server"
Issues = "https://github.com/your-username/mcp-coupang-server/issues"

[project.scripts]
coupang-mcp-server = "src.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 2.2 빌드 및 배포

#### 1. 빌드 도구 설치
```bash
uv add --dev build twine
```

#### 2. 패키지 빌드
```bash
uv run python -m build
```

생성 파일:
- `dist/coupang_mcp_server-1.0.0.tar.gz`
- `dist/coupang_mcp_server-1.0.0-py3-none-any.whl`

#### 3. TestPyPI에 먼저 업로드 (테스트)

**TestPyPI 계정 생성:**
https://test.pypi.org/account/register/

**API 토큰 생성:**
1. Account settings → API tokens → Add API token
2. Token name: `coupang-mcp-upload`
3. Scope: Entire account
4. 생성된 토큰 복사 (한 번만 표시됨)

**업로드:**
```bash
uv run twine upload --repository testpypi dist/*
# Username: __token__
# Password: [복사한 API 토큰]
```

**테스트 설치:**
```bash
pip install --index-url https://test.pypi.org/simple/ coupang-mcp-server
```

#### 4. PyPI에 정식 업로드

**PyPI 계정 생성:**
https://pypi.org/account/register/

**API 토큰 생성** (동일한 방법)

**업로드:**
```bash
uv run twine upload dist/*
```

### 2.3 사용자 설치 방법

이제 사용자들은 다음과 같이 설치할 수 있습니다:

```bash
# pip로 설치
pip install coupang-mcp-server

# uv로 설치
uv pip install coupang-mcp-server

# 특정 버전 설치
pip install coupang-mcp-server==1.0.0
```

### 2.4 Claude Desktop 설정 (PyPI 버전)

PyPI로 설치한 경우에도 **환경 변수 설정이 필요**합니다.

#### 방법 1: 시스템 환경 변수 설정 (권장)

**Windows:**
```powershell
# 시스템 환경 변수 설정
[System.Environment]::SetEnvironmentVariable("COUPANG_ACCESS_KEY", "your_access_key", "User")
[System.Environment]::SetEnvironmentVariable("COUPANG_SECRET_KEY", "your_secret_key", "User")
[System.Environment]::SetEnvironmentVariable("COUPANG_PARTNER_ID", "your_partner_id", "User")
[System.Environment]::SetEnvironmentVariable("COUPANG_SUB_ID", "your_sub_id", "User")

# 또는 GUI로: 시스템 속성 → 고급 → 환경 변수
```

**macOS/Linux:**
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export COUPANG_ACCESS_KEY="your_access_key"
export COUPANG_SECRET_KEY="your_secret_key"
export COUPANG_PARTNER_ID="your_partner_id"
export COUPANG_SUB_ID="your_sub_id"

# 적용
source ~/.bashrc  # 또는 source ~/.zshrc
```

#### 방법 2: Claude Desktop 설정에서 환경 변수 지정

```json
{
  "mcpServers": {
    "coupang": {
      "command": "coupang-mcp-server",
      "env": {
        "COUPANG_ACCESS_KEY": "your_access_key_here",
        "COUPANG_SECRET_KEY": "your_secret_key_here",
        "COUPANG_PARTNER_ID": "your_partner_id_here",
        "COUPANG_SUB_ID": "your_sub_id_here"
      }
    }
  }
}
```

⚠️ **보안 주의**: 이 방법은 API 키가 설정 파일에 평문으로 저장되므로 주의가 필요합니다.

#### 방법 3: .env 파일 사용 (Git 클론 방식과 동일)

특정 디렉토리에 `.env` 파일을 만들고 Claude Desktop 설정에서 경로 지정:

```json
{
  "mcpServers": {
    "coupang": {
      "command": "coupang-mcp-server",
      "cwd": "/path/to/your/.env/directory"
    }
  }
}
```

`.env` 파일 내용:
```env
COUPANG_ACCESS_KEY=your_access_key
COUPANG_SECRET_KEY=your_secret_key
COUPANG_PARTNER_ID=your_partner_id
COUPANG_SUB_ID=your_sub_id
```

**권장 방법**: 시스템 환경 변수 (방법 1)가 가장 안전하고 편리합니다.

---

## 방식 3: Docker 컨테이너

Docker를 사용하여 환경을 격리합니다.

### 3.1 Dockerfile 작성

프로젝트 루트에 `Dockerfile` 생성:

```dockerfile
# Dockerfile
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# UV 설치
RUN pip install uv

# 프로젝트 파일 복사
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY main.py ./

# 의존성 설치
RUN uv sync --frozen

# 환경 변수 설정 (실행 시 오버라이드 필요)
ENV COUPANG_ACCESS_KEY=""
ENV COUPANG_SECRET_KEY=""
ENV COUPANG_PARTNER_ID=""
ENV COUPANG_SUB_ID=""

# 서버 실행
CMD ["uv", "run", "python", "main.py"]
```

### 3.2 .dockerignore 생성

```
# .dockerignore
.git
.env
.venv
__pycache__
*.pyc
tests/
docs/
playground/
.pytest_cache
*.log
```

### 3.3 Docker 이미지 빌드 및 배포

#### 로컬 빌드:
```bash
docker build -t coupang-mcp-server:latest .
```

#### Docker Hub에 배포:

**1. Docker Hub 계정 생성**: https://hub.docker.com/

**2. 로그인:**
```bash
docker login
```

**3. 태그 지정:**
```bash
docker tag coupang-mcp-server:latest yourusername/coupang-mcp-server:latest
docker tag coupang-mcp-server:latest yourusername/coupang-mcp-server:1.0.0
```

**4. 푸시:**
```bash
docker push yourusername/coupang-mcp-server:latest
docker push yourusername/coupang-mcp-server:1.0.0
```

### 3.4 사용자 설치 방법

```bash
# Docker 이미지 가져오기
docker pull yourusername/coupang-mcp-server:latest

# 실행 (.env 파일 사용)
docker run -d \
  --name coupang-mcp \
  --env-file .env \
  yourusername/coupang-mcp-server:latest
```

**주의**: Docker 방식은 Claude Desktop과의 stdio 통신이 복잡하므로 **권장하지 않습니다**.

---

## 방식 4: MCP Registry 등록

공식 MCP Registry에 등록하여 사용자가 쉽게 찾을 수 있도록 합니다.

### 4.1 smithery.ai 등록

Smithery는 MCP 서버 레지스트리입니다.

#### 등록 절차:

1. **Smithery 방문**: https://smithery.ai/
2. **Submit Server** 클릭
3. **필수 정보 입력:**
   - Server Name: `coupang-mcp-server`
   - Description: `Coupang Partners API integration for Claude Desktop`
   - GitHub URL: `https://github.com/your-username/mcp-coupang-server`
   - Installation command: `uv pip install coupang-mcp-server` (PyPI 배포 후)
   - Category: `E-commerce`, `Shopping`, `Affiliate`

4. **문서 링크:**
   - Installation Guide
   - API Reference
   - Examples

5. **Submit** 후 승인 대기

### 4.2 npm 패키지로 배포 (선택사항)

TypeScript/JavaScript로 래퍼를 작성하여 npm에 배포할 수도 있습니다.

**package.json:**
```json
{
  "name": "@yourusername/coupang-mcp-server",
  "version": "1.0.0",
  "description": "Coupang MCP Server",
  "main": "index.js",
  "bin": {
    "coupang-mcp-server": "./bin/cli.js"
  },
  "scripts": {
    "start": "python main.py"
  }
}
```

**설치:**
```bash
npx @yourusername/coupang-mcp-server
```

---

## 사용자 가이드 제공

### 5.1 문서 웹사이트

GitHub Pages나 Read the Docs로 문서 호스팅:

#### GitHub Pages 설정:

1. 저장소 Settings → Pages
2. Source: Deploy from a branch → `main` → `/docs`
3. Save

이제 `https://your-username.github.io/mcp-coupang-server/`에서 문서 확인 가능

#### docs/index.md 생성:

```markdown
# Coupang MCP Server 문서

Claude Desktop에서 쿠팡 파트너스 API를 사용하세요.

## 빠른 시작

1. [설치 가이드](installation-guide.md)
2. [사용 예제](usage-examples.md)
3. [API 레퍼런스](api-reference.md)

## 지원

- [GitHub Issues](https://github.com/your-username/mcp-coupang-server/issues)
- [Discussions](https://github.com/your-username/mcp-coupang-server/discussions)
```

### 5.2 비디오 튜토리얼

YouTube나 Loom으로 설치 과정 녹화:

1. **설치 과정** (5-10분)
   - Python/UV 설치
   - Git 클론
   - 환경 변수 설정
   - Claude Desktop 설정

2. **사용 예제** (5-10분)
   - 상품 검색
   - 딥링크 생성
   - 실제 활용 사례

README에 비디오 링크 추가:

```markdown
## 📺 비디오 가이드

- [설치 방법](https://youtube.com/watch?v=...)
- [사용 예제](https://youtube.com/watch?v=...)
```

### 5.3 블로그 포스트

개발 과정이나 사용법을 블로그에 작성:

- Medium
- Dev.to
- 개인 블로그
- Velog (한국어)

---

## 유지보수 및 업데이트

### 6.1 버전 관리

Semantic Versioning (SemVer) 사용:

- **1.0.0**: 초기 릴리스
- **1.0.1**: 버그 수정
- **1.1.0**: 새 기능 추가
- **2.0.0**: 호환성 없는 변경

### 6.2 업데이트 프로세스

#### 1. 코드 수정 및 테스트
```bash
# 변경사항 테스트
uv run pytest
```

#### 2. 버전 업데이트
```bash
# pyproject.toml에서 버전 변경
version = "1.1.0"
```

#### 3. CHANGELOG 작성

`CHANGELOG.md`:
```markdown
# Changelog

## [1.1.0] - 2025-11-01

### Added
- 새로운 기능 추가

### Fixed
- 버그 수정

### Changed
- 기존 기능 개선
```

#### 4. Git 태그 생성
```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

#### 5. GitHub Release 생성

#### 6. PyPI 업데이트 (해당 시)
```bash
uv run python -m build
uv run twine upload dist/*
```

### 6.3 사용자 알림

- GitHub Discussions에 공지
- README에 최신 버전 명시
- Twitter/X에 공유
- 관련 커뮤니티에 공유

### 6.4 이슈 관리

GitHub Issues 템플릿 생성:

**.github/ISSUE_TEMPLATE/bug_report.md:**
```markdown
---
name: Bug Report
about: 버그를 신고합니다
---

## 버그 설명
간단명료하게 버그를 설명해주세요.

## 재현 방법
1. ...
2. ...

## 예상 동작
어떻게 동작해야 하나요?

## 환경
- OS: [예: Windows 11]
- Python: [예: 3.13.0]
- Claude Desktop: [예: 1.5.0]
```

**.github/ISSUE_TEMPLATE/feature_request.md:**
```markdown
---
name: Feature Request
about: 새로운 기능을 제안합니다
---

## 제안하는 기능
어떤 기능을 원하시나요?

## 사용 사례
어떤 경우에 이 기능이 필요한가요?

## 추가 정보
참고할 만한 내용이 있나요?
```

---

## 체크리스트

배포 전 확인사항:

### 코드 품질
- [ ] 모든 테스트 통과
- [ ] 코드 리뷰 완료
- [ ] 타입 힌트 추가
- [ ] 주석 및 docstring 작성

### 문서
- [ ] README.md 업데이트
- [ ] 설치 가이드 작성
- [ ] API 문서 작성
- [ ] CHANGELOG.md 작성

### 보안
- [ ] `.env` 파일 제외 확인
- [ ] API 키 하드코딩 없음
- [ ] 민감 정보 Git 히스토리 확인

### 배포
- [ ] LICENSE 파일 추가
- [ ] .gitignore 설정
- [ ] GitHub 저장소 공개
- [ ] 릴리스 노트 작성

### 사용자 경험
- [ ] 설치 과정 테스트 (깨끗한 환경에서)
- [ ] Windows/macOS/Linux 호환성 확인
- [ ] 에러 메시지 명확성 확인

---

## 추천 배포 전략

### 1단계: GitHub 저장소 (즉시)
- 가장 간단하고 빠른 방법
- 개발자들이 쉽게 기여 가능
- 무료

### 2단계: PyPI 패키지 (1-2주 후)
- 설치 편의성 증가
- pip/uv로 간편 설치
- 버전 관리 용이

### 3단계: 커뮤니티 홍보 (1개월 후)
- Reddit r/ClaudeAI
- Discord 커뮤니티
- Twitter/X
- 한국 개발자 커뮤니티 (OKKY, 데브시스터즈 등)

### 4단계: MCP Registry (안정화 후)
- Smithery.ai 등록
- 공식 MCP 카탈로그 제안
- 더 많은 사용자 확보

---

## 참고 자료

### MCP 관련
- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Smithery.ai](https://smithery.ai/)

### 패키지 배포
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI](https://pypi.org/)
- [TestPyPI](https://test.pypi.org/)

### 문서 호스팅
- [GitHub Pages](https://pages.github.com/)
- [Read the Docs](https://readthedocs.org/)

---

**마지막 업데이트**: 2025-10-30
