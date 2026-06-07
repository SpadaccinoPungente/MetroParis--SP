from database.DB_connect import DBConnect
from model.fermata import Fermata


class DAO:

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def existsEdge(n1, n2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = """
                SELECT COUNT(*) FROM connessione
                WHERE id_stazP = %s AND id_stazA = %s
                """
        cursor.execute(query, (n1.id_fermata, n2.id_fermata))

        riga = cursor.fetchone()
        exists_edge_flag = (riga[0] > 0) # if riga else False # per gestire anche il caso riga = None
        # La query SELECT COUNT(*) restituisce sempre una riga, anche se il conteggio è zero.
        # - Se l'arco esiste, cursor.fetchone() restituirà qualcosa come (1,).
        # - Se l'arco non esiste, cursor.fetchone() restituirà (0,).
        # Una tupla contenente lo zero (0,) non è vuota, quindi viene valutata come True.
        # Di conseguenza, exists_edge_flag diventerà True in ogni caso, creando archi anche tra stazioni non collegate.

        cursor.close()
        conn.close()
        return exists_edge_flag

    @staticmethod
    def getNeighbors(n):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = """
                SELECT id_stazA
                FROM connessione
                WHERE id_stazP = %s
                """
        cursor.execute(query, (n.id_fermata,))
        result = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = """
                SELECT id_stazP, id_stazA
                FROM connessione
                """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesWithWeight():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = """
                SELECT c.id_stazP, c.id_stazA, COUNT(*) AS weight
                FROM connessione c
                GROUP BY c.id_stazP, c.id_stazA
                """
        cursor.execute(query)
        result = cursor.fetchall() # la list comprehension non serve, è già ciò che viene restituito da cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesWithVelocity():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)  # Usiamo dictionary per comodità di lettura
        query = """
                SELECT c.id_stazP, c.id_stazA, l.velocita
                FROM connessione c
                JOIN linea l ON c.id_linea = l.id_linea
                """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result