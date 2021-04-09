SELECT Accounts.BasePath, COUNT(DISTINCT Machines.Address) as TotalFound,
	COUNT(DISTINCT Machines.Address) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND NOT OSGroupModel.DomainGroup LIKE '%Domain Admins%'
	AND Accounts.AccountType = 'Domain'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
HAVING TotalFound > 1
ORDER BY TotalFound DESC