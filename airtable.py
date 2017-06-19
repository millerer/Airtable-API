# Written by Eric Miller 6-10-17

# This function leverages the Airtable API to paginate results and 
# convert each row from the example table into a python list of dictionaries. 
# Table used:Airtable Example table @ https://airtable.com/tblF9iepElqJVuc9c/viwXMpJ43LffWg0Gq
#
# Run the python script demopAPI.py for a demonstration

# library for website connections. 
# References for functions from: https://docs.python.org/3/library/urllib.request.html#urllib.request.Request + https://docs.python.org/3.4/howto/urllib2.html
import urllib.request

# library for JSON objects
# References for functions from https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
import json


# Make a GET request to the AirTable API and return the JSON object as a dictionary. 'URL' is the url of the test table
def make_request(URL):
	# Attempt a connection to the API site with required login information in the header
	# Required header info referenced from https://airtable.com/appAtdH9G73gQINUZ/api/docs#curl/introduction
	try:
		header = {'Authorization' : 'Bearer keyphF6Ur9r6uPLWM'}
		ApiRequest = urllib.request.Request(URL, headers = header )
		ApiResponse = urllib.request.urlopen(ApiRequest)
	except:
		print("FAILED to connect to URL: " +URL) 
		return
	
	#using the JSON library, convert the JSON object into a dictionary and return
	return json.load(ApiResponse)
	

# Create list of dictionaries containing API table line data. 
def make_dictionary():
	# Dictionary format is: 
    #{'id' : int, 'fields' : {'Name' : string, 'Notes' : string, 'Attachments' : string, 'in CA, but HQ elsewhere': bool, ' Annual Revenue (billions)' double}}
	dictionary_list = []

	# end loop flag
	allRowsChecked = False

	#Keeps track of pagination and offset value to get remaining pages
	page = 1
	offset = ""

	# Get each row in the table and add it as a dictionary to the list 
	while allRowsChecked == False:
		
		# Make an API request to get JSON data (max 100 results at a time). Include an offset value if not on the first page of data
		if page == 1:
			jsonDict = make_request("https://api.airtable.com/v0/appAtdH9G73gQINUZ/Table%201")	
		elif offset != "":
			jsonDict = make_request("https://api.airtable.com/v0/appAtdH9G73gQINUZ/Table%201?offset="+offset)
		else:
			print("ERROR: Missing offset value for page #" + page)
		
		# row parsing loop conditions
		breakLoop = False
		rowNumber = 0
		
		# for each row, parse the values into a dictionary and add it to the list.
		# Row fields are: ID(required), Name(required), Notes, Attachments, California, Revenue
		while breakLoop == False:
			# Get each field, 
			ID = jsonDict['records'][rowNumber]['id']
			Name = jsonDict['records'][rowNumber]['fields']['Name']
			#default to "" or False if the field is missing (which means it had no value in the original table)
			if 'Notes' in jsonDict['records'][rowNumber]['fields']:
				Notes = jsonDict['records'][rowNumber]['fields']['Notes']
			else:
				Notes = ""
			if 'Attachments' in jsonDict['records'][rowNumber]['fields']:
				Attachments = jsonDict['records'][rowNumber]['fields']['Attachments']
			else:
				Attachments = ""
			if 'in CA, but HQ elsewhere' in jsonDict['records'][rowNumber]['fields']:
				California = jsonDict['records'][rowNumber]['fields']['in CA, but HQ elsewhere']
			else:
				California = False
			if 'Annual Revenue (billions)' in jsonDict['records'][rowNumber]['fields']:
				Revenue = jsonDict['records'][rowNumber]['fields']['Annual Revenue (billions)']
			else:
				Revenue = ""
			
			# Use the fields to create a dictionary and append it to the list
			newRow = {'id': ID, 'fields': {'Name': Name, 'Notes': Notes, 'Attachments': Attachments, 'in CA, but HQ elsewhere': California, 'Annual Revenue (billions)': Revenue}}
			dictionary_list.append(newRow)
			rowNumber = rowNumber + 1
			
			# check if another row exists, otherwise end the loop
			try:
				ID = jsonDict['records'][rowNumber]['id']
			except:
				breakLoop = True  
		# Once all of a page's rows have been listed, check for an offset value (which means that more pages exists).
		if 'offset' in jsonDict:
			offset = jsonDict['offset']
			page = page +1
			
		# End if on the last page
		else:
			allRowsChecked = True
	
	#return the list of dictionaries
	return dictionary_list
	


print("DONE!")