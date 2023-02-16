# Add flask to requirements file
from flask import Flask, render_template, request
from helper.NeuronScrapper import NeuronScrapper
import utilities

import logging


application = Flask(__name__)
app = application

logging.basicConfig(filename='ineuron_log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

cat_sub_cat_items = []

data_neuron = NeuronScrapper("https://ineuron.ai")
cat_subcat_data, courses_data = data_neuron.get_data()


@app.route('/',  methods=['GET', 'POST'])
@app.route('/home_page', methods=['GET', 'POST'])
async def home_page():

    if request.method == 'POST':
        return render_template("loading.html")

    return render_template('home.html')

@app.route('/loading')
def loading():
    return render_template("loading.html")


@app.route('/load_data')
def load_data():
    try:
        utilities.save_to_mongodb(cat_subcat_data, courses_data)
        utilities.save_to_mysql(courses_data)

    except Exception as e:
        logging.error(e)


@app.route("/cat_subcat_list", methods=['GET', 'POST'])
async def cat_subcat_list():

    if request.method == 'POST':

        user_sel_cat_subcat = request.form['c_name']
        type_of_id = user_sel_cat_subcat[0:1]
        user_sel_id = user_sel_cat_subcat[1:]

        if type_of_id == 'c':
            sel_cat_subcat_courses = data_neuron.get_cat_courses(courses_data, cat_subcat_data, user_sel_id)
        else:
            sel_cat_subcat_courses = data_neuron.get_subcat_courses(courses_data, user_sel_id)

        return render_template('course_list.html', courses=sel_cat_subcat_courses, user_sel_cat_subcat=user_sel_cat_subcat)

    return render_template("cat_subcat_list.html", cat_subcat_data=cat_subcat_data)


@app.route("/course_list", methods=['GET', 'POST'])
async def course_list():
    if request.method == 'POST':

        user_form_data = request.form['view_detail']
        user_form_data_list = user_form_data.split(',')
        user_sel_course_id = user_form_data_list[0]
        user_sel_course_id = user_sel_course_id[2:]
        user_sel_course_id = user_sel_course_id[:len(user_sel_course_id) - 1]

        user_sel_cat_subcat = user_form_data_list[1]
        user_sel_cat_subcat = user_sel_cat_subcat[2:]
        user_sel_cat_subcat = user_sel_cat_subcat[:len(user_sel_cat_subcat) - 1]

        user_sel_course = data_neuron.get_course(courses_data, user_sel_course_id)

        return render_template('course_detail.html', courses=user_sel_course, user_sel_cat_subcat=user_sel_cat_subcat)

    return render_template("course_list.html", cat_subcat_data=cat_subcat_data)


@app.route('/course_detail', methods=['GET', 'POST'])
def course_detail():

    if request.method == 'POST':

        user_form_data = request.form['pdf']
        user_form_data_list = user_form_data.split(',')
        user_sel_course_id = user_form_data_list[0]
        user_sel_course_id = user_sel_course_id[2:]
        user_sel_course_id = user_sel_course_id[:len(user_sel_course_id) - 1]

        user_sel_cat_subcat = user_form_data_list[1]
        user_sel_cat_subcat = user_sel_cat_subcat[2:]
        user_sel_cat_subcat = user_sel_cat_subcat[:len(user_sel_cat_subcat) - 1]

        user_sel_course = data_neuron.get_course(courses_data, user_sel_course_id)
        utilities.save_to_pdf(user_sel_course)

        return render_template('course_detail.html', courses=user_sel_course, user_sel_cat_subcat=user_sel_cat_subcat)

    return render_template('course_detail.html', cat_subcat_data=cat_subcat_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

