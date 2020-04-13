# Background
Under a cooperative agreement with the U.S. Department of Agriculture (USDA), the [George Washington University Regulatory Studies Center](https://regulatorystudies.columbian.gwu.edu/) conducted research analyzing public comments to inform agency regulatory reform efforts in the United States. A group of faculty members and researchers affiliated with the GW Regulatory Studies Center contributed to the research project, and subject matter experts at the USDA Office of the Chief Economist provided technical advice. The research report is available at: https://regulatorystudies.columbian.gwu.edu/putting-food-table-agriculture-and-regulation.

In this research, we (the GW Regulatory Studies Center research team) developed Python code to retrieve, clean, and analyze data of public comments. We share the code in this repository. The goal is to provide code that can be easily modified for use in other research using public comments.

We will update this repository routinely with new code from the above project and future research using comments. The initial content available in the repository includes the code to retrieve public submissions via the [Regulations.gov API](https://www.regulations.gov/apiOverview), including comments submitted as PDF attachments, and convert them into text data. As we continue uploading new content, we hope other researchers and programmers can contribute to the repository or suggest improvements to make it a more useful tool.

# Retrieving public comments from Regulations.gov
## Regulations.gov API
[Regulations.gov](https://www.regulations.gov/) is a central portal for public users to access U.S. federal regulatory materials and submit comments on proposed regulations. It was launched by the [eRulemaking Program](https://www.regulations.gov/aboutProgram) in January 2003. Today, nearly 300 federal agencies post an average of 8,000 regulations per year, among which the majority receive comments and share them on Regulations.gov, while others accept and post comments via other online platforms.

Regulations.gov offers all its public data in machine readable format via an [API (Application Programming Interface)](https://www.regulations.gov/apiOverview), which allows users to search and retrieve data on public submissions and other regulatory materials in an automated way. All the content that can be obtained using the regular search function on Regulations.gov is available in json or xml format if an equivalent [API query](https://regulationsgov.github.io/developers/console/) is used. This includes the full text of comments and rules, as well as their metadata such as agency name, commenter name, publication date, etc.

For a detailed description of Regulations.gov API, visit: https://regulationsgov.github.io/developers/.

### How to request a API key
The first thing you need to use the Regulations.gov API is a unique API key designated to you or your organization. You can contact the Regulations.gov Help Desk to request an API key, providing the information listed on [this page](https://regulationsgov.github.io/developers/).

You will then receive instructions and a URL for signing up an API key. You will be assigned a API key immediately, but it is not ready for use immediately. You will need to send the key back to the Regulations.gov Help Desk for the developers to activate your key for use on Regulations.gov. The activation process may take a few days to a couple of weeks.

## How to retrieve comments submitted to a docket using API
If you would like to retrieve the full text of comments submitted to a Regulations.gov docket (e.g., [Identifying Regulatory Reform Initiatives](https://www.regulations.gov/docket?D=USDA-2017-0002)), follow these steps:
* Export the docket folder: the exported file contains metadata for all the documents in the docket (e.g., rules, public submissions), including a Document ID for each comment which will be used as an identifier in API quiries.
	* Go to the Docket Folder Summary page ([example](https://www.regulations.gov/docket?D=USDA-2017-0002))
	* Click on View All in the Comments section
	* Click on Export (on top of the results) and save the .csv file to your local folder
* Modify the Python script "Retrive Comments/GetComments.py" to download comments submitted to the docket in both text and attachment format.
	* (For Beginners who use Python for the first time:) Select your preferred development environment for running the Python script (e.g., [PyCharm](https://www.jetbrains.com/pycharm/), [Spyder](https://www.spyder-ide.org/), [Jupyter Notebook](https://jupyter.org/)). You can also install [Anaconda](https://www.anaconda.com/) to help you manage the environment.
	* Modify the script following the annotations in the script, including adding your API key and specifying the location of your exported docket metadata file, etc.
	* Run the script to export all text comments into a .csv file (or any other desired format) and download all comments submitted as PDF or DOC files to your local folder

*Notes: Regulations.gov sets a rate limit of 1,000 requests per hour applied to all API users. A pause is added between two requests using `time.sleep()` in the script to avoid errors. As a result, it may take a long time if you are retrieving a large number of comments.*

