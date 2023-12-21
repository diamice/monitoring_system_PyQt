import os
import matplotlib.pyplot as plt
import mysql.connector
from config import connection_config


def plot_func(connection_config):
    '''
    Получаем даннные о температуре главного двигателя из БД
    :param connection_config:
    :return:
    '''
    with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
        query = """
            SELECT temperature, date_and_time
            FROM engine_temp
            WHERE engine_name='Главный шпиндель' AND (date_and_time LIKE '%2023-12-19%')
            ORDER BY date_and_time
        """
        cursor.execute(query)
        result = cursor.fetchall()

    return result


result = plot_func(connection_config)
plt.figure(figsize=(10, 6))
temperatures, date_and_time = zip(*result)
plt.plot(date_and_time, temperatures, marker='o', linestyle='-', color='b')
plt.title('Температура Главного шпинделя (2023-12-19)')
plt.xlabel('Дата и время')
plt.ylabel('Температура')
plt.grid(True)

image_folder = 'static/images'
os.makedirs(image_folder, exist_ok=True)

image_path = os.path.join(image_folder, 'temperature_plot.png')
plt.savefig(image_path)
