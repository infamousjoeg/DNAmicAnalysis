SELECT Machines.Address,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge,
	COUNT(DISTINCT Machines.Address) as NumMachines
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Machines.Platform = 'Nix'
	AND OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND OSAccounts.LastPasswordSet != ''
	AND Accounts.Name = 'root'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Machines.Address)
ORDER BY MaxPasswordAge DESC