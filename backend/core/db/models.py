import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Go up to /backend
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data.db"

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found at: {DB_PATH}")

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)
# engine = create_async_engine("sqlite+aiosqlite:///backend/data.db", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found at: {DB_PATH}")


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize with sample IELTS questions
#
#
# async def initialize_sample_questions():
#     """Initialize the database with sample IELTS speaking questions"""
#     async with async_session() as session:
#         # Check if questions already exist
#         existing_questions = await session.scalar(select(Question).limit(1))
#         if existing_questions:
#             return
#
#         sample_questions = [
#             # Part 1 Questions (Personal Information)
#             Question(part=1, question_text="Can you tell me about your hometown?",
#                     sample_answer="I'm from [city name], which is a [size] city in [country]. It's known for [famous feature] and I really enjoy living there because of [reason].",
#                     category="Hometown" ),
#             Question(part=1, question_text="What do you do for work?",
#                     sample_answer="I work as a [job title] at [company/place]. My main responsibilities include [duties]. I've been working there for [duration] and I find it [interesting/challenging/rewarding].",
#                     category="Work" ),
#             Question(part=1, question_text="Do you enjoy reading books?",
#                     sample_answer="Yes, I love reading books, especially [genre]. My favorite book is [book name] because [reason]. I usually read [frequency] and I find it helps me [benefit].",
#                     category="Hobbies" ),
#             Question(part=1, question_text="What's your favorite type of food?",
#                     sample_answer="I really enjoy [cuisine type] food, particularly [specific dish]. I like it because of [reason - taste, memories, etc.]. I usually eat it [frequency] and I learned to cook it [how].",
#                     category="Food" ),
#             Question(part=1, question_text="How do you usually spend your weekends?",
#                     sample_answer="On weekends, I usually [activity 1] and [activity 2]. Sometimes I [activity 3] with friends or family. I find weekends are a great time to [relax/pursue hobbies/spend time with loved ones].",
#                     category="Lifestyle" ),
#
#             # Part 2 Questions (Individual Long Turn)
#             Question(part=2, question_text="Describe a place you would like to visit. You should say: where it is, how you know about it, what you would do there, and explain why you would like to visit this place.",
#                     sample_answer="I would like to visit [place name], which is located in [location]. I first learned about it through [source - book, movie, friend, etc.]. If I went there, I would [activities]. I want to visit this place because [reasons - culture, scenery, history, etc.].",
#                     category="Travel" ),
#             Question(part=2, question_text="Describe a person who has influenced you. You should say: who this person is, how you know them, what they have done, and explain why they have influenced you.",
#                     sample_answer="The person who has influenced me most is [person name], who is [relationship]. I know them through [how you met]. They have [achievements/qualities]. They influenced me because [reasons - values, career choice, personal growth, etc.].",
#                     category="People" ),
#             Question(part=2, question_text="Describe an important event in your life. You should say: when it happened, where it took place, what happened, and explain why it was important to you.",
#                     sample_answer="An important event in my life was [event] which happened [when] in [location]. During this event, [what happened]. This event was important because [impact on life, lessons learned, changes made, etc.].",
#                     category="Life Events" ),
#             Question(part=2, question_text="Describe a book that you enjoyed reading. You should say: what the book is about, when you read it, what you learned from it, and explain why you enjoyed reading it.",
#                     sample_answer="I enjoyed reading [book title] by [author], which is about [plot/summary]. I read it [when] and from this book I learned [lessons/knowledge]. I enjoyed it because [reasons - writing style, characters, plot, themes, etc.].",
#                     category="Books" ),
#             Question(part=2, question_text="Describe a skill you would like to learn. You should say: what the skill is, how you would learn it, where you would learn it, and explain why you want to learn this skill.",
#                     sample_answer="I would like to learn [skill], which involves [description]. I would learn it by [methods - classes, online courses, practice, etc.]. I would prefer to learn it at [location - school, home, studio, etc.]. I want to learn this skill because [reasons - career, personal interest, challenge, etc.].",
#                     category="Skills" ),
#
#             # Part 3 Questions (Two-Way Discussion)
#             Question(part=3, question_text="What are the advantages and disadvantages of living in a big city compared to a small town?",
#                     sample_answer="Living in a big city has several advantages such as [advantages - job opportunities, entertainment, services]. However, there are also disadvantages like [disadvantages - cost of living, pollution, stress]. In contrast, small towns offer [benefits - community, peace, lower costs] but may lack [drawbacks - opportunities, services].",
#                     category="Urban vs Rural" ),
#             Question(part=3, question_text="How has technology changed the way people communicate in recent years?",
#                     sample_answer="Technology has dramatically changed communication through [changes - social media, instant messaging, video calls]. This has both positive effects like [benefits - convenience, global connectivity] and negative aspects such as [drawbacks - reduced face-to-face interaction, privacy concerns]. The impact varies across [different groups - age groups, cultures, professions].",
#                     category="Technology" ),
#             Question(part=3, question_text="What role does education play in a person's success?",
#                     sample_answer="Education plays a crucial role in success by providing [benefits - knowledge, skills, opportunities]. However, success isn't solely dependent on formal education as [other factors - experience, networking, personal qualities] also matter. The relationship between education and success varies depending on [factors - field, individual circumstances, definition of success].",
#                     category="Education" ),
#             Question(part=3, question_text="How do you think the environment will change in the next 50 years?",
#                     sample_answer="I believe the environment will change significantly due to [factors - climate change, population growth, technology]. We might see [changes - temperature rise, sea level changes, new technologies]. However, there's also potential for [positive developments - renewable energy, conservation efforts]. The outcome depends largely on [actions - government policies, individual choices, technological advances].",
#                     category="Environment" ),
#             Question(part=3, question_text="What are the main challenges facing young people today?",
#                     sample_answer="Young people today face various challenges including [challenges - job market, housing costs, mental health]. These challenges differ from previous generations due to [factors - technology, economy, social changes]. However, young people also have advantages like [opportunities - technology, global connectivity, education]. The key is [solutions - adaptability, support systems, skill development].",
#                     category="Youth Issues" ),
#         ]
#
#         session.add_all(sample_questions)
#         await session.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
