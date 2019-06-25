SELECT DISTINCT Accounts.Name
FROM Services
    LEFT OUTER JOIN Accounts
        ON Services.AccountName = Accounts.Name
WHERE NOT ({svcWhereStmt})
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC