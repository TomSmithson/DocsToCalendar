import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/documents']


class GoogleDocsReader:
    def __init__(self):
        self._service = None
        self._doc = None
    
    def authenticate(self):
        """
        Authenticating a user and returning a 
        Google Docs service
        """
        creds = None
        if os.path.exists("docs_token.pickle"):
            with open("docs_token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("docs_credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("docs_token.pickle", "wb") as token:
                pickle.dump(creds, token)
        self._service = build("docs", "v1", credentials=creds)

    def get_document(self, document_id):
        """
        Searches for the specified document
        and sets to the object
        """
        self._doc = self._service.documents().get(documentId=document_id).execute()

    def read_document_by_line(self):
        """
        Reads the content of the document
        line by line and appends each line
        to a list
        """
        doc_content = self._doc.get("body").get("content")
        lines = []
        for value in doc_content:
            if "paragraph" in value:
                elements = value.get("paragraph").get("elements")
                for elem in elements:
                    lines.append(elem.get("textRun").get("content"))
        return lines

    def text_to_dict(self, lines):
        """
        Iterates through the list of lines
        strips whitespace, newline characters
        and creates a dictionary {time : activity}
        """
        daily_activities = {}
        for line in lines:
            if ":" in line:
                data = line.split("-")
                data[0] = data[0][:-3]
                data[0], data[1] = data[0].strip(), data[1].strip()
                daily_activities[data[0]] = data[1]
        return daily_activities
