SELECT Accounts.Name, COUNT(Accounts.Name) as TotalFound, HCPA.PasswordLength
FROM HardCodedPasswordAccounts AS HCPA
	LEFT OUTER JOIN Accounts
		ON Accounts.Id = HCPA.WebAppAccount_id
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%'
		OR HCPA.Name LIKE '')
    {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY TotalFound DESC