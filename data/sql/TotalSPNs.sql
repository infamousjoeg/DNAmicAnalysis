SELECT COUNT(Name)
FROM SPN
WHERE LastPasswordSet <= datetime('{scanDateTime}', '-{executionDays} days')
	AND NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%')
	AND Enabled = {disabled}
ORDER BY LOWER(Name) ASC