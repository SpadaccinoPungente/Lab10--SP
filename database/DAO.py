from database.DB_connect import DBConnect
from model.country import Country


class DAO:
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "select * from countries"
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
                select c.state1no, c.state2no 
                from contiguity c
                where c.conttype = 1
                and c.year <= %s
                """
        cursor.execute(query, (anno,))

        res = cursor.fetchall()

        cursor.close()
        conn.close()
        return res