from sqlalchemy import func, desc, select, and_
from sqlalchemy.orm import joinedload, subqueryload

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.connect_db import session


# Запит 1.
# 5 студентів із найбільшим середнім балом з усіх предметів.
def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM
        students AS s
    JOIN
        grades AS g ON s.id = g.student_id
    GROUP BY
        s.id
    ORDER BY
        average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


# Запит 2.
# Студент із найвищим середнім балом з певного предмета.
def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM
        grades AS g
    JOIN
        students AS s ON s.id = g.student_id
    WHERE 
        g.subject_id = 1
    GROUP BY
        s.id
    ORDER BY
        average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


# Запит 3.
# Середній бал у групах з певного предмета.
def select_03():
    """
    SELECT
        groups.id,
        groups.name AS group_name,
        ROUND(AVG(grades.grade), 2) AS average_grade
    FROM
        groups
    JOIN
        students ON groups.id = students.group_id
    JOIN
        grades ON students.id = grades.student_id
    WHERE
        grades.subject_id = 7
    GROUP BY
        groups.id, groups.name
    ORDER BY
        groups.id;
    """
    result = session.query(Group.id, Group.name.label("group_name"), func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Group).join(Student).join(Grade).filter(Grade.subjects_id == 10).group_by(Group.id, Group.name) \
        .order_by(Group.id).all()
    return result


# Запит 4.
# Середній бал на потоці (по всій таблиці оцінок).
def select_04():
    """
    SELECT
        ROUND(AVG(grades.grade), 2) AS average_grade
    FROM
        grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).one()
    return result

# Запит 5.
# Які курси на потоці читає певний викладач.
def select_05():
    """
    SELECT
        subjects.name AS course_name,
        teachers.fullname AS teacher_name
    FROM
        subjects
    JOIN
        teachers ON subjects.teacher_id = teachers.id
    WHERE
        subjects.teacher_id = 8;
    """
    result = session.query(Subject.name.label('course_name'), Teacher.fullname.label('teacher_name')).select_from(Subject) \
        .join(Teacher).filter(Subject.teacher_id == 8).all()
    return result


# Запит 6.
# Cписок студентів у певній групі.
def select_06():
    """
    SELECT
        students.id,
        students.fullname AS student_name,
        groups.name
    FROM
        students
    JOIN
        groups ON students.group_id = groups.id
    WHERE
        students.group_id = 5;
    """
    result = session.query(Student.id, Student.fullname.label('student_name'), Group.name).select_from(Student) \
        .join(Group).filter(Student.group_id == 5).all()
    return result


# Запит 7.
# Оцінки студентів у окремій групі з певного предмета.
def select_07():
    """
    SELECT
            students.id,
            students.fullname AS student_name,
            subjects.name as courses, 
            grades.grade
        FROM
            students
        JOIN
            grades ON students.id = grades.student_id
        JOIN
            subjects ON grades.subject_id = subjects.id 
        WHERE
            students.group_id = 3 AND grades.subject_id = 9;
    """
    result = session.query(Student.id, Student.fullname.label('student_name'), Subject.name.label('courses'), Grade.grade) \
        .select_from(Student).join(Grade).join(Subject).filter(and_(Student.group_id == 3, Grade.subjects_id == 9)).all()
    return result


# Запит 8.
# Середній бал, який ставить певний викладач зі всiх своїх предметів.
def select_08():
    """
    SELECT
        teachers.id,
        teachers.fullname AS teacher_name,
        subjects.name AS course,
        ROUND(AVG(grades.grade), 2) AS average_grade
    FROM
        teachers
    JOIN
        subjects ON teachers.id = subjects.teacher_id
    JOIN
        grades ON subjects.id = grades.subject_id
    where
        teachers.id = 4
    GROUP BY
        teachers.id, subjects.name;
    """
    result = session.query(Teacher.id, Teacher.fullname.label('teacher_name'), Subject.name.label('course'), \
        func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Teacher).join(Subject).join(Grade) \
        .filter(Teacher.id == 4).group_by(Teacher.id, Subject.name).all()
    
    return result


# Запит 9.
# Cписок курсів, які відвідує студент
def select_09():
    """
    SELECT
        DISTINCT
        students.id,
        students.fullname,
        subjects.name AS courses
    FROM
        students
    JOIN
        grades ON students.id = grades.student_id
    JOIN
        subjects ON grades.subject_id = subjects.id
    WHERE
        students.id = 255;
    """
    result = session.query(Student.id, Student.fullname, Subject.name.label('courses')).select_from(Student) \
        .join(Grade).join(Subject).filter(Student.id == 255).distinct().all()
    return result


# Запит 10.
# Cписок курсів, які певному студенту читає певний викладач.
def select_10():
    """
    SELECT
        DISTINCT
        students.id,
        students.fullname,
        subjects.name AS courses,
        teachers.fullname as teacher
    FROM
        students
    JOIN
        grades ON students.id = grades.student_id
    JOIN
        subjects ON grades.subject_id = subjects.id
    JOIN
        teachers ON subjects.teacher_id = teachers.id
    WHERE
        students.id = 444 AND teachers.id = 8;
    """
    result = session.query(Student.id, Student.fullname, Subject.name.label('courses'), Teacher.fullname.label('teacher')) \
        .select_from(Student).join(Grade).join(Subject).join(Teacher).filter(and_(Student.id == 444, Teacher.id == 8)) \
        .distinct().all()
    return result


# Запит 11.
# Середній бал, який певний викладач ставить певному студентові.
def select_11():
    """
    SELECT
        students.id,
        students.fullname,
        teachers.fullname AS teacher,
        ROUND(AVG(grades.grade), 3) AS average_grade
    FROM
        students
    JOIN
        grades ON students.id = grades.student_id
    JOIN
        subjects ON grades.subject_id = subjects.id
    JOIN
        teachers ON subjects.teacher_id = teachers.id
    WHERE
        students.id = 422
        AND subjects.teacher_id = 6
    GROUP BY
        students.id, teachers.fullname;
    """
    result = session.query(Student.id, Student.fullname, Teacher.fullname.label('teacher'), func.round(func.avg(Grade.grade), 2) \
        .label('average_grade')).select_from(Student).join(Grade).join(Subject).join(Teacher) \
        .filter(and_(Student.id == 333, Teacher.id == 5)).group_by(Student.id, Teacher.fullname).one()
    return result


# Запит 12.
# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12():
    """
    SELECT
        MAX(grade_date)
    FROM
        grades AS g
    JOIN
        students AS s ON s.id = g.student_id
    WHERE
        g.subject_id = 2 AND s.group_id = 3;


    SELECT
        s.id, s.fullname, g.grade, g.grade_date
    FROM
        grades AS g
    JOIN
        students AS s ON g.student_id = s.id
    WHERE
        g.subject_id = 2 AND s.group_id = 3 AND g.grade_date = (
            SELECT
                MAX(grade_date)
            FROM
                grades AS g
            JOIN
                students AS s ON s.id = g.student_id
            WHERE
                g.subject_id = 2 AND s.group_id = 3
            );
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    # print(*select_01(), sep = "\n")
    # print(*select_02(), sep = "\n")
    # print(*select_03(), sep = "\n")
    print(select_04(), sep = "\n")
    # print(*select_05(), sep = "\n")
    # print(*select_06(), sep = "\n")
    # print(*select_07(), sep = "\n")
    # print(*select_08(), sep = "\n")
    # print(*select_09(), sep = "\n")
    # print(*select_10(), sep = "\n")
    # print(select_11(), sep = "\n")
    print(select_12(), sep = "\n")
    # [print(indx) for indx in select_12()[0]]

