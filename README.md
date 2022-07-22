# USNEWS College Webscraping
This is a script that uses [Selenium](https://www.selenium.dev/) to scrape the U.S. News Best National Universities ranking:
[Here](https://www.usnews.com/best-colleges/rankings/national-universities)

## Data Description
The data is stored in a `.csv` format that can easily be opened as a [Pandas](https://pandas.pydata.org/) dataframe.

Each school is ordered based on its rank (ascending) and ties are in the order which they appear on the website.

`name`: Name of the university

`rank`: Ranking of the university from USNEWS

`type`: Whether the school is public or private

`founded`: Year that the university was founded

`religon`: The school's religous affiliation (or lack thereof)

`schedule`: Academic schedule of the universtiy

`location_type`: Describes the campus and surrounding area

`phone_num`: The phone number for the university listed on the USNEWS website

`usnews_score`: The "USNEWS Overall score" [see more here](https://www.usnews.com/education/best-colleges/articles/how-us-news-calculated-the-rankings)

`six_year_grad_rate`: The graduation rate of students who attend for six years

`six_year_with_pell`: The graduation rate of six year students who recieved Pell Grants

`six_year_without_pell`: The graduation rate of six year students who did not recieve Pell Grants

`percent_class_less_twenty`: Percentage of classes at the university with less than twenty students

`percent_class_more_fifty`: Percentage of classes at the university with fifty or more students

`student_to_fac`: The student to faculty ratio at the university

`app_deadline`: The application deadline (regular decision)

`app_fee`: The fee to apply to the university

`acceptance_rate`: Percentage of applicants who are accepted to the university

`total_enroll`: Total amount of students enrolled

`undergrad_enroll`: Total amount of undergraduate students enrolled

`grad_enroll`: Total amount of graduate students enrolled

`tuition`: Price of tuition

`room_and_board`: Price of room and board


## Using the Script

1. Have Python, pip, and all necessary libraries installed

2. Install [Firefox](https://www.mozilla.org/en-US/firefox/new/)

3. Download the WebDriver for Firefox: [geckodriver](https://github.com/mozilla/geckodriver/releases)

4. Unzip the file and drag `geckodriver.exe` to the folder where the python scripts are (`.log` and `.csv` files will generate when script is run) 

![image](https://user-images.githubusercontent.com/59097689/180339273-1551b5b8-41cc-4385-8c16-fc5fc81f408f.png)

5. Run `webscraper.py` - I like to minimize every other window as Firefox will open and close many times and acts weird with other windows

6. Results should be in `college_data.csv` (it will be generated if does not exist in current directory and will wipe the old contents before writing updated data)

7. Webscraping is not perfect so there are likely a few html elements in your data so be sure to go and clean it up before usage!
