import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from yaml import safe_load
import telebot
def get_date():
    return (datetime.now() - timedelta(1)).date()


def get_config():
    with open('config.yml' , 'r') as file:
        return safe_load(file).get('config', {})


def get_data(config):
    connection = pymysql.connect(host=config['host'], port=config['port'], 
                         user=config['user'], password=str(config['password']), db=config['db'])
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT host, status, datetime FROM ping WHERE datetime >= {get_date()}")        
            result = cursor.fetchall()
        connection.commit()
    return result


def create_dataframe(data):
    df = pd.DataFrame(data, columns=['ip', 'status', 'datetime'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    return df


def make_graph(df):
    # Подсчет доступности по часам
    availability = df.groupby(['ip', 'hour']).apply(lambda x: (x['status'] == 1).mean() * 100).reset_index(name='availability')

    # Определяем уникальные IP-адреса
    unique_ips = df['ip'].unique()
    # fig, axes = plt.subplots(len(unique_ips), 1, figsize=(10, 5 * len(unique_ips)), sharex=True)
    fig, axes = plt.subplots(len(unique_ips), 1, figsize=(10, 10), sharex=True)  # Задание фиксированного размера

    if len(unique_ips) == 1:
        axes = [axes]  # для случая, когда один IP

    # Построение графика для каждого IP
    for ax, ip in zip(axes, unique_ips):
        ip_data = availability[availability['ip'] == ip]
        ax.plot(ip_data['hour'], ip_data['availability'], marker='o', label=ip)
        for i in range(len(ip_data)):
            ax.text(ip_data['hour'].iloc[i], ip_data['availability'].iloc[i], f'{ip_data["availability"].iloc[i]:.1f}', fontsize=9, ha='right')
        ax.set_ylabel('Availability (%)')
        ax.legend()
        ax.grid(True)
        ax.set_xticks(range(24))  # Устанавливаем метки по часам

    plt.tight_layout()
    plt.savefig('./images/availability_plot.png')

def make_graph1(df):
    # Подсчет доступности по часам
    availability = df.groupby(['ip', 'hour']).apply(lambda x: (x['status'] == 1).mean() * 100).reset_index(name='availability')

    # Построение гистограммы для каждого IP
    unique_ips = df['ip'].unique()
    fig, ax = plt.subplots(figsize=(12, 8))

    for ip in unique_ips:
        ip_data = availability[availability['ip'] == ip]
        ax.bar(ip_data['hour'], ip_data['availability'], label=ip, alpha=0.7)

    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Availability (%)')
    ax.set_title('Hourly Availability')
    ax.legend()
    ax.grid(True)
    plt.xticks(range(24))  # Устанавливаем метки по часам
    plt.tight_layout()
    # plt.savefig('/mnt/data/availability_histogram.png')
    plt.savefig('./images/availability_plot.png')

    plt.show()

def send_to_telegram(message):
    config = get_config()
    bot = telebot.TeleBot(config['telegram_token'])
    chat_id = config['chat_id']
    with open('./images/availability_plot.png', 'rb') as f:
        bot.send_photo(chat_id=chat_id, photo=f)
    bot.send_message(chat_id=chat_id, text=message)

def generate_availability_report(df):
    report = []
    unique_ips = df['ip'].unique()
    for ip in unique_ips:
        ip_data = df[df['ip'] == ip].sort_values(by='datetime')
        total_pings = len(ip_data)
        successful_pings = ip_data['status'].sum()
        availability_percentage = (successful_pings / total_pings) * 100
        report.append(f"IP {ip}, доступность {availability_percentage:.1f}%")

        if availability_percentage < 100:
            down_periods = ip_data[ip_data['status'] == 0]['datetime']
            if not down_periods.empty:
                down_start = down_periods.iloc[0]
                down_end = down_periods.iloc[0]
                for current_time in down_periods.iloc[1:]:
                    if (current_time - down_end) > pd.Timedelta(minutes=10):  # Увеличим интервал до 10 минут
                        report.append(f"Проблемы с доступностью с {down_start} до {down_end}")
                        down_start = current_time
                    down_end = current_time
                report.append(f"Проблемы с доступностью с {down_start} до {down_end}")
    
    return "\n".join(report)



def main():
    config = get_config()
    data = get_data(config)
    df = create_dataframe(data)
    make_graph(df)
    report = generate_availability_report(df)
    send_to_telegram(report)
if __name__ == '__main__':
    main()