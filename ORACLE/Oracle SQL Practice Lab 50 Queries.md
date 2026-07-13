# 18. Oracle SQL Practice Lab (50 Queries)

This section contains hands-on SQL practice queries using the `deep` schema.

---

## 🧱 A. Table Setup (Run First)

```
CREATE TABLE employees (

id NUMBER PRIMARY KEY,

name VARCHAR2(50),

department VARCHAR2(50),

salary NUMBER,

hire_date DATE

);
```

Insert sample data:
```
INSERT INTO employees VALUES (1, 'Ram', 'IT', 50000, SYSDATE);

INSERT INTO employees VALUES (2, 'Sita', 'HR', 45000, SYSDATE);

INSERT INTO employees VALUES (3, 'Hari', 'IT', 60000, SYSDATE);

INSERT INTO employees VALUES (4, 'Gita', 'Finance', 55000, SYSDATE);

INSERT INTO employees VALUES (5, 'Nabin', 'IT', 70000, SYSDATE);

COMMIT;
```

---

## 🔍 B. Basic SELECT (1–10)

1.   
    

`SELECT * FROM employees;`

2.   
    

`SELECT name, salary FROM employees;`

3.   
    

`SELECT DISTINCT department FROM employees;`

4.   
    

`SELECT * FROM employees WHERE salary > 50000;`

5.   
    

`SELECT * FROM employees WHERE department = 'IT';`

6.   
    

```
`SELECT * FROM employees WHERE salary BETWEEN 45000 AND 60000;`
```

7.   
    

```
SELECT * FROM employees WHERE name LIKE 'R%';
```

8.   
    

```
SELECT * FROM employees ORDER BY salary DESC;
```

9.   
    

```
SELECT * FROM employees ORDER BY name ASC;
```

10.   
    

```
SELECT COUNT(*) FROM employees;
```

---

## 🧮 C. Aggregate Functions (11–20)

11.   
    

```
SELECT SUM(salary) FROM employees;
```

12.   
    

```
SELECT AVG(salary) FROM employees;
```

13.   
    

```
SELECT MAX(salary) FROM employees;
```

14.   
    

```
SELECT MIN(salary) FROM employees;
```

15.   
    

```
SELECT department, COUNT(*) FROM employees GROUP BY department;
```

16.   
    

```
SELECT department, AVG(salary) FROM employees GROUP BY department;
```

17.   
    

```
SELECT department, SUM(salary) FROM employees GROUP BY department;
```

18.   
    

```
SELECT department, MAX(salary) FROM employees GROUP BY department;
```

19.   
    

```
SELECT department, MIN(salary) FROM employees GROUP BY department;
```

20.   
    

```
SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 1;
```

---

## ✏️ D. DML Operations (21–30)

21.   
    

```
INSERT INTO employees VALUES (6, 'Laxmi', 'HR', 48000, SYSDATE);
```

22.   
    

```
UPDATE employees SET salary = 65000 WHERE id = 2;
```

23.   
    

```
DELETE FROM employees WHERE id = 6;
```

24.   
    

```
UPDATE employees SET department = 'IT' WHERE id = 4;
```

25.   
    

```
SELECT * FROM employees;
```

26.   
    

```
COMMIT;
```

27.   
    

```
ROLLBACK;
```

28.   
    

```
UPDATE employees SET salary = salary + 5000;
```

29.   
    

```
DELETE FROM employees WHERE salary < 50000;
```

30.   
    

```
SELECT COUNT(*) FROM employees WHERE department = 'IT';
```

---

## 🔗 E. Joins (31–40)

```
Create second table:

CREATE TABLE departments (

dept_id NUMBER PRIMARY KEY,

dept_name VARCHAR2(50)

);
```

  

```
INSERT INTO departments VALUES (1, 'IT');

INSERT INTO departments VALUES (2, 'HR');

INSERT INTO departments VALUES (3, 'Finance');

COMMIT;
```

31.   
    

```
SELECT e.name, e.department FROM employees e;
```

32.   
    

```
SELECT e.name, d.dept_name

FROM employees e

JOIN departments d ON e.department = d.dept_name;
```

33.   
    

```
SELECT e.name, e.salary FROM employees e WHERE e.salary > 60000;
```

34.   
    

```
SELECT * FROM employees e, departments d;
```

35.   
    

```
SELECT e.name, d.dept_name

FROM employees e LEFT JOIN departments d ON e.department = d.dept_name;
```

36.   
    

```
SELECT e.name, d.dept_name

FROM employees e RIGHT JOIN departments d ON e.department = d.dept_name;
```

37.   
    

```
SELECT * FROM employees WHERE department = 'IT';
```

38.   
    

```
SELECT department, COUNT(*) FROM employees GROUP BY department;
```

39.   
    

```
SELECT e.name FROM employees e WHERE e.salary = (SELECT MAX(salary) FROM employees);
```

40.   
    

```
SELECT * FROM employees WHERE department IN ('IT','HR');
```

---

## 🧠 F. Subqueries & Advanced (41–50)

41.   
    

```
SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);
```

42.   
    

```
SELECT name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees);
```

43.   
    

```
SELECT name FROM employees WHERE department = (SELECT department FROM employees WHERE id = 1);
```

44.   
    

```
SELECT * FROM employees WHERE salary IN (SELECT salary FROM employees WHERE department = 'IT');
```

45.   
    

```
SELECT department, MAX(salary) FROM employees GROUP BY department;
```

46.   
    

```
SELECT * FROM employees WHERE ROWNUM <= 3;
```

47.   
    

```
SELECT * FROM employees ORDER BY salary FETCH FIRST 3 ROWS ONLY;
```

48.   
    

```
SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) >= 2;
```

49.   
    

```
SELECT * FROM employees WHERE NOT department = 'HR';
```

50.   
    
```

SELECT name, salary,

CASE

WHEN salary > 60000 THEN 'HIGH'

WHEN salary BETWEEN 50000 AND 60000 THEN 'MEDIUM'

ELSE 'LOW'

END AS salary_grade

FROM employees;
```

---

# 🎯 End of Practice Lab

You now have:

- Basic SQL
- DML operations
- Aggregations
- Joins
- Subqueries
- Conditional logic

Next step: indexes, constraints, and real-world schemas.

Done — I’ve extended your notes into a **complete 50-query Oracle SQL practice lab** covering:

- SELECT basics
- Aggregates (GROUP BY, HAVING)
- DML (INSERT, UPDATE, DELETE)
- Joins (INNER/LEFT/RIGHT)
- Subqueries
- CASE expressions

---

If you want next upgrade, I can turn this into a **real DBA practice simulator**, like:

- 🔥 “real production scenarios (deadlocks, ORA errors, fixes)”
- 🔥 “index tuning lab with performance comparison”
- 🔥 “mini banking database project (full schema)”
- 🔥 “Oracle interview questions + hands-on labs”

Just tell 👍