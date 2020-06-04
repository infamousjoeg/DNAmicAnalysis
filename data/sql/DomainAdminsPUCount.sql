SELECT DISTINCT LOWER(Accounts.Name)
FROM Accounts
	LEFT JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE Accounts.AccountType != 'Local'
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC