SELECT Accounts.BasePath, Machines.Address, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge,
	COUNT(DISTINCT Machines.Address) as NumMachines,
	AVG(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as AvgPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND Accounts.AccountType = 'Domain'
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)