from src.systemOfSchoolSchedule.models.subject import Subject
from src.systemOfSchoolSchedule.dbConfig.connection import Session

def getSubjectById(subjectId: int) -> str:
    with Session() as session:
        subject = session.query(Subject).filter(Subject.subjectId == subjectId).first()
        return subject.subjectName

def getSubjectIdByName(name: str) -> int | None:
    with Session() as session:
        subject = session.query(Subject).filter(Subject.subjectName == name).first()
        return subject.subjectId if subject else  None



def createSubject(subjectName:str):
    with Session.begin() as session:
        subjectExists = session.query(Subject).filter(Subject.subjectName == subjectName).first()
        if subjectExists:
            return subjectExists
        subject = Subject(subjectName= subjectName)
        session.add(subject)
    return subject


def deleteSubject(subjectName:str):
    with Session.begin() as session:
        subjectExists = session.query(Subject).filter(Subject.subjectName == subjectName).first()
        if subjectExists:
            session.delete(subjectExists)
            print("Предмет удален")
        else:
            print("Такого предмета не существует")
