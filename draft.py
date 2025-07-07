# #
# # # class SessionLog(Base):
# # #     __tablename__ = "session_logs"
# # #
# # #     id: Mapped[int] = mapped_column(primary_key=True)
# # #     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
# # #     question: Mapped[str] = mapped_column(String(500))
# # #     user_response: Mapped[str] = mapped_column(Text)
# # #     created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
# #
# # @connection
# # async def get_all_users(session):
# #     result = await session.execute(select(User))
# #     return result.scalars().all()
# #
# #
# # @connection
# # async def get_all_users_info(session):
# #     result = await session.execute(select(User).order_by(User.created_at))
# #     users = result.scalars().all()
# #
# #     if not users:
# #         print("No users found.")
# #         return []
# #
# #     user_list = [f"{i + 1}) first_name: {user.first_name}" for i, user in enumerate(users)]
# #     return user_list
# #
# #
# #
# #
# #
# #
# # @connection
# # async def set_search(session, tg_id, question, answer):
# #     async with session.begin():
# #         try:
# #             user = await session.scalar(select(User).where(User.tg_id == tg_id))
# #             if not user:
# #                 raise ValueError("User not found")
# #
# #             existing_search = await session.scalar(
# #                 select(SessionLog).where(SessionLog.tg_id == tg_id, SessionLog.question == question)
# #             )
# #
# #             if not existing_search:
# #                 search_entry = SessionLog(tg_id=tg_id, question=question, answer=answer)
# #                 session.add(search_entry)
# #                 await session.commit()
# #                 print(f"Search added: {search_entry}")
# #             else:
# #                 print("Search already exists")
# #         except Exception as e:
# #             await session.rollback()
# #             print(f"Error in set_search: {e}")
#
#
# # ###########################################Analytics Endpoints
# @app.get(
#     "/api/analytics/user/{user_id}", response_model=UserScoreSchema, tags=["Analytics"]
# )
# async def get_user_analytics(user_id: int = Path(..., description="User ID")):
#     """
#     Get comprehensive analytics for a user including scores and progress
#     """
#     analytics = await rq.get_user_scores(user_id)
#     if not analytics:
#         raise HTTPException(status_code=404, detail="User not found")
#     return analytics
#
#
# @app.get(
#     "/api/analytics/leaderboard",
#     response_model=List[UserScoreSchema],
#     tags=["Analytics"],
# )
# async def get_leaderboard(
#     limit: int = Query(10, ge=1, le=100, description="Number of top users to return")
# ):
#     """
#     Get leaderboard of users ranked by average score
#     """
#     return await rq.get_leaderboard(limit)
#
#
# @app.get(
#     "/api/analytics/question/{question_id}",
#     response_model=QuestionWithResponsesSchema,
#     tags=["Analytics"],
# )
# async def get_question_analytics(
#     question_id: int = Path(..., description="Question ID")
# ):
#     """
#     Get question with all its responses for analytics
#     """
#     analytics = await rq.get_question_with_responses(question_id)
#     if not analytics:
#         raise HTTPException(status_code=404, detail="Question not found")
#     return analytics





import os

def print_file_tree(start_path):
    for dirpath, dirnames, filenames in os.walk(start_path):
        level = dirpath.replace(start_path, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}- {os.path.basename(dirpath)}/")
        subindent = '  ' * (level + 1)
        for f in filenames:
            print(f"{subindent}- {f}")

print_file_tree("backend")  # or "." if everything is in root
