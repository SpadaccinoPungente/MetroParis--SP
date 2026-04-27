from database.DB_connect import DBConnect
from model.fermata import Fermata
from model.connessione import Connesione


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasconn(u:Fermata, v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazP = %s and c.id_stazA = %s"
        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0

    @staticmethod
    def getvicini(u:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazP = %s"
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connesione(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c "
        cursor.execute(query)

        for row in cursor:
            result.append(Connesione(**row))
        cursor.close()
        conn.close()
        return result