SELECT HCPA.Name, Machines.Address
FROM HardCodedPasswordAccounts AS HCPA
	LEFT OUTER JOIN Accounts
		ON Accounts.Id = HCPA.WebAppAccount_id
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%'
		OR HCPA.Name LIKE '')
	{disabled}
GROUP BY Machines.Address
ORDER BY HCPA.Name, Machines.Address ASC