from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

from src.systemOfSchoolSchedule.repositories.schoolClassRepository import getStudentsByClassLeader

def displayClassStudents(teacherId:int):
    console = Console()

    studentsList = getStudentsByClassLeader(teacherId)

    if not studentsList:
        console.print("Вы не назначены классным руководителем ни у одного класса")
        return

    table = Table(
        title="[bold magneta]СПИСОК УЧЕНИКОВ ВАШЕГО КЛАССА[/bold magneta]",
        box=ROUNDED,
        show_lines=True,
        header_style="bold cyan",
        title_justify="center"
    )

    table.add_column("№", justify="center", width=4)
    table.add_column("ID Ученика", justify="center", width=12, style="dim")
    table.add_column("ФИО Ученика", width=35, style="bold white")
    table.add_column("Логин", width=15, style="green")

    for idx, student in enumerate(studentsList, start=1):
        table.add_row(
            str(idx),
            str(student.userId),
            student.fullName,
            student.login
        )
    console.print(table)
