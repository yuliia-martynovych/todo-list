from controllers.task_controller import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    get_tasks_by_user,
)
from controllers.user_controller import get_user_by_id

import utils.session
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_admin_tasks_menu():
    while True:
        limpiar_consola()
        print("\033[1;96m╔══════════════════════════════════════╗")
        print("║        ✅  MENÚ TO-DO LIST           ║")
        print("╠══════════════════════════════════════╣")
        print("║ \033[1;93m1.\033[1;96m Crear tarea                       ║")
        print("║ \033[1;93m2.\033[1;96m Ver todas las tareas              ║")
        print("║ \033[1;93m3.\033[1;96m Ver tarea por ID                  ║")
        print("║ \033[1;93m4.\033[1;96m Ver tareas por usuario            ║")
        print("║ \033[1;93m5.\033[1;96m Actualizar tarea                  ║")
        print("║ \033[1;93m6.\033[1;96m Eliminar tarea                    ║")
        print("║ \033[1;91m7.\033[1;96m Salir                             ║")
        print("╚══════════════════════════════════════╝\033[0m")

        choice = input("\033[1mSeleccione una opción: \033[0m")
        if choice == "1":
            create_task_menu()
        elif choice == "2":
            get_all_tasks_menu()
        elif choice == "3":
            get_task_by_id_menu()
        elif choice == "4":
            get_tasks_by_user_menu()
        elif choice == "5":
            update_task_menu()
        elif choice == "6":
            delete_task_menu()
        elif choice == "7":
            print("Saliendo del menú...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def display_users_tasks_menu():
    print(utils.session.current_user.id)
    while True:
        limpiar_consola()
        print("\033[1;96m╔══════════════════════════════════════╗")
        print("║        📋  MENÚ TO-DO LIST           ║")
        print("╠══════════════════════════════════════╣")
        print("║ \033[1;93m1.\033[1;96m Crear tarea                       ║")
        print("║ \033[1;93m2.\033[1;96m Ver mis tareas                    ║")
        print("║ \033[1;93m3.\033[1;96m Actualizar tarea                  ║")
        print("║ \033[1;93m4.\033[1;96m Eliminar tarea                    ║")
        print("║ \033[1;91m5.\033[1;96m Salir                             ║")
        print("╚══════════════════════════════════════╝\033[0m")

        choice = input("\033[1mSelecciona una opción (1-5): \033[0m")
        if choice == "1":
            limpiar_consola()
            create_task_menu()
        elif choice == "2":
            limpiar_consola()
            tasks = get_tasks_by_user(utils.session.current_user.id)

            print("\033[1;96m╔══════════════════════════════╗")
            print("║        📋 TUS TAREAS         ║")
            print("╚══════════════════════════════╝\033[0m")

            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"\n\033[1;92m✅ Tarea {i}\033[0m")
                    print(f"\033[1;96m• ID:\033[0m {task.id}")
                    print(f"\033[1;96m• Título:\033[0m {task.name}")
                    if task.description:
                        print(f"\033[1;96m• Descripción:\033[0m {task.description}")
                    else:
                        print("\033[1;96m• Descripción:\033[0m (sin descripción)")
                    print(f"\033[1;96m• ¿Está hecha?:\033[0m {'Sí' if task.is_done else 'No'}")
            else:
                print("\033[1;91m❌ No tienes tareas asignadas.\033[0m")

            print("\n\033[1;94m══════════════════════════════\033[0m")
            input("\033[1;90mPulsa ENTER para continuar...\033[0m")
        elif choice == "3":
            limpiar_consola()
            update_task_menu()
        elif choice == "4":
            limpiar_consola()
            delete_task_menu()
        elif choice == "5":
            break
        else:
            print("Opcion no valida")


def create_task_menu():
    limpiar_consola()
    print("\033[1;96m╔═══════════════════════════════╗")
    print("║        ✏️  CREAR TAREA         ║")
    print("╚═══════════════════════════════╝\033[0m")

    if utils.session.current_user.is_admin:
        print("\033[1m(Eres administrador, puedes asignar tareas a otros usuarios)\033[0m")
        print("")
        name = input("\033[1;93m📌 Nombre de la tarea: \033[0m")
        description = input("\033[1;93m📝 Descripción: \033[0m")
        try:
            id = int(input("\033[1;93m👤 ID del usuario asignado: \033[0m"))
        except ValueError:
            print("\033[1;91mID inválido. Debe ser un número entero.\033[0m")
            return
        task = create_task(name, description, id)
    else:
        name = input("\033[1;93m📌 Nombre de la tarea: \033[0m")
        description = input("\033[1;93m📝 Descripción: \033[0m")
        task = create_task(name, description, utils.session.current_user.id)

    print()
    if task:
        print(f"\033[1;92m✅ Tarea creada:\033[0m {task}")
    else:
        print("\033[1;91m❌ No se pudo crear la tarea.\033[0m")
    input("\n\033[1;90mPulsa ENTER para continuar...\033[0m")


def get_all_tasks_menu():
    limpiar_consola()
    print("\033[1;96m╔══════════════════════════════╗")
    print("║       📋 TODAS LAS TAREAS    ║")
    print("╚══════════════════════════════╝\033[0m")

    tasks = get_all_tasks()

    if tasks:
        for i, task in enumerate(tasks, 1):
            print(f"\n\033[1;92m✅ Tarea {i}\033[0m")
            print(f"\033[1;96m• ID:\033[0m {task.id}")
            print(f"\033[1;96m• Título:\033[0m {task.name}")
            if task.description:
                print(f"\033[1;96m• Descripción:\033[0m {task.description}")
            else:
                print("\033[1;96m• Descripción:\033[0m (sin descripción)")
            print(f"\033[1;96m• ¿Está hecha?:\033[0m {'Sí' if task.is_done else 'No'}")
            user = get_user_by_id(task.user_id)
            print(f"\033[1;96m• Usuario:\033[0m {user.username}")
    else:
        print("\033[1;91m❌ No hay ninguna tarea.\033[0m")

        print("\n\033[1;94m══════════════════════════════\033[0m")
        input("\033[1;90mPulsa ENTER para continuar...\033[0m")

    print("\033[1;94m══════════════════════════════════════\033[0m")
    input("\033[1;90mPulsa ENTER para continuar...\033[0m")


def get_task_by_id_menu():
    limpiar_consola()
    print("\033[1;96m╔══════════════════════════════════════╗")
    print("║      🔍 CONSULTAR TAREA POR ID       ║")
    print("╚══════════════════════════════════════╝\033[0m")

    try:
        task_id = int(input("\033[1;93m🔢 Ingrese el ID de la tarea: \033[0m"))
    except ValueError:
        print("\033[1;91m❌ ID inválido. Debe ser un número entero.\033[0m")
        input("\n\033[1;90mPulsa ENTER para continuar...\033[0m")
        return

    task = get_task_by_id(task_id)

    print()
    if task:
        print("\033[1;92m✅ Tarea encontrada:\033[0m")
        print(f"\033[1;96m• ID:\033[0m {task.id}")
        print(f"\033[1;96m• Título:\033[0m {task.name}")
        if task.description:
            print(f"\033[1;96m• Descripción:\033[0m {task.description}")
        else:
            print("\033[1;96m• Descripción:\033[0m (sin descripción)")
        print(f"\033[1;96m• ¿Está hecha?:\033[0m {'Sí' if task.is_done else 'No'}")
    else:
        print("\033[1;91m❌ No se encontró ninguna tarea con ese ID.\033[0m")
    print("\033[1;94m══════════════════════════════════════\033[0m")
    input("\033[1;90mPulsa ENTER para continuar...\033[0m")


def get_tasks_by_user_menu():
    limpiar_consola()
    print("\033[1;96m╔════════════════════════════════════════════╗")
    print("║     👤 CONSULTAR TAREAS POR USUARIO        ║")
    print("╚════════════════════════════════════════════╝\033[0m")

    try:
        user_id = int(input("\033[1;93m🔢 Ingrese el ID del usuario: \033[0m"))
    except ValueError:
        print("\033[1;91m❌ ID inválido. Debe ser un número entero.\033[0m")
        input("\n\033[1;90mPulsa ENTER para continuar...\033[0m")
        return

    tasks = get_tasks_by_user(user_id)

    print()
    if tasks:
        print(f"\033[1;92m✅ Se encontraron {len(tasks)} tarea(s):\033[0m")
        for i, task in enumerate(tasks, 1):
            print(f"\n\033[1;93m📝 Tarea {i}\033[0m")
            print(f"\033[1;96m• ID:\033[0m {task.id}")
            print(f"\033[1;96m• Título:\033[0m {task.name}")
            if task.description:
                print(f"\033[1;96m• Descripción:\033[0m {task.description}")
            else:
                print("\033[1;96m• Descripción:\033[0m (sin descripción)")
            print(f"\033[1;96m• ¿Está hecha?:\033[0m {'Sí' if task.is_done else 'No'}")
    else:
        print("\033[1;91m❌ No se encontraron tareas para este usuario.\033[0m")

    print("\033[1;94m════════════════════════════════════════════\033[0m")
    input("\033[1;90mPulsa ENTER para continuar...\033[0m")


def update_task_menu():
    limpiar_consola()
    print("\033[1;96m╔══════════════════════════════════╗")
    print("║        🔄 ACTUALIZAR TAREA       ║")
    print("╚══════════════════════════════════╝\033[0m")

    try:
        task_id = int(input("\033[1;93m🔢 Ingrese el ID de la tarea a actualizar: \033[0m"))
    except ValueError:
        print("\033[1;91m❌ ID inválido. Debe ser un número entero.\033[0m")
        input("\033[1;90mPulsa ENTER para continuar...\033[0m")
        return

    name = input("\033[1;93m✏️ Nuevo nombre (dejar vacío para no cambiar): \033[0m")
    description = input("\033[1;93m📝 Nueva descripción (dejar vacío para no cambiar): \033[0m")
    is_done_input = input("\033[1;93m✅ ¿Está completada? (s/n): \033[0m").lower()

    if is_done_input == "s":
        is_done = True
    elif is_done_input == "n":
        is_done = False
    else:
        print("\033[1;91m❌ Opción no válida. La tarea no se actualizará.\033[0m")
        input("\033[1;90mPulsa ENTER para continuar...\033[0m")
        return

    task = update_task(task_id, name, description, is_done)

    print()
    if task:
        print("\033[1;92m✅ Tarea actualizada correctamente:\033[0m")
        print(f"\033[1;96m• ID:\033[0m {task.id}")
        print(f"\033[1;96m• Título:\033[0m {task.name}")
        if task.description:
            print(f"\033[1;96m• Descripción:\033[0m {task.description}")
        else:
            print("\033[1;96m• Descripción:\033[0m (sin descripción)")
        print(f"\033[1;96m• ¿Está hecha?:\033[0m {'Sí' if task.is_done else 'No'}")
    else:
        print("\033[1;91m❌ No se encontró ninguna tarea con ese ID.\033[0m")

    print("\033[1;94m══════════════════════════════════\033[0m")
    input("\033[1;90mPulsa ENTER para continuar...\033[0m")


def delete_task_menu():
    limpiar_consola()
    print("\033[1;96m╔════════════════════════════════╗")
    print("║        🗑️  ELIMINAR TAREA       ║")
    print("╚════════════════════════════════╝\033[0m")

    try:
        task_id = int(input("\033[1;93m🔢 Ingrese el ID de la tarea a eliminar: \033[0m"))
    except ValueError:
        print("\033[1;91m❌ ID inválido. Debe ser un número entero.\033[0m")
        input("\033[1;90mPulsa ENTER para continuar...\033[0m")
        return

    confirm = input("\033[1;93m⚠️ ¿Estás seguro de que quieres eliminarla? (s/n): \033[0m").lower()
    if confirm != "s":
        print("\033[1;94mCancelado. La tarea no fue eliminada.\033[0m")
        input("\033[1;90mPulsa ENTER para continuar...\033[0m")
        return

    deleted = delete_task(task_id)

    print()
    if deleted:
        print("\033[1;92m✅ Tarea eliminada correctamente.\033[0m")
    else:
        print("\033[1;91m❌ No se encontró ninguna tarea con ese ID.\033[0m")

    print("\033[1;94m════════════════════════════════\033[0m")
    input("\033[1;90mPulsa ENTER para continuar...\033[0m")


if utils.session.current_user:
    if utils.session.current_user.is_admin:
        display_admin_tasks_menu()
    else:
        display_users_tasks_menu()
