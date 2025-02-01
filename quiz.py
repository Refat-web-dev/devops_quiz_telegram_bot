from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
import random

LEADERBOARD_FILE = "records.json"

# Функция для загрузки таблицы лидеров из файла
def load_leaderboard():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка загрузки таблицы лидеров: {e}")
    return {}

# Функция для сохранения таблицы лидеров в файл
def save_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(global_leaderboard, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка сохранения таблицы лидеров: {e}")

# Создаем файл, если его нет
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

# Глобальная таблица лидеров загружается из файла
global_leaderboard = load_leaderboard()

# Массив вопросов
sample_questions = [
    {
        "question": "Как расшифровывается LTS?",
        "answers": [
            "a) Long Time Support",
            "b) Long Time Service",
            "c) Long Term Support",
            "d) Linux Term Service",
            "e) Linux Time Support"
        ],
        "correct_answer": "c"
    },
    {
        "question": "Какие убунту являются LTS?",
        "answers": [
            "a) С чётными номерами",
            "b) С нечётными номерами",
            "c) Все",
            "d) Нет таких"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Сколько длится стандартная поддержка Ubuntu?",
        "answers": [
            "a) 1 год",
            "b) 9 месяцев",
            "c) 5-10 лет",
            "d) 3 года",
            "e) 2 года"
        ],
        "correct_answer": "c"
    },
    {
        "question": "Что такое root?",
        "answers": [
            "a) Суперпользователь в UNIX-подобных системах",
            "b) Учетная запись для ограниченных действий",
            "c) Папка, содержащая все файлы системы",
            "d) Пользователь с ограниченными правами"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Как создать суперпользователя при установке и инициализации операционной системы?",
        "answers": [
            "a) С помощью команды useradd",
            "b) Настройкой через sudo",
            "c) Никак, присутствует в системе по умолчанию",
            "d) Настройкой через файл конфигурации"
        ],
        "correct_answer": "c"
    },
    {
        "question": "Кто такие системные пользователи?",
        "answers": [
            "a) Пользователи, управляющие служебными процессами",
            "b) Учетные записи, созданные системой для процессов",
            "c) Обычные пользователи с ограниченными правами",
            "d) Администраторы системы"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Кто такие обычные пользователи?",
        "answers": [
            "a) Администраторы системы",
            "b) Учётные записи пользователей с доступом к служебным процессам",
            "c) Пользователи с ограниченным доступом",
            "d) Учетные записи с правами root"
        ],
        "correct_answer": "b"
    },
    {
        "question": "В чём отличие head от tail?",
        "answers": [
            "a) head читает строки с конца, tail с начала",
            "b) tail читает строки с конца, а head - с начала",
            "c) tail читает весь файл, head только первые строки",
            "d) head читает весь файл, tail только последние строки"
        ],
        "correct_answer": "b"
    },
    {
        "question": "В чём отличие tail от cat?",
        "answers": [
            "a) tail выводит последние n строк, cat выводит весь файл",
            "b) tail читает строки с начала, cat с конца",
            "c) cat выводит последние строки, tail - весь файл",
            "d) tail только записывает, cat только читает"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Как удобно просматривать многостраничный файл?",
        "answers": [
            "a) less",
            "b) more",
            "c) nano",
            "d) head"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Какой командой нельзя попасть в домашнюю директорию?",
        "answers": [
            "a) cd $HOME",
            "b) cd /",
            "c) cd",
            "d) cd ~"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Что такое $?",
        "answers": [
            "a) Переменная, содержащая аргумент предыдущей команды",
            "b) Код возврата последней команды",
            "c) Статус процесса",
            "d) Ничего из вышеперечисленного"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Что такое статус запущенной команды?",
        "answers": [
            "a) Успешное выполнение программы",
            "b) Результат выполнения программы",
            "c) Код возврата команды",
            "d) Время выполнения команды"
        ],
        "correct_answer": "c"
    },
    {
        "question": "Код возврата 0 в bash?",
        "answers": [
            "a) Команда не найдена",
            "b) Ошибка в аргументах",
            "c) В результате выполнения команды возникли ошибки",
            "d) Команда выполнена успешно"
        ],
        "correct_answer": "d"
    },
    {
        "question": "Код возврата 1 в bash?",
        "answers": [
            "a) Команда не найдена",
            "b) Ошибка в аргументах",
            "c) В результате выполнения команды возникли ошибки",
            "d) Команда выполнена успешно"
        ],
        "correct_answer": "c"
    },
    {
        "question": "Какой цифрой обозначается true в bash?",
        "answers": [
            "a) 1",
            "b) 0",
            "c) -1",
            "d) 255"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Docker - это ...?",
        "answers": [
            "a) Инструмент для виртуализации",
            "b) Система контейнеризации",
            "c) Среда разработки",
            "d) Операционная система"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Чем отличается docker от виртуальной машины?",
        "answers": [
            "a) Docker не имеет своего ядра, а виртуальная машина имеет",
            "b) Виртуальная машина виртуализирует аппаратные процессы, а контейнеры - ОС",
            "c) Docker имеет свою операционную систему",
            "d) Ничем не отличаются"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Как посмотреть версию docker?",
        "answers": [
            "a) docker version / docker info",
            "b) docker ls",
            "c) docker status"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Контейнер - это ...?",
        "answers": [
            "a) Запущенный образ docker",
            "b) Образ системы с приложениями",
            "c) Программное обеспечение для виртуализации",
            "d) Полноценная ОС"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Образ - это ... ?",
        "answers": [
            "a) Специальный исполняемый файл, включающий всё необходимое для его запуска",
            "b) Специальный исполняемый файл, содержащий лишь описание самого контейнера",
            "c) Автономный исполняемый пакет части программного обеспечения, включающий всё необходимое для его запуска",
            "d) Программное обеспечение, включающее всё необходимое для запуска"
        ],
        "correct_answer": "c"
    },
    {
        "question": "Что такое Docker Hub?", 
        "answers": [
            "a) Репозиторий для хранения образов с различным программным обеспечением", 
            "b) Сервис для создания контейнеров", 
            "c) Операционная система для работы с Docker", 
            "d) Веб-интерфейс для управления контейнерами"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Dockerfile - это ... ?", 
        "answers": [
            "a) Файл, содержащий инструкции для сборки образа", 
            "b) Конфигурационный файл для контейнера", 
            "c) Сценарий для автоматического развертывания контейнеров", 
            "d) Образ для виртуальной машины"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Что такое docker registry?", 
        "answers": [
            "a) Сервис хранения и распространения образов (Docker Hub является частным случаем registry)", 
            "b) Утилита для управления контейнерами", 
            "c) Система для мониторинга контейнеров", 
            "d) API для интеграции с Docker"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Что такое pipeline?",
        "answers": [
            "a) Последовательность выполнения стадий, каждая из которых включает несколько задач",
            "b) Параллельное выполнение задач",
            "c) Только CI задачи",
            "d) Только CD задачи"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Когда в GitLab запускается пайплайн?", 
        "answers": [
            "a) При любом изменении в удалённом репозитории", 
            "b) Только при изменениях в ветке master", 
            "c) Когда пользователь вручную запускает пайплайн", 
            "d) Когда пайплайн запускается по расписанию"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Напишите этапы CI:", 
        "answers": [
            "a) build, test", 
            "b) deploy, test", 
            "c) build, deploy", 
            "d) test, publish"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Напишите этапы CD:", 
        "answers": [
            "a) deploy staging, deploy production, publish, update configs", 
            "b) test, build, deploy", 
            "c) build, deploy staging", 
            "d) deploy production, rollback"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Что такое GitLab Runner? Это сервис, который...",
        "answers": [
            "a) Выполняет инструкции из .gitlab-ci.yml по заданному таймеру",
            "b) Выполняет функции агента для GitLab, в котором этот агент запущен",
            "c) Запускает bash-скрипт",
            "d) Уведомляет пользователя, чтобы он запустил .gitlab-ci.yml"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Какая команда в GitLab CI сохраняет файлы на 10 дней?", 
        "answers": [
            "a) expire_in: 10 days", 
            "b) save_for: 10 days", 
            "c) keep_files: 10 days", 
            "d) store_for: 10 days"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "Как определить успешность этапа пайплайна CI/CD?",
        "answers": [
            "a) Никак",
            "b) По кодам возврата инструкций из команды script",
            "c) Уведомление в среде запуска инструкций из команды script",
            "d) Всплывающее уведомление в GitLab"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Что такое Kernel?",
        "answers": [
            "a) Имя одного из системных приложений",
            "b) Ядро ОС",
            "c) Графическая оболочка в некоторых дистрибутивах Linux",
            "d) Часть ОС для работы с файловой системой"
        ],
        "correct_answer": "b"
    },
    {
        "question": "Что означает \"user is not in the sudoers file\"?",
        "answers": [
            "a) Ошибка при написании команды добавления пользователя в файл sudoers",
            "b) Данному пользователю не прописано разрешение на выполнение команды sudo в файле /etc/sudoers",
            "c) Ошибка указывает на невозможность добавления пользователя в файл sudoers",
            "d) Пользователь не имеет право на использование sudo"
        ],
        "correct_answer": "b"
    },
    {"question": "Какую комбинацию короткой формы записи нужно использовать для предоставления всех прав для владельца и группы, и прав на чтение и выполнение для остальных?", 
     "answers": ["a) 770", "b) 775", "c) 777", "d) 755"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи нужно использовать для предоставления только прав на чтение для всех?", 
     "answers": ["a) 444", "b) 777", "c) 555", "d) 666"], "correct_answer": "a"},

    {"question": "Какая комбинация короткой формы записи позволяет только владельцу читать и записывать, а группе и остальным — только читать?", 
     "answers": ["a) 644", "b) 777", "c) 755", "d) 444"], "correct_answer": "a"},

    {"question": "Какую комбинацию короткой формы записи следует использовать, чтобы предоставить владельцу права на чтение, запись и исполнение, а группе и остальным — только на чтение?", 
     "answers": ["a) 644", "b) 711", "c) 755", "d) 744"], "correct_answer": "d"},

    {"question": "Какая комбинация короткой формы записи предоставляет все права для владельца и группы, но без прав для остальных?", 
     "answers": ["a) 700", "b) 770", "c) 777", "d) 600"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи нужно использовать для предоставления владельцу всех прав только?", 
     "answers": ["a) 777", "b) 700", "c) 755", "d) 444"], "correct_answer": "b"},

    {"question": "Какая комбинация короткой формы записи позволяет владельцу и группе читать и записывать, а остальным — только читать?", 
     "answers": ["a) 755", "b) 664", "c) 444", "d) 777"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи следует использовать, чтобы предоставить всем права на чтение и исполнение, а владельцу — на запись?", 
     "answers": ["a) 644", "b) 775", "c) 744", "d) 777"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи следует использовать, чтобы предоставить права на чтение и запись владельцу, группе и остальным?", 
     "answers": ["a) 777", "b) 664", "c) 744", "d) 755"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи следует использовать для предоставления прав на чтение, запись и исполнение владельцу, а группе и остальным — только прав на чтение?", 
     "answers": ["a) 744", "b) 775", "c) 777", "d) 444"], "correct_answer": "a"},

    {"question": "Какая комбинация короткой формы записи позволяет владельцу и группе читать и записывать, а остальным — только читать?", 
     "answers": ["a) 755", "b) 644", "c) 777", "d) 774"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи нужно использовать для предоставления владельцу всех прав, группе — прав на чтение и исполнение, а остальным — только прав на исполнение?", 
     "answers": ["a) 711", "b) 751", "c) 777", "d) 700"], "correct_answer": "a"},

    {"question": "Какая комбинация короткой формы записи даёт все права владельцу, но только права на чтение для группы и остальных?", 
     "answers": ["a) 744", "b) 755", "c) 777", "d) 644"], "correct_answer": "a"},

    {"question": "Какая комбинация короткой формы записи позволяет владельцу читать, записывать и выполнять, а группе — только читать и выполнять?", 
     "answers": ["a) 711", "b) 755", "c) 775", "d) 777"], "correct_answer": "b"},

    {"question": "Какая комбинация короткой формы записи позволяет владельцу и группе читать и записывать, а остальным — только читать?", 
     "answers": ["a) 775", "b) 664", "c) 666", "d) 444"], "correct_answer": "b"},

    {"question": "Какую комбинацию короткой формы записи следует использовать, чтобы предоставить владельцу права на чтение, запись и исполнение, группе — только на исполнение, остальным — только на чтение?", 
     "answers": ["a) 714", "b) 744", "c) 775", "d) 777"], "correct_answer": "a"},

    {"question": "Какую комбинацию короткой формы записи нужно использовать для предоставления владельцу всех прав, группе — прав на чтение и выполнение, а остальным — только прав на исполнение?", 
     "answers": ["a) 711", "b) 755", "c) 777", "d) 700"], "correct_answer": "a"},

    {"question": "Какая комбинация короткой формы записи позволяет владельцу и группе читать и записывать, а остальным — только читать?", 
     "answers": ["a) 755", "b) 644", "c) 777", "d) 774"], "correct_answer": "b"},

    {"question": "Какая комбинация короткой формы записи предоставляет все права владельцу, группе и остальным?", 
     "answers": ["a) 777", "b) 666", "c) 775", "d) 755"], "correct_answer": "a"},

    {"question": "Какая комбинация короткой формы записи позволяет владельцу читать, записывать и выполнять, а группе и остальным — только читать?", 
     "answers": ["a) 744", "b) 755", "c) 777", "d) 444"], "correct_answer": "a"},
    {
        "question": "Какой командой меняются права доступа каталога и его содержимого?",
        "answers": [
            "a) chmod -R",
            "b) chmod -all",
            "c) chmod -r",
            "d) chown -R"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Как выйти без сохранения из текстового редактора vi?",
        "answers": [
            "a) :leave",
            "b) :e",
            "c) :q!",
            "d) :exit"
        ],
        "correct_answer": "c"
    },
    {
        "question": "За что отвечает протокол NTP?", 
        "answers": [
            "a) За синхронизацию времени компьютера", 
            "b) За передачу данных между компьютерами", 
            "c) За настройку сетевых интерфейсов", 
            "d) За защиту от вирусов и атак"
        ], 
        "correct_answer": "a"
    },
    {
        "question": "В чём отличие ncdu от du?",
        "answers": [
            "a) ncdu имеет UI",
            "b) Ничем, одинаковая команда",
            "c) Запуск ncdu возможен только через root"
        ],
        "correct_answer": "a"
    },
    {
        "question": "Может ли код возврата в bash быть отрицательным?",
        "answers": [
            "a) Да",
            "b) Нет"
        ],
        "correct_answer": "b"
    },
    {
        "question": "В чём отличие #!/bin/bash от #!/bin/sh?",
        "answers": [
            "a) bash — это более новая и функциональная версия sh",
            "b) sh — это оболочка для выполнения bash-скриптов",
            "c) bash — устаревшая версия sh",
            "d) sh — всегда ссылается на интерпретатор bash"
        ],
        "correct_answer": "a"
    },
    {"question": "Какой параметр в Bash позволяет узнать, существует ли файл и является ли он файлом?", "answers": ["a) -d", "b) -s", "c) -f", "d) -t"], "correct_answer": "c"},
    {"question": "Что произойдёт, если после вызова read не указать переменную? Результат ввода сохранится в:", "answers": ["a) ANSWER", "b) RESULT", "c) QUESTION", "d) REPLY"], "correct_answer": "d"},
    {"question": "Как перенаправить stdout из одной команды в stdin другой?", "answers": ["a) cmd1 <> cmd2", "b) cmd1 2 > cmd2", "c) cmd1 < cmd2", "d) cmd1 | cmd2"], "correct_answer": "d"},
    {"question": "Что делает команда sed -e '1s/Aobba/Aboba/;3,$s/Abboa/Aboba/' myfile?", "answers": ["a) Заменяет Aobba на Aboba в первой строке и Abboa на Aboba с третьей строки до конца", "b) Заменяет все строки файла на Aboba", "c) Удаляет строки с текстом Abboa", "d) Выводит первые три строки файла"], "correct_answer": "a"},
    {"question": "Какой командой вывести 5 последних строк файла?", "answers": ["a) cat file --lines=5", "b) head file lines=5", "c) tail --lines=5 file / tail file --lines=5"], "correct_answer": "c"},
    {"question": "Что неверно в команде touch file1 | cp file1 /tmp/?", "answers": ["a) Неправильный символ |", "b) Отсутствует ключ -r у команды cp", "c) Отсутствует ключ -c у команды touch", "d) Лишний / в пути клонирования"], "correct_answer": "a"},
    {"question": "Какой формат конфигов используется в Dockerfile?", "answers": ["a) Текстовый", "b) YAML", "c) JSON", "d) Config"], "correct_answer": "a"},
    {"question": "Что делает команда docker inspect? Отображает информацию о:", "answers": ["a) Контейнере", "b) Выполненных процессах", "c) Использованных ресурсах", "d) Сети Docker"], "correct_answer": "a"},
    {"question": "Чем отличается docker create от docker run?", "answers": ["a) docker create запускает контейнер без создания, а docker run только создаёт", "b) docker create создаёт контейнер, а docker run - создаёт и запускает", "c) docker create удаляет старый контейнер, а docker run перезаписывает", "d) docker create создаёт образ, а docker run запускает образ"], "correct_answer": "b"},
    {"question": "Как создать образ после изменения в контейнере?", "answers": ["a) docker attach nginx", "b) docker push nginx", "c) docker image prune", "d) docker commit nginx"], "correct_answer": "d"},
    {"question": "Как войти внутрь контейнера?", "answers": ["a) docker attach test1", "b) docker exec -it test1 bash", "c) docker login test1", "d) docker connect test1"], "correct_answer": "b"},
    {"question": "Как посмотреть список всех контейнеров?", "answers": ["a) docker ps", "b) docker ps -a", "c) docker ls -a", "d) docker run"], "correct_answer": "b"},
    {"question": "Как посмотреть список образов?", "answers": ["a) docker images", "b) docker ps", "c) docker run", "d) docker view"], "correct_answer": "a"},
    {"question": "Какой командой можно посмотреть логи контейнера test1?", "answers": ["a) docker logs test1", "b) docker test1logs", "c) dockerlogs test1", "d) docker status test1"], "correct_answer": "a"},
    {"question": "Как правильно написать условие запуска этапа needs в gitlab-ci.yml?", "answers": ["a) needs: \"название этапа\"", "b) needs: [\"название этапа\"]", "c) needs: название этапа", "d) needs: {\"название этапа\"}"], "correct_answer": "b"},
    {"question": "Где можно использовать переменную $CI_JOB_STATUS в GitLab CI?", "answers": ["a) before_script", "b) after_script", "c) artifacts", "d) script"], "correct_answer": "b"},
    {"question": "Как в gitlab-ci.yml указать, что этап будет запущен вручную?", "answers": ["a) needs: - manual", "b) build: - manual", "c) rules: - manual", "d) rules: - when: manual"], "correct_answer": "d"},
    {"question": "Как указать образ для выполнения стадии в GitLab CI?", "answers": ["a) image: image_name", "b) image - image_name", "c) image(container_name)", "d) container: container_name"], "correct_answer": "a"},
    {"question": "Какие executor'ы не бывают у gitlab-runner'а?", 
     "answers": ["a) docker", "b) shell", "c) gitlab-executor", "d) ssh", "e) parallelis", "f) VirtualBox"], 
     "correct_answer": "c"},
    {"question": "За что отвечает SSH?", "answers": ["a) Передача информации", "b) Управление компьютером и TCP-туннелирование", "c) UDP или TCP соединение"], "correct_answer": "b"},
    {"question": "Что в combined log означает поле {user-agent}?", "answers": ["a) Браузер пользователя", "b) ОС пользователя", "c) IP-адрес пользователя", "d) URL, с которого перешел пользователь"], "correct_answer": "a"},
    {"question": "При помощи какой команды можно скопировать файл внутрь образа при написании файла dockerfile?", "answers": ["a) FROM", "b) WORKDIR", "c) COPY", "d) AND"], "correct_answer": "c"},
    {"question": "Что такое демоны?", "answers": ["a) Демоны - это программы, созданные пользователем по имени Демон (Daemon)", "b) Демоны - это собирательное название всех процессов и приложений, использующих Linux", "c) Демон - это завершённый процесс, чей родительский процесс не смог получить об этом информацию", "d) Демон - это работающая в фоновом режиме служебная программа или процесс"], "correct_answer": "d"},
    {"question": "Как удалить контейнер с именем nginx?", "answers": ["a) docker -d nginx", "b) docker rm --name nginx", "c) docker rmi nginx", "d) docker rm nginx"], "correct_answer": "d"},
    {"question": "Номер порта для https (по умолчанию)", "answers": ["a) 443", "b) 80", "c) 22", "d) 5000"], "correct_answer": "a"},
    {"question": "Что выведет на экран следующий скрипт:\n#!/bin/bash\nfunction myfunc {\nlocal temp=$[$value + 5]\necho “$temp”\n}\ntemp=4\nmyfunc\necho $((temp))", "answers": ["a) 5\n4", "b) 5", "c) $9", "d) ошибка"], "correct_answer": "a"},
    {"question": "Как вызвать /usr/bin/script.sh из под root по cron каждый месяц?", "answers": ["a) 0 0 1 * *", "b) * * */12 * *", "c) * * */0 * *", "d) * * 0 * *"], "correct_answer": "a"},
    {"question": "Сколько сервисов могут одновременно использовать один сетевой порт?", "answers": ["a) несколько поочередно", "b) до 3-х приложений одновременно", "c) один порт - одно приложение", "d) неограниченное количество"], "correct_answer": "c"},
    {"question": "Какой параметр в bash позволяет узнать, пустой ли файл?", "answers": ["a) -l", "b) -f", "c) -s", "d) -d"], "correct_answer": "c"},
    {"question": "Какой командой docker можно получить список запущенных контейнеров?", "answers": ["a) docker ps", "b) docker ls -a", "c) docker events", "d) docker ps -a"], "correct_answer": "a"},
    {"question": "Какой командой можно открыть второй терминал?", "answers": ["a) Alt+Ctrl+T", "b) Alt+Ctrl+F2", "c) Alt+T", "d) Alt+F2"], "correct_answer": "a"},
    {"question": "Какая команда выдаёт список всех директорий, находящихся в текущем?", "answers": ["a) ls -R", "b) ls", "c) ps -R", "d) ls -r"], "correct_answer": "a"},
    {"question": "Редактор по умолчанию?", "answers": ["a) vim", "b) vi", "c) mcedit", "d) nano"], "correct_answer": "b"},
    {"question": "Выбрать вариант, который является комментарием", "answers": ["a) echo “Это #комментарий?”", "b) echo ‘Это #комментарий?`", "c) echo Это \#комментарий?", "d) echo Это #комментарий?"], "correct_answer": "d"},
    {"question": "Можно ли в Ubuntu 20.04.3 LTS работать от пользователя root?", "answers": ["a) Можно, по умолчанию", "b) Нужно добавить root при установке", "c) В LTS версиях нельзя работать от пользователя root", "d) Можно, но не по умолчанию, а при помощи вызова su или sudo"], "correct_answer": "d"},
    {"question": "Какой командой изменяются права доступа на файл?", "answers": ["a) chown", "b) mode", "c) chmod", "d) chfile"], "correct_answer": "c"},
    {"question": "Что выведется в результате выполнения\nif [ 4 –gt 5 ]; then echo “0”; else echo “1”; fi?", "answers": ["a) command not found", "b) 4 –gt 5", "c) 0", "d) 1"], "correct_answer": "d"},
    {"question": "Для чего необходимо придерживаться минимального количества вызовов RUN внутри образа?", "answers": ["a) Чтобы не увеличивать объём образа, так как каждый RUN создаёт слой, который требует памяти", "b) Чтобы не увеличивать время запуска контейнера, так как каждый RUN работает последовательно", "c) Для каждого RUN нужен свой dockerfile", "d) Для каждого контейнера есть ограничение на количество RUN"], "correct_answer": "a"},
    {"question": "В чём значение слоёв в образе?", "answers": ["a) Каждый слой описывает, как будет запущено и работать какое-либо приложение", "b) Новый слой – это новые данные, не связанные с предыдущими слоями", "c) Каждый слой описывает какое-то изменение, которое должно быть выполнено с данными на запущенном контейнере", "d) В контейнере каждое приложение устанавливается на слой"], "correct_answer": "c"},
    {"question": "За что отвечает \"%{Referer}i\" в combined Log Format?", "answers": ["a) IP-адрес пользователя", "b) URL, с которого перешел пользователь", "c) Провайдер пользователя", "d) Браузер пользователя"], "correct_answer": "b"},
    {"question": "Каким выражением можно посчитать всех пользователей в системе?", "answers": ["a) cat /etc/passwd | wc -l", "b) cat /etc/passwd wc -l", "c) ls /etc/passwd wc -l", "d) cat /etc/passwd | wc -c"], "correct_answer": "a"},
    {"question": "Что сделает команда du –sh /root/?", "answers": ["a) Выведет общий размер каталога /root/ в человекочитаемом виде", "b) Выведет количество файлов в каталоге /root/", "c) Выведет только список файлов в каталоге /root/", "d) Выведет доступный диск на каталоге /root/"], "correct_answer": "a"},
    {"question": "Какая команда НЕ создаёт папки с именем sus1, sus2, sus3?", "answers": ["a) mkdir sus{1-3}", "b) mkdir sus{1..3}", "c) mkdir sus{1, 2, 3}", "d) mkdir sus[1, 2, 3]"], "correct_answer": "a"},
    {"question": "Как удалённо зайти на компьютер student под ником aboba по SSH?", "answers": ["a) ssh aboba@student", "b) ssh student@aboba", "c) ssh root@aboba", "d) ssh aboba@root"], "correct_answer": "a"},
    {"question": "Как вызвать cron каждые 4 часа?", "answers": ["a) * */4 * * *", "b) 4 * * * *", "c) * 4 * * *", "d) */240 * * * *"], "correct_answer": "a"},
    {"question": "Что выведет скрипт\n\nwhile true; false;\n    echo “success”", "answers": ["a) Success", "b) Бесконечный success", "c) Ничего", "d) 0"], "correct_answer": "c"},
    {"question": "За что отвечает главный поток nginx?", "answers": ["a) Только за управление рабочими процессами", "b) Чтение, проверка конфигураций и управление рабочими процессами", "c) Старт, прерывание и поддержка сконфигурированного количества worker-процессов, также создание, связывание и закрытие сокетов", "d) Все вышеописанное"], "correct_answer": "d"},
    {"question": "Что НЕ является текстовым редактором?", "answers": ["a) nano", "b) vim", "c) mcedit", "d) cat"], "correct_answer": "d"},
    {"question": "Что такое /var/log/auth.log?", "answers": ["a) Журнал логов, который включает удачные и неудачные попытки авторизации пользователей", "b) Журнал логов, который включает только удачные попытки авторизации пользователей", "c) Журнал логов, который включает только неудачные попытки авторизации пользователей", "d) Журнал логов, который включает информацию об авторизованных пользователях в текущий момент"], "correct_answer": "a"},
    {"question": "Что такое Grafana?", "answers": ["a) Инструмент визуализации данных", "b) Графическая оболочка для Ubuntu", "c) Инструмент мониторинга систем", "d) Инструмент для работы с базами данных"], "correct_answer": "a"},
    {"question": "Какая команда в bash позволяет узнать, существует файл и является ли он директорией?", "answers": ["a) -l", "b) -d", "c) -s", "d) -f"], "correct_answer": "b"},
    {"question": "Какие из следующих являются уровнями модели OSI?", 
     "answers": ["a) Физический, Сетевой, Сеансовый, Транспортный, Представления, Прикладной", 
                 "b) Виртуальный, Сетевой, Технический, Сеансовый, Представления", 
                 "c) Сетевой, Транспортный, Физический, Виртуальный, Представления", 
                 "d) Технический, Прикладной, Сеансовый, Сетевой, Физический"], 
     "correct_answer": "a"},
    {"question": "Вывести построчно в цикле for var in $(cat $file)", "answers": ["a) IFS=$’/n’", "b) IFS=$’//n’", "c) IFS=$’\\n’", "d) IFS=$’ln’"], "correct_answer": "c"},
    {"question": "Как удалить все правила из iptables?", "answers": ["a) iptables -F", "b) iptables -L", "c) iptables -X", "d) iptables -R"], "correct_answer": "a"},
    {"question": "Как посмотреть данные по сетевому интерфейсу?", "answers": ["a) tcpdump -i eth0 / tcpdump --interface eth0", "b) tcpdump eth0", "c) tcpdump -l eth0"], "correct_answer": "a"},
    {"question": "Как удалить Docker-образ?", "answers": ["a) docker images rm nginx", "b) docker rmi nginx", "c) docker rm –i nginx", "d) docker rm nginx"], "correct_answer": "b"},
    {"question": "Какое правило iptables отключает приём всех пакетов?", "answers": ["a) iptables -policy INPUT DROP", "b) iptables -policy FORWARD REJECT", "c) iptables -policy POSTROUTING REJECT", "d) iptables -policy POSTROUTING DROP"], "correct_answer": "a"},
    {"question": "Какой способ авторизации ssh является наиболее безопасным?", "answers": ["a) по паролю", "b) по хэш-функции", "c) по ключу", "d) по ответу на секретный вопрос"], "correct_answer": "c"},
    {"question": "Что такое процесс виртуализации?", "answers": ["a) процесс создания программной (виртуальной) версии машины, используя гипервизор", "b) процесс создания программной (виртуальной) версии машины с выделенными ресурсами ЦП, памяти и хранилища, которые заимствуются у физической машины", "c) процесс создания программной (виртуальной) версии машины, разделяющий при этом ресурсы ЦП, памяти и хранилища, которые заимствуются у физической машины", "d) процесс создания программной (виртуальной) версии машины с выделенными ресурсами ЦП, памяти и хранилища, использующий при этом ресурсы ядра ОС"], "correct_answer": "c"},
    {"question": "Какая команда в top отвечает за переключение режима отображения информации о памяти?", "answers": ["a) s", "b) m", "c) n", "d) d"], "correct_answer": "b"},
    {"question": "Что такое pipe?", "answers": ["a) перенаправление стандартного вывода одной команды на стандартный ввод другой команды, но не как аргумент", "b) перенаправление стандартного вывода в файл", "c) перенаправление стандартного вывода в /dev/null", "d) создание однонаправленного канала данных, который можно использовать для взаимодействия между процессами"], "correct_answer": "a"},
    {"question": "Что делает mydir=$(pwd)?", "answers": ["a) переменная mydir копирует работу команды pwd", "b) сохраняет вывод команды pwd в переменную mydir", "c) сохраняет вывод команды pwd в файл mydir", "d) создаёт директорию mydir по пути pwd"], "correct_answer": "b"},
    {"question": "Что делает docker update?", "answers": ["a) обновление контейнера", "b) список контейнеров, которые можно обновить до новой версии программы", "c) запуск остановленного контейнера", "d) первый запуск контейнера"], "correct_answer": "a"},
    {"question": "Основные части архитектуры docker - это …", "answers": ["a) сервис Docker, образы, контейнеры, Docker Registry", "b) сервис Docker, образы, контейнеры, Docker Registry, DockerHub", "c) сервис Docker, образы, контейнеры, Docker Cloud", "d) сервис Docker, Dockerfile, контейнеры, Docker Registry, DockerHub"], "correct_answer": "b"},
    {"question": "Жизненный цикл контейнера", "answers": ["a) создание контейнера, запуск контейнера, работа контейнера, остановка контейнера, возобновление работы контейнера, перезапуск контейнера, приостановка работы контейнера, удаление контейнера", "b) создание контейнера, работа контейнера, остановка контейнера", "c) создание контейнера, запуск контейнера, работа контейнера", "d) создание контейнера, запуск контейнера, удаление контейнера"], "correct_answer": "a"},
    {"question": "Какой параметр нужно применить, чтобы использовать ngx_http_stub_status_module?", "answers": ["a) ngx_http_stub_status_module", "b) http_stub_status_module", "c) --with-http_stub_status_module", "d) --with-ngx_http_stub_status_module"], "correct_answer": "c"},
    {"question": "Как передать параметры из gitlab-ci в bash-скрипт?", "answers": ["a) script: extends CI_PROJECT_NAME", "b) script: (export CI_PROJECT_NAME)", "c) script: export CI_PROJECT_NAME", "d) script: -export .gitlab-ci.yml"], "correct_answer": "b"},
    {"question": "Что выведет скрипт\n#!/bin/bash\ncount=1\ncat ${!#} | while read wrd\ndo\ncount=$(($count+1))\ndone\necho “$count”\nесли будет вызван так: ./script.sh file1 file! File3?", "answers": ["a) количество строк в файле file1", "b) количество строк в file!", "c) количество строк в File3", "d) ошибку"], "correct_answer": "d"},
    {"question": "Как выглядит цикл, вывод из которого направлен в файл?", "answers": ["a) echo $var1\nwhile [var1 -gt 0]\nvar1=$[$var1-1]\ndone > myfile.txt", "b) while [var1 -gt 0]\ndo\necho $var1\nvar1=$[$myfile.txt]\ndo > myfile.txt", "c) while [var1 -gt 0]\ndo\necho $var1\nvar1=$[$var1-1]\ndone > myfile.txt", "d) while [var1 -gt 0]\ndo > myfile.txt\necho $var1\nvar1=$[$var1-1]"], "correct_answer": "c"},
    {"question": "Как в cron вызвать выполнение задачи каждые 2 дня в полдень?", "answers": ["a) 0 12 */2 * * script.sh", "b) 0 12 1/2 * * script.sh", "c) 0 12 2 * * script.sh", "d) 0 12 1-2 * * script.sh"], "correct_answer": "a"},
    {"question": "Какую информацию выводит команда ls -la?", "answers": ["a) права доступа, количество жёстких ссылок, имя владельца, имя группы, размер файла, дата и время последней модификации, имя файла или директории", "b) список всех файлов и директорий с расширенной информацией", "c) права доступа, количество файлов и владельца", "d) подробную информацию только о скрытых файлах"], "correct_answer": "a"},
    {"question": "Для чего нужен ключ -s в команде du -sh?", "answers": ["a) отобразить размер каталога в единицах измерения удобных для человека", "b) отобразить общий размер всех папок в конце вывода", "c) отобразить только суммарный размер каталога, включая всё его содержимое", "d) исключить размер под каталогов в подсчёте суммарного размера каталога"], "correct_answer": "c"},
    {"question": "Как вызвать скрипт по cron’у, который будет выполняться каждый понедельник?", "answers": ["a) * * * * */1", "b) 0 0 * * MON", "c) 0 0 7 * *", "d) 0 0 1 * MON"], "correct_answer": "b"},
    {"question": "Что делает команда sudo rm -rf /*?", "answers": ["a) удаляет всё из директории, в которой находится пользователь", "b) уничтожает все данные с корневого раздела диска", "c) удаляет все файлы из директории, в которой находится пользователь", "d) ничего, такой команды нет"], "correct_answer": "b"},
    {"question": "Вывод какой команды будет отличаться от трёх оставшихся?", "answers": ["a) ls dir1; ls dir2; ls dir3", "b) ls {dir1,dir2,dir3}", "c) ls dir{1,2,3}", "d) ls dir1 dir2 dir3"], "correct_answer": "a"},
    {"question": "Как перенаправить вывод одной команды в поток STDERR?", "answers": ["a) echo “text” > &2", "b) echo “text” >> &2", "c) echo “text” > !2", "d) echo “text” > $2"], "correct_answer": "a"},
    {"question": "Найди ошибку в скрипте\n\nfor ((var1=1; var1<15; var1++))\ndo\nif [$var1 -gt 5] && [$var1 -lt 10]\nthen\ncontinue\nfi\necho “value: $var1”\ndone", "answers": ["a) ошибка в if", "b) ошибка в параметрах цикла for", "c) ошибка в for", "d) ошибок нет"], "correct_answer": "a"},
    {"question": "Какая из предложенных команд копирует только файлы из /sus в /amongus?", "answers": ["a) cp /sus /amongus", "b) cp /sus/* /amongus", "c) cp -f /sus/ /amongus", "d) cp /sus/~ /amongus"], "correct_answer": "b"},
    {"question": "Что означает буква D в названиях, например, sshd?", "answers": ["a) процесс, работающий как сервис (демон)", "b) процесс, имеющий состояние disable", "c) процесс, запущенный системным пользователем", "d) процесс, унаследованный от процесса родителя"], "correct_answer": "a"},
    {"question": "Как расшифровывается du?", "answers": ["a) disk usage", "b) disk user", "c) disk used", "d) disk update"], "correct_answer": "a"},
    {"question": "Для чего нужен FROM в Dockerfile?", "answers": [
        "a) задаёт базовый (родительский) образ", 
        "b) создаёт точку монтирования для работы с постоянным хранилищем", 
        "c) указывает рабочую директорию", 
        "d) выполняет команду и создаёт слой образа"], "correct_answer": "a"
    },
    {"question": "Для чего нужен dockle?", "answers": [
        "a) это инструмент для проверки безопасности образов контейнеров, используемый для поиска уязвимостей", 
        "b) это инструмент для мониторинга процессов в контейнерах", 
        "c) это инструмент для деплоя контейнеров в продакшн", 
        "d) это инструмент для автоматической генерации Dockerfile"], "correct_answer": "a"
    },
    {"question": "Какая команда загружает образ в репозиторий?", "answers": [
        "a) docker pull", 
        "b) docker push", 
        "c) docker commit", 
        "d) docker save"], "correct_answer": "b"
    },
    {"question": "В чём разница между RUN и CMD в Dockerfile?", "answers": [
        "a) RUN выполняются только один раз во время сборки и создают новый слой в итоговом docker-образе; CMD позволяет определить команду по умолчанию, инструкция не выполняется во время сборки", 
        "b) RUN выполняются только один раз во время сборки и создают новый слой в итоговом docker-образе; CMD позволяет определить команду по умолчанию, инструкция выполняется после сборки", 
        "c) RUN выполняются только один раз во время сборки и каждый раз при запуске контейнера; CMD позволяет определить команду по умолчанию, инструкция не выполняется во время сборки", 
        "d) RUN выполняются только один раз во время сборки и каждый раз при запуске контейнера; CMD позволяет определить команду по умолчанию, инструкция выполняется до сборки"], "correct_answer": "a"
    },
    {"question": "В чём разница между registry и repository?", "answers": [
        "a) registry - сервис хранения и распространения образов, repository - набор связанных образов; имеют одно и то же имя, но разные метки", 
        "b) registry - сервис хранения и распространения образов, repository - набор связанных образов; имеют одинаковые метки", 
        "c) registry - локальный сервис хранения и распространения образов, repository - набор связанных образов; имеют одно и то же имя, но разные метки", 
        "d) registry - сервис хранения и распространения образов, который может использоваться на сторонних серверах, repository - локальный registry"], "correct_answer": "a"
    },
    {"question": "Какой командой узнать текущую версию Ubuntu?", "answers": [
        "a) lsb_release -a", 
        "b) ubuntu_version", 
        "c) uname -v", 
        "d) version_check"], "correct_answer": "a"
    },
    {"question": "Может ли код возврата быть дробным числом?", "answers": [
        "a) Да", 
        "b) Нет"], "correct_answer": "b"
    },
    {"question": "Какой кодовый статус у команды «команда не найдена»?", "answers": [
        "a) 0", 
        "b) 2", 
        "c) 126", 
        "d) 127"], "correct_answer": "d"
    },
    {"question": "Что означает переменная $# ?", "answers": [
        "a) Даёт статус выхода последней команды", 
        "b) Даёт PID шелла", 
        "c) Даёт число позиционных параметров в десятичном формате", 
        "d) Параметры, заданные с помощью встроенной команды Set"], "correct_answer": "c"
    },
    {"question": "При помощи какой команды можно осуществить замену содержимого файла по маске?", "answers": [
        "a) pwd", 
        "b) grep", 
        "c) replace", 
        "d) sed"], "correct_answer": "d"
    },
    {"question": "Что такое var/log/dmesg?", "answers": [
        "a) Директория, содержащая журналы с различными сообщениями, полученными от пользователей", 
        "b) Директория, содержащая журналы с различными сообщениями, полученными от системы", 
        "c) Системный журнал, содержащий различные сообщения, полученные от демонов", 
        "d) Системный журнал, содержащий различные сообщения, полученные от ядра"], "correct_answer": "d"
    },
    {"question": "Что такое var/log/syslog?", "answers": [
        "a) Глобальный системный журнал, куда записываются сообщения только о системных ошибках", 
        "b) Глобальный системный журнал, куда записываются сообщения от ядра, различных служб, сетевых интерфейсов и т.д.", 
        "c) Глобальный системный журнал, куда записываются сообщения о выбранных событиях в системе", 
        "d) Глобальный системный журнал, куда записываются сообщения запущенных демонов"], "correct_answer": "b"
    },
    {"question": "Как вывести последние 15 строк файла?", "answers": [
        "a) tail -last15 text.txt", 
        "b) tail -t15 text.txt", 
        "c) tail -s15 text.txt", 
        "d) tail -n15 text.txt"], "correct_answer": "d"
    },
    {"question": "Как вызвать в cron скрипт, который будет выполняться каждый час?", "answers": [
        "a) * 0 * * * script.sh", 
        "b) * 60 * * * script.sh", 
        "c) * */60 * * * script.sh", 
        "d) 0 * * * * script.sh"], "correct_answer": "d"
    },
    {
    "question": "Что выведет следующий код:\n\ntrue\necho $",
    "answers": [
        "a) true",
        "b) 0",
        "c) 1",
        "d) $"
    ],
    "correct_answer": "d"
    },
    {"question": "Чем отличаются > и >> ?", "answers": [
        "a) > перезатрёт предыдущее содержимое файла, если оно было, а >> добавит к нему дополнительно", 
        "b) > добавит новое содержимое в файл, а >> создаст новый файл", 
        "c) > создает резервную копию, а >> добавляет строки в файл", 
        "d) > игнорирует все ошибки, а >> выполняет замену"], "correct_answer": "a"
    },
    {"question": "Чему равна маска подсети в адресе 172.10.8.160/24?", "answers": ["a) 255.255.255.0", "b) 172.10.8.255", "c) 255.255.0.0", "d) 255.255.255.255"], "correct_answer": "a"},
    {"question": "Номер порта ssh по умолчанию?", "answers": ["a) 22", "b) 443", "c) 80", "d) 50000"], "correct_answer": "a"},
    {"question": "На каком порту работает Grafana?", "answers": ["a) 3000", "b) 8000", "c) 443", "d) 8080"], "correct_answer": "a"},
    {"question": "В чём разница «>» и «>>»?", "answers": ["a) Оператор сравнения и перенаправление вывода", "b) Разницы нет", "c) Оператор логического И", "d) Перенаправление ввода и вывод"], "correct_answer": "a"},
    {"question": "Что НЕ показывает команда top?", "answers": ["a) Использование ресурсов процессора", "b) Процессы", "c) Использование ресурсов сетевого трафика", "d) Использование оперативной памяти"], "correct_answer": "c"},
    {"question": "Какие параметры можно мониторить в операционной системе?", "answers": ["a) CPU", "b) Место занимаемое на диске", "c) Статус системы", "d) Доступ к веб-сайту"], "correct_answer": "a"},
    {"question": "По какому протоколу работает служба SSHd по умолчанию?", "answers": ["a) TCP", "b) UDP", "c) ICMP", "d) ARP"], "correct_answer": "a"},
    {"question": "Позволяет ли правило –A RM-Firewall-i-INPUT –p udp –m udp –dport 80 –j ACCEPT обратиться к веб-серверу по 80-му порту?", "answers": ["a) да, так как разрешён порт 80 по UDP", "b) нет, так как разрешён порт 80 по UDP", "c) да, так как разрешён порт 80 по TCP", "d) нет, так как порт 80 не разрешён"], "correct_answer": "b"},
    {"question": "Что за директория «/»?", "answers": ["a) Корень файловой системы", "b) Домашний каталог суперюзера", "c) Виртуальный каталог", "d) Точка монтирования"], "correct_answer": "a"},
    {"question": "Как сохранить в редакторе vi?", "answers": ["a) :w", "b) :s", "c) :save", "d) :write"], "correct_answer": "a"},
    {"question": "Что такое localhost?", "answers": ["a) 192.168.0.255/24", "b) 127.0.0.1/8", "c) 192.0.1.0/24", "d) 127.0.0.1/24"], "correct_answer": "b"},
    {"question": "Укажите динамический порт", "answers": ["a) 80", "b) 443", "c) 8080", "d) 50000"], "correct_answer": "d"},
    {"question": "Что такое SNAT?", "answers": ["a) Изменения адреса и порта назначения пакета в цепочке PREROUTING и OUTPUT", "b) Изменения адреса и порта назначения пакета в цепочке POSTROUTING", "c) Используется для установки битов в поле Type of Service IP заголовка", "d) Предоставляется возможность журналирования текстов в пользовательское пространство"], "correct_answer": "b"},
    {"question": "Какой командой создаётся user?", "answers": ["a) добавить в файл sudoers", "b) использовать команду adduser / useradd", "c) добавить в файл /etc/passwd"], "correct_answer": "b"},
    {"question": "Чему равен адрес сети 128.0.1.1/8?", "answers": ["a) 127.0.0.1", "b) 128.0.0.1", "c) 128.0.1.0", "d) 128.0.0.0"], "correct_answer": "d"},
    {"question": "Что такое dhcp?", "answers": ["a) Протокол прикладного уровня, разрешающий использование статического IP-адреса клиенту в локальной сети", "b) Это стандартный протокол, который позволяет пользователям получать доступ к веб-сайтам, используя удобочитаемые адреса", "c) Это технология сегментации локальной сети на более мелкие виртуальные локальные сети со своими широковещательными доменами", "d) Протокол прикладного уровня, используемый для автоматического назначения динамического IP-адреса клиенту в локальной сети"], "correct_answer": "d"},
    {"question": "Iptables -A INPUT -s 10.3.10.10/24 -j DROP разрешён ли доступ с IP 10.3.10.10?", "answers": ["a) да, так как запрещена сеть 10.3.10.3/24", "b) нет, так как запрещена сеть 10.3.10.0/24", "c) да, так как разрешен доступ с IP 10.3.10.10", "d) нет, так как запрещен доступ с любого IP"], "correct_answer": "b"},
    {"question": "Что будет выведено на экран при выполнении следующих команд?\n\nfalse\necho $", 
     "answers": ["a) 1", "b) true", "c) $", "d) 0"], 
     "correct_answer": "c"},
    {"question": "Как посмотреть всех пользователей системы?", "answers": ["a) cat /etc/passwd", "b) users", "c) who", "d) id"], "correct_answer": "a"},
    {"question": "С каким ключом нужно запустить команду df для отображения информации в человекочитаемом виде?", "answers": ["a) -h", "b) -l", "c) -a", "d) -s"], "correct_answer": "a"},
    {"question": "Сколько портов доступно в системе?", "answers": ["a) 65 535", "b) 1024", "c) 49151", "d) 65536"], "correct_answer": "a"},
    {"question": "Как загрузить образ?", "answers": ["a) docker load", "b) docker image load", "c) оба варианта верны", "d) docker import"], "correct_answer": "c"},
    {"question": "Чему равен адрес сети 10.0.0.20/28?", "answers": ["a) 10.0.0.1", "b) 10.0.0.8", "c) 10.0.0.16", "d) 10.0.0.32"], "correct_answer": "c"},
    {"question": "Как выглядит маска 255.255.255.0 в префиксной записи?", "answers": ["a) /24", "b) /16", "c) /32", "d) 127.0.0.0"], "correct_answer": "a"},
    {"question": "Какая утилита nmap или ping позволяет точно определить наличие хоста в сети?", "answers": ["a) nmap", "b) ping", "c) ping & nmap", "d) netstat"], "correct_answer": "a"},
    {"question": "За что отвечает четвёртый бит в IPv4?", "answers": ["a) Сеть", "b) Подсеть", "c) Хост", "d) Маска"], "correct_answer": "c"},
    {"question": "Что означает chmod +x?", "answers": ["a) Права на исполнение", "b) Права на удаление", "c) Права на чтение", "d) Права на запись"], "correct_answer": "a"},
    {"question": "Что дает ключ -l команде ls?", "answers": ["a) Выводит дополнительную информацию", "b) Выводит список символьных ссылок", "c) Сортирует файлы", "d) Показывает только директории"], "correct_answer": "a"},
    {"question": "Что такое ICMP?", "answers": ["a) Протокол, который используется для передачи сообщений об ошибках и других исключительных ситуациях, возникших при передаче данных", "b) Протокол, который используется для динамического назначения IP адреса", "c) Протокол для безопасной передачи данных", "d) Протокол для передачи видео и аудио данных"], "correct_answer": "a"},
    {"question": "Для чего используется цепочка FORWARD в iptables?", "answers": ["a) Переадресация пакетов", "b) Маршрутизация пакетов", "c) Защита от DDoS атак", "d) Фильтрация трафика"], "correct_answer": "a"},
    {"question": "Что из перечисленного localhost?", "answers": ["a) 127.255.255.1", "b) 1.1.1.1", "c) 255.0.0.1", "d) 192.168.0.1"], "correct_answer": "a"},
    {"question": "Системные порты", "answers": ["a) 0 - 1023", "b) 1024 - 49151", "c) 49152 - 65535", "d) 0 - 65535"], "correct_answer": "a"},
    {"question": "Сколько хостов в подсети /28?", "answers": ["a) 14", "b) 16", "c) 30", "d) 62"], "correct_answer": "a"},
    {"question": "Какой параметр в конфигурации iptables используется для указания цепочки, к которой применяется правило?", "answers": ["a) -D", "b) -C", "c) -j", "d) -A"], "correct_answer": "d"},
    {"question": "Какой параметр в конфигурации iptables используется для указания действия, которое должно быть выполнено, если пакет соответствует правилу?", "answers": ["a) -D", "b) -C", "c) -A", "d) -j"], "correct_answer": "d"},
    {"question": "Какой параметр Docker команды run используется для монтирования тома или директории хоста в контейнер?", "answers": ["a) -e", "b) -v", "c) -w", "d) -m"], "correct_answer": "b"},
    {"question": "Какой из следующих команд Docker используется для создания нового образа контейнера из запущенного контейнера?", "answers": ["a) docker commit", "b) docker save", "c) docker build", "d) docker export"], "correct_answer": "a"},
    {"question": "Какой параметр команды docker run используется для задания лимита по использованию памяти контейнером?", "answers": ["a) --cpus", "b) --limit-mem", "c) --mem-limit", "d) --memory"], "correct_answer": "d"},
    {"question": "Какой параметр в Docker Compose используется для указания зависимости одного сервиса от другого?", "answers": ["a) networks", "b) links", "c) volumes", "d) depends_on"], "correct_answer": "d"},
    {"question": "Какой командой Docker можно перезапустить все остановленные контейнеры?", "answers": ["a) docker run", "b) docker start", "c) docker restart", "d) docker up"], "correct_answer": "b"},
    {"question": "Какой параметр команды docker run используется для публикации порта контейнера на хосте?", 
     "answers": ["a) -P", "b) --port", "c) --expose", "d) -p"], 
     "correct_answer": "d"},
    
    {"question": "Какой формат файлов используется для описания конфигурации контейнеров и их сервисов в Docker Compose?", 
     "answers": ["a) YAML", "b) JSON", "c) XML", "d) INI"], 
     "correct_answer": "a"},
    
    {"question": "Какой командой можно запустить контейнер с определенным именем?", 
     "answers": ["a) docker run --name", "b) docker launch --name", "c) docker start --name", "d) docker create --name"], 
     "correct_answer": "a"},
    
    {"question": "Какой файл используется для описания процесса сборки Docker образа?", 
     "answers": ["a) Dockerfile.json", "b) buildfile", "c) Dockerfile", "d) docker-compose.yml"], 
     "correct_answer": "c"},
    
    {"question": "Какой из следующих ключевых слов в Dockerfile используется для указания базового образа, на котором будет основан создаваемый образ?", 
     "answers": ["a) FROM", "b) BASE", "c) START", "d) IMAGE"], 
     "correct_answer": "a"},
    
    {"question": "Какое ключевое слово в Dockerfile используется для копирования файлов и директорий с хоста в образ?", 
     "answers": ["a) IMPORT", "b) ADD", "c) MOVE", "d) COPY"], 
     "correct_answer": "d"},
    
    {"question": "Какое ключевое слово в Dockerfile используется для выполнения команд в контейнере во время сборки образа?", 
     "answers": ["a) RUN", "b) EXEC", "c) CMD", "d) SHELL"], 
     "correct_answer": "a"},
    
    {"question": "Какое ключевое слово в Dockerfile задает команду, которая будет выполнена при запуске контейнера?", 
     "answers": ["a) STARTCMD", "b) INIT", "c) ENTRYPOINT", "d) BEGIN"], 
     "correct_answer": "c"},
    
    {"question": "Какой файл используется для описания мультиконтейнерных Docker приложений?", 
     "answers": ["a) multi-docker.yml", "b) docker-compose.yml", "c) Docker.config", "d) Dockerfile"], 
     "correct_answer": "b"},
    
    {"question": "Какое ключевое слово в Dockerfile задает рабочую директорию для следующей команды?", 
     "answers": ["a) CHDIR", "b) SETDIR", "c) DIRECTORY", "d) WORKDIR"], 
     "correct_answer": "d"},
    
    {"question": "Какое ключевое слово в Dockerfile используется для установки переменных окружения?", 
     "answers": ["a) VAR", "b) SETENV", "c) EXPORT", "d) ENV"], 
     "correct_answer": "d"},
    
    {"question": "Какое ключевое слово в Dockerfile используется для объявления, что контейнер будет слушать на определенных сетевых портах?", 
     "answers": ["a) EXPOSE", "b) PORT", "c) LISTEN", "d) NETWORK"], 
     "correct_answer": "a"},
    
    {"question": "Какое ключевое слово в Dockerfile используется для добавления метаданных к образу в виде ключ-значение пар?", 
     "answers": ["a) LABEL", "b) META", "c) TAG", "d) INFO"], 
     "correct_answer": "a"},
    
    {"question": "Какой тип сети по умолчанию создается при запуске Docker контейнера без указания опций сети?", 
     "answers": ["a) overlay", "b) none", "c) host", "d) bridge"], 
     "correct_answer": "d"},
    
    {"question": "Какой драйвер сети Docker используется для создания сети, в которой контейнеры могут общаться между собой напрямую, используя сеть хоста?", 
     "answers": ["a) none", "b) host", "c) bridge", "d) macvlan"], 
     "correct_answer": "b"},
    
    {"question": "Какой драйвер сети Docker используется для отключения всех сетевых подключений контейнера?", 
     "answers": ["a) bridge", "b) host", "c) none", "d) macvlan"], 
     "correct_answer": "c"},
    
    {"question": "Какой командой Docker можно создать новую пользовательскую сеть типа bridge?", 
     "answers": ["a) docker network init bridge", "b) docker network create --driver bridge", "c) docker network new bridge", "d) docker network build bridge"], 
     "correct_answer": "b"},
    
    {"question": "Какой параметр команды docker run используется для подключения контейнера к определенной сети?", 
     "answers": ["a) --connect", "b) --link", "c) --network", "d) --net"], 
     "correct_answer": "c"},
    
    {"question": "Какой тип сети Docker позволяет контейнерам разных хостов общаться между собой, предоставляя распределенную сеть?", 
     "answers": ["a) bridge", "b) host", "c) overlay", "d) macvlan"], 
     "correct_answer": "c"},
    
    {"question": "Какой командой Docker можно подключить уже запущенный контейнер к существующей сети?", 
     "answers": ["a) docker network attach", "b) docker network link", "c) docker network connect", "d) docker network join"], 
     "correct_answer": "c"},
    
    {"question": "Какое из следующих утверждений о сети типа macvlan в Docker является верным?", 
     "answers": ["a) Контейнеры получают собственные МАС-адреса и работают как полноценные устройства в сети.", 
                 "b) Контейнеры используют сеть хоста напрямую, без изоляции.", 
                 "c) Контейнеры полностью изолированы от сетевых подключений.", 
                 "d) Контейнеры могут общаться только внутри одного и того же Docker хоста."], 
     "correct_answer": "a"},
    
    {"question": "Какой драйвер сети Docker используется для создания сети, где контейнеры могут общаться друг с другом и с внешними сетями через виртуальный маршрутизатор?", 
     "answers": ["a) macvlan", "b) host", "c) bridge", "d) overlay"], 
     "correct_answer": "d"},
    
    {"question": "Какой командой Docker можно удалить существующую сеть?", 
     "answers": ["a) docker network rm", "b) docker network destroy", "c) docker network delete", "d) docker network remove"], 
     "correct_answer": "a"},
    
    {"question": "Какой файл используется для определения многоконтейнерного приложения в Docker-Compose?", 
     "answers": ["a) docker-compose.yml", "b) compose.yaml", "c) docker-compose.json", "d) Dockerfile"], 
     "correct_answer": "a"},
      {"question": "Какая команда Docker-Compose используется для создания и запуска всех служб, определенных в файле docker-compose.yml?", 
     "answers": ["a) docker-compose up", "b) docker-compose run", "c) docker-compose start", "d) docker-compose build"], 
     "correct_answer": "a"},
    
    {"question": "Какое ключевое слово в файле docker-compose.yml используется для указания образа, который будет использоваться для создания контейнера?", 
     "answers": ["a) image", "b) container", "c) build", "d) service"], 
     "correct_answer": "a"},
    
    {"question": "Какой параметр можно использовать в docker-compose.yml для определения зависимости одного сервиса от другого?", 
     "answers": ["a) depends_on", "b) needs", "c) links", "d) requires"], 
     "correct_answer": "a"},
    
    {"question": "Какая команда Docker-Compose используется для остановки и удаления всех контейнеров, сетей и томов, созданных с помощью команды docker-compose up?", 
     "answers": ["a) docker-compose remove", "b) docker-compose stop", "c) docker-compose destroy", "d) docker-compose down"], 
     "correct_answer": "d"},
    
    {"question": "Какое ключевое слово в файле docker-compose.yml используется для указания переменных окружения для сервиса?", 
     "answers": ["a) variables", "b) env", "c) env_vars", "d) environment"], 
     "correct_answer": "d"},
    
    {"question": "Какой параметр в docker-compose.yml используется для указания монтирования томов?", 
     "answers": ["a) binds", "b) volumes", "c) storage", "d) mounts"], 
     "correct_answer": "b"},
    
    {"question": "Какой параметр в docker-compose.yml используется для указания портов, которые должны быть опубликованы на хосте?", 
     "answers": ["a) publish", "b) expose", "c) ports", "d) forward"], 
     "correct_answer": "c"},
    
    {"question": "Какая команда Docker-Compose используется для просмотра логов всех служб, определенных в docker-compose.yml?", 
     "answers": ["a) docker-compose view", "b) docker-compose logs", "c) docker-compose show", "d) docker-compose display"], 
     "correct_answer": "b"},
    
    {"question": "Чем отличается CMD от ENTRYPOINT в DockerFile?", 
     "answers": ["a) CMD задает команду по умолчанию, которая может быть переопределена при запуске контейнера. ENTRYPOINT определяет неизменяемую команду, которая всегда будет выполняться. CMD обычно используется для указания параметров для ENTRYPOINT.", 
                 "b) CMD и ENTRYPOINT выполняют одно и то же, с той разницей, что CMD всегда можно изменить.", 
                 "c) CMD используется для запуска дополнительных программ внутри контейнера, а ENTRYPOINT — для конфигурации контейнера.", 
                 "d) CMD задает имя контейнера, а ENTRYPOINT — его тип."], 
     "correct_answer": "a"},
    
    {"question": "Чем отличается COPY от ADD?", 
     "answers": ["a) COPY копирует файлы из локальной системы в контейнер. ADD может извлекать архивы и загружать данные по URL.", 
                 "b) COPY извлекает архивы, а ADD только копирует файлы.", 
                 "c) COPY может работать с URL, а ADD только с файлами.", 
                 "d) COPY и ADD выполняют одинаковую задачу, разница только в синтаксисе."], 
     "correct_answer": "a"},
    
    {"question": "Какой из следующих команд Docker CLI используется для отображения журналов (логов) для контейнера?", 
     "answers": ["a) docker status", "b) docker report", "c) docker view", "d) docker logs"], 
     "correct_answer": "d"},
    
    {"question": "В чём разница между контейнеризацией и виртуализацией?", 
     "answers": ["a) Контейнеризация использует контейнеры для изоляции приложений и их зависимостей на уровне операционной системы, что делает контейнеры более лёгкими по сравнению с виртуальными машинами. Виртуализация создает полноценные виртуальные машины с собственными ОС поверх гипервизора, что требует больше ресурсов.", 
                 "b) Контейнеры и виртуальные машины одинаковы, разница только в цене.", 
                 "c) Контейнеризация использует виртуальные машины, а виртуализация работает с контейнерами.", 
                 "d) Контейнеризация требует больше ресурсов, чем виртуализация, и наоборот."], 
     "correct_answer": "a"}    
]

# Состояния квиза
active_quizzes = {}  # {chat_id: {"remaining_questions": [...], "scores": {user_id: score}}}

# Начать квиз
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in active_quizzes:
        await update.message.reply_text("Квиз уже идет! Подождите его завершения.")
        return

    # Инициализация квиза
    random.shuffle(sample_questions)  # Перемешиваем список вопросов
    active_quizzes[chat_id] = {"remaining_questions": sample_questions.copy(), "scores": {}}
    await send_question(update, context)

# Отправить вопрос
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    quiz = active_quizzes.get(chat_id)
    if not quiz:
        await update.message.reply_text("Квиз не запущен. Используйте /quiz, чтобы начать.")
        return

    if not quiz["remaining_questions"]:
        await end_quiz(update, context)  # Завершаем квиз, если вопросы закончились
        return

    # Берем первый вопрос из перемешанного списка
    question_data = quiz["remaining_questions"][0]
    question_text = f"Вопрос: {question_data['question']}\n\n" + "\n".join(question_data["answers"])
    await update.message.reply_text(question_text)

# Обработать ответ
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "Участник"
    quiz = active_quizzes.get(chat_id)

    if not quiz:
        return  # Игнорируем, если квиз не идет

    answer = update.message.text.lower().strip()
    if answer not in ["a", "b", "c", "d", "e"]:
        return  # Игнорируем сообщения не из набора [a, b, c, d, e]

    # Проверяем правильность ответа
    question_data = quiz["remaining_questions"].pop(0)  # Убираем вопрос после обработки
    if answer == question_data["correct_answer"]:
        quiz["scores"][user_id] = quiz["scores"].get(user_id, 0) + 1
        await update.message.reply_text(f"Правильно, {username}! 🎉")
    else:
        await update.message.reply_text(f"Неправильно, {username}. Правильный ответ: {question_data['correct_answer']}")

    # Переходим к следующему вопросу или заканчиваем квиз
    if quiz["remaining_questions"]:
        await send_question(update, context)
    else:
        await end_quiz(update, context)

# Завершить квиз
async def end_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global global_leaderboard
    chat_id = update.effective_chat.id
    quiz = active_quizzes.pop(chat_id, None)

    if not quiz:
        await update.message.reply_text("Квиз уже завершен.")
        return

    # Обновляем глобальную таблицу лидеров
    for user_id, score in quiz["scores"].items():
        user_id = str(user_id)  # Приводим user_id к строке для совместимости
        username = "Хазрат" if user_id == "1415003296" else (await update.effective_chat.get_member(int(user_id))).user.first_name
        if user_id in global_leaderboard:
            global_leaderboard[user_id]["score"] += score
        else:
            global_leaderboard[user_id] = {"username": username, "score": score}

    # Сохраняем обновленную таблицу лидеров
    save_leaderboard()

    # Выводим таблицу лидеров квиза
    scores = quiz["scores"]
    if scores:
        leaderboard = "\n".join(
            [
                f"{'Хазрат' if user_id == '1415003296' else (await update.effective_chat.get_member(int(user_id))).user.first_name}: {score}"
                for user_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)
            ]
        )
        await update.message.reply_text(f"Квиз завершен! 🎉\nТаблица лидеров для этого квиза:\n\n{leaderboard}")
    else:
        await update.message.reply_text("Никто не ответил на вопросы. 😔")

# Показать таблицу лидеров
async def show_records(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not global_leaderboard:
        await update.message.reply_text("Таблица лидеров пока пуста.")
        return

    leaderboard = "\n".join(
        [
            f"{'Хазрат' if user_id == '1415003296' else record['username']}: {record['score']}"
            for user_id, record in sorted(global_leaderboard.items(), key=lambda x: x[1]['score'], reverse=True)
        ]
    )
    await update.message.reply_text(f"Текущая таблица лидеров:\n\n{leaderboard}")


# Команда для завершения квиза вручную
async def stop_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in active_quizzes:
        await update.message.reply_text("Квиз не активен.")
        return

    # Завершаем квиз
    await end_quiz(update, context)
    await update.message.reply_text("Квиз завершен по вашему запросу.")

# Показать таблицу лидеров
async def show_records(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not global_leaderboard:
        await update.message.reply_text("Таблица лидеров пока пуста.")
        return

    leaderboard = "\n".join(
        [
            f"{record['username']}: {record['score']}"
            for record in sorted(global_leaderboard.values(), key=lambda x: x['score'], reverse=True)
        ]
    )
    await update.message.reply_text(f"Текущая таблица лидеров:\n\n{leaderboard}")

# Основной код
def main():
    application = Application.builder().token("7696889634:AAFvquRqGjd9mdY7EgU5QrSJQXpNvGMwTHQ").build()

    # Регистрируем команды
    application.add_handler(CommandHandler("quiz", start_quiz))
    application.add_handler(CommandHandler("stop", stop_quiz))
    application.add_handler(CommandHandler("records", show_records))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
