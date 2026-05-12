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
    
    def remove_ticket(self, ticket_id) -> bool:
        """Deletes a ticket by its ID."""
        try:
            with self.connection.session as session:
                ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
                if not ticket:
                    return False # Ticket doesn't exist
                
                session.delete(ticket)
                session.commit()
                return True
        except Exception as e:
            st.error(f"Failed to delete ticket: {e}")
            return False

    def remove_customer(self, customer_id) -> bool:
        """
        Deletes a customer. 
        ### Will fail if the customer has existing tickets due to RESTRICT constraints.
        """
        try:
            with self.connection.session as session:
                customer = session.query(Customer).filter(Customer.id == customer_id).first()
                if not customer:
                    return False
                
                session.delete(customer)
                session.commit()
                return True
        except Exception as e:
            st.error(f"Cannot delete customer. They may have active tickets. Error: {e}")
            return False

    def remove_showing(self, show_id) -> bool:
        """
        Deletes a showing.
        ### Will fail if tickets are already booked for this show.
        """
        try:
            with self.connection.session as session:
                showing = session.query(Showing).filter(Showing.id == show_id).first()
                if not showing:
                    return False
                
                session.delete(showing)
                session.commit()
                return True
        except Exception as e:
            st.error(f"Cannot delete showing. Tickets may be tied to it. Error: {e}")
            return False

    def remove_movie(self, movie_id) -> bool:
        """
        Deletes a movie. 
        # this will wipe the movie from existing tickets/showings but won't delete the tickets themselves.
        """
        try:
            with self.connection.session as session:
                movie = session.query(Movie).filter(Movie.id == movie_id).first()
                if not movie:
                    return False
                
                session.delete(movie)
                session.commit()
                return True
        except Exception as e:
            st.error(f"Failed to delete movie: {e}")
            return False
        
    def remove_all_tickets_for_showing(self, show_id) -> int:
        """
        Deletes all tickets associated with a specific showing.
        
        :return: Returns the number of tickets deleted, or -1 if an error occurred.
        """
        try:
            with self.connection.session as session:
                # .delete() performs a bulk delete on all matching rows
                deleted_count = session.query(Ticket).filter(Ticket.show_id == show_id).delete()
                session.commit()
                return deleted_count
        except Exception as e:
            st.error(f"Failed to delete tickets for showing: {e}")
            return -1

    def remove_all_tickets_for_movie(self, movie_id) -> int:
        """
        Deletes all tickets associated with a specific movie across ALL showings.

        :return: Returns the number of tickets deleted, or -1 if an error occurred.
        """
        try:
            with self.connection.session as session:
                deleted_count = session.query(Ticket).filter(Ticket.movie == movie_id).delete()
                session.commit()
                return deleted_count
        except Exception as e:
            st.error(f"Failed to delete tickets for movie: {e}")
            return -1

    def remove_all_showings_for_movie(self, movie_id) -> dict:
        """
        Deletes all showings for a specific movie.
        Wipes tickets for those showings first, then removes the showings.

        :return: Dictionary with counts: {'showings_removed': int, 'tickets_removed': int}
                 Returns None if an error occurred.
        """
        try:
            with self.connection.session as session:
                # Step 1: Wipe all tickets tied to any showing of this movie
                # .in_() performs one fast bulk delete instead of looping
                tickets_removed = session.query(Ticket).filter(
                    Ticket.show_id.in_(
                        session.query(Showing.id).filter(Showing.movie == movie_id)
                    )
                ).delete(synchronize_session=False)
                
                # Step 2: Delete the showings themselves
                showings_removed = session.query(Showing).filter(
                    Showing.movie == movie_id
                ).delete()
                
                session.commit()
                return {
                    "showings_removed": showings_removed,
                    "tickets_removed": tickets_removed
                }
        except Exception as e:
            st.error(f"Failed to remove showings for movie: {e}")
            return None

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

        :return: dataframe with columns: title, tickets_sold, revenue
        """
        return self.get_query("select title, count(*) as tickets_sold, sum(price) as revenue from ticket join movie on ticket.movie = movie.id group by title;")
    
    def ticket_sales_by_genre(self) -> pd.DataFrame:
        """
        Fetch live ticket sales data from the database, grouped by genre.

        :return: DataFrame with columns: genre, tickets_sold, revenue
        """
        return self.get_query("select genre, count(*) as tickets_sold, sum(price) as revenue from ticket join movie on ticket.movie = movie.id group by genre;")

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
    
    def get_customer_by_id(self, customer_id) -> Customer:
        """Retrieve customer data from database by ID"""
        try:
            with self.connection.session as session:
                from database.theater_database import Customer
                customer = session.query(Customer).filter(Customer.id == customer_id).first()
                return customer
        except Exception as e:
            st.error(f"Error fetching customer: {e}")
            return None
    
    def get_all_tickets_by_customer(self, customer_id) -> pd.DataFrame:
        """Retrive all tickets for a customer"""
        with self.connection.session as session:
            query = session.query(Ticket).join(Movie, Ticket.movie == Movie.id).join(Showing, Ticket.show_id == Showing.id)
            query = query.filter(Ticket.customer == customer_id)
                
            result = query.options(joinedload(Ticket.customer_ref)).all()
            return pd.DataFrame([{
                "ticket_id": ticket.id,
                "title": ticket.movie_ref.title,
                "date": ticket.showing_ref.date,
                "time": ticket.showing_ref.time.strftime('%I:%M %p'),
                "genre": ticket.movie_ref.genre,
                "price": ticket.price
            } for ticket in result])
        
