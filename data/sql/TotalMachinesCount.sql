SELECT DISTINCT COUNT(Machines.Id) as TotalMachines
FROM Machines
WHERE ScanResult <> 'Failed'