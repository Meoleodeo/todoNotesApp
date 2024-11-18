-- Enable SQL Server Authentication
EXEC xp_instance_regwrite 
    N'HKEY_LOCAL_MACHINE', 
    N'Software\Microsoft\MSSQLServer\MSSQLServer',
    N'LoginMode',
    REG_DWORD,
    2
GO

-- Configure SQL Server for mixed mode authentication
USE [master]
GO
EXEC xp_instance_regwrite 
    N'HKEY_LOCAL_MACHINE', 
    N'Software\Microsoft\MSSQLServer\MSSQLServer',
    N'SecurityMode',
    REG_DWORD,
    2
GO

-- Enable TCP/IP Protocol
EXEC sp_configure 'show advanced options', 1
GO
RECONFIGURE
GO
EXEC sp_configure 'remote access', 1
GO
RECONFIGURE
GO

-- Set up firewall rule (requires admin privileges)
EXEC xp_cmdshell 'netsh advfirewall firewall add rule name="SQL Server" dir=in action=allow protocol=TCP localport=1433'
GO

-- Enable SQL Server Browser service
EXEC xp_cmdshell 'sc config "SQL Server Browser" start= auto'
EXEC xp_cmdshell 'net start "SQL Server Browser"'
GO