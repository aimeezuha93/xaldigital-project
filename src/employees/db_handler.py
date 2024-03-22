import os
import logging
from sqlalchemy import create_engine, text


class DbOperations:
    def __init__(self):
        self.engine = create_engine(os.getenv("DB_URL"))

    def save_in_db(
        self,
        first_name: str,
        last_name: str,
        company_name: str,
        address: str,
        city: str,
        state: str,
        zip: int,
        phone1: str,
        phone2: str,
        email: str,
        department: str,
    ) -> None:
        query = f"""
                    INSERT INTO public.employees (
                        "first_name",
                        "last_name",
                        "company_name",
                        "address",
                        "city",
                        "state",
                        "zip",
                        "phone1",
                        "phone2",
                        "email",
                        "department"
                    ) VALUES (
                        '{first_name}',
                        '{last_name}',
                        '{company_name}',
                        '{address}',
                        '{city}',
                        '{state}',
                        '{zip}',
                        '{phone1}',
                        '{phone2}',
                        '{email}',
                        '{department}');
                """
        with self.engine.begin() as conn:
            try:
                conn.execute(text(query))
            except Exception as e:
                logging.error(f"Postgres Error: {e}")
            finally:
                conn.close()

    def get_from_db(self, email: str):
        query = f"""
                    SELECT * from public.employees
                    WHERE email = '{email}'
                """
        with self.engine.begin() as conn:
            try:
                r = conn.execute(text(query)).fetchall()
                return r
            except Exception as e:
                logging.error(f"Postgres Error: {e}")
            finally:
                conn.close()

    def update_from_db(self, email: str, department: str) -> None:
        query = f"""
                    UPDATE public.employees
                    SET department = '{department}'
                    WHERE email = '{email}'
                """
        with self.engine.begin() as conn:
            try:
                conn.execute(text(query))
            except Exception as e:
                logging.error(f"Postgres Error: {e}")
            finally:
                conn.close()

    def delete_from_db(self, email: str):
        query = f"""
                    DELETE FROM public.employees
                    WHERE email = '{email}'
                """
        with self.engine.begin() as conn:
            try:
                conn.execute(text(query))
            except Exception as e:
                logging.error(f"Postgres Error: {e}")
            finally:
                conn.close()
