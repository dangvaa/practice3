import os


# STU-PY-04: Нарушение именования (camelCase вместо snake_case)
# STU-PY-05: Отсутствие docstring (нет документации функции)
def calculateResults(filePath):

    # STU-PY-06: Хардкод абсолютного пути
    archive_path = "C:/Users/Admin/Documents/lab_work/backup"

    # STU-PY-01: Открытие файла без контекстного менеджера 'with'
    f = open(filePath, "r")
    data = f.read()

    # STU-PY-03: Высокая цикломатическая сложность (McCabe)
    if len(data) > 0:
        for line in data.split("\n"):
            if "error" in line:
                if "critical" in line:
                    for char in line:
                        if char.isdigit():
                            if int(char) > 5:
                                print("High priority error found")
                            else:
                                print("Low priority error")
                else:
                    print("General error")

    try:
        result = 100 / len(data)
    except:
        # STU-PY-02: Подавление ошибки (Silent Exception)
        pass

    f.close()
    return True


# Еще одна функция без документации
def Process_Data():
    print("Processing...")
