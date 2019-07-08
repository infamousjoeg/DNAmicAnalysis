SELECT DISTINCT Accounts.Name
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE NOT (Accounts.Name LIKE '%*%'
	OR Accounts.Name LIKE '')
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
    AND ({whereStmt})
	{disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC