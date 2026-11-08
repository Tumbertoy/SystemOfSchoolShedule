import os

from rich.console import Console
from src.systemOfSchoolSchedule.repositories.userRepostiory import getNameById
import datetime
import readchar
from rich.table import Table
from rich.box import ROUNDED
from rich.live import Live
from src.systemOfSchoolSchedule.repositories.schoolClassRepository import getNameClassById
from src.systemOfSchoolSchedule.repositories.scheduleRepository import getScheduleForClass, getScheduleForTeacher

def interactiveScheduleViewerForTeacher(teacherId: int):
    teacherName = getNameById(teacherId)
    console = Console()
    today = datetime.datetime.today().date()
    currentMonday = today - datetime.timedelta(days=today.weekday())

    # инструкция
    console.print("\n[dim]Управление: [<-] Прошлая неделя | [->] Следующая неделя | [q] Выход[/dim]\n")

    with Live(auto_refresh=False, screen=True) as live:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            currentWeeklySchedule = getScheduleForTeacher(teacherId, currentMonday)

            endOfWeek = currentMonday + datetime.timedelta(days=6)

            # Сборка таблицы
            table = Table(
                title=f"РАСПИСАНИЕ ДЛЯ УЧИТЕЛЯ {teacherName}\n[cyan]Неделя: {currentMonday.strftime('%d.%m.%Y')} - {endOfWeek.strftime('%d.%m.%Y')}[/cyan]",
                box=ROUNDED,
                show_lines=True,
                header_style='bold magenta',
                title_justify='center'
            )

            table.add_column("Дата и день", width=18, justify="center")
            table.add_column("№ Урока", style="dim", width=4, justify="center")
            table.add_column("Предмет", style="bold white", width=25)
            table.add_column("Класс", style="cyan", width=12, justify="center")

            daysNames = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

            for dayIndex in range(7):
                dayDate = currentMonday + datetime.timedelta(days=dayIndex)
                dayLessons = currentWeeklySchedule.get(dayIndex, [])

                isToday = (dayDate == today)
                dateColor = "bold bright_green" if isToday else "bold yellow"
                dateStr = f"[{dateColor}]{dayDate.strftime('%d.%m.%Y')} ({daysNames[dayIndex]})[/{dateColor}]"

                if not dayLessons:
                    table.add_row(dateStr, "", "[dim italic]Выходной день[/dim italic]", "")
                else:
                    for idx, lesson in enumerate(dayLessons):
                        table.add_row(
                            dateStr if idx == 0 else "",
                            str(lesson[0]),  # LessonNumber
                            str(lesson[1]),  # subject
                            getNameById(lesson[2])  # classId
                        )
            console.print(table)
            key = input()
            if key == "":
                currentMonday += datetime.timedelta(days=7)
            elif key == "-":
                currentMonday -= datetime.timedelta(days=7)
            elif key.lower() == "q":
                break


def interactiveScheduleViewer(classId: int):
    className = getNameClassById(classId)
    console = Console()
    today = datetime.datetime.today().date()
    currentMonday = today - datetime.timedelta(days=today.weekday())

    #инструкция
    console.print("\n[dim]Управление: [<-] Прошлая неделя | [->] Следующая неделя | [q] Выход[/dim]\n")

    with Live(auto_refresh=False) as live:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            currentWeeklySchedule = getScheduleForClass(classId, currentMonday)
            endOfWeek = currentMonday + datetime.timedelta(days=6)

            #Сборка таблицы
            table = Table(
                title=f"РАСПИСАНИЕ ДЛЯ КЛАССА {className}\n[cyan]Неделя: {currentMonday.strftime('%d.%m.%Y')} - {endOfWeek.strftime('%d.%m.%Y')}[/cyan]",
                box=ROUNDED,
                show_lines=True,
                header_style='bold magenta',
                title_justify='center'
            )

            table.add_column("Дата и день", width=18, justify="center")
            table.add_column("№ Урока", style="dim", width=4, justify="center")
            table.add_column("Предмет", style="bold white", width=25)
            table.add_column("Учитель", style="cyan", width=12, justify="center")

            daysNames=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

            for dayIndex in range(7):
                dayDate = currentMonday + datetime.timedelta(days=dayIndex)
                dayLessons = currentWeeklySchedule.get(dayIndex,[])

                isToday = (dayDate == today)
                dateColor = "bold bright_green" if isToday else "bold yellow"
                dateStr = f"[{dateColor}]{dayDate.strftime('%d.%m.%Y')} ({daysNames[dayIndex]})[/{dateColor}]"

                if not dayLessons:
                    table.add_row(dateStr, "", "[dim italic]Выходной день[/dim italic]", "")
                else:
                    for idx, lesson in enumerate(dayLessons):
                        table.add_row(
                            dateStr if idx == 0 else "",
                            str(lesson[0]), #LessonNumber
                            str(lesson[1]), #subject
                            getNameById(lesson[2]) #teacherId
                        )
            console.print(table)
            key = input()
            if key == "":
                currentMonday += datetime.timedelta(days=7)
            elif key == "-":
                currentMonday -= datetime.timedelta(days=7)
            elif key.lower() == "q":
                break
