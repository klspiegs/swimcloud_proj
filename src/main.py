import csv
from bs4 import BeautifulSoup as bs
import time as _time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

def getTeamID(team_name):
	team_number = -1

	#search for the specified team
	for index, row in teams.iterrows():
		if row['team_name'] == team_name:
			team_number = row['team_ID']
	return team_number

def getWebpage(url):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
	driver.get(url)
	print('STOP')
	print(url)
	_time.sleep(3)
	html = driver.page_source

	soup = bs(html, 'html.parser')
	try:
		table = soup.find('table', attrs={'class': 'c-table-clean'})
		if table:
			teams_list = table.find('tbody').find_all('tr')
			print("Teams list found!")
			# Access the fourth <tr> (index starts at 0, so the fourth is index 3)
			fourth_tr = teams_list[3]

			# Print or process the fourth <tr>
			print(fourth_tr)
		else:
			print("Table with class 'c-table-clean' not found.")
	except AttributeError:
		print("Error: The table or tbody element is missing.")



teams = pd.read_csv('collegeSwimmingTeams.csv')

# 1 = free
# 2 = back
# 3 = breast
# 4 = fly
# 5 = IM
# 6 = free relay
# 7 = medley relay

events = ['150', '1100', '1200', '1500', '11000', '11650',
			'250', '2100', '2200',
			'350', '3100', '3200',
			 '450', '4100', '4200',
			 '5100', '5200', '5400',
			 '6200', '6400', '6800',
			 '7200', '7400',
			 'split_150', 'split_1100', 'split_1200',
			 'split_250', 'split_350', 'split_3100',
			 'split_450', 'split_4100']

temp_events = ['150']


for value in teams.iloc[:, 0]:  # .iloc[:, 0] selects the first column
	team = value
	curr_id = getTeamID(value)
	for event in temp_events:
		url = 'https://www.swimcloud.com/team/'+ str(curr_id) + '/times/?dont_group=false&event='+ event + '&event_course=Y&gender=M&page=1&region&season_id=27&tag_id&team_id=' + str(curr_id) + '&year=2024'
		getWebpage(url)
		

