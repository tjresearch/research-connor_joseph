from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pickle


# gauth = GoogleAuth()                                                                                #
# gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script     #
# drive = GoogleDrive(gauth)                                                                          #
                                                                                                      #
# with open("auth.pkl", 'wb') as output:                                                              #
#   pickle.dump(drive, output)                                                                        # Makes it so I don't have to 
                                                                                                      # reauthorize every time.
drive = "insantiating"                                                                                # May need to do this once every
with open("auth.pkl", 'rb') as input:                                                                 # so often though
  drive = pickle.load(input)                                                                          #


mimetypes = { # this rn makes all spreadsheet downlads csv files instead
  "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.google-apps.spreadsheet": "text/csv",
  "pickle_file": "application/octet-stream"
}

# downloads "export.pkl" from folder "best_model"
# "best_model" must have only 1 file
fileList = drive.ListFile({'q': "'1O05mvsXheQUR5xLoPKhmjuVffnHB4-1_' in parents and trashed=false"}).GetList() # that weird jjumble of stuff is the fodler id it is in the folder url
for file in fileList:
  print('Title: %s, ID: %s' % (file['title'], file['id']))
  # Get the folder ID that you want
  file_obj = drive.CreateFile({'id': file['id']})
  file_obj.GetContentFile('export.pkl', mimetypes["pickle_file"])


# # View all folders and file in your Google Drive
# fileList = drive.ListFile({'q': "'1O05mvsXheQUR5xLoPKhmjuVffnHB4-1_' in parents and trashed=false"}).GetList() # that weird jjumble of stuff is the fodler id it is in the folder url
# for file in fileList:
#   print('Title: %s, ID: %s' % (file['title'], file['id']))
#   # Get the folder ID that you want
#   if(file['title'] == "To Share"):
#       fileID = file['id']


# # Downloads to the same folder as this code
# # when downloaded with the same name, it updates the existing file
# file_obj = drive.CreateFile({'id': '1PQKfzakChzgtgx55dKHjZQW4OzDf5s-LBsQEKJZ8bvc'})
# file_obj.GetContentFile('vsc.csv', mimetypes["application/vnd.google-apps.spreadsheet"])



# # Initialize GoogleDriveFile instance with file id.
# file1 = drive.CreateFile({"mimeType": "text/csv", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
# file1.SetContentFile("small_file.csv")
# file1.Upload() # Upload the file.
# print('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))


# """
# file_list = drive.ListFile({'q': "'<folder ID>' in parents and trashed=false"}).GetList()
# """
# fileList = drive.ListFile({'q': "'2mavWSQhVfr7GnX2JHa45Qd43bTaYCHXE' in parents and trashed=false"}).GetList()
# for file in fileList:
#   print('Title: %s, ID: %s' % (file['title'], file['id']))
#    # Get the folder ID that you want
#   if(file['title'] == "picture"):
#       fileID = file['id']


# # Initialize GoogleDriveFile instance with file id.
# file2 = drive.CreateFile({'id': fileID})
# file2.Trash()  # Move file to trash.
# file2.UnTrash()  # Move file out of trash.
# file2.Delete()  # Permanently delete the file.