# 📥 Audio Video Saver API

A simple **FastAPI** application to fetch video info, download videos, or download audio with metadata, served from your own server with **DuckDNS** dynamic DNS support.

---

## 🚀 Features

✅ Get video formats and metadata  
✅ Download videos in selected formats  
✅ Download audio with metadata as MP3  
✅ Serve downloads from `/downloads`  
✅ CORS enabled for any origin  
✅ Daily auto-cleanup of old downloads  
✅ Supports dynamic IP with DuckDNS  

---

## ⚙️ Project Structure

| File / Folder     | Description                                 |
|------------------|---------------------------------------------|
| `main.py`         | FastAPI server with endpoints               |
| `utility.py`      | Core logic for yt-dlp operations            |
| `static/`         | Static files (e.g., favicon)                |
| `downloads/`      | Directory where all downloads are saved     |
| `cleanup.sh`      | Daily folder cleanup script                 |

---

## 🔗 API Endpoints

| Method | Route              | Description                              |
|--------|-------------------|------------------------------------------|
| `GET`  | `/`               | Health check – returns `{"message": "Hello World"}` |
| `POST` | `/info`           | Takes `url` → Returns formats, metadata, thumbnail |
| `POST` | `/download`       | Takes `url` and `format_id` → Downloads video |
| `POST` | `/music_download` | Takes `url` → Downloads audio as MP3 with metadata |

---

## 🌍 How It’s Served

Your API is exposed on **port 9600**.

Accessible via:

- **Local IP**: `http://<your_local_ip>:9600`  
- **Public IP**: `http://<your_public_ip>:9600`  
- **DuckDNS domain**: `http://<your_subdomain>.duckdns.org:9600`

> ⚠️ Use `http`, unless you add HTTPS via a reverse proxy like **NGINX + Let’s Encrypt**.

---

## 🌐 DuckDNS Dynamic IP

**How it works:**

- You set up DuckDNS to point your custom subdomain to your current public IP.
- A cron job runs every 5 minutes to auto-update your DuckDNS record.

### 🔁 Example Cron Job

```bash
*/5 * * * * ~/duckdns.sh >/dev/null 2>&1
