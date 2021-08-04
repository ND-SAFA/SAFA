package edu.nd.crc.safa.importer;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.sql.DataSource;

import edu.nd.crc.safa.constants.DatabaseVariables;
import edu.nd.crc.safa.database.configuration.SQLConnection;
import edu.nd.crc.safa.output.error.ServerError;

import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.stereotype.Component;

@Component
public class MySQL {
    public static class FileInfo {
        public List<String> uploadedFiles = new ArrayList<String>();
        public List<String> expectedFiles = new ArrayList<String>();
        public List<String> generatedFiles = new ArrayList<String>();
        public List<String> expectedGeneratedFiles = new ArrayList<String>();
    }

    public final int CONNECTION_TIMEOUT = 10000;


    public Connection getConnection() throws ServerError {
        try {
            return createConnectionPool().getConnection();
        } catch (SQLException e) {
            throw new ServerError("Could not connect to MySQL database: " + e.getMessage());
        }
    }

    private DataSource createConnectionPool() throws ServerError {
        //TODO: delete this
        SQLConnection.assertValidCredentials();
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        //dataSource.setDriverClassName("org.h2.Driver");
        dataSource.setUrl(DatabaseVariables.SQL_URL);
        dataSource.setUsername(DatabaseVariables.SQL_USERNAME);
        dataSource.setPassword(DatabaseVariables.SQL_PASSWORD);
        return dataSource;
    }

    public Boolean tableExists(String tableName) throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            String sqlTableCheck = String.format("SELECT 1 FROM information_schema.tables where table_schema = "
                + "'safa-db'" + " AND table_name = '%s' limit 1;", tableName); // TODO: remove hard coded database
            ResultSet rs = stmt.executeQuery(sqlTableCheck);
            rs.next();

            return rs.getRow() != 0;
        } catch (SQLException e) {
            throw new ServerError("checking if table exists", e);
        }
    }


    public void createTableList(String tableName, Boolean generated) throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            if (!tableExists("uploaded_and_generated_tables")) {
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", "uploaded_and_generated_tables")
                    + "tablename VARCHAR(255) PRIMARY KEY,\n"
                    + "is_generated TINYINT NOT NULL"
                    + ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println(String.format("CREATED TABLE: %s.", "uploaded_and_generated_tables"));
            }

            System.out.println(String.format("Updating TABLE: %s...", "uploaded_and_generated_tables"));
            String sqlUpdateTable = String.format(
                "INSERT INTO %s (tablename, is_generated)\n",
                "uploaded_and_generated_tables")
                + String.format("VALUES ('%s', %s)\n", tableName, generated)
                + String.format("ON DUPLICATE KEY UPDATE tablename = '%s', is_generated = %s", tableName,
                generated);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println(String.format("UPDATED TABLE: %s.", "uploaded_and_generated_tables"));
        } catch (SQLException e) {
            throw new ServerError("creating table list", e);
        }
    }
}
