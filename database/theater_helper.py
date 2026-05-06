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
        
    def add_showing(self, movie_id, room_number, date, time):
        with self.connection.session as session:
            new_showing = Showing(
                movie=movie_id,
                room_number=room_number,
                date=date,
                time=time,
                date_entered=datetime.now()
            )
            session.add(new_showing)
            session.commit()
            return True
        
    def update_customer(self, customer_id, first_name=None, last_name=None, email=None, phone=None, age=None):
        with self.connection.session as session:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                return False
            
            if first_name is not None:
                customer.first_name = first_name
                
            if last_name is not None:
                customer.last_name = last_name
                
            if email is not None:
                customer.email = email
                
            if phone is not None:
                customer.phone_number = phone
                
            if age is not None:
                customer.age = age
                
            session.commit()
            return True
    
    def update_movie(self, movie_id, title=None, studio=None, genre=None, age_rating=None, runtime=None):
        with self.connection.session as session:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if not movie:
                return False
            
            if title is not None:
                movie.title = title
                
            if studio is not None:
                movie.studio = studio
                
            if genre is not None:
                movie.genre = genre
                
            if age_rating is not None:
                movie.age_rating = age_rating
                
            if runtime is not None:
                movie.runtime = runtime
                
            session.commit()
            return True
    
    def update_showing(self, show_id, movie_id=None, room_number=None, date=None, time=None):
        with self.connection.session as session:
            showing = session.query(Showing).filter(Showing.id == show_id).first()
            if not showing:
                return False
            
            if movie_id is not None:
                showing.movie = movie_id
                
            if room_number is not None:
                showing.room_number = room_number
                
            if date is not None:
                showing.date = date
                
            if time is not None:
                showing.time = time
                
            session.commit()
            return True
        
    def update_ticket(self, ticket_id, customer_id=None, movie_id=None, show_id=None, price=None):
        with self.connection.session as session:
            ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                return False
            
            if customer_id is not None:
                ticket.customer = customer_id
                
            if movie_id is not None:
                ticket.movie = movie_id
                
            if show_id is not None:
                ticket.show_id = show_id
                
            if price is not None:
                ticket.price = price
                
            session.commit()
            return True

    def get_query(self, query):
        """
        ONLY FOR SELECT QUERIES\n
        PLEASE DONT USE THIS FOR ANYTHING OTHER THAN SELECT QUERIES
        """
        return self.connection.query(query, ttl=600)
