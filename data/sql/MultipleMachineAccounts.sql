SELECT Accounts.Name, COUNT(1) as TotalFound
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND Accounts.AccountType != 'Local'
	{disabled}
GROUP BY LOWER(Accounts.Name)
HAVING TotalFound > 1