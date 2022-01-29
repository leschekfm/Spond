from datetime import date
import os
import argparse
import asyncio
import csv
import spond
from config import username, password

parser = argparse.ArgumentParser()
parser.add_argument("start", help="Start date to query for (format YYYY-MM-DD)", type=date.fromisoformat)
parser.add_argument("end", help="End date to query for (format YYYY-MM-DD)", type=date.fromisoformat)
args = parser.parse_args()

async def main():
    s = spond.Spond(username=username, password=password)
    events = await s.getEventsBetween(args.start, args.end)
    
    if not os.path.exists('./exports'):
            os.makedirs('./exports')

    with open(os.path.join("./exports", 'attendance.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        spamwriter.writerow(["Start","Ende","Bezeichnung","Trainer","Zusage"])

        for e in events:
            for o in e['owners']:
                person = await s.getPerson(o['id'])
                fullName = person['firstName'] + ' ' + person['lastName']
                spamwriter.writerow([e['startTimestamp'], e['endTimestamp'], e['heading'], fullName, o['response']])
            
    await s.clientsession.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

