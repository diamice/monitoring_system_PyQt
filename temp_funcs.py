import mysql.connector
def engine_temperature(connection_config):
    '''
    Получаем температуру для каждого двигателя
    :param connection_config:
    :return:
    '''
    with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
        query = """
            WITH RankedData AS (
              SELECT
                engine_name,
                temperature,
                date_and_time,
                ROW_NUMBER() OVER (PARTITION BY engine_name ORDER BY date_and_time DESC) AS row_num
              FROM
                data_for_monitoring_system.engine_temp
            )
            SELECT
              engine_name,
              temperature,
              date_and_time
            FROM
              RankedData
            WHERE
              row_num = 1;
        """
        cursor.execute(query)
        engine_data = cursor.fetchall()

    return engine_data


def engine_avg_temp(connection_config, date='2023-12-18'):
    '''
    Получаем среднюю температуру для каждого двигателя
    :param connection_config:
    :param date:
    :return:
    '''
    with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
        query = f"""
         SELECT
         engine_name,
         AVG(temperature) AS avg_temperature
         FROM
         data_for_monitoring_system.engine_temp
         WHERE
         DATE(date_and_time) = '{date}'
         GROUP BY
         engine_name;
         """
        cursor.execute(query)
        average_data = cursor.fetchall()

    return average_data