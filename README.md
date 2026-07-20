# 📈 US Stock Market News Email Bot

A Python automation that fetches the latest US stock market headline and emails it every weekday (Mon–Fri) at 9:40 AM ET.

## Setup

### 1. Create GitHub Repository
- Go to github.com and create a new repo (e.g., `stock-news-bot`)
- Make it Public or Private

### 2. Upload Files
- Upload `main.py`, `requirements.txt`, and `README.md`
- Create folder `.github/workflows/` and add `daily-news.yml`

### 3. Add Repository Secrets
Go to **Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets:

| Secret Name | Value |
|-------------|-------|
| `ALPHA_VANTAGE_API_KEY` | `YN6IS40RBNSQJWT9` |
| `EMAIL_SENDER` | `mckeepspatrol@gmail.com` |
| `EMAIL_PASSWORD` | `abcmckee999` |
| `EMAIL_RECIPIENT` | `coda0418@hotmail.com` |

### 4. Test It
- Go to **Actions** tab
- Click **"Daily Stock Market News Email"**
- Click **"Run workflow"** → **"Run workflow"**
- Check your email at `coda0418@hotmail.com`!

## Schedule
Runs automatically at **9:40 AM ET, Monday–Friday**.

## API
Uses [Alpha Vantage](https://www.alphavantage.co) free tier (500 calls/day).
