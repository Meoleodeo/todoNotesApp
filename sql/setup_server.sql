-- Create login for the application
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'sa')
BEGIN
    CREATE LOGIN [sa] WITH PASSWORD = '1234567'
END
GO

-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TodoNotesDB')
BEGIN
    CREATE DATABASE TodoNotesDB
END
GO

USE TodoNotesDB
GO

-- Create tables
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[todos]') AND type in (N'U'))
BEGIN
    CREATE TABLE todos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        task NVARCHAR(500) NOT NULL,
        link NVARCHAR(1000),
        created_at DATETIME DEFAULT GETDATE()
    )
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[notes]') AND type in (N'U'))
BEGIN
    CREATE TABLE notes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        title NVARCHAR(200) NOT NULL,
        content NVARCHAR(MAX),
        pinned BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE()
    )
END
GO

-- Grant permissions
IF EXISTS (SELECT * FROM sys.database_principals WHERE name = 'sa')
BEGIN
    GRANT SELECT, INSERT, UPDATE, DELETE ON todos TO [sa]
    GRANT SELECT, INSERT, UPDATE, DELETE ON notes TO [sa]
END
GO