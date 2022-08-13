from base import app
from flask import render_template, redirect, request, url_for
from base.com.dao.area_dao import AreaDAO
from base.com.dao.crossroad_dao import CrossroadDAO
from base.com.vo.crossroad_vo import CrossroadVO
from base.com.controller.login_controller import admin_login_session, admin_logout_session

@app.route('/admin/load_crossroad')
def admin_load_crossroad():
    try:
        if admin_login_session() == "admin":
            area_dao = AreaDAO()
            area_vo_list = area_dao.view_area()
            return render_template('admin/addCrossroad.html', area_vo_list=area_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_crossroad page route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_crossroad', methods=['POST'])
def admin_insert_crossroad():
    try:
        if admin_login_session() == "admin":
            crossroad_vo = CrossroadVO()
            crossroad_dao = CrossroadDAO()
            crossroad_vo.crossroad_area_id = request.form.get('crossroadAreaId')
            crossroad_vo.crossroad_name = request.form.get('crossroadName')
            crossroad_dao.insert_crossroad(crossroad_vo)
            return redirect(url_for('admin_view_crossroad'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_insert_crossroad page route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_crossroad')
def admin_view_crossroad():
    try:
        if admin_login_session() == "admin":
            crossorad_dao = CrossroadDAO()
            crossroad_vo_list = crossorad_dao.view_crossroad()
            return render_template('admin/viewCrossroad.html', crossroad_vo_list=crossroad_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_crossroad page route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_crossroad')
def admin_delete_crossroad():
    try:
        if admin_login_session() == "admin":
            crossoroad_dao = CrossroadDAO()
            crossroad_vo = CrossroadVO()
            crossroad_id = request.args.get('crossroadId')
            crossroad_vo.crossroad_id = crossroad_id
            crossoroad_dao.delete_crossroad(crossroad_vo)
            return redirect(url_for('admin_view_crossroad'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_crossroad page route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_crossroad')
def admin_edit_crossroad():
    try:
        if admin_login_session() == "admin":
            crossroad_dao = CrossroadDAO()
            crossroad_vo = CrossroadVO()
            area_dao = AreaDAO()
            crossroad_vo.crossroad_id = request.args.get('crossroadId')

            crossroad_vo_list = crossroad_dao.edit_crossroad(crossroad_vo)
            area_vo_list = area_dao.view_area()
            return render_template('admin/editCrossroad.html', crossroad_vo_list=crossroad_vo_list,
                                   area_vo_list=area_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_crossroad page route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_crossroad', methods=['POST'])
def admin_update_crossroad():
    try:
        if admin_login_session() == "admin":
            crossroad_dao = CrossroadDAO()
            crossroad_vo = CrossroadVO()
            crossroad_vo.crossroad_id = request.form.get('crossroadId')
            crossroad_vo.crossroad_name = request.form.get('crossroadName')
            crossroad_vo.crossroad_area_id = request.form.get('crossroadAreaId')
            crossroad_dao.update_crossroad(crossroad_vo)
            return redirect(url_for('admin_view_crossroad'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_crossroad page route exception occured>>>>>>>>>>", ex)
