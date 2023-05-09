import datetime
import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text as sa_text
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@192.168.56.101:5432/tutor"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class StudentFormModel(db.Model):
    __tablename__ = 'student_form'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    prefer_start_time = db.Column(db.Time())
    prefer_end_time = db.Column(db.Time())
    day = db.Column(db.String())
    instrument = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, name, last_name, prefer_start_time, prefer_end_time, day, instrument):
        self.name = name
        self.last_name = last_name
        self.prefer_start_time = prefer_start_time
        self.prefer_end_time = prefer_end_time
        self.day = day
        self.instrument = instrument

    def __repr__(self):
        return f"<Student form {self.name}>"


class TeacherFormModel(db.Model):
    __tablename__ = 'teacher_form'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    work_start_time = db.Column(db.Time())
    work_end_time = db.Column(db.Time())
    instrument = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, name, last_name, work_start_time, work_end_time, instrument):
        self.name = name
        self.last_name = last_name
        self.work_start_time = work_start_time
        self.work_end_time = work_end_time
        self.instrument = instrument

    def __repr__(self):
        return f"<Teacher form {self.name}>"


class InstrumentsModel(db.Model):
    __tablename__ = 'instruments'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    instrument = db.Column(db.String(50), nullable=False)

    def __init__(self, instrument):
        self.instrument = instrument

    def __repr__(self):
        return f"<Instrument {self.instrument}>"


class ResultScheduleModel(db.Model):
    __tablename__ = 'result_schedule_form'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)
    teacher = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    instrument = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, name, last_name, start_time, end_time, instrument):
        self.name = name
        self.last_name = last_name
        self.start_time = start_time
        self.end_time = end_time
        self.instrument = instrument

    def __repr__(self):
        return f"<Result form {self.name}>"


@app.route('/student_form', methods=['POST', 'GET'])
def handle_student_records():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_record = StudentFormModel(name=data['name'], last_name=data['last_name'], prefer_start_time=data['prefer_start_time'],
                                  prefer_end_time=data['prefer_end_time'], day=data['day'], instrument=data['instrument'])
            db.session.add(new_record)
            db.session.commit()
            return {"message": "Новая запись успешно добавлена"}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        records = StudentFormModel.query.all()
        results = [
            {
                "name": record.name,
                "last_name": record.last_name,
                "start_time": record.prefer_start_time,
                "end_time": record.prefer_end_time,
                "instrument": record.instrument,
            } for record in records]

        return {"count": len(results), "record": results}


@app.route('/teacher_form', methods=['POST', 'GET'])
def handle_teacher_records():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_record = TeacherFormModel(name=data['name'], last_name=data['last_name'], work_start_time=data['work_start_time'],
                                  work_end_time=data['work_end_time'], instrument=data['instrument'])
            db.session.add(new_record)
            db.session.commit()
            return {"message": "Новая запись успешно добавлена"}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        records = TeacherFormModel.query.all()
        results = [
            {
                "name": record.name,
                "last_name": record.last_name,
                "start_time": record.work_start_time,
                "end_time": record.work_end_time,
                "instrument": record.instrument,
            } for record in records]

        return {"count": len(results), "record": results}


@app.route('/instruments', methods=['POST', 'GET'])
def handle_instruments():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_record = InstrumentsModel(instrument=data['instrument'])
            db.session.add(new_record)
            db.session.commit()
            return {"message": "Новая запись успешно добавлена"}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        records = InstrumentsModel.query.all()
        results = [
            {
                "id": record.id,
                "instrument": record.instrument,
            } for record in records]

        return {"count": len(results), "record": results}


@app.route('/result', methods=['POST', 'GET'])
def handle_result():
    if request.method == 'POST':
        student_records = StudentFormModel.query.order_by(StudentFormModel.prefer_start_time, StudentFormModel.prefer_end_time).all()
        results = [
            {
                "id": record.id,
                "name": record.name,
                "last_name": record.last_name,
                "prefer_start_time": record.prefer_start_time,
                "prefer_end_time": record.prefer_end_time,
                "instrument": record.instrument,
            } for record in student_records]
        # res = json.dumps(results, default=json_util.default)
        return {"message": json.dumps(results, default=str)}
            # return {"message": "Расписание составлено"}
        #else:
            #return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        records = ResultScheduleModel.query.all()
        results = [
            {
                "id": record.id,
                "student": record.student,
                "teacher": record.teacher,
                "start_time": record.start_time,
                "end_time": record.end_time,
                "instrument": record.instrument,
            } for record in records]

        return {"count": len(results), "record": results}
