SELECT Accounts.Name,
	(SELECT COUNT(Machines.Address) FROM Machines
		LEFT OUTER JOIN Accounts AS A1
			ON Machines.Id = A1.Machine_id
		WHERE A1.Name = Accounts.Name) AS MachineCount,
	(SELECT SUM(IsPrivileged) FROM Accounts AS A1 WHERE A1.Name = Accounts.Name) AS PrivilegedCount
FROM Accounts
	OUTER LEFT JOIN WindowsAccounts
		ON WindowsAccounts.OSAccount_id = Accounts.Id
	OUTER LEFT JOIN OSAccounts
		ON WindowsAccounts.OSAccount_id = OSAccounts.AccountBase_id
	OUTER LEFT JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND WindowsAccounts.CausesVulnerabilityOnXOfMachines > 0
	AND PrivilegedCount > 0
	{disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY MachineCount DESC