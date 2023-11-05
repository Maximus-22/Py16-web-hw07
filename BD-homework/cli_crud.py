import argparse


from sqlalchemy import func, desc, select, and_
from sqlalchemy.exc import SQLAlchemyError

from conf.connect_db import session
from conf.models import Group, Teacher, Subject, Student


" CRUD Table Groups "

def create_group(id, name):
    new_group = Group(name = name)
    try:
        session.add(new_group)
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()

def list_groups(*args):
    groups = session.query(Group).all()
    for group in groups:
        print(f"Group ID: {group.id}, Name: {group.name}")

def update_group(group_id, new_name):
    group = session.query(Group).filter_by(id = group_id).first()
    if group:
        try:
            group.name = new_name
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()    
    else:
        print(f"Group with ID {group_id} not found.")

def delete_group(group_id, name):
    group = session.query(Group).filter_by(id = group_id).first()
    if group:
        try:
            session.delete(group)
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()
    else:
        print(f"Group with ID {group_id} not found.")



" CRUD Table Teachers "

def create_teacher(id, fullname):
    new_teacher = Teacher(fullname = fullname)
    try:
        session.add(new_teacher)
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()

def list_teachers(*args):
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"Teacher ID: {teacher.id}, Fullname: {teacher.fullname}")

def update_teacher(teacher_id, new_fullname):
    teacher = session.query(Teacher).filter_by(id = teacher_id).first()
    if teacher:
        try:
            teacher.fullname = new_fullname
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()    
    else:
        print(f"Teacher with ID {teacher_id} not found.")

def delete_teacher(teacher_id, fullname):
    teacher = session.query(Teacher).filter_by(id = teacher_id).first()
    if teacher:
        try:
            session.delete(teacher)
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()
    else:
        print(f"Teacher with ID {teacher_id} not found.")



" CRUD Table Subjects "

def create_subject(teacher_id, name):
    new_subject = Subject(name = name, teacher_id = teacher_id)
    try:
        session.add(new_subject)
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()

def list_subjects(*args):
    subjects = session.query(Subject).all()
    for subj in subjects:
        print(f"Subject ID: {subj.id}, Course name: {subj.name}")

def update_subject(subject_id, new_name):
    subject = session.query(Subject).filter_by(id = subject_id).first()
    if subject:
        try:
            subject.name = new_name
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()

def delete_subject(subject_id, name):
    subject = session.query(Subject).filter_by(id = subject_id).first()
    if subject:
        try:
            session.delete(subject)
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()



" CRUD Table Students "

def create_student(group_id, fullname):
    new_student = Student(fullname = fullname, group_id = group_id)
    try:
        session.add(new_student)
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()

def list_students_in_group(group_id, fullname):
    students = session.query(Student).filter_by(group_id = group_id).all()
    for student in students:
        print(f"Student ID: {student.id}, Fullname: {student.fullname}")

def update_student(student_id, new_fullname):
    student = session.query(Student).filter_by(id = student_id).first()
    if student:
        try:
            student.fullname = new_fullname
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()
    else:
        print(f"Student with ID {student_id} not found.")

def delete_student(student_id, fullname):
    student = session.query(Student).filter_by(id = student_id).first()
    if student:
        try:
            session.delete(student)
            session.commit()
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()
    else:
        print(f"Student with ID {student_id} not found.")


COMMANDS_MAP = {"create_group": create_group, "create_student": create_student, \
                "create_subject": create_subject, "create_teacher": create_teacher, \
                "list_group": list_groups, "list_student": list_students_in_group, \
                "list_subject": list_subjects, "list_teacher": list_teachers, \
                "update_group": update_group, "update_student": update_student, \
                "update_subject": update_subject, "update_teacher": update_teacher, \
                "remove_group": delete_group, "remove_student": delete_student, \
                "remove_subject": delete_subject, "remove_teacher": delete_teacher,}


def execute_command(action, model, id = None, name = None):
    command = f"{action}_{model}"
    if command in COMMANDS_MAP:
        print(command)
        COMMANDS_MAP[command](id, name)
    else:
        print("This command dosn't exist in \{COMMANDS_MAP\}.")


def parser_command_row():
    parser = argparse.ArgumentParser(description = "Realization CRUD queryes for batabase PostgreSQL[hw-06].")
    parser.add_argument("-a", "--action", choices = ["create", "list", "update", "remove"], required = True, \
                        help = "Available аction to perform: [create], [list], [update] and [remove].")
    parser.add_argument("-m", "--model", choices = ["Teacher", "Group", "Student", "Subject"], required = True, \
                        help = "The models for changes: [Teacher], [Group], [Student], [Subject].")
    parser.add_argument("--id", type = int, help = "Record ID for [update] and [remove] actions.")
    parser.add_argument("--name", help = "NAME of the record for [create] and [update] actions.")

    args = parser.parse_args()
    (action, model, id, name,) = args.action, args.model.lower(), args.id, args.name
    
    return action, model, id, name


if __name__ == "__main__":
    command_row = parser_command_row()
    execute_command(*command_row)