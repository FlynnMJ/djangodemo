import json
import time
import pyodbc

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.db import connections


def timestamp_datatime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt


def get_connection():
    print("get connection")
    conn = pyodbc.connect('DRIVER=SQL Server Native Client 10.0;SERVER=127.0.0.1;DATABASE=znykt_auto;UID=sa;PWD=123456')
    return conn


def close_connection(conn):
    print('close connection')
    conn.close()


@csrf_exempt
@api_view(http_method_names=['POST', 'GET'])  # 只允许post
@permission_classes((permissions.AllowAny,))
def getrecord(request):
    conn = get_connection()
    resp = []
    try:
        parameter = request.data
        print(parameter)
        for p in parameter:
            print(p)
            carNumber = p['carNumber']
            print(carNumber)
            cur = conn.cursor()
            cur.execute('SELECT TOP 1  CPH car_number, InTime enter_time  FROM MYCARCOMERECORD where cph= %s',
                        (carNumber,))
            results = cur.fetchall()
            for row in results:
                carNumber = row[0];
                startTime = row[1];
                obj = {'carNumber': carNumber, 'startTime': startTime}
                resp.append(obj)
                print(carNumber)
                print(startTime)
    finally:
        close_connection(conn)

    # conn = get_connection()
    # resp = []
    # try:
    #     cur = conn.cursor()
    #     cur.execute('SELECT TOP 1  CPH car_number, InTime enter_time  FROM MYCARCOMERECORD ')
    #     results = cur.fetchall()
    #     for row in results:
    #         carNumber = row[0];
    #         startTime = row[1];
    #         obj = {'carNumber': carNumber, 'startTime': startTime}
    #         resp.append(obj)
    # finally:
    #     close_connection(conn)
    return Response(resp)


@csrf_exempt
@api_view(http_method_names=['post'])  # 只允许post
@permission_classes((permissions.AllowAny,))
def open(request):
    conn = get_connection()
    try:
        parameter = request.data
        for p in parameter:
            print(p)
            carNumber = p['carNumber']
            leaveTime = p['leaveTime']
            leaveTime = timestamp_datatime(leaveTime / 1000)
            print(carNumber)
            print(leaveTime)
            # 更新数据库
            cur = conn.cursor()
            cur.execute("update MYCARCOMERECORD set InTime=%s WHERE cph=%s",
                        (leaveTime, carNumber))
    finally:
        close_connection(conn)

    resp = 'success'
    return Response({'code': resp})
