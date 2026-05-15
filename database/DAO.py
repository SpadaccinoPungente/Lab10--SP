from database.DB_connect import DBConnect
from model.country import Country


class DAO:

    @staticmethod
    def get_all_countries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT CCode, StateAbb, StateNme FROM country"
        cursor.execute(query)

        result = []
        for row in cursor: result.append(Country(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_borders(year, id_map):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Filtriamo direttamente in SQL per anno e confine via terra (conttype = 1)
        query = """
                SELECT state1no, state2no
                FROM contiguity
                WHERE year <= %s AND conttype = 1
                """
        cursor.execute(query, (year,))

        result = []
        for row in cursor:
            c1 = id_map.get(row['state1no'])
            c2 = id_map.get(row['state2no'])
            # Se entrambi gli stati esistono, aggiungiamo l'arco
            if c1 and c2: result.append((c1, c2))

        cursor.close()
        conn.close()
        return result