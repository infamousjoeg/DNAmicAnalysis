SELECT DISTINCT Accounts.Name
FROM Services
    LEFT OUTER JOIN Accounts
        ON Services.AccountName = Accounts.Name
WHERE NOT ({whereStmt})
    AND NOT (Accounts.Name LIKE '%*%'
        OR Accounts.Name LIKE '')
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC