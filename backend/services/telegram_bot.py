import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
import conn as rq
from typing import Optional
import json
from dotenv import load_dotenv

load_dotenv()

import os

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration (you'll need to set these)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")  # Replace with your bot token
API_BASE_URL = "http://localhost:8000/api"  # Your FastAPI server URL


class SpeakoAIBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all bot handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("practice", self.practice_command))
        self.application.add_handler(CommandHandler("progress", self.progress_command))
        self.application.add_handler(
            CommandHandler("leaderboard", self.leaderboard_command)
        )

        # Callback query handler for inline keyboards
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

        # Message handler for user responses
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_user_response)
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user

        # Register user in database
        try:
            user_data = await rq.set_user(
                tg_id=user.id, first_name=user.first_name, username=user.username
            )

            welcome_message = f"""
🎉 Welcome to SpeakoAI, {user.first_name}!

I'm your IELTS Speaking practice assistant. I can help you:
• Practice with real IELTS speaking questions
• Get AI-powered scoring and feedback
• Track your progress over time
• Compare your performance with others

Use these commands:
/start - Show this welcome message
/practice - Start practicing IELTS speaking
/progress - View your progress and scores
/leaderboard - See top performers
/help - Show help information

Ready to start practicing? Use /practice to begin!
            """

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🎯 Start Practice", callback_data="practice_start"
                    )
                ],
                [InlineKeyboardButton("📊 My Progress", callback_data="progress")],
                [InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(welcome_message, reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error registering user: {e}")
            await update.message.reply_text(
                "Sorry, there was an error. Please try again later."
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 SpeakoAI Help

**Commands:**
/start - Welcome message and main menu
/practice - Start IELTS speaking practice
/progress - View your progress and scores
/leaderboard - See top performers
/help - Show this help message

**IELTS Speaking Parts:**
• Part 1: Personal information (4-5 minutes)
• Part 2: Individual long turn (3-4 minutes)  
• Part 3: Two-way discussion (4-5 minutes)

**How to Practice:**
1. Use /practice to start
2. Choose a part (1, 2, or 3)
3. Answer the question in detail
4. Get AI scoring and feedback
5. Track your progress over time

**Scoring (0-9 scale):**
• Fluency & Coherence
• Pronunciation
• Grammar
• Vocabulary
• Overall Band Score

Need more help? Contact support@speakoai.com
        """
        await update.message.reply_text(help_text)

    async def practice_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle /practice command"""
        keyboard = [
            [
                InlineKeyboardButton(
                    "Part 1 - Personal Info", callback_data="practice_part_1"
                )
            ],
            [
                InlineKeyboardButton(
                    "Part 2 - Long Turn", callback_data="practice_part_2"
                )
            ],
            [
                InlineKeyboardButton(
                    "Part 3 - Discussion", callback_data="practice_part_3"
                )
            ],
            [InlineKeyboardButton("Random Question", callback_data="practice_random")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🎯 Choose an IELTS Speaking part to practice:", reply_markup=reply_markup
        )

    async def progress_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle /progress command"""
        user = update.effective_user

        try:
            # Get user from database
            user_data = await rq.get_user(tg_id=user.id)
            if not user_data:
                await update.message.reply_text("Please use /start to register first.")
                return

            # Get user analytics
            analytics = await rq.get_user_scores(user_id=user_data["id"])

            if analytics and analytics.total_responses > 0:
                progress_text = f"""
📊 Your Progress Report

**Overall Statistics:**
• Total Responses: {analytics.total_responses}
• Average Overall Score: {analytics.average_overall_score:.1f}/9.0
• Best Score: {analytics.best_score:.1f}/9.0

**Detailed Scores:**
• Fluency: {analytics.average_fluency_score:.1f}/9.0
• Pronunciation: {analytics.average_pronunciation_score:.1f}/9.0
• Grammar: {analytics.average_grammar_score:.1f}/9.0
• Vocabulary: {analytics.average_vocabulary_score:.1f}/9.0

**Recent Scores:**
{', '.join([f"{score:.1f}" for score in analytics.recent_scores[:5]])}

Keep practicing to improve your scores! 🚀
                """
            else:
                progress_text = """
📊 Your Progress Report

You haven't practiced yet! 
Use /practice to start your IELTS speaking journey.

Your scores will appear here after you complete some practice sessions.
                """

            await update.message.reply_text(progress_text)

        except Exception as e:
            logger.error(f"Error getting progress: {e}")
            await update.message.reply_text(
                "Sorry, there was an error getting your progress."
            )

    async def leaderboard_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle /leaderboard command"""
        try:
            leaderboard = await rq.get_leaderboard(limit=10)

            if leaderboard:
                leaderboard_text = "🏆 Top Performers\n\n"
                for i, user in enumerate(leaderboard, 1):
                    score = user.average_overall_score or 0
                    leaderboard_text += f"{i}. {user.first_name} - {score:.1f}/9.0 ({user.total_responses} responses)\n"
            else:
                leaderboard_text = "No users have practiced yet. Be the first! 🚀"

            await update.message.reply_text(leaderboard_text)

        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            await update.message.reply_text(
                "Sorry, there was an error getting the leaderboard."
            )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()

        if query.data == "practice_start":
            await self.practice_command(update, context)
        elif query.data == "progress":
            await self.progress_command(update, context)
        elif query.data == "leaderboard":
            await self.leaderboard_command(update, context)
        elif query.data.startswith("practice_part_"):
            part = int(query.data.split("_")[-1])
            await self.send_question(update, context, part=part)
        elif query.data == "practice_random":
            await self.send_question(update, context, part=None)
        elif query.data.startswith("answer_"):
            question_id = int(query.data.split("_")[-1])
            await self.handle_question_response(update, context, question_id)

    async def send_question(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        part: Optional[int] = None,
    ):
        """Send a question to the user"""
        try:
            if part:
                questions = await rq.get_questions_by_part(part)
            else:
                questions = await rq.get_all_questions()

            if not questions:
                await update.callback_query.edit_message_text(
                    "No questions available at the moment."
                )
                return

            # Select a random question
            import random

            question = random.choice(questions)

            # Store question in context for later use
            context.user_data["current_question"] = question

            question_text = f"""
🎯 IELTS Speaking Part {question.part}

**Question:**
{question.question_text}

{f"**Sample Answer Structure:**\n{question.sample_answer}" if question.sample_answer else ""}

Please provide your detailed answer. Take your time and speak naturally!
            """

            keyboard = [
                [
                    InlineKeyboardButton(
                        "✅ I've Answered", callback_data=f"answer_{question.id}"
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.callback_query.edit_message_text(
                question_text, reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Error sending question: {e}")
            await update.callback_query.edit_message_text(
                "Sorry, there was an error. Please try again."
            )

    async def handle_question_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, question_id: int
    ):
        """Handle when user indicates they've answered a question"""
        await update.callback_query.edit_message_text(
            "Great! Now please send me your answer as a text message. "
            "I'll analyze it and provide you with scores and feedback."
        )
        context.user_data["waiting_for_response"] = question_id

    async def handle_user_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle user's text response to a question"""
        user = update.effective_user
        response_text = update.message.text

        if "waiting_for_response" not in context.user_data:
            await update.message.reply_text(
                "Please use /practice to start a practice session first."
            )
            return

        question_id = context.user_data["waiting_for_response"]

        try:
            # Get user from database
            user_data = await rq.get_user(tg_id=user.id)
            if not user_data:
                await update.message.reply_text("Please use /start to register first.")
                return

            # Create user response (with mock scores for now)
            # In a real implementation, you'd integrate with an AI service for scoring
            import random

            mock_scores = {
                "fluency_score": round(random.uniform(6.0, 8.5), 1),
                "pronunciation_score": round(random.uniform(6.0, 8.5), 1),
                "grammar_score": round(random.uniform(6.0, 8.5), 1),
                "vocabulary_score": round(random.uniform(6.0, 8.5), 1),
                "overall_score": round(random.uniform(6.0, 8.5), 1),
                "ai_feedback": "Good effort! Try to expand your vocabulary and work on pronunciation. Consider using more complex sentence structures.",
            }

            response_data = {
                "user_id": user_data["id"],
                "question_id": question_id,
                "response_text": response_text,
                **mock_scores,
            }

            # Save response to database
            saved_response = await rq.create_user_response(response_data)

            # Generate feedback message
            feedback_message = f"""
🎯 Your Response Analysis

**Your Answer:**
{response_text[:200]}{"..." if len(response_text) > 200 else ""}

**Scores (IELTS Band Scale):**
• Fluency & Coherence: {mock_scores['fluency_score']}/9.0
• Pronunciation: {mock_scores['pronunciation_score']}/9.0
• Grammar: {mock_scores['grammar_score']}/9.0
• Vocabulary: {mock_scores['vocabulary_score']}/9.0
• **Overall Band Score: {mock_scores['overall_score']}/9.0**

**AI Feedback:**
{mock_scores['ai_feedback']}

**Tips for Improvement:**
• Practice speaking for 2-3 minutes on each topic
• Record yourself and listen for pronunciation
• Expand your vocabulary with synonyms
• Use a variety of sentence structures

Ready for another question? Use /practice to continue!
            """

            await update.message.reply_text(feedback_message)

            # Clear the waiting state
            del context.user_data["waiting_for_response"]

        except Exception as e:
            logger.error(f"Error processing response: {e}")
            await update.message.reply_text(
                "Sorry, there was an error processing your response."
            )

    def run(self):
        """Run the bot"""
        logger.info("Starting SpeakoAI Telegram Bot...")
        self.application.run_polling()


if __name__ == "__main__":
    bot = SpeakoAIBot()
    bot.run()
