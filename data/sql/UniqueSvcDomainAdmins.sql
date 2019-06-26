SELECT DISTINCT Accounts.Name
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE NOT (Accounts.Name LIKE '%*%'
	OR Accounts.Name LIKE '')
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
    AND ({whereStmt})
ORDER BY Accounts.Name ASC