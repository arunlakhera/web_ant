import logging
import pymongo
import pymysql


class NeuronDb:
    """
    Class for Database operations in MySQL ,MongoDB Amazon S3
    """

    ############ MySQL SECTION ############
    def connect_mysql(self, host, username, password):

        """
        :param host:  MySQL host link
        :param username:  username to connect to MySQL
        :param password: password to connect to MySQL
        :return: sqlconnection & sqlcursor
        """

        try:
            sql_connection = pymysql.connect(host=host, user=username, password=password)
            sql_cursor = sql_connection.cursor()

            logging.info("Connected to MySQL Database...")

            return sql_connection, sql_cursor
        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while connecting to MySQL: Check Host/Username/Password"
            logging.info(err_msg)

    def create_mysql_db(self, sql_cursor, db_name):

        """
        :param sql_cursor: Takes sqlcurosr as input
        :return:
        """

        try:
            # Create Database
            sql_createdb = f"CREATE DATABASE IF NOT EXISTS {db_name}"
            sql_cursor.execute(sql_createdb)
            sql_cursor.connection.commit()
            msg = f"Created Database...{db_name}"
            logging.info(msg)

            # Use Database created
            sql_usedb = f"USE {db_name}"
            sql_cursor.execute(sql_usedb)

            msg = f"Using Database...{db_name}"
            logging.info(msg)
        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while creating Database: iNeuronDb"
            logging.info(err_msg)

    def create_mysql_table(self, sql_cursor, table_name):
        """

        :param sql_cursor: Takes sqlcursor as input
        :param table_name: Takes table_name for table to create
        :return: Creates table in the database
        """
        try:
            # Create Table
            sql_create_tab = f"CREATE TABLE IF NOT EXISTS {table_name} ( course_id VARCHAR(100) NOT NULL, course_name TEXT, course_description TEXT, PRIMARY KEY (course_id))"
            sql_cursor.execute(sql_create_tab)
            msg = f"Created Table...{table_name}"
            logging.info(msg)

        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while creating Table: {table_name}"
            logging.info(err_msg)

    def insert_mysql_data(self, sql_conn, sql_cursor, table_name, courses_data):
        """

        :param sql_conn: Takes sql_conn as input
        :param sql_cursor: Takes sql_cursor as input
        :param courses_data: Takes courses_data to be insrted into the table
        :return: Inserts data into the table
        """
        try:
            total_data = f'Total data to Insert: {len(courses_data)}'
            logging.info(total_data)

            # Insert Data into Table
            for course in courses_data:
                c_id = course['course_id']
                c_name = course['course_name']
                c_desc = course['course_description']

                data = (c_id, c_name, c_desc)
                sql_insert = (f"""INSERT IGNORE INTO {table_name}(course_id, course_name, course_description) VALUES(%s, %s, %s)""")
                sql_cursor.execute(sql_insert, data)

            sql_conn.commit()

            sql_count = f'''SELECT COUNT(*) FROM {table_name}'''
            total_inserted = sql_cursor.execute(sql_count)
            total_data_inserted = f'Total data Inserted in Table: {total_inserted}'
            logging.info(total_data_inserted)

        except Exception as e:
            sql_conn.rollback()
            logging.error(e)
            err_msg = f"Error occurred while Inserting Data in Table"
            logging.info(err_msg)

    def close_mysql(self, sql_connection):
        """
        :param sql_connection: Takes sql_connection as input
        :return: Closes the MySQL Connection
        """
        try:
            # Close MySQL Connection
            sql_connection.close()
            logging.info("MySQL Connection...Closed")
        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while closing MySQL Connection."
            logging.info(err_msg)

    ############ MONGO DB SECTION ############

    def connect_mongo(self, mongo_client):
        """

        :param mongo_client: Takes client link as input
        :return: creates connection and returns connection
        """

        try:
            # MongoDB Connection
            client = pymongo.MongoClient(mongo_client)
            logging.info("MongoDB Connection...Done")

            return client

        except Exception as e:
            logging.error(e)
            err_msg = f"MongoDB Connection....Error"
            logging.info(err_msg)

    def create_mongo_db(self, mongodb_client, mongodb_name):
        """

        :param mongodb_client: Takes mongodb client
        :param mongodb_name: Takes mongodb name
        :return: returns the database name
        """
        try:
            # Create mongodb database
            mongo_db = mongodb_client[mongodb_name]
            logging.info("MongoDB Database...Done")

            return mongo_db

        except Exception as e:
            logging.error(e)
            err_msg = f"Creating MongoDB Database....Error"
            logging.info(err_msg)

    def create_mongo_coll(self, mongodb_db, coll_name):
        """
        :param mongodb_db: Takes mongodb database
        :param coll_name: Takes collection name
        :return: Creates and returns collection
        """
        try:
            # Create mongodb collection
            mongodb_coll = mongodb_db[coll_name]

            msg= f"MongoDB Collection {coll_name} ...Created"
            logging.info(msg)

            return mongodb_coll

        except Exception as e:
            logging.error(e)
            err_msg = f"MongoDB Collection {coll_name}....Failed"
            logging.info(err_msg)

    def mongo_insert(self, coll_name, data):
        """

        :param coll_name: Takes collection name
        :param data: Takes data to be inserted into collection
        :return: Inserts data into mongo db collection
        """
        try:
            # Insert data into collection
            coll_name.insert_many(data)

            logging.info("MongoDB Data Insert ...Done")

        except Exception as e:
            logging.error(e)
            err_msg = f"MongoDB Data Insert...Failed"
            logging.info(err_msg)


