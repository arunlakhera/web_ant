import logging
from fpdf import FPDF


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

        file_name = f"{user_sel_course[0]['course_id']}.pdf"

        pdf.output(file_name)
    except Exception as e:
        logging.error(e)

    # Save to S3

