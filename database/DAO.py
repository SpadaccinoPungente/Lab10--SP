from database.DB_connect import DBConnect
from model.country import Country


class DAO:
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM country"
        cursor.execute(query)

        res = []
        for row in cursor: res.append(Country(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdges(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
                SELECT state1no, state2no 
                FROM contiguity 
                WHERE year <= %s AND conttype = 1
                AND state1no < state2no
                """
        cursor.execute(query, (anno,))

        res = cursor.fetchall()

        cursor.close()
        conn.close()
        return res