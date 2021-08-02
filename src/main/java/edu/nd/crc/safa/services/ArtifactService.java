package edu.nd.crc.safa.services;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.error.ServerError;

public class ArtifactService {
    public void createArtifactTableHelper(Statement stmt,
                                          String intTableName,
                                          String tableName,
                                          String filePath,
                                          String colHeader) throws ServerError {

        try {
            if (tableExists(intTableName)) {
                String sqlTruncate = String.format("TRUNCATE TABLE %s", intTableName);
                stmt.executeUpdate(sqlTruncate);
            } else {
                System.out.println("CREATING INTERMEDIATE ARTIFACT TABLE");
                String sqlCreateTempTable = String.format("CREATE TABLE %s (\n", intTableName)
                    + "db_id INT AUTO_INCREMENT PRIMARY KEY,\n"
                    + "id VARCHAR(255) NOT NULL,\n"
                    + "summary TEXT NOT NULL,\n"
                    + "content TEXT NOT NULL\n"
                    + ");";
                stmt.executeUpdate(sqlCreateTempTable);
                System.out.println("CREATED INTERMEDIATE ARTIFACT TABLE");
            }

            String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, intTableName)
                + "FIELDS TERMINATED BY ','\n"
                + "ENCLOSED BY '\"'\n"
                + "LINES TERMINATED BY '\\n'\n"
                + "IGNORE 1 ROWS\n"
                + colHeader
                + ";";

            stmt.executeUpdate(sqlLoadData);
            System.out.println(String.format("LOADED FILE: %s INTO INTERMEDIATE TABLE", filePath));

            String sqlTrim = String.format("UPDATE %s SET\n", intTableName)
                + "id = TRIM(TRIM(BOTH '\r' from id)),\n"
                + "summary = TRIM(TRIM(BOTH '\r' from summary)),\n"
                + "content = TRIM(TRIM(BOTH '\r' from content));";

            stmt.executeUpdate(sqlTrim);
            System.out.println("TRIMMED columns for INTERMEDIATE TABLE");

            String sqlDeleteErrors = String.format("DELETE FROM artifact_error\n")
                + String.format("WHERE tablename = '%s';", tableName);

            stmt.executeUpdate(sqlDeleteErrors);

            String sqlInsertDups = "INSERT INTO artifact_error (tablename, id, line, descr)\n"
                + String.format("SELECT '%s', t1.id, t1.db_id, 'DUPLICATE ARTIFACT ID: LINE SKIPPED.' FROM %s t1\n",
                tableName, intTableName)
                + String.format("INNER JOIN %s t2\n", intTableName)
                + "WHERE t1.db_id > t2.db_id AND t1.id = t2.id;";

            stmt.executeUpdate(sqlInsertDups);
            System.out.println("INSERTED Duplicates into TABLE artifact_error\n");

            String sqlLineUpdate = "UPDATE artifact_error SET line = line + 1\n"
                + String.format("WHERE tablename = '%s';", tableName);

            stmt.executeUpdate(sqlLineUpdate);
            System.out.println("Updated Line numbers.\n");
        } catch (SQLException e) {
            throw new ServerError("creating artifact table helper", e);
        }
    }

    public void createArtifactTable(String tableName,
                                    String filePath,
                                    String colHeader) throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            String intTableName = "intermediate_" + tableName;
            if (!tableExists("artifact_error")) {
                System.out.println("CREATING NEW ARTIFACT ERROR TABLE: artifact_error...");
                String sqlCreateErrorTable = "CREATE TABLE artifact_error (\n"
                    + "db_id INT AUTO_INCREMENT PRIMARY KEY,"
                    + "tablename VARCHAR(255),\n"
                    + "id VARCHAR(255),\n"
                    + "line INT,\n"
                    + "descr VARCHAR(255) NOT NULL"
                    + ");";
                stmt.executeUpdate(sqlCreateErrorTable);
                System.out.println("CREATED NEW ARTIFACT ERROR TABLE: artifact_error...");
            }

            createArtifactTableHelper(stmt, intTableName, tableName, filePath, colHeader);

            if (tableExists(tableName)) {
                String sqlTruncateArtifactTable = String.format("TRUNCATE TABLE %s", tableName);
                stmt.executeUpdate(sqlTruncateArtifactTable);
            } else {
                System.out.println("CREATING NEW ARTIFACT TABLE");
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName)
                    + "id VARCHAR(255) PRIMARY KEY,\n"
                    + "summary TEXT NOT NULL,\n"
                    + "content TEXT NOT NULL"
                    + ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println("CREATED NEW ARTIFACT TABLE");
            }

            String sqlUpdateTable = String.format("INSERT INTO %s (id, summary, content)\n", tableName)
                + String.format("SELECT id, summary, content FROM %s\n", intTableName)
                + String.format("ON DUPLICATE KEY UPDATE id = %s.id;", tableName);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println("INSERTED DATA into ARTIFACT TABLE");


            stmt.executeUpdate(String.format("DROP TABLE %s", intTableName));
            System.out.println("DELETED INTERMEDIATE ARTIFACT TABLE");

            createTableList(tableName, false);
        } catch (SQLException e) {
            throw new ServerError("creating artifact table", e);
        }
    }

    public List<List<String>> getArtifactData(String tableName) throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();

            String sqlGetData = String.format("SELECT id, summary, content FROM %s;", tableName);

            ResultSet rs = stmt.executeQuery(sqlGetData);

            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getString(3));
                data.add(row);
            }

            return data;
        } catch (SQLException e) {
            throw new ServerError("retrieving artifact data", e);
        }
    }
}
