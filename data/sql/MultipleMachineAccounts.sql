SELECT Accounts.Name, COUNT(1) as TotalFound
FROM Accounts
WHERE Accounts.Name IS NOT ''
	AND Accounts.Name NOT LIKE '%*%'
	AND Accounts.AccountType != 'Local'
GROUP BY Accounts.Name
HAVING TotalFound > 1