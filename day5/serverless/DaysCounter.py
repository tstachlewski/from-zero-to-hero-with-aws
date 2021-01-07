from datetime import date
from datetime import datetime
import json

def lambda_handler(event, context):
    
    year = event["year"]
    month = event["month"]
    day = event["day"]
    
    birth_date = datetime.strptime(year+"-"+month+"-"+day, "%Y-%m-%d")
    
    birth_date = date(int(year), int(month), int(day))
    today_date = date.today()
    number_days = today_date - birth_date

    return {
        'statusCode': 200,
        'body': json.dumps('You were born ' + str(number_days.days) + ' days ago!' ) 
    }
