SELECT Accounts.Name, WindowsAccounts.CausesVulnerabilityOnXOfMachines, Machines.Address,
	CASE Machines.ProductType WHEN 'Workstation' THEN 1 ELSE 0 END AS Workstation,
	CASE Machines.ProductType WHEN 'Server' THEN 1 ELSE 0 END AS Server,
	(SELECT SUM(IsPrivileged) FROM Accounts AS A1 WHERE A1.Name = Accounts.Name) AS PrivilegedCount
FROM Accounts
	LEFT OUTER JOIN WindowsAccounts
		ON WindowsAccounts.OSAccount_id = Accounts.Id
	LEFT OUTER JOIN OSAccounts
		ON WindowsAccounts.OSAccount_id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND WindowsAccounts.CausesVulnerabilityOnXOfMachines > 0
	AND PrivilegedCount > 0
	{disabled}
ORDER BY LOWER(Accounts.Name) ASC