SELECT COUNT(DISTINCT Name) AS TotalFound
FROM SPN
WHERE NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%')
	{disabled}