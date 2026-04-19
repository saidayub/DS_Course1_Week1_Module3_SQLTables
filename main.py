# CodeGrade step0
# Run this cell without changes

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# CodeGrade step1
# Replace None with your code
df_boston = pd.read_sql("""SELECT firstName, lastName, jobTitle
                           FROM employees e
                           INNER JOIN offices o ON  o.officeCode = e.officeCode
                           WHERE o.city = 'Boston'
             """,conn)

# CodeGrade step2
# Replace None with your code
df_zero_emp = pd.read_sql("""SELECT 
                                o.officeCode, 
                                o.city, 
                                o.country
                            FROM offices o
                            LEFT JOIN employees e ON o.officeCode = e.officeCode
                            WHERE e.employeeNumber IS NULL;
                            """, conn)

# CodeGrade step3
# Replace None with your code
df_employee = pd.read_sql("""
                        SELECT 
                            e.firstName, 
                            e.lastName, 
                            o.city, 
                            o.state
                        FROM employees e
                        LEFT JOIN offices o ON e.officeCode = o.officeCode
                        ORDER BY e.firstName, e.lastName;
                        """,conn)
# CodeGrade step4
# Replace None with your code
df_contacts = pd.read_sql("""
                        SELECT 
                            c.contactFirstName, 
                            c.contactLastName, 
                            c.phone, 
                            c.salesRepEmployeeNumber
                        FROM customers c
                        LEFT JOIN orders o ON c.customerNumber = o.customerNumber
                        WHERE o.orderNumber IS NULL
                        ORDER BY c.contactLastName;
                        """, conn)
# CodeGrade step5
# Replace None with your code
df_payment = pd.read_sql("""SELECT 
                                c.contactFirstName, 
                                c.contactLastName, 
                                p.paymentDate, 
                                p.amount
                            FROM customers c
                            INNER JOIN payments p ON c.customerNumber = p.customerNumber
                            ORDER BY CAST(p.amount AS FLOAT) DESC;
                            """, conn)
# CodeGrade step6
# Replace None with your code
df_credit = pd.read_sql("""SELECT 
                            e.employeeNumber, 
                            e.firstName, 
                            e.lastName, 
                            COUNT(c.customerNumber) AS customer_count
                        FROM employees e
                        INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                        GROUP BY e.employeeNumber, e.firstName, e.lastName
                        HAVING AVG(c.creditLimit) > 90000
                        ORDER BY customer_count DESC;
                        """,conn)
# CodeGrade step7
# Replace None with your code
df_product_sold = pd.read_sql("""SELECT 
                                    p.productName, 
                                    COUNT(od.orderNumber) AS numorders, 
                                    SUM(od.quantityOrdered) AS totalunits
                                FROM products p
                                JOIN orderdetails od ON p.productCode = od.productCode
                                GROUP BY p.productName
                                ORDER BY totalunits DESC;
""",conn)
# CodeGrade step8
# Replace None with your code
df_total_customers = pd.read_sql("""
                                SELECT 
                                    p.productName, 
                                    p.productCode, 
                                    COUNT(DISTINCT o.customerNumber) AS numpurchasers
                                FROM products p
                                JOIN orderdetails od ON p.productCode = od.productCode
                                JOIN orders o ON od.orderNumber = o.orderNumber
                                GROUP BY p.productCode, p.productName
                                ORDER BY numpurchasers DESC;
""",conn)
# CodeGrade step9
# Replace None with your code
df_customers = pd.read_sql("""
                        SELECT 
                                o.officeCode, 
                                o.city, 
                                COUNT(c.customerNumber) AS n_customers
                        FROM offices o
                            JOIN employees e ON o.officeCode = e.officeCode
                            JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                            GROUP BY o.officeCode, o.city
                            ORDER BY n_customers DESC;
                            """, conn)
# CodeGrade step10
# Replace None with your code
df_under_20 = pd.read_sql("""
                        WITH UnderperformingProducts AS (
                        SELECT od.productCode
                        FROM orderdetails od
                        JOIN orders o ON od.orderNumber = o.orderNumber
                        GROUP BY od.productCode
                        HAVING COUNT(DISTINCT o.customerNumber) < 20
                            )
                            SELECT DISTINCT
                                e.employeeNumber, 
                                e.firstName, 
                                e.lastName, 
                                o.city, 
                                o.officeCode
                            FROM employees e
                            JOIN offices o ON e.officeCode = o.officeCode
                            JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                            JOIN orders ord ON c.customerNumber = ord.customerNumber
                            JOIN orderdetails od ON ord.orderNumber = od.orderNumber
                            WHERE od.productCode IN (SELECT productCode FROM UnderperformingProducts);
                            """,conn)
# Run this cell without changes

conn.close()