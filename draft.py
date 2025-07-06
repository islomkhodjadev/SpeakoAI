#
# # class SessionLog(Base):
# #     __tablename__ = "session_logs"
# #
# #     id: Mapped[int] = mapped_column(primary_key=True)
# #     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
# #     question: Mapped[str] = mapped_column(String(500))
# #     user_response: Mapped[str] = mapped_column(Text)
# #     created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
#
# @connection
# async def get_all_users(session):
#     result = await session.execute(select(User))
#     return result.scalars().all()
#
#
# @connection
# async def get_all_users_info(session):
#     result = await session.execute(select(User).order_by(User.created_at))
#     users = result.scalars().all()
#
#     if not users:
#         print("No users found.")
#         return []
#
#     user_list = [f"{i + 1}) first_name: {user.first_name}" for i, user in enumerate(users)]
#     return user_list
#
#
#
#
#
#
# @connection
# async def set_search(session, tg_id, question, answer):
#     async with session.begin():
#         try:
#             user = await session.scalar(select(User).where(User.tg_id == tg_id))
#             if not user:
#                 raise ValueError("User not found")
#
#             existing_search = await session.scalar(
#                 select(SessionLog).where(SessionLog.tg_id == tg_id, SessionLog.question == question)
#             )
#
#             if not existing_search:
#                 search_entry = SessionLog(tg_id=tg_id, question=question, answer=answer)
#                 session.add(search_entry)
#                 await session.commit()
#                 print(f"Search added: {search_entry}")
#             else:
#                 print("Search already exists")
#         except Exception as e:
#             await session.rollback()
#             print(f"Error in set_search: {e}")

