from ping3 import ping
from yaml import safe_load
import pymysql


def save_data(data, config):
    """ Сохрание данных """
    connection = pymysql.connect(host=config['host'], port=config['port'], 
                         user=config['user'], password=str(config['password']), db=config['db'])
    with connection:
        with connection.cursor() as cursor:
            for host, status in data.items():
                sql = f"INSERT into ping (host, status, datetime) VALUES ('{host}', '{status}', NOW())"
                cursor.execute(sql)        
        connection.commit()


def get_hosts() -> list:
    """ Список хостов для проверки """
    with open('config.yml', 'r') as file:
        return safe_load(file).get('hosts', [])
    
    
def get_config():
    """ Настройки  """
    with open('config.yml', 'r') as file:
        return safe_load(file).get('config', {})
    

def check_ping(hosts):
    """ Проверка хостов """
    data = {}
    for host in hosts:
        if ping(host): data[host] = 1
        else: data[host] = 0
    return data


def main():
    hosts = get_hosts()
    data = check_ping(hosts)
    config = get_config()
    save_data(data, config)


if __name__ == '__main__':
    main()