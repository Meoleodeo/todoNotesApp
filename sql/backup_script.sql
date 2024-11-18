-- Create backup directory if it doesn't exist
EXEC xp_cmdshell 'if not exist "C:\SQLBackups" mkdir "C:\SQLBackups"'
GO

-- Backup database
BACKUP DATABASE TodoNotesDB
TO DISK = 'C:\SQLBackups\TodoNotesDB.bak'
WITH FORMAT,
    MEDIANAME = 'TodoNotesBackup',
    NAME = 'Full Backup of TodoNotesDB';
GO

-- Create maintenance plan for regular backups
USE [msdb]
GO

-- Create backup job
IF NOT EXISTS (SELECT * FROM msdb.dbo.sysjobs WHERE name = N'TodoNotesDB_Backup')
BEGIN
    EXEC dbo.sp_add_job
        @job_name = N'TodoNotesDB_Backup',
        @description = N'Daily backup of TodoNotesDB'

    EXEC sp_add_jobstep
        @job_name = N'TodoNotesDB_Backup',
        @step_name = N'Backup Database',
        @subsystem = N'TSQL',
        @command = N'BACKUP DATABASE TodoNotesDB TO DISK = ''C:\SQLBackups\TodoNotesDB.bak'' WITH FORMAT'

    EXEC dbo.sp_add_schedule
        @schedule_name = N'DailyBackup',
        @freq_type = 4,
        @freq_interval = 1,
        @active_start_time = 010000

    EXEC sp_attach_schedule
        @job_name = N'TodoNotesDB_Backup',
        @schedule_name = N'DailyBackup'

    EXEC dbo.sp_add_jobserver
        @job_name = N'TodoNotesDB_Backup'
END
GO