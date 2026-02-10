### **I. What is SQLi?**

- Attack on a web application's database server.
- Malicious SQL queries are executed.
- Consequences: Data theft, deletion, alteration, authentication bypass.
### **II. Database Basics:**

- **Database:** Organized collection of data.
- **DBMS (Database Management System):** Controls the database (MySQL, Microsoft SQL Server, PostgreSQL, SQLite).
- **Tables:** Store related data within a database.
- **Columns (Fields):** Define the type of data stored (integers, strings, dates).
- **Rows (Records):** Individual lines of data.
- **Key Field:** Unique identifier for each row (often auto-incrementing integer).
- **Relational Databases:** Tables with relationships between them.
- **Non-Relational (NoSQL) Databases:** More flexible, don't use tables and rows.
### **III. Basic SQL Commands:**

- **SELECT:** Retrieve data.
    - `SELECT * FROM users;` (all columns)
    - `SELECT username, password FROM users;` (specific columns)
    - `SELECT * FROM users LIMIT 1;` (limit results)
    - `SELECT * FROM users WHERE username='admin';` (filter with WHERE clause)
    - `SELECT * FROM users WHERE username LIKE 'a%';` (wildcard matching)
- **UNION:** Combine results of multiple SELECT statements.
- **INSERT:** Add new data.
    - `INSERT INTO users (username, password) VALUES ('bob', 'password123');`
- **UPDATE:** Modify existing data.
    - `UPDATE users SET username='root', password='pass123' WHERE username='admin';`
- **DELETE:** Remove data.
    - `DELETE FROM users WHERE username='martin';`
### **IV. SQL Injection Explained:**

- Occurs when user-supplied data is included in SQL queries.
- _Example:_ `https://website.thm/blog?id=2;--`
    - Injects `;--` to terminate the original query and comment out the rest.
### **V. SQLi Types:**

- **In-Band:** Same channel for exploitation and data retrieval.
    - **Error-Based:** Database errors reveal information.
    - **Union-Based:** Uses UNION to extract data.
- **Blind:** Little or no feedback from the server.
    - **Boolean-Based:** True/false responses.
    - **Time-Based:** Time delays indicate successful queries.
- **Out-of-Band:** Separate channels for attack and data retrieval (e.g., HTTP requests, DNS requests).
### **VI. SQLi Remediation:**

- **Prepared Statements (Parameterized Queries):** Separate SQL code from user data.
- **Input Validation:** Sanitize and filter user input.
- **Escaping User Input:** Prevent special characters from breaking queries or enabling injection.