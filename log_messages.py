import mysql.connector


def log_list(connection_config, filter_value='all', date_filter=None):
    '''
    Получаем данные из БД которые отсносятся к сообщениям
    :param connection_config:
    :param filter_value:
    :param date_filter:
    :return:
    '''
    with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
        if filter_value == 'important':
            query = "SELECT * FROM data_for_monitoring_system.logs WHERE severity='high' ORDER BY timestamp DESC LIMIT 3"
        elif date_filter:
            query = f"SELECT * FROM data_for_monitoring_system.logs WHERE DATE(timestamp) = '{date_filter}' ORDER BY timestamp DESC LIMIT 3"
        elif filter_value == 'execution_error':
            query = "SELECT * FROM data_for_monitoring_system.logs WHERE message_type LIKE '%ошибка%' ORDER BY timestamp DESC LIMIT 3"
        else:
            query = "SELECT * FROM data_for_monitoring_system.logs ORDER BY timestamp DESC LIMIT 3"

        cursor.execute(query)
        message_list = cursor.fetchall()

    return message_list
