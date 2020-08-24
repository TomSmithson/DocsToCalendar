from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/documents']

DOCUMENT_ID = "1P3A5Oj-5BPJaVfKwKxcaxHiH4BR72ouGY5hcu68Wq0I"


class GoogleDocsReader:
    def __init__(self):
        self._service = None
        self._doc = None
    
    def authenticate(self):
        """Authenticating a user and returning a service"""
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        self._service = build("docs", "v1", credentials=creds)

    def get_document(self, document_id):
        self._doc = self._service.documents().get(documentId=document_id).execute()

    def read_document_by_line(self):
        doc_content = self._doc.get("body").get("content")
        lines = []
        for value in doc_content:
            if "paragraph" in value:
                elements = value.get("paragraph").get("elements")
                for elem in elements:
                    lines.append(elem.get("textRun").get("content"))
        return lines

    def text_to_dict(self, lines):
        daily_activities = {}
        for line in lines:
            if ":" in line:
                data = line.split("-")
                data[0], data[1] = data[0].strip(), data[1].strip()
                daily_activities[data[0]] = data[1]
        return daily_activities


def main():
    doc = GoogleDocsReader()
    doc.authenticate()
    doc.get_document(DOCUMENT_ID)
    lines = doc.read_document_by_line()
    daily = doc.text_to_dict(lines)

    for k, v in daily.items():
        print("{} : {}".format(k, v))


if __name__ == '__main__':
    main()