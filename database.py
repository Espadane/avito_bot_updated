from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import Session, DeclarativeBase
from logger import logger


try:
    engine = create_engine('sqlite:///database.db')
except Exception as error:
    logger.warning(error)


class Base(DeclarativeBase):
    pass


class Subscriptions(Base):
    """
        таблица подписок пользоветеля
    """
    __tablename__ = 'subscriptions'
    id = Column(Integer(), primary_key=True)
    subscription = Column(String(200), nullable=False)


class Posts(Base):
    """
        таблица отправленных объявлений в чат для проверки
    """
    __tablename__ = 'posts'
    id = Column(Integer(), primary_key=True)
    post_name = Column(String(200), nullable=False)
    post_link = Column(String(200), nullable=False)


try:
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
except Exception as error:
    logger.warning(error)


def check_request_in_db(request_link):
    """
        проверка наличия подписки в базе данных
    """
    request = session.query(Subscriptions).filter(
        Subscriptions.subscription == request_link
    ).first()

    return request


def insert_request_to_subscription(request_link):
    """
        добавление подписки в базу данных
    """
    subscriptions = Subscriptions(
        subscription=request_link
    )
    try:
        session.add(subscriptions)
        session.commit()
        logger.debug('Подписка добавлена')
    except Exception as error:
        logger.warning(error)


def check_post_in_db(post_link):
    """
        проверка нахождения объявления в базе данных
    """
    request = session.query(Posts).filter(
        Posts.post_link == post_link
    ).first()

    return request


def insert_post_to_posts(post_name, post_link):
    """
        вставка объявления в базу данных
    """
    posts = Posts(
        post_name=post_name,
        post_link=post_link
    )
    try:
        session.add(posts)
        session.commit()
        logger.debug(f'Объявление {post_name} добавлено')
    except Exception as error:
        logger.warning(error)


def get_all_subscriptions():
    """
        получение списка всех подписок пользователя
    """
    all_subscriptions = session.query(Subscriptions).all()

    return all_subscriptions


def unsubscription(request_link):
    """
        удаление подписки из базы данных
    """
    subscription = session.query(Subscriptions).filter(
        Subscriptions.subscription == request_link
    ).first()
    try:
        session.delete(subscription)
        session.commit()
    except Exception as error:
        logger.warning(error)
