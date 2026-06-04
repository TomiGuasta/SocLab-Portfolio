# Lessons Learned, Detection Opportunities and Comparative Analysis

## Comparative Analysis

| Feature            | LOW     | MEDIUM   | HIGH   |
| ------------------ | ------- | -------- | ------ |
| User Enumeration   | Yes     | Partial  | Yes    |
| UNION Injection    | Yes     | Limited  | No     |
| Schema Enumeration | Yes     | Limited  | No     |
| Data Extraction    | Yes     | Limited  | No     |
| Input Validation   | Minimal | Moderate | Strong |
| Exploitability     | High    | Medium   | Low    |

---

# Why HIGH Was Different

Unlike LOW and MEDIUM, the HIGH implementation validates user input before constructing the SQL query.

The critical protection is:

```php
is_numeric($id)
```

This function restricts accepted values to numeric representations only.

As a consequence:

* Quotes are rejected.
* SQL operators are rejected.
* Comments are rejected.
* UNION statements are rejected.
* Boolean logic payloads are rejected.

---

# Numeric Behavior Analysis

The following values were accepted:

```text
1
0001
1.0
2.0
1e0
```

Reason:

PHP interprets all of them as valid numeric values.

Examples:

1e0 = 1 × 10^0 = 1

0001 = 1

1.0 = 1

This behavior demonstrates that validation focuses on numeric legitimacy rather than exact formatting.

---

# Detection Opportunities

A Blue Team could detect:

## Enumeration Activity

Sequential requests:

```text
?id=1
?id=2
?id=3
?id=4
?id=5
```

Indicators:

* Repeated access patterns
* Incremental object references

---

## SQL Injection Probing

Examples:

```text
'
"
OR 1=1
UNION SELECT
```

Indicators:

* Repeated failed requests
* Suspicious URL parameters

---

## Numeric Evasion Attempts

Examples:

```text
0001
1.0
1e0
```

Indicators:

* Non-standard numeric representations
* Automated fuzzing behavior

---

# Defensive Lessons

## Input Validation Works

The assessment demonstrated how a simple validation mechanism can significantly reduce attack surface.

---

## Validation Alone Is Not Enough

The application still uses dynamic SQL construction.

More secure implementations should use:

* Prepared Statements
* Parameterized Queries
* Stored Procedures where appropriate

---

## Source Code Review Is Essential

Observing application behavior alone did not fully explain the results.

The source code revealed the actual defensive control responsible for blocking exploitation.

---

# Final Lessons Learned

1. Enumeration is not exploitation.

2. Successful exploitation is not required to complete a valuable assessment.

3. Understanding defensive mechanisms is a critical security skill.

4. Source code review often provides answers that black-box testing cannot.

5. Attack surface reduction can dramatically change exploitation outcomes.

6. Modern defensive development should combine validation with parameterized queries.

7. Security assessments should document both successful and unsuccessful attack paths.

8. A failed attack can still produce valuable security intelligence.

---

# Final Technical Conclusion

LOW security was fully exploitable.

MEDIUM reduced exploitability through additional filtering.

HIGH successfully prevented practical SQL Injection by enforcing numeric-only input validation.

Although the application still relies on legacy SQL construction methods, the implemented controls were sufficient to defeat all tested payloads during this assessment.

The exercise provided a complete view of SQL Injection evolution from vulnerable to significantly hardened implementations.
