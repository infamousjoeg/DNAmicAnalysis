SELECT DISTINCT Accounts.Name
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE Accounts.AccountType = 'Domain'
	AND Accounts.Name NOT LIKE '%*%'
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
ORDER BY Accounts.Name ASC