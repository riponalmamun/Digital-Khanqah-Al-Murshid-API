# 🕌 Digital Khanqah Al Murshid API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)](https://openai.com)

> An AI-powered Islamic Sufi guidance platform providing spiritual wisdom, Quranic explanations, Hadith insights, and personalized meditation through natural conversation and voice interaction.

## 📖 Overview

Digital Khanqah Al Murshid API is a comprehensive RESTful API that combines artificial intelligence with authentic Islamic scholarship to provide spiritual guidance in the tradition of Sufism. The platform offers multi-language support, voice interaction capabilities, and access to Quranic and Hadith resources, all designed with the compassionate wisdom of a Sufi spiritual guide (Murshid).

### Key Features

- 🤖 **AI Murshid** - Conversational AI spiritual guide with authentic Sufi personality
- 📖 **Quran Integration** - Complete Quran with AI-powered explanations and translations
- 📜 **Hadith Library** - Major Hadith collections with simplified explanations
- 🧘 **Spiritual Guidance** - Personalized advice for spiritual development
- 🎧 **Voice Interaction** - Speech-to-text and text-to-speech capabilities
- 🌍 **Multi-language** - Support for English, Urdu, Arabic, Hindi, and Bengali
- 🕌 **Meditation Scripts** - AI-generated guided meditation sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ElevenLabs API key ([Get one here](https://elevenlabs.io))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/riponalmamun/Digital-Khanqah-Al-Murshid-API.git
   cd Digital-Khanqah-Al-Murshid-API
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   ```

   Required variables in `.env`:
   ```env
   OPENAI_API_KEY=sk-proj-your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ```

5. **Run the development server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - **Interactive Documentation (Swagger UI)**: http://localhost:8000/docs
   - **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
   - **API Root**: http://localhost:8000

## 📚 API Documentation

### Core Endpoints

#### AI Murshid (Spiritual Chatbot)

**Chat with AI Murshid**
```http
POST /api/murshid/chat
Content-Type: application/json

{
  "message": "How do I develop patience in difficult times?",
  "language": "en",
  "user_id": "user123"
}
```

**Get Daily Spiritual Advice**
```http
GET /api/murshid/daily-naseehah?language=en
```

#### Quran

**Explain Quranic Verse**
```http
POST /api/quran/explain
Content-Type: application/json

{
  "surah_number": 1,
  "ayah_number": 1,
  "language": "en"
}
```

**Get Surah Information**
```http
GET /api/quran/surah/1
```

**Search Quran**
```http
GET /api/quran/search?query=mercy&language=en
```

#### Hadith

**Explain Hadith**
```http
POST /api/hadith/explain
Content-Type: application/json

{
  "collection": "bukhari",
  "book_number": 1,
  "language": "en"
}
```

**Get Random Hadith**
```http
GET /api/hadith/random?language=en
```

**List Collections**
```http
GET /api/hadith/collections
```

#### Spiritual Guidance

**Get Personalized Spiritual Advice**
```http
POST /api/spiritual/advice
Content-Type: application/json

{
  "topic": "overcoming anger",
  "user_level": "beginner",
  "language": "en"
}
```

**Generate Meditation Script**
```http
POST /api/spiritual/meditation
Content-Type: application/json

{
  "goal": "stress relief",
  "duration_minutes": 10,
  "language": "en"
}
```

**Get Zikr Suggestions**
```http
GET /api/spiritual/zikr-suggestions?mood=anxious&language=en
```

#### Voice Interaction

**Text to Speech (Download MP3)**
```http
POST /api/voice/generate?speed=0.85
Content-Type: application/json

{
  "text": "Bismillah ir-Rahman ir-Rahim",
  "language": "ar",
  "voice_style": "calm"
}
```

**Voice Chat (Upload Audio, Get Voice Response)**
```http
POST /api/voice/chat?language=en&response_speed=0.85
Content-Type: multipart/form-data

audio: [audio file]
```

### Response Examples

**AI Murshid Response:**
```json
{
  "response": "As-salamu alaykum, dear seeker. Patience is a virtue that grows through conscious practice...",
  "language": "en",
  "timestamp": "2025-12-26T12:00:00",
  "tokens_used": 450
}
```

**Quran Explanation:**
```json
{
  "surah_number": 1,
  "surah_name": "Al-Fatihah",
  "ayah_number": 1,
  "arabic_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "translation": "In the name of Allah, the Most Gracious, the Most Merciful",
  "explanation": "This opening verse establishes the foundation of all actions...",
  "language": "en"
}
```

## 🛠️ Technology Stack

### Core Framework
- **[FastAPI](https://fastapi.tiangolo.com)** - Modern, fast web framework for building APIs
- **[Uvicorn](https://www.uvicorn.org)** - Lightning-fast ASGI server

### AI & Machine Learning
- **[OpenAI GPT-4](https://openai.com/gpt-4)** - Advanced language model for AI Murshid responses
- **[OpenAI Whisper](https://openai.com/research/whisper)** - Speech-to-text transcription
- **[ElevenLabs](https://elevenlabs.io)** - High-quality text-to-speech synthesis

### Data Sources
- **[Quran.com API](https://api.quran.com)** - Complete Quran with translations
- **[Hadith API](https://github.com/fawazahmed0/hadith-api)** - Authentic Hadith collections
- **[Aladhan API](https://aladhan.com/prayer-times-api)** - Prayer times and Islamic utilities

### Additional Libraries
- **Pydantic** - Data validation and settings management
- **HTTPX** - Async HTTP client
- **Python-dotenv** - Environment variable management

## 🌍 Supported Languages

| Language | Code | Status |
|----------|------|--------|
| English | `en` | ✅ Full Support |
| Urdu | `ur` | ✅ Full Support |
| Arabic | `ar` | ✅ Full Support |
| Hindi | `hi` | ✅ Full Support |
| Bengali | `bn` | ✅ Full Support |

## 📁 Project Structure

```
Digital-khanqah-api/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration and settings
│   ├── api/                   # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── murshid.py        # AI Murshid endpoints
│   │   ├── quran.py          # Quran endpoints
│   │   ├── hadith.py         # Hadith endpoints
│   │   ├── spiritual.py      # Spiritual guidance endpoints
│   │   └── voice.py          # Voice interaction endpoints
│   ├── services/              # Business logic and external API integrations
│   │   ├── __init__.py
│   │   ├── openai_service.py
│   │   ├── elevenlabs_service.py
│   │   ├── quran_service.py
│   │   ├── hadith_service.py
│   │   └── aladhan_service.py
│   ├── models/                # Data models and schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── prompts.py        # AI system prompts
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore
└── README.md
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 and Whisper | Yes |
| `ELEVENLABS_API_KEY` | ElevenLabs API key for voice synthesis | Yes |
| `QURAN_API_URL` | Quran API base URL | No (default provided) |
| `HADITH_API_URL` | Hadith API base URL | No (default provided) |
| `ALADHAN_API_URL` | Aladhan API base URL | No (default provided) |
| `APP_NAME` | Application name | No |
| `APP_VERSION` | Application version | No |
| `DEBUG` | Enable debug mode | No |

### Voice Speed Settings

Control voice playback speed for different use cases:

- `0.5` - Very slow (ideal for learning)
- `0.7` - Slow (Quranic recitation pace)
- `0.85` - Moderately slow (default, clear pronunciation)
- `1.0` - Normal conversational speed
- `1.5` - Fast (quick information delivery)

## 💰 Cost Considerations

### API Usage Costs (Approximate)

| Service | Cost per Request | Monthly (1000 users) |
|---------|------------------|----------------------|
| OpenAI GPT-4 | $0.02 - $0.04 | $50 - $150 |
| OpenAI Whisper | $0.006/minute | $20 - $50 |
| ElevenLabs | $0.001/1000 chars | $5 - $22 |
| Islamic APIs | Free | $0 |
| **Total** | | **$75 - $222/month** |

### Cost Optimization Tips

- Use response length limits
- Implement caching for common queries
- Cache Quran and Hadith data locally
- Set up rate limiting per user tier

## 🔒 Security

### Best Practices

- ✅ Never commit `.env` file to version control
- ✅ Rotate API keys regularly
- ✅ Implement rate limiting in production
- ✅ Use HTTPS in production
- ✅ Validate all user inputs
- ✅ Implement authentication for production use

### API Key Safety

```bash
# ❌ NEVER do this
git add .env

# ✅ Always verify
git status  # .env should not appear
```

If you accidentally expose API keys:
1. Immediately revoke them from the provider dashboard
2. Generate new keys
3. Update your `.env` file
4. Remove the commit from Git history

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start the server: `uvicorn main:app --reload`
2. Open http://localhost:8000/docs
3. Try the interactive endpoints

### Testing with cURL

```bash
# Test AI Murshid
curl -X POST "http://localhost:8000/api/murshid/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"How do I increase my faith?","language":"en"}'

# Test Daily Naseehah
curl "http://localhost:8000/api/murshid/daily-naseehah?language=en"

# Test Quran Explanation
curl -X POST "http://localhost:8000/api/quran/explain" \
  -H "Content-Type: application/json" \
  -d '{"surah_number":1,"ayah_number":1,"language":"en"}'
```

## 🚀 Deployment

### Option 1: Render.com (Recommended for Free Tier)

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Add environment variables in dashboard
4. Deploy!

### Option 2: Railway.app

1. Create account at [railway.app](https://railway.app)
2. Import GitHub repository
3. Add environment variables
4. Deploy automatically

### Option 3: Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t digital-khanqah-api .
docker run -p 8000:8000 --env-file .env digital-khanqah-api
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Update documentation for new features
- Test your changes thoroughly
- Keep commits atomic and well-described

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing GPT-4 and Whisper APIs
- **ElevenLabs** for high-quality voice synthesis
- **Quran.com** for comprehensive Quranic resources
- **Hadith API** by fawazahmed0 for Hadith collections
- **Aladhan** for Islamic utilities
- All contributors and the open-source community

## 📧 Contact & Support

- **Developer**: Ripon Al Mamun
- **GitHub**: [@riponalmamun](https://github.com/riponalmamun)
- **Project Link**: [https://github.com/riponalmamun/Digital-Khanqah-Al-Murshid-API](https://github.com/riponalmamun/Digital-Khanqah-Al-Murshid-API)

### Getting Help

- 📖 Check the [API Documentation](http://localhost:8000/docs)
- 🐛 [Report bugs](https://github.com/riponalmamun/Digital-Khanqah-Al-Murshid-API/issues)
- 💡 [Request features](https://github.com/riponalmamun/Digital-Khanqah-Al-Murshid-API/issues)
- ⭐ Star the repo if you find it useful!

## 🎯 Roadmap

### Planned Features

- [ ] User authentication and authorization
- [ ] Database integration for conversation history
- [ ] Additional language support (Turkish, Malay, etc.)
- [ ] Mobile SDK for easier integration
- [ ] Advanced analytics dashboard
- [ ] Sufi poetry and literature database
- [ ] Community features and discussions
- [ ] Progressive Web App (PWA) interface

## ⚠️ Disclaimer

This API provides spiritual guidance based on AI interpretation of Islamic texts and Sufi traditions. While every effort is made to ensure authenticity and accuracy, users should consult qualified Islamic scholars for definitive religious guidance. The AI responses should be viewed as supplementary spiritual inspiration rather than authoritative religious rulings.

---

<div align="center">

**Made with ❤️ for the spiritual seekers around the world**

*"Indeed, in the remembrance of Allah do hearts find rest." - Quran 13:28*

</div>
