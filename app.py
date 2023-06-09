import datetime
import json

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/tutor"
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
    instrument = db.Column(db.ARRAY(db.UUID(as_uuid=True)), default=uuid.uuid4)

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
    day = db.Column(db.String())
    instrument = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, student, teacher, start_time, end_time, day, instrument):
        self.student = student
        self.teacher = teacher
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        self.instrument = instrument

    def __repr__(self):
        return f"<Result form {self.name}>"


@app.route('/student_form', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def handle_student_records():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                new_record = StudentFormModel(name=data['name'], last_name=data['last_name'],
                                              prefer_start_time=data['prefer_start_time'],
                                              prefer_end_time=data['prefer_end_time'], day=data['day'],
                                              instrument=data['instrument'])
                db.session.add(new_record)
                db.session.commit()
                return {"message": "Новая запись успешно добавлена"}
            else:
                return {"error": "The request payload is not in JSON format"}
        except:
            return {"Message": "Пока"}
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

        return json.dumps(results, default=str)


@app.route('/teacher_form', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def handle_teacher_records():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_record = TeacherFormModel(name=data['name'], last_name=data['last_name'],
                                          work_start_time=data['work_start_time'],
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

        return json.dumps(results, default=str)


@app.route('/instruments', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
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

        return results


def shortener(record, is_person):
    if record != None:
        id = record.id
        try:
            name = record.name
        except:
            name = record.instrument
        if is_person:
            name = record.name + " " + record.last_name
        return {
            'id': id,
            'name': name
        }
    else:
        return None


@app.route('/result', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def handle_result():
    if request.method == 'POST':
        student_records = StudentFormModel.query.order_by(StudentFormModel.prefer_start_time,
                                                          StudentFormModel.prefer_end_time).all()
        teacher_records = TeacherFormModel.query.order_by(TeacherFormModel.work_start_time,
                                                          TeacherFormModel.work_end_time).all()
        student_tuple = [
            {
                "id": record.id,
                "name": record.name,
                "last_name": record.last_name,
                "prefer_start_time": record.prefer_start_time,
                "prefer_end_time": record.prefer_end_time,
                "day": record.day,
                "instrument": record.instrument,
                "active": 'true'
            } for record in student_records]
        teacher_tuple = [
            {
                "id": record.id,
                "name": record.name,
                "last_name": record.last_name,
                "work_start_time": record.work_start_time,
                "work_end_time": record.work_end_time,
                "instrument": record.instrument,
            } for record in teacher_records]
        result = []
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        ResultScheduleModel.query.delete()

        for i in range(len(teacher_tuple)):
            for x in weekdays:
                cache = []
                for j in range(len(student_tuple)):
                    if teacher_tuple[i]['name'] == "Резерв":
                        break
                    else:
                        if student_tuple[j]['day'] == x:
                            student_instrument = student_tuple[j]['instrument']
                            teacher_instruments = teacher_tuple[i]['instrument']
                            if student_instrument in teacher_instruments:
                                if student_tuple[j]['prefer_start_time'] in cache:
                                    student_tuple[j]['active'] = 'res'
                                else:
                                    for z in range(len(teacher_tuple[i]['instrument'])):
                                        if student_tuple[j]['active'] == 'true':
                                            if student_tuple[j]['instrument'] == teacher_tuple[i]['instrument'][z]:
                                                if teacher_tuple[i]['work_start_time'] <= student_tuple[j][
                                                    'prefer_start_time'] and \
                                                        student_tuple[j]['prefer_end_time'] <= teacher_tuple[i]['work_end_time']:
                                                    student_tuple[j]['active'] = 'false'
                                                    result.append({'student': student_tuple[j]['id'], 'teacher': str(teacher_tuple[i]['id']),
                                                                   'start_time': str(student_tuple[j]['prefer_start_time']),
                                                                   'end_time': str(student_tuple[j]['prefer_end_time']),
                                                                   'day': str(x),
                                                                   'instrument': teacher_tuple[i]['instrument'][z]})
                                if student_tuple[j]['prefer_start_time'] not in cache:
                                    cache.append(student_tuple[j]['prefer_start_time'])

        for n in range(len(student_tuple)):
            if student_tuple[n]['active'] == 'true':
                student_tuple[n]['active'] = 'res'

        for i in range(len(teacher_tuple)):
            for j in range(len(student_tuple)):
                for z in range(len(teacher_tuple[i]['instrument'])):
                    if teacher_tuple[i]['work_start_time'] <= student_tuple[j]['prefer_start_time'] and \
                            student_tuple[j]['prefer_end_time'] <= teacher_tuple[i]['work_end_time'] and \
                            student_tuple[j]['active'] == 'res' and student_tuple[j]['instrument'] == teacher_tuple[i]['instrument'][z] and teacher_tuple[i]['name'] == "Резерв":
                            result.append({'student': str(student_tuple[j]['id']), 'teacher': teacher_tuple[i]['id'],
                                           'start_time': str(student_tuple[j]['prefer_start_time']),
                                           'end_time': str(student_tuple[j]['prefer_end_time']),
                                           'day': str(student_tuple[j]['day']),
                                           'instrument': teacher_tuple[i]['instrument'][z]})

        for record in result:
            db.session.add(ResultScheduleModel(student=record['student'], teacher=record['teacher'],
                                               start_time=record['start_time'],
                                               end_time=record['end_time'], day=record['day'],
                                               instrument=record['instrument']))
            db.session.commit()
        return Response("{'message':'OK'}", status=201, mimetype='application/json')
    elif request.method == 'GET':
        records = ResultScheduleModel.query.all()
        results = []
        for record in records:
            teacher = shortener(TeacherFormModel.query.get(record.teacher), True)
            student = shortener(StudentFormModel.query.get(record.student), True)
            instrument = shortener(InstrumentsModel.query.get(record.instrument), False)
            results.append({
                "id": record.id,
                "student": student,
                "teacher": teacher,
                "start_time": record.start_time,
                "end_time": record.end_time,
                "day": record.day,
                "instrument": instrument,
            })

        return json.dumps(results, default=str)
