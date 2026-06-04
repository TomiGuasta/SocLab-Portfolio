# DVWA SQL Injection Assessment (LOW, MEDIUM, HIGH)

## Overview

This repository documents a complete security assessment of the SQL Injection module in Damn Vulnerable Web Application (DVWA).

The objective was to understand how SQL Injection behaves under different security configurations, evaluate mitigation effectiveness, analyze source code, and compare attack surfaces across LOW, MEDIUM, and HIGH security levels.

This project was performed in a controlled laboratory environment for educational and defensive cybersecurity purposes.

---

## Scope

Target Application:

* DVWA (Damn Vulnerable Web Application)

Modules Assessed:

* SQL Injection (LOW)
* SQL Injection (MEDIUM)
* SQL Injection (HIGH)

Assessment Type:

* Manual Security Testing
* Source Code Review
* Comparative Analysis

---

## Environment

### Attacker Machine

* Kali Linux

### Target Machine

* DVWA
* PHP
* MySQL

### Network

* Isolated Lab Environment

---

## Objectives

* Identify SQL Injection behavior at each security level.
* Compare attack surface reduction techniques.
* Understand defensive coding mechanisms.
* Analyze source code implementation.
* Document offensive and defensive observations.

---

## Key Findings

### LOW

* Full SQL Injection exploitation possible.
* UNION-based attacks successful.
* Database enumeration successful.
* Table discovery successful.
* User data extraction successful.

### MEDIUM

* Increased resistance against common payloads.
* Some injection vectors remained viable.
* Additional filtering mechanisms observed.

### HIGH

* Traditional SQL Injection payloads blocked.
* Input validation enforced through `is_numeric()`.
* UNION-based attacks unsuccessful.
* Boolean-based attacks unsuccessful.
* Numeric coercion techniques accepted but did not lead to exploitation.

---

## User Enumeration Results

Valid Records Identified:

| ID | User          |
| -- | ------------- |
| 1  | admin         |
| 2  | Gordon Brown  |
| 3  | Hack Me       |
| 4  | Pablo Picasso |
| 5  | Bob Smith     |

IDs greater than 5 returned no records.

---

## Security Controls Observed

### LOW

No meaningful protections.

### MEDIUM

Partial filtering mechanisms.

### HIGH

* stripslashes()
* mysql_real_escape_string()
* is_numeric()

---

## Major Lesson

The most important lesson learned during this assessment was that not every security engagement ends with successful exploitation.

Understanding why a mitigation works is just as valuable as exploiting a vulnerability.

The HIGH security level demonstrated how strict input validation can dramatically reduce attack surface even when the application still uses dynamically constructed SQL queries.

---

## Repository Structure

README.md

COMMANDS_USED.md

LESSONS_LEARNED_AND_ANALYSIS.md

REPORT_FINAL_DVWA_SQLI_HIGH.pdf

screenshots/

---

## Disclaimer

This project was conducted exclusively in a controlled laboratory environment for educational and defensive cybersecurity training.
