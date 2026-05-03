import streamlit as st
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Float, Date, Integer, String, Time, DateTime, ForeignKey
import numpy as np
import pandas as pd

"""ORM classes for the theater database."""

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movie"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=False)
    studio = Column(String(45), nullable=False)
    genre = Column(String(45))
    age_rating = Column(String(45))
    runtime = Column(Time)
    date_entered = Column(DateTime, nullable=False)
    
    # foreign keys
    showings = relationship("Showing", back_populates="movie_ref")
    tickets = relationship("Ticket", back_populates="movie_ref")

class Customer(Base):
    __tablename__ = "customer"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(45), nullable=False)
    phone_number = Column(String(45), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    age = Column(Integer)
    date_entered = Column(DateTime)
    
    # foreign keys
    tickets = relationship("Ticket", back_populates="customer_ref")

class Showing(Base):
    __tablename__ = "showing"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    # foreign Keys
    movie = Column(
        Integer, 
        ForeignKey("movie.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    room_number = Column(String(45), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    date_entered = Column(DateTime)

    movie_ref = relationship("Movie", back_populates="showings")
    tickets = relationship("Ticket", back_populates="showing_ref")

class Ticket(Base):
    __tablename__ = "ticket"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # foreign Keys
    customer = Column(
        Integer, 
        ForeignKey("customer.id", ondelete="RESTRICT", onupdate="CASCADE"), 
        nullable=False
    )
    movie = Column(
        Integer, 
        ForeignKey("movie.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    show_id = Column(
        Integer, 
        ForeignKey("showing.id", ondelete="NO ACTION", onupdate="NO ACTION")
    )
    price = Column(Float, nullable=False)
    date_entered = Column(DateTime)

    customer_ref = relationship("Customer", back_populates="tickets")
    movie_ref = relationship("Movie", back_populates="tickets")
    showing_ref = relationship("Showing", back_populates="tickets")