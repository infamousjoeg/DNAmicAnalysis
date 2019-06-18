SELECT DISTINCT COUNT(Accounts.Name) as TotalCount
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE Accounts.AccountType = 'Domain'
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'