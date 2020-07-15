SELECT Accounts.Name, COUNT(Machines.Address) AS TotalMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE Machines.ProductType = 'Server'
	AND NOT (Accounts.Name = ''
		OR Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE 'S-%'
		OR Accounts.Name LIKE '%admin%')
	AND NOT ({whereStmt})
	AND NOT OSAccounts.Description LIKE 'Built-in account for administering the computer/domain'
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY TotalMachines DESC