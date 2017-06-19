from airtable import make_dictionary

# Demonstration of using the Airtable API to paginate results and converting each row into a pythonlist of dictionaries. 
# Per instructions, I am using the 'test' table at: https://airtable.com/tblF9iepElqJVuc9c/viwXMpJ43LffWg0Gq
def main():
	# Using the Airtable API, create a list of all table rows stored as dictionaries. 
	# The dictionary format is: {'id' : int, 'fields' : {'Name' : string, 'Notes' : string, 'Attachments' : string, 'in CA, but HQ elsewhere': bool, 'Annual Revenue (billions)' double}}
	AirtableList = make_dictionary()
	
	#Print all of the company names in the list
	names = ""
	row = 0
	while row < len(AirtableList):
		names = names + AirtableList[row]['fields']['Name'] + ", "
		row = row + 1
	print("Companies in the list: \n\n"+names)
	
	#Print out companies that have their annual revenue recorded
	revenueCompanies = "\n\nComapnies with Recorded Annual Revenue (billions): \n\n"
	row = 0
	while row < len(AirtableList):
		if AirtableList[row]['fields']['Annual Revenue (billions)'] != "":
			revName = AirtableList[row]['fields']['Name']
			revAmount = AirtableList[row]['fields']['Annual Revenue (billions)']
			revenueCompanies = revenueCompanies + revName + ": $"+str(revAmount)+"\n"
		row = row + 1

	print(revenueCompanies)
	
	

if __name__ == "__main__":
    main()
