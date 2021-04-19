SELECT LOWER(Accounts.Name) as UserName
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE Accounts.AccountType != 'Domain'
	AND ({whereStmt})
	AND OSAccounts.Enabled = {disabled}
GROUP BY UserName
ORDER BY UserName ASC