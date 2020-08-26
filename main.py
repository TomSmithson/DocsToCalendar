from GoogleDocsReader import GoogleDocsReader
from GoogleCalendarWriter import GoogleCalendarWriter


# Todo - Create an event class for each of the events. This event has a summary, location, description, start time, end time, attendees


DOCUMENT_ID = "1FpMPtMouXdr9Jh6ukO0hxG6VKa753O3LXow-c60zCxA"

def main():
    doc = GoogleDocsReader()
    doc.authenticate()
    doc.get_document(DOCUMENT_ID)
    lines = doc.read_document_by_line()
    daily = doc.text_to_dict(lines)

    cal = GoogleCalendarWriter()
    cal.authenticate()
    # cal.add_events_to_calendar(daily)
    cal.delete_all_daily_events()


if __name__ == '__main__':
    main()