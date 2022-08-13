from datetime import timedelta
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string, random, smtplib
from base import app
from flask import render_template, redirect, request, url_for, make_response, flash, session
from base.com.dao.login_dao import LoginDAO
from base.com.vo.login_vo import LoginVO

global_loginvo_list = []
global_login_secretkey_set = {0}


@app.route('/', methods=['GET'])
def admin_load_login():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        print("admin_load_login route exception occured>>>>>>>>>>", ex)


@app.route("/admin/validate_login", methods=['POST'])
def admin_validate_login():
    try:
        global global_loginvo_list
        global global_login_secretkey_set

        login_username = request.form.get('loginUsername')
        login_password = request.form.get('loginPassword')

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username
        login_vo.login_password = login_password

        login_vo_list = login_dao.validate_login(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        print("in admin_validate_login login_list>>>>>>>>>>>", login_list)
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username or password is incorrect !'
            flash(error_message)
            return redirect(url_for('admin_load_login'))
        elif login_list[0]['login_status'] == 'inactive':
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect(url_for('admin_load_login'))
        else:
            for row1 in login_list:
                login_id = row1['login_id']
                login_username = row1['login_username']
                login_role = row1['login_role']
                login_secretkey = row1['login_secretkey']
                login_vo_dict = {
                    login_secretkey: {'login_username': login_username, 'login_role': login_role, 'login_id': login_id}}
                if len(global_loginvo_list) != 0:
                    for i in global_loginvo_list:
                        tempList = list(i.keys())
                        global_login_secretkey_set.add(tempList[0])
                    login_secretkey_list = list(global_login_secretkey_set)
                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:
                    global_loginvo_list.append(login_vo_dict)
                if login_role == 'admin':
                    response = make_response(redirect(url_for('admin_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')
                    print("in admin_validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in admin_validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response
                elif login_role == 'user':
                    response = make_response(redirect(url_for('user_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')
                    print("in admin_validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in admin_validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response
                else:
                    return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_validate_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_dashboard', methods=['GET'])
def admin_load_dashboard():
    try:
        if admin_login_session() == 'admin':
            login_username = request.cookies.get('login_username')
            return render_template('admin/index.html', login_username=login_username)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/user/load_dashboard', methods=['GET'])
def user_load_dashboard():
    try:
        if admin_login_session() == 'user':
            login_username = request.cookies.get('login_username')
            return render_template('traffic_police_station/index.html', login_username=login_username)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/admin/login_session')
def admin_login_session():
    try:
        global global_loginvo_list
        login_role_flag = ""
        print("before login_role_flag=", login_role_flag)
        print("before len(login_role_flag)>>>>>>>>>>", len(login_role_flag))

        login_secretkey = request.cookies.get('login_secretkey')
        print("in admin_login_session login_secretkey>>>>>>>>>", login_secretkey)

        if login_secretkey is None:
            return redirect('/')
        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                elif i[login_secretkey]['login_role'] == 'user':
                    login_role_flag = "user"

        print("after login_role_flag>>>>>>>>>>", login_role_flag)
        print("after len(login_role_flag)>>>>>>>>>>", len(login_role_flag))

        if len(login_role_flag) != 0:
            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")
        return login_role_flag
    except Exception as ex:
        print("admin_login_session route exception occured>>>>>>>>>>", ex)


@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session():
    try:
        global global_loginvo_list
        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')
        print("in admin_logout_session login_secretkey>>>>>>>>>", login_secretkey)
        print("in admin_logout_session login_username>>>>>>>>>", login_username)
        print("in admin_logout_session type of login_secretkey>>>>>>>>>", type(login_secretkey))
        print("in admin_logout_session type of login_username>>>>>>>>>", type(login_username))

        response = make_response(redirect('/'))
        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', login_secretkey, max_age=0)
            response.set_cookie('login_username', login_username, max_age=0)
            for i in global_loginvo_list:
                if login_secretkey in i.keys():
                    global_loginvo_list.remove(i)
                    print("in admin_logout_session global_loginvo_list>>>>>>>>>>>>>>>", global_loginvo_list)
                    break
        return response
    except Exception as ex:
        print("in admin_logout_session route exception occured>>>>>>>>>>", ex)


@app.route('/admin/block_user')
def admin_block_user():
    try:
        login_id = request.args.get('loginId')
        login_vo = LoginVO()
        login_dao = LoginDAO()
        login_vo.login_id = login_id
        login_vo.login_status = 'inactive'
        login_dao.block_user(login_vo)
        return redirect(url_for('admin_view_user'))
    except Exception as ex:
        print("in admin_block_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/unblock_user')
def admin_unblock_user():
    try:
        login_id = request.args.get('loginId')
        login_vo = LoginVO()
        login_dao = LoginDAO()
        login_vo.login_id = login_id
        login_vo.login_status = 'active'
        login_dao.unblock_user(login_vo)
        return redirect(url_for('admin_view_user'))
    except Exception as ex:
        print("in admin_unblock_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_forgot_password')
def admin_load_forgot_password():
    try:
        return render_template('admin/loadForgotPassword.html')
    except Exception as ex:
        print("in admin_load_forgot_password route exception occured>>>>>>>>>>", ex)


def generate_otp():
    global now
    now = time.time()
    otp = int(''.join((random.choice(string.digits)) for x in range(4)))
    # print(type(otp))
    print("otp >>>>>>>>>>>>>", otp)
    session['otp'] = otp

    sender = "aibasedememo@gmail.com"
    receiver = session['login_username']
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "OTP From AI Based E-Memo"
    body = "Your OTP for Forget Password is {}\n\t Please Validate Within 60 Seconds.".format(otp)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "AiBasedEMemo")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


@app.route('/admin/validate_username', methods=['POST'])
def admin_validate_username():
    try:

        login_dao = LoginDAO()
        login_vo = LoginVO()
        login_vo.login_username = request.form.get('username')
        login_vo_list = login_dao.validate_username(login_vo)
        print("login_vo_list>>>>>>>>>>", login_vo_list)
        if len(login_vo_list) == 0:
            error_message = 'username not exits !'
            flash(error_message)
            return redirect('/')
        else:
            session['login_id'] = login_vo_list[0].login_id
            session['login_username'] = login_vo_list[0].login_username
            generate_otp()
            return render_template("admin/loadSendOtp.html")
    except Exception as ex:
        print("in admin_validate_username route exception occured>>>>>>>>>>", ex)


@app.route('/admin/resend_otp')
def admin_resend_otp():
    try:
        generate_otp()
        return render_template('admin/loadSendOtp.html')
    except Exception as ex:
        print("in admin_resend_otp route exception occured>>>>>>>>>>", ex)


@app.route('/admin/validate_otp', methods=['POST'])
def admin_validate_otp():
    try:
        later = time.time()
        if int(later - now) < 60:
            user_otp = int(request.form.get('otp'))
            session_otp = session['otp']
            if user_otp == session_otp:
                return render_template("admin/ResetPassword.html")
            else:
                session.pop('otp')
                error_message = ' Invalid OTP ! Click On Resend OTP'
                flash(error_message)
                return render_template("admin/loadSendOtp.html")
        else:
            error_message = 'Session Time out! Click on Resend OTP'
            flash(error_message)
            return render_template("admin/loadSendOtp.html")

    except Exception as ex:
        print("in admin_validate_otp route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_reset_password', methods=['POST'])
def admin_update_reset_password():
    try:
        new_password = request.form.get('newPassword')
        print("new_password>>>>>>>>>>>>>>", new_password)
        confirm_password = request.form.get('confirmPassword')
        print("confirm_password>>>>>>>>>>>", confirm_password)
        login_id = session['login_id']
        if new_password == confirm_password:
            login_vo = LoginVO()
            login_dao = LoginDAO()
            login_vo.login_password = confirm_password
            login_vo.login_id = login_id
            login_dao.update_password(login_vo)
            return redirect('/')
        else:
            error_message = 'Both Passwords Are Not Matched Please Enter Again !'
            flash(error_message)
            return redirect(url_for('admin_load_reset_password'))
    except Exception as ex:
        print("in admin_update_reset_password route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_reset_password')
def admin_load_reset_password():
    try:
        return render_template('admin/resetPassword.html')
    except Exception as ex:
        print("in admin_load_reset_password route exception occured>>>>>>>>>>", ex)
