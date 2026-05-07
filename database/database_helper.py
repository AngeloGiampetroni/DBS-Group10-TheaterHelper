from datetime import datetime
from database.theater_database import Movie, Customer, Showing, Ticket
from sqlalchemy.orm import joinedload
import streamlit as st
import pandas as pd

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
    
    def get_movies_with_filters(self, genre=None, age_rating=None):
        """
        Fetch movies from the database with optional filters for genre and age rating.

        :param genre: Optional genre filter (string)
        :param age_rating: Optional age rating filter (string)
        :return: DataFrame with columns: id, title, studio, genre, age_rating, runtime
        """
        with self.connection.session as session:
            query = session.query(Movie)
            
            if genre:
                query = query.filter(Movie.genre == genre)
                
            if age_rating:
                query = query.filter(Movie.age_rating == age_rating)
                
            result = query.all()
            return pd.DataFrame([{
                "id": movie.id,
                "title": movie.title,
                "studio": movie.studio,
                "genre": movie.genre,
                "age_rating": movie.age_rating,
                "runtime": movie.runtime
            } for movie in result]) 
        
    def get_tickets_with_filters(self, genre=None):
        """
        Fetch tickets from the database with optional filter for genre.

        :param genre: Optional genre filter (string)
        :return: DataFrame with columns: ticket_id, customer_name, title, genre, price
        """
        with self.connection.session as session:
            query = session.query(Ticket).join(Movie, Ticket.movie == Movie.id)
            
            if genre:
                query = query.filter(Movie.genre == genre)
                
            result = query.options(joinedload(Ticket.customer_ref)).all()
            return pd.DataFrame([{
                "ticket_id": ticket.id,
                "customer_name": f"{ticket.customer_ref.first_name} {ticket.customer_ref.last_name}",
                "title": ticket.movie_ref.title,
                "genre": ticket.movie_ref.genre,
                "price": ticket.price
            } for ticket in result])

    def ticket_sales_by_movie(self) -> pd.DataFrame:
        """
        Fetch live ticket sales data from the database, grouped by movie title.

        :return: DataFrame with columns: movie.id, sum of price, and title (joined from movie table)
        """
        return self.get_query("select movie, sum(price) from ticket group by movie;")


    def revenue_by_genre(self) -> pd.DataFrame:
        """
        Fetch live ticket sales data from the database, grouped by genre.

        :return: DataFrame with columns: genre and sum of price
        """
        return self.get_query("select genre, sum(price) as revenue from ticket join movie on ticket.movie = movie.id group by genre;")

    def get_all_genres(self) -> pd.DataFrame:
        """
        Fetch all unique genres from the movie table.

        :return: DataFrame with a single column 'genre' containing unique genres
        """
        return self.get_query("select distinct genre from movie;")
    
    def get_all_agerating(self) -> pd.DataFrame:
        """
        Fetch all unique age ratings from the movie table.

        :return: DataFrame with a single column 'age_rating' containing unique age ratings
        """
        return self.get_query("select distinct age_rating from movie;")
    
    def get_showing_dates(self) -> pd.DataFrame:
        """
        Fetch all unique show dates from the showing table.

        :return: DataFrame with a single column 'date' containing unique show dates
        """
        return self.get_query("select distinct date from showing;")


