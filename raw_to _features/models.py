from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    position = Column(String(50))
    birth_date = Column(Date)
    nationality = Column(String(100))

    # Relationship to Team
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStat", back_populates="player")
    transfers = relationship("Transfer", foreign_keys="[Transfer.player_id]", back_populates="player")

class Team(Base):
    __tablename__ = 'teams'
    
    team_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    league = Column(String(100))
    coach = Column(String(255))

    # Relationship to Players
    players = relationship("Player", back_populates="team")
    # transfers_from = relationship("Transfer", foreign_keys="[Transfer.from_team_id]", back_populates="from_team")
    # transfers_to = relationship("Transfer", foreign_keys="[Transfer.to_team_id]", back_populates="to_team")

class Match(Base):
    __tablename__ = 'matches'
    
    match_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    league = Column(String(100))
    season = Column(String(50))
    home_team_id = Column(Integer, ForeignKey('teams.team_id'))
    away_team_id = Column(Integer, ForeignKey('teams.team_id'))
    stadium = Column(String(255))
    goals_home = Column(Integer)
    goals_away = Column(Integer)

    # Relationships
    player_stats = relationship("PlayerStat", back_populates="match")

class PlayerStat(Base):
    __tablename__ = 'player_stats'
    
    player_id = Column(Integer, ForeignKey('players.player_id'), primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.match_id'), primary_key=True)
    goals = Column(Integer)
    assists = Column(Integer)
    minutes_played = Column(Integer)
    passing_accuracy = Column(DECIMAL(5, 2))
    shots = Column(Integer)
    tackles = Column(Integer)
    rating = Column(DECIMAL(3, 1))

    # Relationships
    player = relationship("Player", back_populates="stats")
    match = relationship("Match", back_populates="player_stats")

class Transfer(Base):
    __tablename__ = 'transfers'
    
    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    from_team_id = Column(Integer, ForeignKey('teams.team_id'))
    to_team_id = Column(Integer, ForeignKey('teams.team_id'))
    transfer_date = Column(Date)
    transfer_fee = Column(DECIMAL(15, 2))

    # Relationships
    player = relationship("Player", back_populates="transfers")
