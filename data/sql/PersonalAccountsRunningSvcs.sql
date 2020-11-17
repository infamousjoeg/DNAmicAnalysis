SELECT DISTINCT Accounts.Name,
    COUNT(Accounts.Name) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Services
    LEFT OUTER JOIN Accounts
        ON Services.IAccount_id = Accounts.Id
    LEFT OUTER JOIN OSAccounts
        ON Accounts.Id = OSAccounts.AccountBase_id
WHERE NOT ({whereStmt})
    AND NOT (Accounts.Name LIKE '%*%'
        OR Accounts.Name LIKE '')
    AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC