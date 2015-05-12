"""
- Script navigates to http://slashdot.org
- Gets the number of articles on the home page
- Gets the image icons in the articles and lists them
- Makes a random selection on the daily poll
- Gets the number of votes for the vote submitted

"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
import htmltestrunner


class Slashdot(unittest.TestCase):

    # test setup
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()
        self.base_url = "http://slashdot.org/"

    # test clean up
    def tearDown(self):
        self.driver.quit()



    # Navigate to the Slashdot homepage
    def test_slashdot_home_page(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertIn("Slashdot", driver.title)
    #
    # # Get the number of articles in home page
    def test_get_total_articles(self):
        driver = self.driver
        driver.get(self.base_url)
        # wait until page is fully loaded in browser and find all articles
        articles = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "story")))
        total_articles = len(articles)
        self.assertEqual(total_articles, 15)
        print "There are {} articles on the Slashdot home page".format(total_articles)

    # Get images in articles and add to list
    def test_get_images_in_articles(self):
        driver = self.driver
        driver.get(self.base_url)
        images = driver.find_elements_by_xpath("//span[@class= 'topic']/a/img")
        # verify number of images
        self.assertEqual(len(images), 15)
        # print list of image files for articles
        for image in images:
            print image.get_attribute("src")[28:]

    # make random poll selection, vote and get number of votes of similar poll selection
    def test_vote_on_poll(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.implicitly_wait(20)

        # check if poll is visible on page
        poll = driver.find_element_by_id("poll")

        if poll.is_displayed():
            # get number of poll options
            poll_options = driver.find_elements_by_xpath("//span[@class= 'grid_2']/input")
            number = len(poll_options)

            # generate random number based on available poll options
            poll_selection = str(randint(1, number))
            poll_value = driver.find_element_by_xpath("//span[@class = 'grid_2']/input[@value= '%s']" % poll_selection)
            poll_value.click()
            driver.find_element_by_xpath("//input[@value= 'Vote']").click()

            # Get number of poll results
            results = driver.find_elements_by_xpath("//strong[@class= 'barVotes']")
            # verify poll options is equal to number in results
            self.assertEqual(number, len(results))
            index = int(poll_selection) - 1
            poll_options = driver.find_elements_by_css_selector('.barAnswer')
            print "The option selected - '{0}', has {1}".format(poll_options[index].text, results[index].text)

        else:
            print "Poll option not present, you have already voted"



if __name__ == "__main__":
    #unittest.main()
    htmltestrunner.main()


