import os
import pickle
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import cv2
from base import app
import face_recognition
from flask import render_template, request, redirect, url_for
from imutils import paths
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.citizendetails_dao import CitizenDetailsDAO
from base.com.vo.citizendetails_vo import CitizenDetailsVO
from base.com.vo.fine_receipt_vo import FineReceiptVO
from base.com.dao.finereceipt_dao import FineReceiptDAO


@app.route('/traffic_police_station/load_face_recongize')
def user_load_face_recognize():
    try:
        if admin_login_session() == "user":
            return render_template('traffic_police_station/addFaceRecognize.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_load_face_recognize route exception occured>>>>>>>>>>", ex)


def face_encoding():
    imagePaths = list(paths.list_images('base/static/adminResources/citizendetails'))
    imagePaths = [x.replace('\\', '/') for x in imagePaths]
    # print("ImagePath>>>>>>>", imagePaths)
    knownEncodings = []
    knownNames = []
    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        name = imagePath.split('/')
        name = name[-1][:-4]
        # print('name >>>>>>>>>', name)
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Use Face_recognition to locate faces
        boxes = face_recognition.face_locations(rgb, model='hog')
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    # save emcodings along with their names in dictionary data
    data = {"encodings": knownEncodings, "names": knownNames}
    # print("data>>>>>>>>", data)
    # use pickle to save data into a file for later use
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()


face_encoding()


@app.route('/traffic_police_station/perform_face_recongize', methods=['POST'])
def user_perform_face_recognize():
    try:
        if admin_login_session() == "user":

            citizendetails_dao = CitizenDetailsDAO()
            citizendetails_vo = CitizenDetailsVO()

            # find path of xml file containing haarcascade file
            cascPathface = os.path.abspath("base/static/adminResources/weights/haarcascade_frontalface_alt2.xml")
            # print("cascPathface>>>>>>>", cascPathface)
            # load the harcaascade in the cascade classifier
            faceCascade = cv2.CascadeClassifier(cascPathface)
            # load the known faces and embeddings saved in last file
            data = pickle.loads(open('face_enc', "rb").read())
            print("Streaming started")
            video_capture = cv2.VideoCapture(0)
            # loop over frames from the video file stream
            while True:
                # grab the frame from the threaded video stream
                ret, frame = video_capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray,
                                                     scaleFactor=1.1,
                                                     minNeighbors=5
                                                     )

                # convert the input frame from BGR to RGB

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # the facial embeddings for face in input

                encodings = face_recognition.face_encodings(rgb)
                names = []
                face_recognition_flag = False

                # loop over the facial embeddings incase

                # we have multiple embeddings for multiple faces
                if not face_recognition_flag:
                    for encoding in encodings:
                        # Compare encodings with encodings in data["encodings"]
                        # Matches contain array with boolean values and True for the embeddings it matches closely
                        # and False for rest
                        matches = face_recognition.compare_faces(data["encodings"], encoding)
                        print("matches>>>>>>>>>>", matches)
                        # set name = unknown if no encoding matches
                        name = "Unknown"
                        # check to see if we have found a match
                        if True in matches:
                            # Find positions at which we get True and store them
                            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                            counts = {}
                            # loop over the matched indexes and maintain a count for
                            # each recognized face face
                            print('matchedIdxs>>>>>>>>>>>>>>>>', matchedIdxs)
                            if len(matchedIdxs) == 1:
                                face_recognition_flag = True
                                name = data["names"][matchedIdxs[0]]
                                counts[name] = counts.get(name, 0) + 1
                                print('count>>>>>>>>', counts)
                                name = max(counts, key=counts.get)
                                names.append(name)
                                print('names>>>>>>>>>>>>', names)
                                ##############################################
                                for ((x, y, w, h), name) in zip(faces, names):
                                    # rescale the face coordinates
                                    # draw the predicted face name on the image
                                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                    cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                                                0.75, (0, 255, 0), 2)

                if face_recognition_flag:
                    cv2.imshow("Detected Frame", frame)
                    cv2.waitKey(5000)
                    video_capture.release()
                    cv2.destroyAllWindows()
                    file_name = names[0] + '.jpg'
                    citizendetails_vo.citizen_filename = file_name
                    citizen_vo_list = citizendetails_dao.view_file_path(citizendetails_vo)
                    return render_template('traffic_police_station/addFineReceipt.html',
                                           citizen_vo_list=citizen_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_perform_face_recognize route exception occured>>>>>>>>>>", ex)


@app.route('/traffic_police_station/insert_finereceipt', methods=['POST'])
def user_insert_finereceipt():
    try:
        if admin_login_session() == "user":
            finereciept_vo = FineReceiptVO()
            finereceipt_dao = FineReceiptDAO()
            citizen_id = request.form.get('citizenId')
            citizen_username = request.form.get('citizenUsername')
            citizen_contact = request.form.get('citizenContact')
            citizen_email = request.form.get('citizenEmail')
            finereceipt_datetime = datetime.datetime.now()

            citizen_fine_reason = request.form.getlist('choice')
            citizen_fine_reason = ", ".join(citizen_fine_reason)
            citizen_fine_amount = request.form.get('citizenFineAmount')
            finereciept_vo.finereceipt_citizendetails_id = citizen_id
            finereciept_vo.finereceipt_reason = citizen_fine_reason
            finereciept_vo.finereceipt_datetime = finereceipt_datetime
            finereciept_vo.finereceipt_amount = citizen_fine_amount
            finereceipt_dao.insert_finereceipt(finereciept_vo)
            print("data inserted succesfully >>>>>>>>>>>>>>>>>>")

            sender = "aibasedememo@gmail.com"
            receiver = citizen_email
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "E-Memo Fine Reciept"
            body = 'Your Fine Details Described Below : \n\n\t Citizen Username : {} \n\t Citizen Contact : {} \n\t Citizen E-Mail : {} \n\t Citizen Fine Reason : {} \n\t Citizen Fine Amount : {}'.format(
                citizen_username, citizen_contact, citizen_email, citizen_fine_reason, citizen_fine_amount)

            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "AiBasedEMemo")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()
            return redirect('/traffic_police_station/view_fine_receipt')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_insert_fine_receipt route exception occured>>>>>>>>>>", ex)


@app.route('/traffic_police_station/view_fine_receipt')
def user_view_fine_receipt():
    try:
        if admin_login_session() == "user":
            print('--------------------------- before dao call')
            finereceipt_dao = FineReceiptDAO()
            finereceipt_vo_list = finereceipt_dao.user_view_finereceipt()
            print('---------------------------after dao call')
            print("finereceipt_vo_list>>>>>>>>>", finereceipt_vo_list)
            return render_template('traffic_police_station/viewFineReceipt.html',
                                   finereceipt_vo_list=finereceipt_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_view_fine_receipt route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_fine_receipt')
def admin_view_fine_receipt():
    try:
        if admin_login_session() == "admin":
            finereceipt_dao = FineReceiptDAO()
            finereceipt_vo_list = finereceipt_dao.admin_view_finereceipt()
            print("finereceipt_vo_list>>>>>>>>>", finereceipt_vo_list)
            return render_template('admin/viewFineReceipt.html',
                                   finereceipt_vo_list=finereceipt_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_fine_receipt route exception occured>>>>>>>>>>", ex)
