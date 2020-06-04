SELECT DISTINCT Accounts.Name
FROM Services
    LEFT OUTER JOIN Accounts
        ON Services.AccountName = Accounts.Name
    LEFT OUTER JOIN OSAccounts
        ON Accounts.Id = OSAccounts.AccountBase_id
WHERE NOT ({whereStmt})
    AND NOT (Accounts.Name LIKE '%*%'
        OR Accounts.Name LIKE '')
    AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC