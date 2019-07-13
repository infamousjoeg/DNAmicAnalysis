SELECT COUNT(DISTINCT SPN.Name) AS TotalFound
FROM SPN
	LEFT OUTER JOIN Accounts
		ON SPN.Name = Accounts.Name
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE NOT (SPN.Name LIKE '%*%'
		OR SPN.Name LIKE ''
		OR SPN.Name LIKE 'S-%')
	{disabled}