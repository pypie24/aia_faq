from sqlalchemy.ext.asyncio import AsyncSession


class BaseServiceDBSession:
    def __init__(self, session: AsyncSession):
        self.session = session
