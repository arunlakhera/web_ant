import logging
from fpdf import FPDF
import boto3
from helper.NeuronDb import NeuronDb


def save_to_s3(filename):
    """
    :param filename: takes filename of file to store in s3
    :return: Saves file to Amazon s3
    """
    # Create an S3 access object
    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            Filename=filename,
            Bucket="arunpdf",
            Key=filename,
        )
    except Exception as e:
        logging.error(e)


def save_to_pdf(user_sel_course):
    """
    Function to convert data to PDF
    :param user_sel_course:
    This creates and saves PDF file.
    """
    try:
        for course in user_sel_course:
            course_id = str(course['course_id'])
            course_name = str(course['course_name'])
            course_description = str(course['course_description'])
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
        pdf.multi_cell(200, 10, txt=f"Requirements: {course_requirements}", align='L')
        pdf.multi_cell(200, 10, txt=f"Features: {course_features}", align='L')
        pdf.multi_cell(200, 10, txt=f"Instructor Name: {instructor_name}", align='L')
        pdf.multi_cell(200, 10, txt=f"Instructors Social: {instructors_social}", align='L')
        pdf.multi_cell(200, 10, txt=f"Instructor Description: {instructor_description}", align='L')

        # file_name = f"{user_sel_course[0]['course_id']}.pdf"
        file_name = f"{course_id}.pdf"

        logging.info(f"File Name for PDF: {file_name}")

        # Save pdf file
        pdf.output(file_name)

        # save to s3
        save_to_s3(file_name)

    except Exception as e:
        logging.error(e)


def save_to_mongodb(cat_subcat_data, courses_data):
    """
    :param cat_subcat_data:
    :param courses_data:
    Stores Data into MonoDB Database
    """
    password = "pwdineuron"
    mongodb_link = f"mongodb+srv://ineuron:{password}@cluster0.eltt8.mongodb.net/?retryWrites=true&w=majority"
    neuron_db = NeuronDb()

    mongodb_client = neuron_db.connect_mongo(mongodb_link)
    mongodb_name = 'ineuron'
    mongodb_db = neuron_db.create_mongo_db(mongodb_client, mongodb_name)
    coll_name = 'cat_subcat'
    mongodb_cat_subcat_coll = neuron_db.create_mongo_coll(mongodb_db, coll_name)
    coll_name = 'courses'
    mongodb_courses_coll = neuron_db.create_mongo_coll(mongodb_db, coll_name)

    neuron_db.mongo_insert(mongodb_cat_subcat_coll, cat_subcat_data)
    neuron_db.mongo_insert(mongodb_courses_coll, courses_data)


def save_to_mysql(courses_data):
            """
            :param courses_data: Pass courses data

            Stores passed data into MySQL Database
            """

            host = "ineurondb.cckavecit4n5.ap-northeast-1.rds.amazonaws.com"
            username = "ineuron"
            password = "pwdineuron"

            neuron_db = NeuronDb()

            # Connect to MySQL Server
            sql_conn, sql_cursor = neuron_db.connect_mysql(host, username, password)

            # Create Database
            db_name = 'iNeuronDb'
            neuron_db.create_mysql_db(sql_cursor, db_name)

            # Create Table
            table_name = 'courses'
            neuron_db.create_mysql_table(sql_cursor, table_name)

            # Insert Data into table
            neuron_db.insert_mysql_data(sql_conn, sql_cursor, table_name, courses_data)
