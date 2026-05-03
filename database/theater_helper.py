from datetime import datetime
from database.theater_database import Movie, Customer, Showing, Ticket
from sqlalchemy.orm import joinedload

class TheaterDBHelper:
    def __init__(self, connection):
        self.connection = connection

    def add_movie(self, title, studio, genre, age_rating, runtime):
        with self.connection.session as session:
            new_movie = Movie(
                title=title,
                studio=studio,
                genre=genre,
                age_rating=age_rating,
                runtime=runtime,
                date_entered=datetime.now()
            )
            session.add(new_movie)
            session.commit()
            return True

    def add_customer(self, first_name, last_name, email, phone, age):
        with self.connection.session as session:
            new_cust = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone,
                age=age,
                date_entered=datetime.now()
            )
            session.add(new_cust)
            session.commit()
            return True

    def add_ticket(self, customer_id, movie_id, show_id, price):
        with self.connection.session as session:
            new_ticket = Ticket(
                customer=customer_id,
                movie=movie_id,
                show_id=show_id,
                price=price,
                date_entered=datetime.now()
            )
            session.add(new_ticket)
            session.commit()
            return True

    def get_query(self, query):
        """
        ONLY FOR SELECT QUERIES\n
        PLEASE DONT USE THIS FOR ANYTHING OTHER THAN SELECT QUERIES
        """
        return self.connection.query(query, ttl=600)
