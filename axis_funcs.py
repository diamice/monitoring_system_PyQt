import mysql.connector


def axis_status_finder(connection_config):
    '''
    Получить из БД статус готовности
    :param connection_config:
    :return:
    '''
    with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
        query = """
            SELECT t1.*
            FROM data_for_monitoring_system.axis_status t1
            JOIN (
                SELECT axis_name, MAX(datetime) AS max_datetime
                FROM data_for_monitoring_system.axis_status
                GROUP BY axis_name
            ) t2 ON t1.axis_name = t2.axis_name AND t1.datetime = t2.max_datetime
            ORDER BY t1.datetime DESC;
        """
        cursor.execute(query)
        axis_list = cursor.fetchall()

    return axis_list
