SELECT Accounts.Name, Machines.Address,
	COUNT(DISTINCT Machines.Address) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Machines.Platform = 'Nix'
	AND OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND OSAccounts.LastPasswordSet != ''
	AND Accounts.AccountType = 'Local'
	AND MaxPasswordAge != '0'
	AND ({whereStmt})
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Machines.Address)
ORDER BY MaxPasswordAge DESC