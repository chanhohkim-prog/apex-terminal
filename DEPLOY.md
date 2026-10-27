# 🌐 Apex Terminal 클라우드 배포 가이드 (Cloud Deployment Guide)

언제 어디서나 스마트폰이나 다른 노트북에서도 접속할 수 있도록 클라우드에 배포하는 **가장 추천하는 3가지 방법**입니다.

---

## 🏆 추천 1. [가장 쉽고 무료] Vercel (프론트엔드) + Render/Railway (백엔드)
> **비용: 0원 (무료 티어 활용)** / **소요 시간: 약 5분** / **난이도: ★☆☆☆☆ (초보자 추천)**

### 1단계: GitHub 저장소 만들기
1. GitHub(github.com)에 로그인 후 새 Repository 생성 (예: `next-bl-terminal`)
2. 내 컴퓨터의 프로젝트 폴더에서 git 푸시:
   ```bash
   git init
   git add .
   git commit -m "feat: Apex Terminal launch"
   git remote add origin https://github.com/당신의깃허브/next-bl-terminal.git
   git push -u origin main
   ```

### 2단계: 백엔드 배포 (Render.com 또는 Railway.app)
1. [Render.com](https://render.com) 접속 후 가입 (무료)
2. **New +** ➔ **Web Service** 클릭
3. 방금 올린 GitHub 저장소 선택
4. 설정값 입력:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Create Web Service** 클릭! ➔ 1분 후 `https://apex-backend-xxxx.onrender.com` 같은 고유 URL이 생성됩니다.

### 3단계: 프론트엔드 배포 (Vercel)
1. [Vercel.com](https://vercel.com) 접속 후 GitHub 계정으로 로그인 (무료)
2. **Add New...** ➔ **Project** ➔ 동일한 GitHub 저장소 `Import`
3. 설정값 입력:
   - **Root Directory**: `frontend` 선택
   - **Environment Variables**:
     - Key: `NEXT_PUBLIC_API_URL`
     - Value: `https://apex-backend-xxxx.onrender.com` (2단계에서 나온 백엔드 주소)
4. **Deploy** 버튼 클릭! ➔ 1분 후 `https://apex-terminal.vercel.app`으로 전 세계 어디서든 열립니다! 🎉

---

## 🚀 추천 2. [올인원 원클릭] Railway (railway.app)
> **비용: 매달 $5 무료 크레딧 제공** / **소요 시간: 3분** / **난이도: ★☆☆☆☆**

1. [Railway.app](https://railway.app) 가입 후 GitHub 연동
2. **New Project** ➔ **Deploy from GitHub repo** 선택
3. 백엔드와 프론트엔드를 각각 서비스로 추가하고 `docker-compose.yml` 또는 Dockerfile을 지정하면 자동 배포 완료!

---

## 🏛️ 추천 3. [진짜 서버 운영] AWS Lightsail 또는 AWS EC2
> **비용: 월 $3.5 (약 4,800원) 또는 EC2 1년 무료 티어** / **소요 시간: 10분**

내가 단독 클라우드 가상 서버(Linux)를 소유하고 Docker 컨테이너로 영구 구동하는 방식입니다.

1. **AWS Console** 접속 ➔ **Amazon Lightsail** 이동
2. **Create Instance** 클릭:
   - Platform: `Linux/Unix`
   - Blueprint: `OS Only` ➔ `Ubuntu 22.04 LTS`
   - Instance Plan: `$3.50/month` 선택 (첫 달 무료)
3. 생성된 인스턴스의 브라우저 SSH 터미널 접속:
   ```bash
   # 1. Docker & Docker Compose 설치
   sudo apt update && sudo apt install -y docker.io docker-compose git
   sudo usermod -aG docker ubuntu

   # 2. 코드 다운로드
   git clone https://github.com/당신의깃허브/next-bl-terminal.git
   cd next-bl-terminal

   # 3. 도커 컴포즈 원클릭 무중단 백그라운드 구동!
   docker-compose up -d --build
   ```
4. AWS Lightsail 방화벽(Networking) 탭에서 **3000** 포트와 **8000** 포트를 열어주면 끝!
   - `http://내-서버-IP:3000` 으로 접속 가능합니다.
