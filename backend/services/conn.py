from backend.core.db.models import async_session

print(f"🔍 [conn.py] async_session imported: {async_session} (type: {type(async_session)})")

def connection(func):
    async def inner(*args, **kwargs):
        print(f"🔧 [conn.py] About to open session from: {async_session}")
        session_obj = async_session()
        print(f"🧪 [conn.py] session_obj = async_session(): {session_obj} (type: {type(session_obj)})")

        try:
            async with session_obj as session:
                print("✅ [conn.py] Successfully opened session")
                result = await func(session, *args, **kwargs)
                print("🔁 [conn.py] Function executed with DB session")
                return result
        except Exception as e:
            print(f"❌ [conn.py] Exception inside connection wrapper: {e}")
            raise e
    return inner
