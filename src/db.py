from sqlalchemy import ARRAY, BigInteger, Column, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from config import settings

Base = declarative_base()


class UsersOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    approved: Mapped[bool] = mapped_column(server_default="False")
    roles = mapped_column(ARRAY(String))


sync_engine = create_engine(settings.DATABASE_URL, echo=False)
try:
    Base.metadata.create_all(sync_engine, checkfirst=True)
finally:
    sync_engine.dispose()


engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
Session = async_sessionmaker(engine)


async def get_user(user_id: int) -> UsersOrm:
    async with Session() as session:
        return await session.get(UsersOrm, user_id)


async def register_user(  # noqa: PLR0913
    user_id: int,
    first_name: str,
    last_name: str,
    username: str,
    roles: list,
    approved: bool = False,
) -> bool:
    async with Session() as session:
        try:
            stmt = UsersOrm(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                approved=approved,
                roles=roles,
            )
            session.add(stmt)
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False  # already registered user
