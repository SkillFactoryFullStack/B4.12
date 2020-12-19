# импортируем библиотеку sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# импортируем библиотеку datetime
from datetime import date

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class Athelete(Base):
    """
    Описывает структуру таблицы athlete для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    """
        Описывает структуру таблицы user для хранения регистрационных данных пользователей
        """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.REAL)


def connect_db():
    """
        Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
        """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sa.orm.sessionmaker(engine)
    # возвращаем сессию
    return session()

def find(user_id, session):
    """
    Производит поиск пользователя в таблице user по заданному id
    """
    query = session.query(User).filter(User.id == user_id)
    # подсчитываем количество найденных записей, если таковых нет, возвращаем None
    if not query.count():
        return
    # возвращаем информацию о том, что пользователь найден
    return query.all()[0]

def request_data(user, session):
    """
    Находит атлета с ближайшей датой рождения и ближайшего по росту
    """
    if len(user.birthdate) < 10:
        close_date = None
    else:
        query = session.query(Athelete).order_by('birthdate')
        user_birthdate = date(int(user.birthdate[0:4]), int(user.birthdate[5:7]), int(user.birthdate[8:10]))
        close_dates = user_birthdate - date(1500, 1, 1)
        for sportsman in query.all():
            sportsman_birthdate = date(int(sportsman.birthdate[0:4]), int(sportsman.birthdate[5:7]), int(sportsman.birthdate[8:10]))
            if abs(user_birthdate - sportsman_birthdate) <= close_dates:
                close_dates = abs(user_birthdate - sportsman_birthdate)
                close_date = sportsman
            else:
                break

    query = session.query(Athelete).order_by('height')
    close_heights = user.height
    for sportsman in query.all():
        if not sportsman.height:
            continue
        if abs(user.height - sportsman.height) <= close_heights:
            close_heights = abs(user.height - sportsman.height)
            close_height = sportsman
        else:
            break

    # возвращаем искомых ближайших
    return close_date, close_height


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    print("Привет! Введите пользователя. \nМы найдем атлета с ближайшей датой рождения и ближайшего по росту.")
    user_id = int(input("Идентификатор пользователя: "))
    user = find(user_id, session)
    if user:
        close_date, close_height = request_data(user, session)
        print("\nДата рождения пользователя:", user.birthdate)
        if close_date:
            print("Атлет с ближайшей датой рождения:\n", close_date.id, close_date.name, close_date.birthdate)
        else:
            print("Ни один атлет даже близко не родился.")
        print("\nРост пользователя:", user.height)
        print("Ближайший по росту атлет:\n", close_height.id, close_height.name, close_height.height)
    else:
        print("Пользователь с таким идентификатором отсутствует в базе данных.")


if __name__ == "__main__":
    main()
