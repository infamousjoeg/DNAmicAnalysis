SELECT DISTINCT LOWER(Address)
FROM Accounts
WHERE AccountType = 'Domain'
	AND NOT Address LIKE 'S-%'