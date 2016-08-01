from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import os, sys
import csv
from csv import reader
import matplotlib.pyplot as plt


def main():
    ##open firefox
    profile = webdriver.FirefoxProfile()
    # custom location
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', os.getcwd())#to make current location the location for download
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    driver = webdriver.Firefox(firefox_profile=profile)

    ##getting to data.gov data catalog
    driver.get('https://catalog.data.gov/')
    ## go to the search element
    element = driver.find_element_by_name('q')
    ##enter keys in search
    element.send_keys('Demographic Statistics By Zip Code')
    ##press enter after giving the search text
    element.send_keys(Keys.ENTER)
    ## click the required data link
    history_link = driver.find_element_by_partial_link_text('Demographic Statistics By Zip Code')
    history_link.click()

    ##click the download page
    csv_link = driver.find_element_by_partial_link_text('Comma Separated Values File')
    csv_link.click()

    ##downloading the file
    download_link = driver.find_element_by_partial_link_text('Download')
    download_link.click()
    ##closing the firefox driver. i.e closing the firefox window
    tear_down(driver)
    
    ##calling matplotlib to plot the graphs
    stockvol_plot()



def stockvol_plot():
    os.chdir(os.getcwd())
    # open the csv sheet and store the data in a list
    with open('Demographic_Statistics_By_Zip_Code.csv', 'r') as f:
        data = list(reader(f))
        jurisdiction = [i[0] for i in data[1::]]
        numOfParticipants = [i[1] for i in data[1::]]

        plt.plot(jurisdiction, numOfParticipants, color='green', marker='o', linestyle='solid')
        plt.title('Number of Participants per Jurisdiction in New York')
        plt.xlabel('Jurisdiction\'s Zip Code')
        plt.ylabel('Number of Participants')
        plt.show()

        countFemale = [i[2] for i in data[1::]]
        plt.plot(jurisdiction, countFemale, color='red', marker='o', linestyle='solid')
        plt.title('Number of Female Participants per Jurisdiction in New York')
        plt.xlabel('Jurisdiction in NewYork')
        plt.ylabel('Number of Female Participants')
        plt.show()

        countMale = [i[4] for i in data[1::]]
        plt.plot(jurisdiction, countMale,  color='blue', marker='o', linestyle='solid')
        plt.title('Number of Male Participants per Jurisdiction in New York')
        plt.xlabel('Jurisdiction in NewYork')
        plt.ylabel('Number of Male Participants')
        plt.show()

##function to tear down driver after 2 seconds of completion
def tear_down(driver):
    time.sleep(2)
    driver.quit()


main()

