import logging
from fpdf import FPDF
import boto3
import pymongo
import pymysql


def save_to_s3(filename):
    """
    :param filename: takes filename of file to store in s3
    :return:
    """
    # Create an S3 access object
    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            Filename=filename,
            Bucket="arunpdf",
            Key="course.pdf",
        )
    except Exception as e:
        logging.error(e)


def save_to_pdf(user_sel_course):
    """
    Function to convert data to PDF
    :param user_sel_course:
    :return: status of pdf in bool
    """
    try:
        for course in user_sel_course:
            course_id = course['course_id']
            course_name = course['course_name']
            course_description = course['course_description']
            course_mode = str(course['course_mode'])
            course_curriculum = str(course['course_curriculum'])
            course_requirements = str(course['course_requirements'])
            course_features = str(course['course_features'])
            instructor_name = str(course['instructor_name'])
            instructors_social = str(course['instructors_social'])
            instructor_description = str(course['instructor_description'])
        # variable for pdf
        pdf = FPDF('L')

        # Add a page
        pdf.add_page()

        # setting style and font
        pdf.set_font("Arial", size=10)

        # create a cell
        pdf.cell(200, 10, txt=course_name, ln=1, align='C')

        pdf.cell(200, 10, txt=f"Course ID: {course_id}", ln=2, align='L')
        pdf.multi_cell(200, 10, txt=f"Description: {course_description}", align='L')
        pdf.multi_cell(200, 10, txt=f"Mode: {course_mode}", align='L')
        pdf.multi_cell(200, 10, txt=f"Curriculum: {course_curriculum}", align='L')
        pdf.multi_cell(200, 10, txt=f"Requirements: {course_requirements}", align='L')
        pdf.multi_cell(200, 10, txt=f"Features: {course_features}", align='L')
        pdf.multi_cell(200, 10, txt=f"Instructor Name: {instructor_name}", align='L')
        pdf.multi_cell(200, 10, txt=f"Instructors Social: {instructors_social}", align='L')
        pdf.multi_cell(200, 10, txt=f"Instructor Description: {instructor_description}", align='L')

        # file_name = f"{user_sel_course[0]['course_id']}.pdf"
        file_name = "course.pdf"

        # Save pdf file
        pdf.output(file_name)

        # save to s3
        save_to_s3(file_name)

    except Exception as e:
        logging.error(e)


def save_to_mongodb(cat_subcat_data, courses_data):

    try:
        logging.info("Connecting to Mongo Database...")
        client = pymongo.MongoClient("mongodb+srv://ineuron:pwdineuron@cluster0.eltt8.mongodb.net/?retryWrites=true&w=majority")
        database = client['ineuron']
        logging.info("..Done")

        logging.info("Saving to Mongo Database...")
        cat_subcat_coll = database['cat_subcat']
        courses_coll = database['courses']

        cat_subcat_coll.insert_many(cat_subcat_data)
        courses_coll.insert_many(courses_data)

        logging.info("...Done")
    except Exception as e:
        logging.error(e)


def save_to_mysql(courses_data):

    try:
        logging.info("Connecting to MySQL Database...")

        sql_conn = pymysql.connect(host="ineurondb.cckavecit4n5.ap-northeast-1.rds.amazonaws.com", user="ineuron",
                                password="pwdineuron")
        sql_cursor = sql_conn.cursor()

        logging.info("..Done")


        logging.info("Creating Database...")

        sql_createdb = '''CREATE DATABASE IF NOT EXISTS iNeuronDb'''
        sql_cursor.execute(sql_createdb)
        sql_cursor.connection.commit()

        logging.info("...Done")

        logging.info("Use Database...")

        sql_usedb = '''USE iNeuronDb'''
        sql_cursor.execute(sql_usedb)
        logging.info("...Done")

        logging.info("Create Table...")

        sql_create_tab = '''CREATE TABLE IF NOT EXISTS courses ( course_id TEXT, course_name TEXT, course_description TEXT)'''
        sql_cursor.execute(sql_create_tab)
        logging.info("...Done")

        logging.info("Insert Table...")

        for course in courses_data:
            c_id = course['course_id']
            c_name = course['course_name']
            c_desc = course['course_description']

            data = (c_id, c_name, c_desc)
            sql_insert = ("""INSERT INTO courses(course_id, course_name, course_description) VALUES(%s, %s, %s)""")

            sql_cursor.execute(sql_insert, data)
        sql_conn.commit()

        logging.info("...Done")

        logging.info("Closing Connection...")
        sql_conn.close()
        logging.info("...Done")

    except Exception as e:
        logging.error(e)
