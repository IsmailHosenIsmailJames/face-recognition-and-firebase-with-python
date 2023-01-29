import room_routine
import time
import os
import cv2
import pickle
import mediapipe as mp
import face_recognition
import firebase_admin
from firebase_admin import credentials,firestore


# initialize firebase server
cd = credentials.Certificate("tpi-student-database-15c14-firebase-adminsdk-fkfla-12512f7f93.json")
firebase_admin.initialize_app(cd)
datab = firestore.client()
usersref = datab.collection(u'all user')
docs = usersref.stream()

# initialize mediapipe for faster work
mp_face_detection = mp.solutions.face_detection

def load_data(subject:dict):
    face = []
    roll = []
    reg = []
    names = []
    emails = []
    data_path = f"face data/shift {subject['shift']}/{subject['deperment'].lower()}/semester {subject['semester']}/"
    if(subject["group"] == 'AB'):
        face_data_1 = open(f'{data_path}/A/face data.pkl', 'rb')
        face_list_1 = pickle.load(face_data_1)
        face_data_2 = open(f'{data_path}/B/face data.pkl', 'rb')
        face_list_2 = pickle.load(face_data_2)
        name_1 = open(f'{data_path}/A/names data.pkl', 'rb')
        name_list_1 = pickle.load(name_1)
        email_1 = open(f'{data_path}/A/emails data.pkl', 'rb')
        email_list_1 = pickle.load(email_1)
        email_2 = open(f'{data_path}/B/emails data.pkl', 'rb')
        email_list_2 = pickle.load(email_2)
        name_2 = open(f'{data_path}/B/names data.pkl', 'rb')
        name_list_2 = pickle.load(name_2)
        roll_1 = open(f'{data_path}/A/roll data.pkl', 'rb')
        roll_list_1 = pickle.load(roll_1)
        roll_2 = open(f'{data_path}/B/roll data.pkl', 'rb')
        roll_list_2 = pickle.load(roll_2)
        reg_data_1 = open(f'{data_path}/A/registation data.pkl', 'rb')
        reg_list_1 = pickle.load(reg_data_1)
        reg_data_2 = open(f'{data_path}/B/registation data.pkl', 'rb')
        reg_list_2 = pickle.load(reg_data_2)
        face_data_1.close()
        face_data_2.close()
        name_1.close()
        name_2.close()
        roll_1.close()
        roll_2.close()
        reg_data_2.close()
        reg_data_1.close()
        face = face_list_1  + face_list_2
        names = name_list_1  + name_list_2
        roll = roll_list_1  + roll_list_2
        reg = reg_list_1  + reg_list_2
        emails = email_list_1 + email_list_2
    else:
        face_data = open(f'{data_path}/A/face data.pkl', 'rb')
        face = pickle.load(face_data)
        name_data = open(f'{data_path}/A/names data.pkl', 'rb')
        names = pickle.load(name_data)
        roll_data = open(f'{data_path}/A/roll data.pkl', 'rb')
        roll = pickle.load(roll_data)
        reg_data = open(f'{data_path}/A/registation data.pkl', 'rb')
        reg = pickle.load(reg_data)
        email_data = open(f'{data_path}/A/emails data.pkl', 'rb')
        emails = pickle.load(email_data)
        email_data.close()
        face_data.close()
        name_data.close()
        roll_data.close()
        reg_data.close()
    return (face, names, roll, reg, emails)

camera_311 = cv2.VideoCapture(0)

json = room_routine.routine()
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence= 0.5) as face_detection:
    while (camera_311.isOpened()):
        now = time.ctime().split(' ')
        minutes = now[3].split(':')
        minutes = int(minutes[0])*60 + int(minutes[1])
        # trying to upgrading the system
        details_of_camera = ((camera_311, 311),)
        for cam in details_of_camera:
            camera = cam[0]
            room = cam[1]
            for subject in json[room][now[0]]:
                start_time = subject['start_time'] 
                end_time = subject['end_time']
                # load all data
                if(start_time <= minutes <= end_time):
                    present_file_path = f"present data/{now[4]}_{now[1]}_{now[2]}_{now[0]}/{subject['shift']}/{subject['deperment']}/{subject['semester']}/{subject['group']}/"
                    try: os.makedirs(present_file_path)
                    except: None
                    face, names, roll, reg , emails = load_data(subject=subject)
                    success, image = camera_311.read()
                    if not success: continue
                    image.flags.writeable = False
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = face_detection.process(image)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.detections:
                        for detection in results.detections:
                            face_data = detection.location_data.relative_bounding_box
                            img_shape = image.shape
                            # make image smaller for better performence
                            xmin = int(face_data.xmin * img_shape[1])
                            ymin = int(face_data.ymin * img_shape[0])
                            xmax = int(xmin + face_data.width * img_shape[1])
                            ymax = int(ymin + face_data.height * img_shape[0])
                            xmin, ymin, xmax, ymax = xmin -10, ymin - 60, xmax + 20, ymax + 20
                            if xmin < 0: xmin = 0
                            if ymin < 0: ymin = 0
                            if xmax > img_shape[0]: xmax = img_shape[1] - 1
                            if ymax > img_shape[1]: ymax = img_shape[0] - 1
                            # croped_image = cv2.resize(image[ymin:ymax,xmin:xmax], (0, 0), fx=0.75, fy=0.75)
                            croped_image = image[ymin:ymax,xmin:xmax]
                            encodeings = face_recognition.face_encodings(croped_image)
                            if(len(encodeings) != 0):
                                compare_result = face_recognition.face_distance(face, encodeings[0])
                                same_face = 0
                                for face_ditance in compare_result:
                                    if face_ditance < 0.45: same_face +=1; print(face_ditance)
                                if(same_face == 1):
                                    compare_result = list(compare_result)
                                    index = compare_result.index(min(compare_result))
                                    print(names[index], roll[index], reg[index])

                                    
                                    try:
                                        present_file = open(f"{present_file_path}/{subject['teacher']}_{subject['subject']}_{subject['subject_code']}_{now[4]}_{now[1]}_{now[2]}_{now[0]}.pkl", 'rb') 
                                        lst = pickle.load(file=present_file)
                                        present_file.close()
                                    except:  lst = []
                                    for i in lst:
                                        if names[index] in i:
                                            print("Already present token")
                                            break
                                    else:
                                        lst.append(f'{names[index]}_{roll[index]}_{reg[index]}_{now[3]}')
                                        present_file_w = open(f"{present_file_path}/{subject['teacher']}_{subject['subject']}_{subject['subject_code']}_{now[4]}_{now[1]}_{now[2]}_{now[0]}.pkl", 'w+b')
                                        pickle.dump(file=present_file_w, obj= lst)
                                        present_file_w.close()
                                        print("successfully taken present")

                                elif(same_face > 1):
                                    error = f"Cause error: Find same face encodings.\nError in : {subject['shift']}/{subject['deperment'].lower()}/semester {subject['semester']}\nPlease cheak this problem"
                                    print(error)
                                    error_file =  open(f'error/same_face.txt', 'wt')
                                    error_file.write(error)
                                    error_file.close()
                            cv2.rectangle(img=image, pt1=(xmin, ymin), pt2=(xmax, ymax),color=(0, 255, 255), thickness=2 )
                    cv2.imshow(f'{room}', image)
                    if cv2.waitKey(1) & 0xFF == ord("b"):
                        break

cv2.destroyAllWindows()