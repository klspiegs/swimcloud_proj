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

extracted_data = []

def getTeamID(team_name):
	team_number = -1

	#search for the specified team
	for index, row in teams.iterrows():
		if row['team_name'] == team_name:
			team_number = row['team_ID']
	return team_number

def getWebpage(url, extracted_data):
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
			
			if len(teams_list) < 4: 
				# deals with if the 4th time isn't found,
				# feel free to delete if you'd rather just not include it.
				# if you want to leave it in, maybe you can move the championship
				# field out of this, since it's retrieved again below :3
				print("Fourth tr does not exist!")
				name = "N/A" 
				championship = teams_list[0].find_all('td')[2].find('a').text.strip()
				time = "N/A"

			else: 
				fourth_tr = teams_list[3] # Access the fourth <tr> (index starts at 0, so the fourth is index 3)
				# below works for my block-y output, since it's matching on the a hrefs w/in the HTML
				name = fourth_tr.find_all('td')[1].find('a').text.strip() 
				championship = fourth_tr.find_all('td')[2].find('a').text.strip()
				time = fourth_tr.find_all('td')[3].find('a').text.strip()
				
			extracted_data.append([name, championship, time])
			#print(extracted_data)
		else:
			print("Table with class 'c-table-clean' not found.")
	except AttributeError:
		print("Error: The table or tbody element is missing.")
	
	driver.quit()

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

count = 0 # remove this

for value in teams.iloc[:, 0]:  # .iloc[:, 0] selects the first column
	team = value
	curr_id = getTeamID(value)
	for event in temp_events:
		url = 'https://www.swimcloud.com/team/'+ str(curr_id) + '/times/?dont_group=false&event='+ event + '&event_course=Y&gender=M&page=1&region&season_id=27&tag_id&team_id=' + str(curr_id) + '&year=2024'
		getWebpage(url, extracted_data)

	count += 1
	if count == 11: # only going up to 10 for the sake of testing. otherwise, very slow...
		break

# writes out to csv after the loop has finished
with open('fourth_best_time_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Name', 'Championship', 'Time'])
		writer.writerows(extracted_data)

		print("Data has been written to fourth_best_time_results.csv")
		

