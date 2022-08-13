import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, flash, redirect, url_for
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.dao.traffic_police_station_dao import TrafficPoliceStationDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.traffic_police_station_vo import TrafficPoliceStationVO
from base.com.dao.area_dao import AreaDAO


@app.route('/admin/load_user', methods=['GET'])
def admin_load_user():
    try:
        if admin_login_session() == "admin":
            area_dao = AreaDAO()
            area_vo_list = area_dao.view_area()
            return render_template('admin/addUser.html', area_vo_list=area_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_load_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_user', methods=['POST'])
def admin_insert_user():
    try:
        if admin_login_session() == "admin":
            login_vo = LoginVO()
            login_dao = LoginDAO()

            traffic_police_station_vo = TrafficPoliceStationVO()
            traffic_police_station_dao = TrafficPoliceStationDAO()

            traffic_police_station_name = request.form.get('trafficPolicestationName')
            traffic_police_station_area_id = request.form.get('trafficPolicestationAreaId')
            traffic_police_head_name = request.form.get('trafficPoliceHeadName')
            traffic_police_head_contact = request.form.get('trafficPoliceHeadContact')
            traffic_police_head_username = request.form.get('trafficPoliceHeadUsername')

            login_password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
            print("in admin_insert_user login_password>>>>>>>>>", login_password)

            login_secretkey = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(32))
            print("in admin_insert_user login_secretkey>>>>>>>", login_secretkey)
            login_vo_list = login_dao.view_login()
            print("in admin_insert_user login_vo_list>>>>>>", login_vo_list)
            if len(login_vo_list) != 0:
                for i in login_vo_list:
                    if i.login_secretkey == login_secretkey:
                        login_secretkey = ''.join(
                            (random.choice(string.ascii_letters + string.digits)) for x in range(32))
                    if i.login_username == traffic_police_head_username:
                        error_message = "The username is already exists !"
                        flash(error_message)
                        return redirect(url_for('admin_view_user'))

            sender = "aibasedememo@gmail.com"
            receiver = traffic_police_head_username
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "Your Password For  AIBasedEMemo"
            msg.attach(MIMEText(login_password, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "AiBasedEMemo")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            login_vo.login_username = traffic_police_head_username
            login_vo.login_password = login_password
            login_vo.login_role = "user"
            login_vo.login_status = "active"
            login_vo.login_secretkey = login_secretkey
            login_dao.insert_login(login_vo)

            traffic_police_station_vo.traffic_police_station_name = traffic_police_station_name
            traffic_police_station_vo.traffic_police_station_area_id = traffic_police_station_area_id
            traffic_police_station_vo.traffic_police_head_name = traffic_police_head_name
            traffic_police_station_vo.traffic_police_head_contact = traffic_police_head_contact
            traffic_police_station_vo.traffic_police_station_login_id = login_vo.login_id
            traffic_police_station_dao.insert_user(traffic_police_station_vo)
            return redirect(url_for('admin_view_user'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_insert_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_user')
def admin_view_user():
    try:
        if admin_login_session() == "admin":
            traffic_police_station_dao = TrafficPoliceStationDAO()
            traffic_police_station_vo_list = traffic_police_station_dao.view_user()
            return render_template('admin/viewUser.html', traffic_police_station_vo_list=traffic_police_station_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_user route exception occured>>>>>>>>>>", ex)
        
        
