import logging
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import json

ineuron_url = "https://ineuron.ai"


class NeuronScrapper:
    """
    This class provides data retrievel methods from website link of iNeuron
    """

    def __init__(self, url):
        self._url = ineuron_url
        self._logger = logging.getLogger("NeuronScrapper")

    def get_webpage(self):
        try:

            self._logger.debug("Getting Webpage...")
            uclient = uReq(ineuron_url)
            self._logger.debug("Done")

        except Exception as e:
            self._logger.error(e)
        else:
            return uclient

    def read_webpage(self, uclient):
        try:
            self._logger.debug("Reading Webpage...")
            ineuron_page = uclient.read()
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return ineuron_page

    def convert_webpage_to_html(self, ineuron_page):
        try:
            self._logger.debug("Converting Webpage to HTML...")

            ineuron_html = bs(ineuron_page, "html.parser")

            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return ineuron_html

    def extract_raw_data(self, ineuron_html):
        try:
            self._logger.debug("Extracting Raw Data...")
            bigboxes = ineuron_html.select("script", {"id": "__NEXT_DATA__"})
            self._logger.debug("Done")

        except Exception as e:
            self._logger.error(e)
        else:
            return bigboxes

    def convert_to_json(self, box):
        try:
            self._logger.debug("Converting to JSON...")
            json_object = json.loads(box.getText())
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return json_object

    def extract_cat_subcat(self, json_object):
        course_cat_sub_cat_list = []
        try:
            self._logger.debug("Getting Category and Subcategory Data...")

            cat_sub_cat_data = json_object['props']['pageProps']['initialState']['init']['categories']

            for kc in cat_sub_cat_data.keys():
                sub_cat_list = cat_sub_cat_data[kc]['subCategories'].keys()

                for ksc in sub_cat_list:
                    course_cat_sub_cat_list.append(
                        {'cat_id': kc, 'cat_name': cat_sub_cat_data[kc]['title'], 'sub_cat_id': ksc,
                         'sub_cat_name': cat_sub_cat_data[kc]['subCategories'][ksc]['title']})

            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
            course_cat_sub_cat_list.append({"ERROR": "Error in Extracting Category Data"})
        else:
            return course_cat_sub_cat_list

    def extract_courses(self, json_object):

        try:
            self._logger.debug("Getting Courses Data...")
            course_data = json_object['props']['pageProps']['initialState']['init']['courses']

            course_keys = course_data.keys()
            course_list = []

            for k in course_keys:

                course_name = k
                course_id = course_data[k]['_id']
                course_description = course_data[k]['description']
                course_mode = course_data[k]['mode']
                course_cat_id = course_data[k]['categoryId']

                if 'classTimings' in course_data[k]:
                    course_timings = course_data[k]['classTimings']
                elif 'batches' in course_data[k]:
                    course_timings = course_data[k]['batches']
                else:
                    course_timings = "NA"

                course_requirements = ''
                course_curriculum = ''
                course_features = ''

                for i in range(len(course_data[k]['courseMeta'])):
                    course_curriculum = course_data[k]['courseMeta'][i]['overview']['learn']
                    course_requirements = course_data[k]['courseMeta'][i]['overview']['requirements']
                    course_features = course_data[k]['courseMeta'][i]['overview']['features']

                instructor_id = []
                instructor_name = []
                instructors_social = []
                instructor_description = []

                for i in range(len(course_data[k]['instructorsDetails'])):

                    instructor_id.insert(i, course_data[k]['instructorsDetails'][i]['_id'])

                    instructor_name.insert(i, course_data[k]['instructorsDetails'][i]['name'])

                    if 'social' in course_data[k]['instructorsDetails'][i]:
                        instructors_social.insert(i, course_data[k]['instructorsDetails'][i]['social'])
                    else:
                        instructors_social.insert(i, "NA")

                    if 'description' in course_data[k]['instructorsDetails'][i]:
                        instructor_description.insert(i, course_data[k]['instructorsDetails'][i]['description'])
                    else:
                        instructor_description.insert(i, "NA")

                course_list.append({
                    'course_id': course_id,
                    'course_name': course_name,
                    'course_description': course_description,
                    'course_mode': course_mode,
                    'course_cat_id': course_cat_id,
                    'course_curriculum': course_curriculum,
                    'course_requirements': course_requirements,
                    'course_features': course_features,
                    'instructor_id': instructor_id,
                    'instructor_name': instructor_name,
                    'instructors_social': instructors_social,
                    'instructor_description': instructor_description
                })

            self._logger.debug("Done")

            return course_list
        except Exception as e:
            self._logger.error(e)
        return [{"ERROR": 'Error in Extracting Courses Data'}]

    # Function to fetch website data
    def get_data(self):

        uclient = self.get_webpage()
        ineuron_page = self.read_webpage(uclient)
        ineuron_html = self.convert_webpage_to_html(ineuron_page)
        bigboxes = self.extract_raw_data(ineuron_html)

        json_object = self.convert_to_json(bigboxes[23])

        cat_sub_cat_data = self.extract_cat_subcat(json_object)

        try:
            self._logger.debug("Saving cat_sub_cat_data.json")
            save_file = open("cat_sub_cat_data.json", "w")
            json.dump(cat_sub_cat_data, save_file, indent=4)
            save_file.close()
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)

        courses_data = self.extract_courses(json_object)

        try:
            self._logger.debug("Saving courses_data.json")
            save_file = open("courses_data.json", "w")
            json.dump(courses_data, save_file, indent=4)
            save_file.close()
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)

        return cat_sub_cat_data, courses_data

    def get_cat_courses(self, courses_data, cat_subcat_data, cat_id):
        cat_subcat_list = []
        for i in range(len(cat_subcat_data)):
            if cat_subcat_data[i]['cat_id'] == cat_id:
                cat_subcat_list.append(cat_subcat_data[i]['sub_cat_id'])

        cat_courses = self.get_subcat_courses(courses_data, cat_subcat_list)
        return cat_courses

    def get_subcat_courses(self, courses_data, subcat_id):
        subcat_courses = []
        for i in range(len(courses_data)):
            if courses_data[i]['course_cat_id'] in subcat_id:
                subcat_courses.append(courses_data[i])
        return subcat_courses

    def get_course(self, courses_data, course_id):
        selected_course = []

        for i in range(len(courses_data)):
            if courses_data[i]['course_id'] == course_id:
                selected_course.append(courses_data[i])

        return selected_course
