from os import listdir
from os import makedirs
from os import remove
from pickle import dump
from pickle import load
import firebase_admin
from firebase_admin import credentials,firestore


# initialize firebase server
cd = credentials.Certificate("tpi-student-database-15c14-firebase-adminsdk-fkfla-12512f7f93.json")
firebase_admin.initialize_app(cd)
datab = firestore.client()

firebase_location_ref = datab.collection(u'present file')
error = []

def uploade():
    path = "present data"
    for date in listdir(path= path):
        for shift in listdir(f'{path}/{date}'):
            for deperment in listdir(f'{path}/{date}/{shift}'):
                for semester in listdir(f'{path}/{date}/{shift}/{deperment}'):
                    for group in listdir(f'{path}/{date}/{shift}/{deperment}/{semester}'):
                        for file in listdir(f'{path}/{date}/{shift}/{deperment}/{semester}/{group}'):
                            file_path = f'{path}/{date}/{shift}/{deperment}/{semester}/{group}/{file}'
                            try:
                                file_ = open(file_path, 'rb')
                                list_of_present = load(file=file_)
                                firebase_doc_ref = firebase_location_ref.document(f'{date}_{shift}_{deperment}_{semester}_{group}_{file}')
                                firebase_doc_ref.set({
                                    "list" : list_of_present
                                })
                                Uploaded_present_file_path = f'Uploaded Present File/{date}/{shift}/{deperment}/{semester}/{group}/'
                                try: makedirs(Uploaded_present_file_path)
                                except: print("No need to create Folder :\n", " "*5, Uploaded_present_file_path)
                                remove(path=file_path)
                                Uploaded_present_file = open(f'{Uploaded_present_file_path}/{file}', 'wb')
                                dump(file=Uploaded_present_file, obj= list_of_present)
                                Uploaded_present_file.close()
                                file_.close()
                                print("Successfully Uploaded file:", " "*5, file_path)
                            except Exception:
                                error.append((file_path, Exception.mro()))
                                print(f"No valid data contain in: ", file_path)

uploade()

for i in error:
    print("Cause error: \n"," "*5, str(i[1]), "\nDo you want to delete this file :\n", " "*5, i[0], "Delete the file? [Y/N]Y: ", end="")
    p = input().lower()
    if(p=='y'):
        remove(i[0])
    else:
        print("File did not delete.")