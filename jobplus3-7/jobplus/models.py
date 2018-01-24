from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate= datetime.utcnow)

user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user_id', ondelete='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job_id', ondelete= 'CASCADE'))
    )

class User(Base, UserMixin):
    __tablename__ = 'user'

    R_USER = 10
    R_COMPANY = 20
    R_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.Stirng(256), nullable=False)
    role = db.Column(db.SmallInteger, default=R_USER)
    resume = db.relationship('Resume', uselist=False)
    collect_jobs = db.relationship('Job', secondary=user_job)
    upload_resume_url = db.Column(db.String(64))

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_passwor)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @porperty
    def is_admin(self):
        return self.role == self.R_ADMIN

    @property
    def is_company(self):
        return self.role == self.R_COMPANY


class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    job_experiences = db.relationship('JobExperience')
    edu_experiences = db.relationship('EduExperience')
    project_experiences = db.relationship('ProjectExperience')

    def profile(self):
        pass

class Experience(Base):
    __abstract_ = True

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    description = db.Column(db.String(1024))

class JobExperience(Experience):
    __tablename__ = 'job_experience'

    company = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(32), nullable=False)
    specialty = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(16))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

class ProjectExperice(Experience):
    __tablename__ = 'project_experience'

    name = db.Column(db.String(32), nullable=False)
    role = db.Column(db.Sting(32))
    technologys = db.Column(db.Sting(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

class Company(Base):
    __talbename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True, unique=True)
    slug = db.Column(db.String(64), nullable=False, index=True, unique=True)
    logo = db.Column(db.String(64), nullable=False)
    site = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(100))
    about = db.Column(db.String(1024))
    tags = db.Column(db.String(128))
    stack = db.Column(db.String(128))
    team_introduction = db.Column(db.String(256))
    welfares = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))

    def __repr__(self):
        return '<Company {}>'.format(self.name)

class Job(Base):
    __tablename__ = 'job'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(32))
    tags = db.Column(db.String(128))
    experience_requirement = db.Column(db.String(32))
    degree_requirement = db.Column(db.String(32))
    is_fulltime = db.Column(db.Boolean, default=True)
    is_open = db.Column(db.Boolean, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)
    views_count - db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Job {}>'.format(self.name)

class Dilivery(Base):
    __tablename__ = 'delivery'

    S_WAITING = 1
    S_REJECT = 2
    S_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    job.id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    response = db.Column(db.String(256))
