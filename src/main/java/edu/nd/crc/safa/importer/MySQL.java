package edu.nd.crc.safa.importer;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.sql.DataSource;

import edu.nd.crc.safa.dao.Links;
import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.warnings.Rule;

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

    String mysqlURL = System.getenv("_MY_SQL_URL");
    String mysqlUser = System.getenv("_MY_SQL_USERNAME");
    String mysqlPassword = System.getenv("_MY_SQL_PASSWORD");

    public final int CONNECTION_TIMEOUT = 10000;

    public MySQL() {
    }

    public Connection getConnection() throws ServerError {
        try {
            return createConnectionPool().getConnection();
        } catch (SQLException e) {
            throw new ServerError("Could not connect to MySQL database: " + e.getMessage());
        }
    }

    private DataSource createConnectionPool() throws ServerError {
        //TODO: Create bean from this so it can be reused!
        hasValidCredentials();

        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        //dataSource.setDriverClassName("org.h2.Driver");
        dataSource.setUrl(mysqlURL);
        dataSource.setUsername(mysqlUser);
        dataSource.setPassword(mysqlPassword);
        return dataSource;
    }

    private void hasValidCredentials() throws ServerError {
        if (mysqlUser == null) {
            throw new ServerError("MySQL user is null");
        } else if (mysqlPassword == null) {
            throw new ServerError("MySQL Password is null");
        } else if (mysqlURL == null) {
            throw new ServerError("MySQL url is null");
        }
    }

    public void verifyConnection() throws ServerError {
        try {
            getConnection().isValid(CONNECTION_TIMEOUT);
        } catch (SQLException e) {
            throw new ServerError("SQL Connection is not valid");
        }
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

    public void createGeneratedTraceMatrixTable(String tableName, String filePath) throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            Boolean exists = tableExists(tableName);

            if (exists) {
                updateGeneratedTraceMatrixTable(stmt, tableName, filePath);
            } else {
                createGeneratedTraceMatrixTable(stmt, tableName, filePath);
            }
        } catch (SQLException e) {
            throw new ServerError("creating generated trace matrix table", e);
        }
    }

    public void createGeneratedTraceMatrixTable(Statement stmt, String tableName, String filePath) throws ServerError {
        try {
            System.out.println(String.format("CREATING NEW GENERATED TABLE: %s...", tableName));

            String sqlCreateTable = String.format(
                "CREATE TABLE %s (\n", tableName)
                + "id INT AUTO_INCREMENT PRIMARY KEY,\n"
                + "source VARCHAR(255) NOT NULL,\n"
                + "target VARCHAR(255) NOT NULL,\n"
                + "score FLOAT NOT NULL,\n"
                + "approval INT NOT NULL DEFAULT 2,\n"
                + "UNIQUE KEY source_target (source,target)\n"
                + ");";

            stmt.executeUpdate(sqlCreateTable);
            System.out.println(String.format("CREATED NEW GENERATED TABLE: %s.", tableName));

            String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName)
                + "FIELDS TERMINATED BY ','\n"
                + "ENCLOSED BY '\"'\n"
                + "LINES TERMINATED BY '\\n'\n"
                + "IGNORE 1 ROWS\n"
                + "(source, target, score);";

            stmt.executeUpdate(sqlLoadData);
            System.out.println(String.format("LOADED GENERATED FILE: %s INTO TABLE: %s.", filePath, tableName));

            String sqlTrim = String.format("UPDATE %s SET\n", tableName)
                + "source = TRIM(TRIM(BOTH '\r' from source)),\n"
                + "target = TRIM(TRIM(BOTH '\r' from target));";

            stmt.executeUpdate(sqlTrim);
            System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");

            createTableList(tableName, true);
        } catch (SQLException e) {
            throw new ServerError("creating new generated trace matrix table", e);
        }
    }

    public void updateGeneratedTraceMatrixTable(Statement stmt, String tableName, String filePath) throws ServerError {
        try {
            System.out.println(String.format("UPDATING GENERATED TABLE: %s...", tableName));

            String tempTableName = String.format("temp_%s", tableName);

            String sqlCreateTempTable = String.format("CREATE TEMPORARY TABLE %s\n", tempTableName)
                +
                String.format("SELECT * FROM %s\n", tableName) + "LIMIT 0;";

            stmt.executeUpdate(sqlCreateTempTable);
            System.out.println("CREATED TEMPORARY TABLE.");

            String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tempTableName)
                + "FIELDS TERMINATED BY ','\n"
                + "ENCLOSED BY '\"'\n"
                + "LINES TERMINATED BY '\\n'\n"
                + "IGNORE 1 ROWS\n"
                + "(source, target, score);";

            stmt.executeUpdate(sqlLoadData);
            System.out.println(String.format("LOADED DATA FILE: %s INTO TEMPORARY TABLE.", filePath));

            String sqlTrim = String.format("UPDATE %s SET\n", tempTableName)
                + "source = TRIM(TRIM(BOTH '\r' from source)),\n"
                + "target = TRIM(TRIM(BOTH '\r' from target));";

            stmt.executeUpdate(sqlTrim);
            System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");

            String newTable = String.format("new_%s", tableName);
            if (tableExists(newTable)) {
                String sqlDelete = String.format("DROP TABLE %s", newTable);
                stmt.executeUpdate(sqlDelete);
                System.out.println("DELETED ABANDONED GENERATED TABLE");
            }

            String sqlCreateNewTable = String.format("CREATE TABLE %s (\n", newTable) // Create New Table.
                + "id INT AUTO_INCREMENT PRIMARY KEY,\n"
                + "source VARCHAR(255) NOT NULL,\n"
                + "target VARCHAR(255) NOT NULL,\n"
                + "score FLOAT NOT NULL,\n"
                + "approval INT NOT NULL DEFAULT 2,\n"
                + "UNIQUE KEY source_target (source,target)\n"
                + ");";

            stmt.executeUpdate(sqlCreateNewTable);
            System.out.println("CREATED NEW GENERATED TABLE.");

            String sqlJoin = String.format("INSERT INTO %s (source, target, score, approval)\n", newTable)
                + "SELECT temp.source, temp.target, temp.score, IFNULL(old.approval,2)\n"
                + String.format("FROM %s temp\n", tempTableName)
                + String.format("LEFT JOIN %s old\n", tableName)
                + "ON temp.source = old.source AND temp.target = old.target;";

            stmt.executeUpdate(sqlJoin);
            System.out.println("UPDATED TABLE.");

            String dropTables = String.format("DROP TABLES %s, %s", tempTableName, tableName);
            stmt.executeUpdate(dropTables);
            System.out.println("DELETED TEMPORARY AND OLD TABLE.");

            String renameNewTable = String.format("RENAME TABLE %s TO %s", newTable, tableName);
            stmt.executeUpdate(renameNewTable);
            System.out.println("RENAMED NEW TABLE TO OLD TABLE.");
        } catch (SQLException e) {
            throw new ServerError("update generated trace matrix table", e);
        }
    }

    public void clearTimTables() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            Boolean artifactsExists = tableExists("tim_artifact");
            Boolean traceExists = tableExists("tim_trace_matrix");

            if (artifactsExists) {
                String sqlClearArtifactsTable = String.format("TRUNCATE TABLE %s\n", "tim_artifact");
                stmt.executeUpdate(sqlClearArtifactsTable);
                System.out.println("CLEARED TABLE tim_artifact");
            }

            if (traceExists) {
                String sqlClearTraceTable = String.format("TRUNCATE TABLE %s\n", "tim_trace_matrix");
                stmt.executeUpdate(sqlClearTraceTable);
                System.out.println("CLEARED TABLE tim_trace_matrix");
            }
        } catch (SQLException e) {
            throw new ServerError("clearing TIM tables", e);
        }
    }

    public void createTimArtifactsTable(String artifact, String tablename, String filename)
        throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            Boolean exists = tableExists("tim_artifact");

            if (exists) {
                updateTimArtifactsTable(stmt, artifact, tablename, filename);
            } else {
                newTimArtifactsTable(stmt);
                updateTimArtifactsTable(stmt, artifact, tablename, filename);
            }
        } catch (SQLException e) {
            throw new ServerError("creating TIM artifact table", e);
        }
    }

    public void newTimArtifactsTable(Statement stmt) throws ServerError {
        try {
            System.out.println(String.format("CREATING NEW TIM ARTIFACTS TABLE: %s...", "tim_artifact"));
            String sqlCreateTable = String.format("CREATE TABLE %s (\n", "tim_artifact")
                + "artifact VARCHAR(255) PRIMARY KEY,\n"
                + "tablename VARCHAR(255) NOT NULL,\n"
                + "filename VARCHAR(255) NOT NULL"
                + ");";

            stmt.executeUpdate(sqlCreateTable);
            System.out.println(String.format("CREATED NEW TIM ARTIFACTS TABLE: %s.", "tim_artifact"));
        } catch (SQLException e) {
            throw new ServerError("new TIM artifact table", e);
        }
    }

    public void updateTimArtifactsTable(Statement stmt, String artifact, String tablename, String filename)
        throws ServerError {
        try {
            System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_artifact"));
            String sqlUpdateTable = String.format("INSERT INTO %s (artifact, tablename, filename)\n", "tim_artifact")
                + String.format("VALUES ('%s', '%s', '%s')\n", artifact, tablename, filename)
                + String.format("ON DUPLICATE KEY UPDATE artifact = '%s', tablename = '%s', filename = '%s'",
                artifact, tablename, filename);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println(String.format("UPDATED TIM ARTIFACTS TABLE: %s.", "tim_artifact"));
        } catch (SQLException e) {
            throw new ServerError("updating TIM artifact table", e);
        }
    }

    public void createUpdateTIMTraceMatrixTable(String traceMatrixName,
                                                String traceMatrixTableName,
                                                String sourceArtifact,
                                                String targetArtifact,
                                                Boolean generated,
                                                String filename) throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();

            if (tableExists("tim_trace_matrix")) {
                updateTimTraceMatrixTable(stmt, traceMatrixName, traceMatrixTableName,
                    sourceArtifact, targetArtifact, generated, filename);
            } else {
                newTimTraceMatrixTable(stmt);
                updateTimTraceMatrixTable(stmt, traceMatrixName, traceMatrixTableName,
                    sourceArtifact, targetArtifact, generated, filename);
            }
        } catch (SQLException e) {
            throw new ServerError("creating TIM trace matrix table", e);
        }
    }

    public void newTimTraceMatrixTable(Statement stmt) throws ServerError {
        try {
            String sqlCreateTable = String.format("CREATE TABLE %s (\n", "tim_trace_matrix")
                + "trace_matrix VARCHAR(255) PRIMARY KEY,\n"
                + "source_artifact VARCHAR(255) NOT NULL,\n"
                + "target_artifact VARCHAR(255) NOT NULL,\n"
                + "is_generated TINYINT NOT NULL,\n"
                + "tablename VARCHAR(255) NOT NULL,\n"
                + "filename VARCHAR(255) NOT NULL"
                + ");";

            stmt.executeUpdate(sqlCreateTable);
        } catch (SQLException e) {
            throw new ServerError("creating TIM trace matrix table", e);
        }
    }

    public void updateTimTraceMatrixTable(Statement stmt,
                                          String traceMatrixName,
                                          String traceMatrixTableName,
                                          String sourceArtifact,
                                          String targetArtifact,
                                          Boolean generated,
                                          String filename) throws ServerError {
        try {
            System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_trace_matrix"));
            String sqlUpdateTable = String.format("INSERT INTO %s (trace_matrix, source_artifact, target_artifact,"
                + "is_generated, tablename, filename)\n", "tim_trace_matrix")
                + String.format("VALUES ('%s', '%s', '%s', %s, '%s', '%s')\n",
                traceMatrixName, sourceArtifact, targetArtifact, generated, traceMatrixTableName, filename)
                + String.format("ON DUPLICATE KEY UPDATE trace_matrix = '%s', source_artifact = '%s', "
                    + "target_artifact = '%s', is_generated = %s, tablename = '%s', filename = '%s';",
                traceMatrixName, sourceArtifact, targetArtifact, generated, traceMatrixTableName, filename);


            stmt.executeUpdate(sqlUpdateTable);
            System.out.println(String.format("UPDATED TIM TRACE MATRIX TABLE: %s.", "tim_trace_matrix"));
        } catch (SQLException e) {
            throw new ServerError("Failed to update TIM trace matrix table");
        }
    }

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


    public void createTraceMatrixTable(String tableName, String filePath, String colHeader) throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            String intTableName = "intermediate_" + tableName;

            if (!tableExists("trace_matrix_error")) {
                System.out.println("CREATING NEW Trace Matrix ERROR TABLE: trace_matrix_error...");
                String sqlCreateErrorTable = "CREATE TABLE trace_matrix_error (\n"
                    + "db_id INT AUTO_INCREMENT PRIMARY KEY,"
                    + "tablename VARCHAR(255),\n"
                    + "source VARCHAR(255),\n"
                    + "target VARCHAR(255),\n"
                    + "line INT,\n"
                    + "descr VARCHAR(255) NOT NULL"
                    + ");";
                stmt.executeUpdate(sqlCreateErrorTable);
                System.out.println("CREATED NEW ARTIFACT ERROR TABLE: trace_matrix_error...");
            }

            createTraceMatrixHelper(stmt, intTableName, tableName, filePath, colHeader);

            if (tableExists(tableName)) {
                String sqlTruncateArtifactTable = String.format("TRUNCATE TABLE %s", tableName);
                stmt.executeUpdate(sqlTruncateArtifactTable);
            } else {
                System.out.println(String.format("CREATING NEW TRACE MATRIX TABLE: %s...", tableName));
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName)
                    + "source VARCHAR(255),\n"
                    + "target VARCHAR(255),\n"
                    + "score FLOAT NOT NULL DEFAULT 1,\n"
                    + "approval INT NOT NULL DEFAULT 2,\n"
                    + "PRIMARY KEY (source, target)"
                    + ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println("CREATED NEW TRACE MATRIX TABLE");
            }

            String sqlUpdateTable = String.format("INSERT INTO %s (source, target, score, approval)\n", tableName)
                + String.format("SELECT source, target, score, approval FROM %s\n", intTableName)
                + String.format("ON DUPLICATE KEY UPDATE source = %s.source, target = %s.target;",
                tableName, tableName);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println("INSERTED DATA from %s into TRACE MATRIX TABLE: %s.");


            stmt.executeUpdate(String.format("DROP TABLE %s", intTableName));
            System.out.println("DELETED INTERMEDIATE TRACE MATRIX TABLE");

            createTableList(tableName, false);
        } catch (SQLException e) {
            throw new ServerError("create trace matrix table", e);
        }
    }

    public void createTraceMatrixHelper(Statement stmt,
                                        String intTableName,
                                        String tableName,
                                        String filePath,
                                        String colHeader) throws ServerError {
        try {
            if (tableExists(intTableName)) {
                String sqlTruncate = String.format("TRUNCATE TABLE %s", intTableName);
                stmt.executeUpdate(sqlTruncate);
            } else {
                System.out.println("CREATING INTERMEDIATE TRACE MATRIX TABLE");
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", intTableName)
                    + "db_id INT AUTO_INCREMENT PRIMARY KEY,\n"
                    + "source VARCHAR(255),\n"
                    + "target VARCHAR(255),\n"
                    + "score FLOAT NOT NULL DEFAULT 1,\n"
                    + "approval INT NOT NULL DEFAULT 2\n"
                    + ");";
                stmt.executeUpdate(sqlCreateTable);
                System.out.println("CREATED INTERMEDIATE TRACE MATRIX TABLE");
            }

            String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, intTableName)
                + "FIELDS TERMINATED BY ','\n"
                + "ENCLOSED BY '\"'\n"
                + "LINES TERMINATED BY '\\n'\n"
                + "IGNORE 1 ROWS\n"
                + colHeader + ";";

            stmt.executeUpdate(sqlLoadData);
            System.out.println(String.format("LOADED FILE: %s INTO INTERMEDIATE TRACE MATRIX TABLE.", filePath));

            String sqlTrim = String.format("UPDATE %s SET\n", intTableName)
                + "source = TRIM(TRIM(BOTH '\r' from source)),\n"
                + "target = TRIM(TRIM(BOTH '\r' from target));";

            stmt.executeUpdate(sqlTrim);
            System.out.println("TRIMMED columns for INTERMEDIATE TABLE");

            String sqlDeleteErrors = String.format("DELETE FROM trace_matrix_error\n")
                + String.format("WHERE tablename = '%s';", tableName);

            stmt.executeUpdate(sqlDeleteErrors);

            String sqlInsertDups = "INSERT INTO trace_matrix_error (tablename, source, target, line, descr)\n"
                + String.format("SELECT '%s', t1.source, t1.target, t1.db_id, 'DUPLICATE LINK: LINE SKIPPED.' FROM "
                + "%s t1\n", tableName, intTableName)
                + String.format("INNER JOIN %s t2\n", intTableName)
                + "WHERE t1.db_id > t2.db_id AND t1.source = t2.source AND t1.target = t2.target;";

            stmt.executeUpdate(sqlInsertDups);
            System.out.println("INSERTED Duplicates into TABLE trace_matrix_error\n");

            String sqlLineUpdate = "UPDATE trace_matrix_error SET line = line + 1\n"
                + String.format("WHERE tablename = '%s';", tableName);

            stmt.executeUpdate(sqlLineUpdate);
            System.out.println("Updated Line numbers.\n");
        } catch (SQLException e) {
            throw new ServerError("creating trace matrix helper", e);
        }
    }

    public FileInfo getFileInfo() throws ServerError {
        FileInfo fileInfo = new FileInfo();

        List<List<String>> artifact_rows = getTimArtifactData();

        for (List<String> artifact_row : artifact_rows) {
            String tablename = artifact_row.get(1);
            String filename = String.format("\"%s\"", artifact_row.get(2));

            fileInfo.expectedFiles.add(filename);

            if (tableExists(tablename)) {
                fileInfo.uploadedFiles.add(filename);
            }
        }

        List<List<String>> trace_rows = getTimTraceData();

        for (List<String> trace_row : trace_rows) {
            boolean generated = trace_row.get(3).equals("1");
            String tableName = trace_row.get(4);
            String filename = String.format("\"%s\"", trace_row.get(5));

            if (generated) {
                fileInfo.expectedGeneratedFiles.add(filename);

                if (tableExists(tableName)) {
                    fileInfo.generatedFiles.add(filename);
                }
            } else {
                fileInfo.expectedFiles.add(filename);

                if (tableExists(tableName)) {
                    fileInfo.uploadedFiles.add(filename);
                }
            }
        }

        return fileInfo;
    }

    public void traceArtifactCheck() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            Boolean timTraceExists = tableExists("tim_trace_matrix");
            Boolean timArtifactsExists = tableExists("tim_artifact");

            if (timTraceExists && timArtifactsExists) {
                String sqlCheck = "SELECT trace.artifact FROM\n"
                    +
                    "(SELECT source_artifact AS artifact FROM tim_trace_matrix UNION SELECT target_artifact FROM"
                    + " tim_trace_matrix) AS trace\n"
                    + "LEFT JOIN tim_artifact ON tim_artifact.artifact = trace.artifact\n"
                    + "WHERE tim_artifact.artifact IS NULL;";

                ResultSet rs = stmt.executeQuery(sqlCheck);

                List<String> missingArtifacts = new ArrayList<String>();

                while (rs.next()) {
                    missingArtifacts.add(rs.getString(1));
                }

                if (missingArtifacts.size() != 0) {
                    throw new ServerError(String.format("Artifacts: %s do not appear under the datafiles section of "
                        + "your tim.json", missingArtifacts.toString()));
                }
            }
        } catch (SQLException e) {
            throw new ServerError("trace artifact check", e);
        }
    }

    public String getLinkErrors() throws ServerError {
        HashMap<String, Set<String>> artifact_map = new HashMap<String, Set<String>>();
        StringBuilder errorText = new StringBuilder();

        List<List<String>> artifactRows = getTimArtifactData();

        for (List<String> artifactRow : artifactRows) {
            String artifactName = artifactRow.get(0);
            String artifactTableName = artifactRow.get(1);
            Set<String> ids = new HashSet<String>();

            List<List<String>> artifact_data_rows = getArtifactData(artifactTableName);
            for (List<String> row : artifact_data_rows) {
                ids.add(row.get(0));
            }

            artifact_map.put(artifactName, ids);
        }

        List<List<String>> traceRows = getTimTraceData();

        for (List<String> traceRow : traceRows) {
            if (traceRow.get(3).equals("1")) {
                continue;
            }

            String traceMatrix = traceRow.get(0);

            String source_artifact = traceRow.get(1);
            Set<String> sources = artifact_map.get(source_artifact);

            String target_artifact = traceRow.get(2);
            Set<String> targets = artifact_map.get(target_artifact);


            if (sources == null && targets == null) {
                errorText.append(String.format("ERROR: TRACE MATRIX: %s DESC: source artifact: %s and target "
                    + "artifact: %s does not exist in the database. Make sure these artifacts are part of your "
                    + "tim file.\n", traceMatrix, source_artifact, target_artifact));
                continue;
            }

            if (sources == null) {
                errorText.append(String.format("ERROR: TRACE MATRIX: %s DESC: source artifact %s does not exist in "
                        + "the database. Make sure this artifact is part of your tim file.\n",
                    traceMatrix,
                    source_artifact));
                continue;
            }

            if (targets == null) {
                errorText.append(String.format("ERROR: TRACE MATRIX: %s DESC: target artifact %s does not exist in "
                        + "the database. Make sure this artifact is part of your tim file.\n",
                    traceMatrix, target_artifact));
                continue;
            }

            int line_num = 0;
            String traceTableName = traceRow.get(4);

            List<List<String>> traceDataRows = getNonGeneratedTraceData(traceTableName);

            for (List<String> row : traceDataRows) {
                String sid = row.get(0);
                String tid = row.get(1);
                line_num++;

                if (!sources.contains(sid)) {
                    errorText.append(String.format("ERROR: TRACE MATRIX: %s Line Number: %s DESC: source artifact %s"
                        + " does not contain ID: %s\n", traceMatrix, line_num, source_artifact, sid));

                }

                if (!targets.contains(tid)) {
                    errorText.append(String.format("ERROR: TRACE MATRIX: %s Line Number: %s DESC: source artifact %s"
                        + " does not contain ID: %s\n", traceMatrix, line_num, target_artifact, tid));
                }
            }
        }

        return Base64.getEncoder().encodeToString(errorText.toString().getBytes());
    }

    public String getUploadErrorLog() throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            System.out.println("Upload Flatfile Error Log...");

            if (!(tableExists("artifact_error") && tableExists("trace_matrix_error"))) {
                System.out.println("Upload Flatfile Error Log: Empty...");
                return "";
            }

            ArrayList<Object> artifactHeader = new ArrayList<Object>();
            artifactHeader.add("\"FILE NAME\"");
            artifactHeader.add("\"ID\"");
            artifactHeader.add("\"LINE\"");
            artifactHeader.add("\"DESC\"");

            List<ArrayList<Object>> result = new ArrayList<ArrayList<Object>>();
            result.add(artifactHeader);

            String sqlArtifactError = "SELECT tablename, id, line, descr FROM artifact_error";
            ResultSet rsArtifactError = stmt.executeQuery(sqlArtifactError);

            while (rsArtifactError.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(String.format("\"%s\"", rsArtifactError.getString(2)));
                row.add(String.format("\"%s\"", rsArtifactError.getString(3)));
                row.add(rsArtifactError.getInt(4));
                row.add(rsArtifactError.getString(5));
                result.add(row);
            }

            ArrayList<Object> traceHeader = new ArrayList<Object>();
            traceHeader.add("\"FILE NAME\"");
            traceHeader.add("\"SOURCE ID\"");
            traceHeader.add("\"TARGET ID\"");
            traceHeader.add("\"LINE\"");
            traceHeader.add("\"DESC\"");
            result.add(traceHeader);

            String sqlTraceError = "SELECT tablename, source, target, line, descr FROM trace_matrix_error";
            ResultSet rsTraceError = stmt.executeQuery(sqlTraceError);

            while (rsTraceError.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(String.format("\"%s\"", rsTraceError.getString(2)));
                row.add(String.format("\"%s\"", rsTraceError.getString(3)));
                row.add(String.format("\"%s\"", rsTraceError.getString(4)));
                row.add(rsTraceError.getInt(5));
                row.add(String.format("\"%s\"", rsTraceError.getString(6)));
                result.add(row);
            }

            byte[] content = result.toString().getBytes();
            String returnStr = Base64.getEncoder().encodeToString(content);

            return returnStr;
        } catch (SQLException e) {
            throw new ServerError("retrieving upload error log", e);
        }
    }

    public String clearUploadedFlatfiles() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            if (tableExists("uploaded_and_generated_tables")) {
                String sqlUploadedFiles = "SELECT tablename\n"
                    + "FROM uploaded_and_generated_tables\n"
                    + "WHERE is_generated = 0;";

                ResultSet rs = stmt.executeQuery(sqlUploadedFiles);
                ArrayList<String> tables = new ArrayList<String>();

                while (rs.next()) {
                    tables.add(rs.getString(1));
                }

                if (tableExists("artifact_error")) {
                    stmt.executeUpdate("DROP TABLE artifact_error");
                }

                if (tableExists("trace_matrix_error")) {
                    stmt.executeUpdate("DROP TABLE trace_matrix_error");
                }

                if (tables.size() == 0) {
                    stmt.executeUpdate("DROP TABLE uploaded_and_generated_tables");
                    return "No generated files";
                }

                String deleteTables = tables.toString().replace("[", "").replace("]", "");
                String sqlDropTables = String.format("DROP TABLES %s;", deleteTables);
                stmt.executeUpdate(sqlDropTables);

                String sqlDeleteTables = "DELETE FROM uploaded_and_generated_tables WHERE is_generated = 0;";
                stmt.executeUpdate(sqlDeleteTables);

                return "Uploaded files have successfully been cleared";
            } else {
                return "No uploaded files";
            }
        } catch (SQLException e) {
            throw new ServerError("clear uploaded flat files", e);
        }
    }

    public String clearGeneratedFlatfiles() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            if (tableExists("uploaded_and_generated_tables")) {
                String sqlUploadedFiles = "SELECT tablename\n"
                    + "FROM uploaded_and_generated_tables\n"
                    + "WHERE is_generated = 1;";

                ResultSet rs = stmt.executeQuery(sqlUploadedFiles);
                ArrayList<String> tables = new ArrayList<String>();

                while (rs.next()) {
                    tables.add(rs.getString(1));
                }

                if (tables.size() == 0) {
                    stmt.executeUpdate("DROP TABLE uploaded_and_generated_tables");
                    return "No generated files";
                }

                String deleteTables = tables
                    .toString()
                    .replace("[", "")
                    .replace("]", "");
                String sqlDropTables = String.format("DROP TABLES %s;", deleteTables);
                stmt.executeUpdate(sqlDropTables);

                String sqlDeleteTables = "DELETE FROM uploaded_and_generated_tables WHERE is_generated = 1;";
                stmt.executeUpdate(sqlDeleteTables);

                return "Generated files have successfully been cleared";
            } else {
                return "No generated files";
            }
        } catch (SQLException e) {
            throw new ServerError("clearing generated flat files", e);
        }
    }

    public List<List<String>> generateInfo() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();

            String sqlUploadedFiles = "SELECT tim_source.tablename as source_tablename,\n"
                + "tim_target.tablename as target_tablename,\n"
                + "tim_trace_matrix.tablename as dest_tablename\n"
                + "FROM tim_trace_matrix\n"
                + "LEFT JOIN tim_artifact as tim_source\n"
                + "ON tim_source.artifact = tim_trace_matrix.source_artifact\n"
                + "AND is_generated = 1\n"
                + "LEFT JOIN tim_artifact as tim_target\n"
                + "ON tim_target.artifact = tim_trace_matrix.target_artifact\n"
                + "AND is_generated = 1\n"
                + "where tim_source.tablename IS NOT NULL AND tim_target.tablename IS NOT NULL;";

            ResultSet rs = stmt.executeQuery(sqlUploadedFiles);

            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getString(3));
                data.add(row);
            }

            return data;
        } catch (SQLException e) {
            throw new ServerError("generate information", e);
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

    public List<List<String>> getNonGeneratedTraceData(String tablename) throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();

            String sqlGetData = String.format("SELECT source, target FROM %s;", tablename);

            ResultSet rs = stmt.executeQuery(sqlGetData);

            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                data.add(row);
            }

            return data;
        } catch (SQLException e) {
            throw new ServerError("retrieving non generated trace data", e);
        }
    }

    public List<List<String>> getGeneratedTraceData(String tablename) throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();

            String sqlGetData = String.format("SELECT source, target, score, approval FROM %s;", tablename);

            ResultSet rs = stmt.executeQuery(sqlGetData);

            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(Float.toString(rs.getFloat(3)));
                row.add(String.valueOf(rs.getInt(4)));
                data.add(row);
            }

            return data;
        } catch (SQLException e) {
            throw new ServerError("retrieving generated trace data", e);
        }
    }

    public List<List<String>> getTimArtifactData() throws ServerError {
        try {
            List<List<String>> data = new ArrayList<List<String>>();
            if (!tableExists("tim_artifact")) {
                return data;
            }
            Statement stmt = getConnection().createStatement();
            String sqlGetData = String.format("SELECT artifact, tablename, filename FROM %s;", "tim_artifact");

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
            throw new ServerError("retrieving TIM artifact data", e);
        }
    }

    public List<List<String>> getTimTraceData() throws ServerError {
        try {
            List<List<String>> data = new ArrayList<List<String>>();
            if (!tableExists("tim_trace_matrix")) {
                return data;
            }
            Statement stmt = getConnection().createStatement();
            String sqlGetData = String.format("SELECT trace_matrix, source_artifact, target_artifact, is_generated, "
                + "tablename, filename FROM %s;", "tim_trace_matrix");
            ResultSet rs = stmt.executeQuery(sqlGetData);

            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getString(3));
                row.add(rs.getString(4));
                row.add(rs.getString(5));
                row.add(rs.getString(6));
                data.add(row);
            }

            return data;
        } catch (SQLException e) {
            throw new ServerError("retrieving TIM trace data", e);
        }
    }

    public void saveLayout(String hash, String b64EncodedLayout) throws ServerError {
        try {
            Boolean exists = tableExists("saved_layouts");
            Statement stmt = getConnection().createStatement();
            if (!exists) {
                String sqlCreateTable = String.format("CREATE TABLE saved_layouts (\n")
                    + "hash VARCHAR(255) PRIMARY KEY,\n"
                    + "b64e_layout BLOB NOT NULL\n"
                    + ");";
                stmt.executeUpdate(sqlCreateTable);
            }

            String sqlUpsertLayout = String.format("INSERT INTO saved_layouts (hash, b64e_layout) VALUES ('%s', "
                + "'%s')\n", hash, b64EncodedLayout)
                + String.format("ON DUPLICATE KEY UPDATE b64e_layout='%s';", b64EncodedLayout);
            stmt.executeUpdate(sqlUpsertLayout);
        } catch (SQLException e) {
            throw new ServerError("saving layout", e);
        }
    }

    public String fetchLayout(String hash) throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            String sqlQueryLayout = String.format("SELECT b64e_layout FROM saved_layouts WHERE hash='%s';", hash);
            ResultSet rs = stmt.executeQuery(sqlQueryLayout);
            rs.first();
            return rs.getString("b64e_layout");
        } catch (SQLException e) {
            throw new ServerError("retrieving layout", e);
        }
    }


    public List<Rule> getWarnings(String project) throws ServerError {
        try {
            List<Rule> result = new ArrayList<Rule>();

            createWarningsTable();
            Connection conn = getConnection();

            PreparedStatement preparedStmt = conn.prepareStatement("SELECT nShort, nLong, rule FROM "
                + "project_warning_rules WHERE projectId = ?");
            preparedStmt.setString(1, project);

            ResultSet rs = preparedStmt.executeQuery();
            while (rs.next()) {
                System.out.println(rs.toString());
                String nShort = rs.getString(1);
                String nLong = rs.getString(2);
                String rule = rs.getString(3);
                result.add(new Rule(nShort, nLong, rule));
            }
            conn.close();

            return result;
        } catch (SQLException e) {
            throw new ServerError("retrieve warnings", e);
        }
    }

    public void newWarning(String project, String nShort, String nLong, String rule) throws ServerError {
        try {
            createWarningsTable();

            Connection conn = getConnection();
            PreparedStatement preparedStmt = conn.prepareStatement("INSERT INTO project_warning_rules(projectId, "
                + "nShort,"
                + " nLong, rule) VALUES (?, ?, ?, ?);");
            preparedStmt.setString(1, project);
            preparedStmt.setString(2, nShort);
            preparedStmt.setString(3, nLong);
            preparedStmt.setString(4, rule);
            System.out.println(preparedStmt.execute());
            conn.close();
        } catch (SQLException e) {
            throw new ServerError("create a new warning", e);
        }
    }

    public void createWarningsTable() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            if (!tableExists("project_warning_rules")) {
                String sqlCreateErrorTable = "CREATE TABLE project_warning_rules (\n"
                    + "db_id INT AUTO_INCREMENT PRIMARY KEY,"
                    + "projectId VARCHAR(1024),\n"
                    + "nShort VARCHAR(1024) NOT NULL,\n"
                    + "nLong VARCHAR(1024) NOT NULL,\n"
                    + "rule VARCHAR(1024) NOT NULL);";
                stmt.executeUpdate(sqlCreateErrorTable);
            }
        } catch (SQLException e) {
            throw new ServerError("create warnings table", e);
        }
    }

    // Links
    public Integer getLinkApproval(String project, String source, String target) throws ServerError {
        Integer result = -1;
        try (Connection conn = getConnection()) {
            List<String> tables = new ArrayList<String>();
            try (Statement s = conn.createStatement()) {
                ResultSet rs = s.executeQuery("SELECT tablename FROM uploaded_and_generated_tables");
                while (rs.next()) {
                    tables.add(rs.getString(1));
                }
            }

            boolean found = false;
            for (String table : tables) {
                PreparedStatement p = conn.prepareStatement(String.format("SELECT approval FROM %s WHERE source = ? "
                    + "AND target = ?", table));
                p.setString(1, source);
                p.setString(2, target);

                ResultSet rs = p.executeQuery();
                if (rs.first()) {
                    if (found) {
                        throw new ServerError(String.format("multiple generated links found between %s and %s",
                            source, target));
                    }
                    found = true;
                    result = rs.getInt(1);
                }
            }
            if (!found) {
                throw new ServerError(String.format("generated link not found"));
            }
        } catch (SQLException e) {
            throw new ServerError("get link approval", e);
        }
        return result;
    }

    public boolean updateLink(String project, Links links) throws ServerError {
        boolean succeeded = false;

        try (Connection conn = getConnection()) {
            List<String> tables = new ArrayList<String>();

            try (Statement s = conn.createStatement()) {
                ResultSet rs = s.executeQuery("SELECT tablename FROM uploaded_and_generated_tables");
                while (rs.next()) {
                    tables.add(rs.getString(1));
                }
            }


            for (int i = 0; i < links.links.size(); i++) {
                Links.Link link = links.links.get(i);
                System.out.println(link.source);
                if (link.approval < 0 || link.approval > 2) {
                    throw new ServerError(String.format("Invalid link approval value"));
                }

                for (String table : tables) {
                    System.out.println(table);
                    PreparedStatement s = conn.prepareStatement(String.format("UPDATE %s SET approval = ? WHERE "
                        + "source = ? AND target = ?", table));
                    s.setInt(1, link.approval);
                    s.setString(2, link.source);
                    s.setString(3, link.target);
                    succeeded |= (s.executeUpdate() > 0);
                }
            }
        } catch (SQLException e) {
            throw new ServerError("update links in project", e);
        }

        return succeeded;
    }

    // Artifacts
    public List<String> getArtifacts(String project) throws ServerError {
        try {
            List<String> result = new ArrayList<String>();
            Statement s = getConnection().createStatement();
            ResultSet rs = s.executeQuery("SELECT artifact FROM tim_artifact");
            while (rs.next()) {
                result.add(rs.getString(1));
            }

            return result;
        } catch (SQLException e) {
            throw new ServerError("retrieve artifacts in project", e);
        }
    }

    public List<Map<String, Object>> getArtifactLinks(String project,
                                                      String source,
                                                      String target,
                                                      Double minScore) throws ServerError {
        List<Map<String, Object>> result = new ArrayList<Map<String, Object>>();
        try (Connection conn = getConnection()) {
            PreparedStatement s = conn.prepareStatement("SELECT tablename FROM tim_trace_matrix WHERE "
                + "source_artifact = ? AND target_artifact = ?");
            s.setString(1, source);
            s.setString(2, target);

            ResultSet rsSource = s.executeQuery();
            if (!rsSource.first()) {
                String errorMessage = String.format("generated links table not found between %s and %s", source,
                    target);
                throw new ServerError(errorMessage);
            }
            String linkTable = rsSource.getString(1);
            String sqlString = "SELECT source, target, score, approval, %s.summary AS source_summary, %s.summary AS"
                + " target_summary FROM %s LEFT JOIN %s ON %s.id=source LEFT JOIN %s ON %s.id=target WHERE "
                + "score >= ? ORDER BY score DESC";
            source = source.toLowerCase();
            target = target.toLowerCase();
            sqlString = String.format(sqlString, source, target, linkTable, source, source, target, target);

            try (Statement sLink = conn.createStatement()) {
                PreparedStatement sLinks = conn.prepareStatement(sqlString);
                sLinks.setDouble(1, minScore);

                ResultSet rs = sLinks.executeQuery();
                while (rs.next()) {
                    Map<String, Object> link = new HashMap<String, Object>();
                    link.put("source", rs.getString(1));
                    link.put("target", rs.getString(2));
                    link.put("score", rs.getDouble(3));
                    link.put("approval", rs.getString(4));
                    link.put("source_summary", rs.getString(5));
                    link.put("target_summary", rs.getString(6));
                    result.add(link);
                }
            }
            return result;
        } catch (SQLException e) {
            throw new ServerError("retrieve artifact links", e);
        }
    }
}
