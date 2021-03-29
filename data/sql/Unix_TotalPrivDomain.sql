SELECT DISTINCT LOWER(Accounts.Name) as UserName
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE Accounts.AccountType != 'Local'
	AND Accounts.IsPrivileged = 1
	AND OSAccounts.Enabled = {disabled}
GROUP BY UserName
ORDER BY UserName ASC