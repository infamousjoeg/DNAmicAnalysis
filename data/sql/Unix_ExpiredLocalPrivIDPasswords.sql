SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	COUNT(DISTINCT Machines.Address) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN SshKeys
		ON OSAccounts.AccountBase_id = SshKeys.Id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{executionDays} days')
	AND Accounts.AccountType = 'Local'
	AND SshKeys.SshKeyType IS NULL
	AND NOT Accounts.Name LIKE ''
	AND Machines.Platform = 'Nix'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY PasswordAge DESC