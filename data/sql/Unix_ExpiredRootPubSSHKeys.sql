SELECT LOWER(Machines.Address) as MachineAddress, SshKeys.LastModifyDate,
	COUNT(DISTINCT Machines.Address) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(SshKeys.LastModifyDate)) As Integer)) as MaxKeyAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN SshData
		ON OSAccounts.SshData_id = SshData.Id
	LEFT OUTER JOIN SshKeys
		ON SshData.Id = SshKeys.SshData_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Machines.Platform = 'Nix'
	AND SshKeys.LastModifyDate <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND SshKeys.LastModifyDate != ''
	AND SshKeys.SshKeyType = 'Public'
	AND Accounts.Name = 'root'
	AND OSAccounts.Enabled = {disabled}
GROUP BY MachinesAddress
ORDER BY MaxKeyAge DESC