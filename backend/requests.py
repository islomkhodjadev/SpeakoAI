from sqlalchemy import select
from models import async_session, User, Question
from schemas import QuestionSchema, UserSchema


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def set_user(session, tg_id: int, first_name: str = None):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        return user
    new_user = User(tg_id=tg_id, first_name=first_name)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@connection
async def get_user(session, tg_id: int):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return None
    return UserSchema.model_validate(user).model_dump()


@connection
async def get_all_questions(session):
    result = await session.execute(select(Question))
    questions = result.scalars().all()
    return [QuestionSchema.model_validate(q).model_dump() for q in questions]
