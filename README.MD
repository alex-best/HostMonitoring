markdown
Копировать код
# IP Availability Monitoring Script

This script pings a list of IP addresses at regular intervals, logs their availability status, and generates a daily report. The report includes a graphical representation of availability and detailed periods of downtime for each IP address. The results are sent to a specified Telegram chat.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `pandas`
  - `matplotlib`
  - `PyMySQL`
  - `python-telegram-bot`
  - `pyyaml`

You can install the required libraries using pip:

```bash
pip install pandas matplotlib pymysql python-telegram-bot pyyaml
Configuration
Create a config.yml file with the following structure:

yaml
Копировать код
config:
  host: "your_database_host"
  port: 3306
  user: "your_username"
  password: "your_password"
  db: "your_database_name"
  telegram_token: "your_telegram_bot_token"
  chat_id: "your_chat_id"
host: The hostname of your MySQL database.
port: The port number of your MySQL database (default is 3306).
user: The username to connect to your MySQL database.
password: The password to connect to your MySQL database.
db: The name of your MySQL database.
telegram_token: The API token of your Telegram bot.
chat_id: The chat ID where the report will be sent.
Database Setup
Ensure you have a MySQL database set up with a table to store the ping results. The table structure should look like this:

sql
Копировать код
CREATE TABLE ping (
    ip VARCHAR(15),
    status INT,
    datetime DATETIME
);
ip: The IP address being pinged.
status: The status of the ping (1 for success, 0 for failure).
datetime: The date and time of the ping.
Usage
Ensure your MySQL database is running and accessible.
Update the config.yml file with your database and Telegram bot details.
Run the script:
bash
Копировать код
python your_script.py
Script Explanation
Functions
get_date()

Returns the current date minus one day.
get_config()

Reads and returns the configuration from config.yml.
get_data()

Connects to the MySQL database and retrieves ping data from the previous day.
create_dataframe(data)

Converts the retrieved data into a pandas DataFrame and adds an hour column.
plot_availability_combined(df)

Generates a combined availability plot for each IP address and saves it as an image.
generate_availability_report(df)

Generates a textual report of the availability of each IP address, including periods of downtime.
send_to_telegram(message)

Sends the generated report and plot image to the specified Telegram chat.
Main Script
The main script fetches the data, creates a DataFrame, generates the availability plot, creates a report, and sends the report and plot to Telegram.

Cron Jobs
It is assumed that the ping script will be run by cron every X minutes, and the report script will also be run by cron at the start of each new day.

Example cron jobs:

cron
Копировать код
# Run the ping script every 10 minutes
*/10 * * * * /usr/bin/python3 /path/to/ping_script.py

# Run the report script at the start of each new day
0 0 * * * /usr/bin/python3 /path/to/report_script.py
Example Output
The report sent to Telegram will look something like this:

yaml
Копировать код
IP 192.168.0.1, доступность 69.8%
Проблемы с доступностью с 2024-07-21 21:28:05 до 2024-07-21 21:31:02
Проблемы с доступностью с 2024-07-21 21:32:04 до 2024-07-21 21:34:02
...
IP 192.168.0.2, доступность 100.0%
IP 192.168.0.3, доступность 100.0%
IP 192.168.0.4, доступность 100.0%
Troubleshooting
If you encounter any issues, ensure that:

Your MySQL database is running and accessible.
The config.yml file is correctly configured.
You have installed all required Python libraries.
If you continue to experience problems, please check the error messages and consult the documentation for the respective libraries.

Скрипт мониторинга доступности IP
Этот скрипт пингует список IP-адресов через регулярные интервалы, логирует их статус доступности и генерирует ежедневный отчет. Отчет включает графическое представление доступности и подробные периоды недоступности для каждого IP-адреса. Результаты отправляются в указанный чат Telegram.

Необходимые условия
Python 3.x
Требуемые библиотеки Python:
pandas
matplotlib
PyMySQL
python-telegram-bot
pyyaml
Вы можете установить необходимые библиотеки с помощью pip:

bash
Копировать код
pip install pandas matplotlib pymysql python-telegram-bot pyyaml
Конфигурация
Создайте файл config.yml со следующей структурой:

yaml
Копировать код
config:
  host: "your_database_host"
  port: 3306
  user: "your_username"
  password: "your_password"
  db: "your_database_name"
  telegram_token: "your_telegram_bot_token"
  chat_id: "your_chat_id"
host: Имя хоста вашей базы данных MySQL.
port: Номер порта вашей базы данных MySQL (по умолчанию 3306).
user: Имя пользователя для подключения к вашей базе данных MySQL.
password: Пароль для подключения к вашей базе данных MySQL.
db: Имя вашей базы данных MySQL.
telegram_token: API токен вашего Telegram-бота.
chat_id: ID чата, куда будет отправлен отчет.
Настройка базы данных
Убедитесь, что у вас есть база данных MySQL с таблицей для хранения результатов пинга. Структура таблицы должна выглядеть так:

sql
Копировать код
CREATE TABLE ping (
    ip VARCHAR(15),
    status INT,
    datetime DATETIME
);
ip: IP-адрес, который пингуется.
status: Статус пинга (1 для успешного, 0 для неудачного).
datetime: Дата и время пинга.
Использование
Убедитесь, что ваша база данных MySQL запущена и доступна.
Обновите файл config.yml с деталями вашей базы данных и Telegram-бота.
Запустите скрипт:
bash
Копировать код
python your_script.py
Объяснение скрипта
Функции
get_date()

Возвращает текущую дату за вычетом одного дня.
get_config()

Читает и возвращает конфигурацию из config.yml.
get_data()

Подключается к базе данных MySQL и извлекает данные о пингах за предыдущий день.
create_dataframe(data)

Преобразует извлеченные данные в DataFrame pandas и добавляет столбец с часами.
plot_availability_combined(df)

Генерирует комбинированный график доступности для каждого IP-адреса и сохраняет его как изображение.
generate_availability_report(df)

Генерирует текстовый отчет о доступности каждого IP-адреса, включая периоды недоступности.
send_to_telegram(message)

Отправляет сгенерированный отчет и изображение графика в указанный чат Telegram.
Основной скрипт
Основной скрипт извлекает данные, создает DataFrame, генерирует график доступности, создает отчет и отправляет отчет и график в Telegram.

Cron Jobs
Предполагается, что скрипт проверки будет запускаться по крону раз в X минут, а скрипт отчета также будет запускаться по крону в начале новых суток.

Примеры cron задач:

cron
Копировать код
# Запуск скрипта проверки каждые 10 минут
*/10 * * * * /usr/bin/python3 /path/to/ping_script.py

# Запуск скрипта отчета в начале каждого нового дня
0 0 * * * /usr/bin/python3 /path/to/report_script.py
Пример вывода
Отчет, отправленный в Telegram, будет выглядеть примерно так:

yaml
Копировать код
IP 192.168.0.1, доступность 69.8%
Проблемы с доступностью с 2024-07-21 21:28:05 до 2024-07-21 21:31:02
Проблемы с доступностью с 2024-07-21 21:32:04 до 2024-07-21 