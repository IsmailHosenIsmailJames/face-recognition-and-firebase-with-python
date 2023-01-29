import os
import cv2
import face_recognition
import pickle
cause_error = 0
path = 'face data'
list_shift = os.listdir(path)
for shift in list_shift:
    list_deperment = os.listdir(f'{path}/{shift}')
    for deperment in list_deperment:
        list_semester = os.listdir(f'{path}/{shift}/{deperment}')
        for semester in list_semester:
            list_of_group = os.listdir(f'{path}/{shift}/{deperment}/{semester}')
            for group in list_of_group:
                # loade all important files
                current_path = f'{shift}/{deperment}/{semester}/{group}'
                face_file = open(f'{path}/{current_path}/face data.pkl', 'rb')
                face_encodeings = pickle.load(face_file)
                name_file = open(f'{path}/{current_path}/names data.pkl', 'rb')
                names = pickle.load(name_file)
                reg_file = open(f'{path}/{current_path}/registation data.pkl', 'rb')
                reg = pickle.load(reg_file)
                roll_file = open(f'{path}/{current_path}/roll data.pkl', 'rb')
                roll = pickle.load(roll_file)
                emails_file = open(f'{path}/{current_path}/emails data.pkl', 'rb')
                emails = pickle.load(emails_file)
                emails_file.close()
                face_file.close()
                name_file.close()
                reg_file.close()
                roll_file.close()
                for i in range(0, len(face_encodeings)):
                    for j in range(0, len(face_encodeings)):
                        if(i != j):
                            compare_result = face_recognition.compare_faces([face_encodeings[i]], face_encodeings[j], tolerance=0.47)
                            if compare_result[0] == True:
                                img1_name = f'{list(roll)[i]}_{list(reg)[i]}_{list(names)[i]}_{list(emails)[i]}.jpg'
                                img2_name = f'{list(roll)[j]}_{list(reg)[j]}_{list(names)[j]}_{list(emails)[j]}.jpg'
                                print(f"Found same face in : {current_path}")
                                print(' '*4, "Same file are :")
                                print(f'{" "*10}{img1_name}\n{" "*10}{img2_name}')
                                image1_path = f'img data/{current_path}/{img1_name}'
                                img1 = cv2.imread(image1_path)
                                image2_path = f'img data/{current_path}/{img2_name}'
                                img2 = cv2.imread(image2_path)
                                try: os.makedirs(f'error/same face/{current_path}/')
                                except: print(f"No need to create folder : error/smae face/{current_path}/")
                                cv2.imwrite(img= img1, filename= f'error/same face/{current_path}/{img1_name}')
                                cv2.imwrite(img= img2, filename= f'error/same face/{current_path}/{img2_name}')