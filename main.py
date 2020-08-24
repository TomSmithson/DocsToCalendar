from GoogleDocsReader import GoogleDocsReader
from GoogleCalendarWriter import GoogleCalendarWriter


# Todo - Create an event class for each of the events. This event has a summary, location, description, start time, end time, attendees




DOCUMENT_ID = "1P3A5Oj-5BPJaVfKwKxcaxHiH4BR72ouGY5hcu68Wq0I"

def main():
    doc = GoogleDocsReader()
    doc.authenticate()
    doc.get_document(DOCUMENT_ID)
    lines = doc.read_document_by_line()
    daily = doc.text_to_dict(lines)

    for k, v in daily.items():
        print("{} : {}".format(k, v))

    cal = GoogleCalendarWriter()
    cal.authenticate()
    # cal.get_upcoming_events(10)
    cal.add_events_to_calendar(daily)



if __name__ == '__main__':
    main()