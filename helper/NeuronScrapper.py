import logging
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import json

ineuron_url = "https://ineuron.ai"


class NeuronScrapper:
    """
    This class provides data retrieval methods from website link of iNeuron
    """

    def __init__(self, url):
        """
        :param url: initialize url to scrap
        """
        self._url = ineuron_url
        self._logger = logging.getLogger("NeuronScrapper")

    def get_webpage(self):
        """
        :return: uclient
        Request is made to url and result is stored in uclient which is
        then returned back.
        """
        try:

            self._logger.debug("Getting Webpage...")
            uclient = uReq(ineuron_url)
            self._logger.debug("Done")

        except Exception as e:
            self._logger.error(e)
        else:
            return uclient

    def read_webpage(self, uclient):
        """

        :param uclient:
        :return: ineuron_page
        Takes uclient as input, reads the page and returns result
        """
        try:
            self._logger.debug("Reading Webpage...")
            ineuron_page = uclient.read()
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return ineuron_page

    def convert_webpage_to_html(self, ineuron_page):
        """
        :param ineuron_page:
        :return: html page
        Takes input raw content of website read and using beautifulsoup
        parses html
        """
        try:
            self._logger.debug("Converting Webpage to HTML...")

            ineuron_html = bs(ineuron_page, "html.parser")

            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return ineuron_html

    def extract_raw_data(self, ineuron_html):
        """
        :param ineuron_html:
        :return: related portion of extracted data
        Scrapes the required raw data from the html page
        """
        try:
            self._logger.debug("Extracting Raw Data...")
            bigboxes = ineuron_html.select("script", {"id": "__NEXT_DATA__"})
            self._logger.debug("Done")

        except Exception as e:
            self._logger.error(e)
        else:
            return bigboxes

    def convert_to_json(self, box):
        """

        :param box:
        :return: returns json object
        Takes input required data and returns in json format
        """
        try:
            self._logger.debug("Converting to JSON...")
            json_object = json.loads(box.getText())
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return json_object

    def extract_cat_subcat(self, json_object):
        """

        :param json_object:
        :return: list of category and subcategory data
        Extract category and sub category data
        """
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
        """

        :param json_object:
        :return: course related data
        Takes input json obecjt and returns course data
        """

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
        """
        :return: category and courses data
        Collects data, parses and returns category,subcategory and courses data
        """

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
        """

        :param courses_data:
        :param cat_subcat_data:
        :param cat_id:
        :return: returns only courses for the category provided
        Takes input courses_data, cat_subcat_data and cat_it and based on cat_id returns
        only those courses that belong to it.
        """
        cat_subcat_list = []
        for i in range(len(cat_subcat_data)):
            if cat_subcat_data[i]['cat_id'] == cat_id:
                cat_subcat_list.append(cat_subcat_data[i]['sub_cat_id'])

        cat_courses = self.get_subcat_courses(courses_data, cat_subcat_list)
        return cat_courses

    def get_subcat_courses(self, courses_data, subcat_id):
        """

        :param courses_data:
        :param subcat_id:
        :return: only those courses are returned that belong to particular sub category
        Takes input courses data and sub_Cat_id and returns only those courses that matches
        the sub category id provided
        """
        subcat_courses = []
        for i in range(len(courses_data)):
            if courses_data[i]['course_cat_id'] in subcat_id:
                subcat_courses.append(courses_data[i])
        return subcat_courses

    def get_course(self, courses_data, course_id):
        """

        :param courses_data:
        :param course_id:
        :return: course that belongs to the course_id provided
        Takes courses data and course id as input and returns only that course that matches
        """
        selected_course = []

        for i in range(len(courses_data)):
            if courses_data[i]['course_id'] == course_id:
                selected_course.append(courses_data[i])

        return selected_course
