from classes import Connection
from flask import jsonify, abort
import datetime
import csv
import json
import logging


class Weight():

    ################################################
    # check if date_text is valid Datetime
    ################################################
    @staticmethod
    def validate(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y%m%d%I%M%S')
        except ValueError:
            return 0
        return 1



    ################################################################
    # get weights between to points (duration)  t1 - t2 & filter
    #   -  t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
    #   -  f - comma delimited list of directions. default is "in,out,none"
    #   - filter = “in,out,none”
    #   - default t1 is "today at 000000". default t2 is "now". 
    #   - Returns an array of json objects, one per weighing 
    ################################################################
    
    @staticmethod
    def weights_get(time_from, time_to, filter):

        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")


        ##############################    Valid start_time argument   ###########################        
        if time_from is None:
            t1 = datetime.datetime.now().strftime("%Y%m%d"+"000000")
            logging.warning("query run with default Time ' :  {} - 404 ".format(str(t1)))            
        elif Weight.validate(str(time_from)):
            t1 = time_from
        else:
            logging.warning("datetime is not valid ' :  {} - 404 ".format(str(time_from)))
            abort(404)


        ##############################    Valid end_time  argument   ###########################

        if time_to is None:
            t2 = time_actual
            logging.warning("item id is not valid 'None' :  {} - 404 ".format(str(t2)))

        elif Weight.validate(str(time_to)):
            t2 = time_to
            logging.warning("query run with default Time ' :  {} - 404 ".format(str(t2)))
        else:
            logging.warning("datetime is not valid ' :  {} - 404 ".format(str(time_to)))
            abort(404)

        ##############################     execute Query       ###########################

        f = []
        if filter is None:
            f = ["in", "out", "none"]
        else:
            f = str(filter).split(',')

        sql_select_Query = "select * from transactions where " + \
            "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        list_of_transactions = []

        for row in rows:
            if row[2] in f:
                # na if some of containers have unknown tara
                if any(x in str(row[4]).split(',') for x in Weight.unknown_weights()):
                    neto = "na"
                else:
                    neto = row[7]
                transact = {
                    'id': row[0],
                    'direction': row[2],
                    'bruto': row[5],
                    'neto': neto,
                    'produce': row[8],
                    'containers': str(row[4]).split(',')
                }
                list_of_transactions.append(transact)

        return jsonify({'transactions': list_of_transactions})

 
    # Returns a list of all recorded containers that have unknown weight
    @staticmethod
    def unknown_weights():
        list_of_unknown = []
        sql_select_Query = "select * from containers_registered"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        for row in rows:
            if not str(row[1]).isdigit():
                list_of_unknown.append(row[0])
        return list_of_unknown
    
    # upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers. 
    # File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    @staticmethod
    def batch_weight(fileName):
        flag = False
        ids = []
        weights = []
        convert = False
        print(type(fileName))
        print(fileName)
        if fileName.endswith('.csv'):
            try:
                spamReader = csv.reader(
                    open('./in/'+fileName, newline=''), delimiter=',', quotechar='|')
                ids = []
                weights = []
                for row in spamReader:
                    ids.append(row[0])
                    weights.append(row[1])
                if str(weights[0]) == '"lbs"':
                    convert = True
                weights.pop(0)
                ids.pop(0)
                flag = True
            except IOError as e:  # TODO write to LOGFILE
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror)), 404

        elif fileName.endswith('.json'):
            try:
                with open('./in/'+fileName) as json_file:
                    data = json.loads(json_file.read())
                if data[1]["unit"] == 'lbs':
                    convert = True
                for truck in data:
                    ids.append(truck["id"])
                    weights.append(truck["weight"])
                flag = True
            except IOError as e:  # TODO write to LOGFILE
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror)), 404

        if convert:
            for i in range(len(weights)):
                weights[i] = str(int(0.453592*float(weights[i])))
        for i in range(len(ids)):
            ids[i] = '"' + ids[i] + '"'
            #print("id:"+ids[i]+", weight: "+weights[i])
            #toSend.append("('{}', '{}', 'kg')".format(ids[i], weights[i]))
            query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES(%s,%s,'kg');" % (
                ids[i], weights[i])
            print(query)
            Connection.Mysql.exec_query(query)
            print(query)

        if flag:
            return "OK"
        else:
            return "Error", 404

    @staticmethod
    def container_weight(id_num):
        sql_select_Query = "select * from containers_registered where container_id=" + "'" + id_num + "'"
        rows = Connection.Mysql.exec_query(sql_select_Query)
        if not rows:
            abort(404)
        return str(rows[0][1])
    
    
    @staticmethod
    def last_action(id_num,direction,in_direction=False):
        if in_direction:
            sql_select_Query = "select * from transactions where truck=" + "'" + id_num + "'" + " and direction=" + "'in'" + " order by datetime desc limit 1" 
        if direction:
            sql_select_Query = "select * from transactions where truck=" + "'" + id_num + "'" + " and direction in " + "('in','out')" + " order by datetime desc limit 1" 
        else:
            sql_select_Query = "select * from transactions where truck=" + "'" + id_num + "'" + " order by datetime desc limit 1" 
        
        rows = Connection.Mysql.exec_query(sql_select_Query)
        if not rows or rows[0][2] == "none":
            return "not found"
            
        return rows[0]
   
   
    @staticmethod
    def all_containers_here(containers_list):
        for id_num in containers_list:
            sql_select_Query = "select * from containers_registered where container_id=" + "'" + id_num + "'"
            rows = Connection.Mysql.exec_query(sql_select_Query)
            if not rows:
                return False

        return True