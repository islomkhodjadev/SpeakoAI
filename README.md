# SpeakoAI - IELTS Speaking Practice Platform

A comprehensive platform for IELTS speaking practice with AI-powered scoring, feedback, and progress tracking. The system includes a FastAPI backend with full CRUD operations, Telegram bot integration, and comprehensive analytics.

## 🚀 Features

### Core Features
- **IELTS Speaking Questions**: 15+ questions across all 3 parts with sample answers
- **User Management**: Telegram user integration and profile management
- **Response Tracking**: Record and analyze user speaking responses
- **AI Scoring**: Automated scoring for fluency, pronunciation, grammar, and vocabulary
- **Feedback System**: AI-generated feedback for improvement
- **Analytics**: User progress tracking and leaderboards
- **Swagger Documentation**: Complete API documentation

### IELTS Speaking Parts Covered
- **Part 1**: Personal information and familiar topics (4-5 minutes)
- **Part 2**: Individual long turn with cue card (3-4 minutes)
- **Part 3**: Two-way discussion on abstract topics (4-5 minutes)

## 📋 Requirements

- Python 3.8+
- SQLite (for development)
- Telegram Bot Token (for bot integration)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SpeakoAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   ```

4. **Initialize the database**
   ```bash
   
   python ./backend/models.py
   ```

## 🚀 Running the Application

### Start the FastAPI Server
```bash
python ./backend/main.py
```

The API will be available at `http://localhost:8000`

### Start the Telegram Bot
```bash

python ./backend/telegram_bot.py
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints Overview

#### Users
- `POST /api/users/` - Create a new user
- `GET /api/users/` - Get all users
- `GET /api/users/{tg_id}` - Get user by Telegram ID
- `PUT /api/users/{tg_id}` - Update user
- `DELETE /api/users/{tg_id}` - Delete user

#### Questions
- `POST /api/questions/` - Create a new question
- `GET /api/questions/` - Get all questions
- `GET /api/questions/{question_id}` - Get question by ID
- `GET /api/questions/part/{part}` - Get questions by IELTS part
- `GET /api/questions/category/{category}` - Get questions by category
- `GET /api/questions/difficulty/{difficulty}` - Get questions by difficulty
- `PUT /api/questions/{question_id}` - Update question
- `DELETE /api/questions/{question_id}` - Delete question

#### User Responses
- `POST /api/responses/` - Create a new user response
- `GET /api/responses/` - Get all responses
- `GET /api/responses/{response_id}` - Get response by ID
- `GET /api/responses/user/{user_id}` - Get user's responses
- `GET /api/responses/question/{question_id}` - Get responses for a question
- `PUT /api/responses/{response_id}` - Update response
- `DELETE /api/responses/{response_id}` - Delete response

#### Feedback
- `POST /api/feedbacks/` - Create a new feedback
- `GET /api/feedbacks/` - Get all feedback
- `GET /api/feedbacks/{feedback_id}` - Get feedback by ID
- `GET /api/feedbacks/user/{user_id}` - Get user's feedback
- `PUT /api/feedbacks/{feedback_id}` - Update feedback
- `DELETE /api/feedbacks/{feedback_id}` - Delete feedback

#### Analytics
- `GET /api/analytics/user/{user_id}` - Get user analytics
- `GET /api/analytics/leaderboard` - Get leaderboard
- `GET /api/analytics/question/{question_id}` - Get question analytics

#### Telegram Integration
- `POST /api/telegram/user` - Create/get user from Telegram

## 🤖 Telegram Bot Commands

- `/start` - Welcome message and registration
- `/help` - Show help information
- `/practice` - Start IELTS speaking practice
- `/progress` - View your progress and scores
- `/leaderboard` - See top performers

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `tg_id` (Telegram User ID)
- `first_name`
- `username`
- `created_at`

### Questions Table
- `id` (Primary Key)
- `part` (1, 2, or 3)
- `question_text`
- `sample_answer`
- `category`
- `difficulty`
- `created_at`

### User Responses Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `question_id` (Foreign Key)
- `response_text`
- `audio_file_path`
- `fluency_score` (0-9)
- `pronunciation_score` (0-9)
- `grammar_score` (0-9)
- `vocabulary_score` (0-9)
- `overall_score` (0-9)
- `ai_feedback`
- `created_at`

### Feedback Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `ai_comment`
- `created_at`

## 🎯 Sample Questions Included

### Part 1 Questions (Easy)
1. Can you tell me about your hometown?
2. What do you do for work?
3. Do you enjoy reading books?
4. What's your favorite type of food?
5. How do you usually spend your weekends?

### Part 2 Questions (Medium)
1. Describe a place you would like to visit
2. Describe a person who has influenced you
3. Describe an important event in your life
4. Describe a book that you enjoyed reading
5. Describe a skill you would like to learn

### Part 3 Questions (Hard)
1. What are the advantages and disadvantages of living in a big city?
2. How has technology changed the way people communicate?
3. What role does education play in a person's success?
4. How do you think the environment will change in the next 50 years?
5. What are the main challenges facing young people today?

## 🔧 Configuration

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite+aiosqlite:///backend/data.db
```

### Database Configuration
The system uses SQLite by default for development. For production, you can modify the database URL in `models.py`:

```python
# For PostgreSQL
engine = create_async_engine("postgresql+asyncpg://user:password@localhost/speakoai")

# For MySQL
engine = create_async_engine("mysql+aiomysql://user:password@localhost/speakoai")
```

## 🧪 Testing

### Manual Testing
1. Start the FastAPI server
2. Visit `http://localhost:8000/docs`
3. Test endpoints using the Swagger UI

### API Testing Examples

#### Create a User
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "tg_id": 123456789,
    "first_name": "John",
    "username": "john_doe"
  }'
```

#### Get Questions by Part
```bash
curl -X GET "http://localhost:8000/api/questions/part/1"
```

#### Create a Response
```bash
curl -X POST "http://localhost:8000/api/responses/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "question_id": 1,
    "response_text": "I am from London, which is a large city in England...",
    "fluency_score": 7.5,
    "pronunciation_score": 7.0,
    "grammar_score": 8.0,
    "vocabulary_score": 7.5,
    "overall_score": 7.5,
    "ai_feedback": "Good response with clear structure..."
  }'
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
1. Use a production database (PostgreSQL/MySQL)
2. Set up proper authentication and authorization
3. Configure HTTPS
4. Set up monitoring and logging
5. Use environment variables for sensitive data
6. Implement rate limiting
7. Set up backup strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: support@speakoai.com
- Create an issue in the repository
- Check the API documentation at `/docs`

## 🔮 Future Enhancements

- [ ] Audio recording and analysis
- [ ] Real-time AI scoring integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Practice sessions with time limits
- [ ] Peer review system
- [ ] Custom question creation
- [ ] Export progress reports
- [ ] Integration with other language learning platforms 