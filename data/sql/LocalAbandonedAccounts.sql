SELECT Accounts.Name, Machines.Address, OSAccounts.LastLogon, OSAccounts.LastPasswordSet,
	COUNT(Accounts.Name) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND OSAccounts.LastLogon <= datetime('{scanDateTime}', '-1 year')
	AND Accounts.AccountType = 'Local'
	AND NOT (OSAccounts.Description LIKE 'Built-in account for administering the computer/domain'
		OR Accounts.Name = 'Administrator')
	AND (OSGroupModel.Name LIKE 'Administrators'
		OR OSGroupModel.Name LIKE 'Power Users')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)