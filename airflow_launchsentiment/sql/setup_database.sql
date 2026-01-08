-- Create database if it does not exist
IF NOT EXISTS (
    SELECT name
    FROM sys.databases
    WHERE name = 'LaunchSentimentDB'
)
BEGIN
    CREATE DATABASE LaunchSentimentDB;
END;
GO

-- Switch to the database
USE LaunchSentimentDB;
GO

-- Create table if it does not exist
IF NOT EXISTS (
    SELECT *
    FROM sys.tables
    WHERE name = 'pageviews'
)
BEGIN
    CREATE TABLE pageviews (
        company VARCHAR(255) NOT NULL,
        views INT NOT NULL,
        date DATE NOT NULL,
        hour INT NOT NULL
    );
END;
GO

-- Create unique index to prevent duplicate loads
IF NOT EXISTS (
    SELECT *
    FROM sys.indexes
    WHERE name = 'ux_pageviews_company_run'
)
BEGIN
    CREATE UNIQUE INDEX ux_pageviews_company_run
    ON pageviews (company, date, hour);
END;
GO
