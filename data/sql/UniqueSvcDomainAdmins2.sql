SELECT DISTINCT Services.AccountName
FROM Services
	LEFT OUTER JOIN Accounts
		ON Services.AccountName = Accounts.Name
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE OSGroupModel.DomainGroup LIKE '%Domain Admins%'
	AND NOT ({whereStmt})
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Services.AccountName)
ORDER BY Services.AccountName ASC