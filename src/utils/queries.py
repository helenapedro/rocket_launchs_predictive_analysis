from .db import get_connection

def fetch_unique_launch_sites():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT LAUNCH_SITE FROM SPACEXTBL")
    rows = cursor.fetchall()
    connection.close()
    return [row[0] for row in rows]

def fetch_launch_count(launch_site):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM SPACEXTBL WHERE LAUNCH_SITE = %s"
    cursor.execute(query, (launch_site,))
    result = cursor.fetchone()[0]
    connection.close()
    return result

def fetch_payload_mass_by_customer(customer):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = %s"
    cursor.execute(query, (customer,))
    result = cursor.fetchone()[0]
    connection.close()
    return result

def fetch_avg_payload_mass_by_booster(booster_version):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE %s"
    cursor.execute(query, (booster_version,))
    result = cursor.fetchone()[0]
    connection.close()
    return result

def fetch_mission_outcomes():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT MISSION_OUTCOME, COUNT(MISSION_OUTCOME) AS TOTAL_NUMBER FROM SPACEXTBL GROUP BY MISSION_OUTCOME"
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows

def fetch_failed_landings():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT LANDING_OUTCOME, BOOSTER_VERSION, LAUNCH_SITE FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)'"
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows