markdown
Copy
# 🔥 SH4D0W Leech Bot 🖤

[![Deploy on Heroku](https://img.shields.io/badge/Deploy-Heroku-purple.svg)](https://heroku.com/deploy?template=https://github.com/20255-ee-085/SH4D0W-Leech-Bot)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/20255-ee-085/SH4D0W-Leech-Bot/blob/main/SH4D0W_Leech.ipynb)
[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-blue.svg)](https://render.com/deploy?repo=https://github.com/20255-ee-085/SH4D0W-Leech-Bot)

Advanced Telegram Leech Bot with Queue Management and Multi-Platform Support

## 🌟 Features

- **Batch Processing**: Group downloads with custom names
- **Quality Selection**: Choose from 144p to 1080p
- **Multi-Format Support**: Videos, PDFs, Documents, Images
- **Queue System**: Parallel downloads with speed control
- **Progress Tracking**: Real-time progress bars
- **Thumbnail Support**: Custom thumbnails for uploads
- **Admin Controls**: Restricted access to authorized users
- **Auto Cleanup**: Temporary file management
- **Multi-Deploy**: Ready for Heroku, Render, Colab, etc.

## 🚀 Deployment

### Environment Variables
```env
API_ID=1234567
API_HASH=abcdef123456789
BOT_TOKEN=123:ABC
ADMIN_ID=00000000
MAX_CONCURRENT=3
Heroku deployment button
Click the Heroku Deploy button above

Add buildpacks:

heroku/python

heroku-community/apt

Set environment variables

Deploy!

https://colab.research.google.com/github/20255-ee-085/SH4D0W-Leech-Bot/blob/main/SH4D0W_Leech.ipynb
Open in Colab

!git clone https://github.com/20255-ee-085/SH4D0W-Leech-Bot
%cd SH4D0W-Leech-Bot
!chmod +x start.sh
!./start.sh

Create new Web Service

Connect your repository

Set environment variables

Use Docker deployment

Deploy!

📚 Commands
/start - Show welcome message

/upload - Start leeching process

/help - Show help documentation

/set - Configure upload parameters

/speedtest - Check server speed

Copy

**4. heroku.yml**
```yaml
build:
  docker:
    web: Dockerfile
  config:
    NODE_ENV: production