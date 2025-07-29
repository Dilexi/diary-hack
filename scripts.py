from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from random import choice
import argparse


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject, commendation):
    lessons_student = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject__title__contains=subject).order_by('-date')
    if not lessons_student.exists():
        print(f"Уроки по предмету '{subject}' для {schoolkid.full_name} не найдены.")
        return
    lesson_student = lessons_student.first()
    Commendation.objects.create(text=commendation, created=lesson_student.date, schoolkid=schoolkid, subject=lesson_student.subject, teacher=lesson_student.teacher) 


def main():
    parser = argparse.ArgumentParser(description="Скрипт позволяет исправить оценки, удалить замечания и добавить похвалу ученику.")
    parser.add_argument("full_name", type=str, help="ФИО ученика (можно частично, например 'Иванов Иван')")
    parser.add_argument("subject", type=str, help="Название предмета (например, 'Математика')")
    args = parser.parse_args()
    full_name = args.full_name
    subject = args.subject
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!'
    ]
    commendation = choice(commendations)
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=full_name)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников по запросу '{full_name}'. Уточните ФИО.")
        return
    except Schoolkid.DoesNotExist:
        print(f"Ученик с ФИО, содержащим '{full_name}', не найден.")
        return
    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, subject, commendation)


if __name__=='__main__':
    main()