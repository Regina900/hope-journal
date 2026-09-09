from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    journal_entries = db.relationship(
        "JournalEntry",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<User {self.username}>"


class JournalEntry(db.Model):
    __tablename__ = "journal_entries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    mood = db.Column(
        db.String(50),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    response = db.relationship(
        "AIResponse",
        backref="journal_entry",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<JournalEntry {self.id}>"


class AIResponse(db.Model):
    __tablename__ = "ai_responses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    journal_entry_id = db.Column(
        db.Integer,
        db.ForeignKey("journal_entries.id"),
        nullable=False,
        unique=True
    )

    emotional_state = db.Column(
        db.String(100),
        nullable=True
    )

    main_concern = db.Column(
        db.Text,
        nullable=True
    )

    biblical_encouragement = db.Column(
        db.Text,
        nullable=True
    )

    scripture_reference = db.Column(
        db.String(100),
        nullable=True
    )

    scripture_text = db.Column(
        db.Text,
        nullable=True
    )

    hope_message = db.Column(
        db.Text,
        nullable=True
    )

    prayer = db.Column(
        db.Text,
        nullable=True
    )

    reflection_question = db.Column(
        db.Text,
        nullable=True
    )

    affirmation = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<AIResponse {self.id}>"


class Scripture(db.Model):
    __tablename__ = "scriptures"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    book = db.Column(
        db.String(50),
        nullable=False
    )

    chapter = db.Column(
        db.Integer,
        nullable=False
    )

    verse = db.Column(
        db.String(30),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    theme = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Scripture {self.book} {self.chapter}:{self.verse}>"


class Prayer(db.Model):
    __tablename__ = "prayers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    journal_entry_id = db.Column(
        db.Integer,
        db.ForeignKey("journal_entries.id"),
        nullable=True
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Prayer {self.id}>"


class Reflection(db.Model):
    __tablename__ = "reflections"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    journal_entry_id = db.Column(
        db.Integer,
        db.ForeignKey("journal_entries.id"),
        nullable=True
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Reflection {self.id}>"