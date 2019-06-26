SELECT DISTINCT Services.AccountName
FROM Services
	LEFT OUTER JOIN Accounts
		ON Services.AccountName = Accounts.Name
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE OSGroupModel.DomainGroup LIKE '%Domain Admins%'
	AND NOT ({whereStmt})
ORDER BY Services.AccountName ASC