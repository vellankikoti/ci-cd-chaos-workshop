from testcontainers.mysql import MySqlContainer
import sqlalchemy

def test_mysql_container():
    print("🐳 Spinning up MySQL in Docker... (Testcontainers magic!)")
    with MySqlContainer('mysql:8.0') as mysql:
        engine = sqlalchemy.create_engine(mysql.get_connection_url())
        with engine.connect() as conn:
            result = conn.execute("SELECT VERSION()")
            version = result.fetchone()[0]
            print(f"✅ Connected to MySQL version: {version}")
            assert version.startswith("8."), "MySQL version is not 8.x! Chaos wins!"
    print("🎉 MySQL test passed! Your pipeline is chaos-resistant!") 