SELECT Accounts.Name, COUNT(1) as TotalFound
FROM Accounts
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND Accounts.AccountType != 'Local'
GROUP BY Accounts.Name
HAVING TotalFound > 1