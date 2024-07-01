from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, DateTime, func

PG_DSN = 'sqlite+aiosqlite:///data.db'

engine = create_async_engine(PG_DSN)


class Base(DeclarativeBase, AsyncAttrs):
    pass


Session = async_sessionmaker(engine, expire_on_commit=False)


class Advert(Base):
    __tablename__ = 'user_advert'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    registration_time = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(70), nullable=False)

    @property
    def dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'registration_time': int(self.registration_time.timestamp()),
            'owner': self.owner
        }
