package edu.nd.crc.safa.importer;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.hibernate.validator.internal.util.CollectionHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import java.util.List;

import javax.naming.spi.DirStateFactory.Result;

import java.util.ArrayList;
import java.util.Base64;

@Component
public class MySQL {

    public MySQL() {}

    public static class FileInfo {
        public List<String> uploadedFiles = new ArrayList<String>();
        public List<String> expectedFiles = new ArrayList<String>();
        public List<String> generatedFiles = new ArrayList<String>();
        public List<String> expectedGeneratedFiles = new ArrayList<String>();
    }

    public static Connection startDB() throws Exception {
        String databaseURL = "jdbc:mysql://mysql:3306/safa-db?useSSL=false";
        String user = "user";
        String password = "secret3";
        Connection conn = null;
        
        Class.forName("com.mysql.cj.jdbc.Driver");
        conn = DriverManager.getConnection(databaseURL,user,password);
        if (conn == null) {
            throw new Exception("COULD NOT CONNECT TO DATABASE");
        }

        System.out.println("CONNECTED TO THE DATABASE.");
        return conn;
    }

    public static Boolean tableExists(String tableName) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            System.out.println(String.format("Checking if %s exists", tableName));
            String sqlTableCheck = String.format("SELECT COUNT(*) FROM information_schema.tables where table_schema = 'safa-db' AND table_name = '%s';", tableName);
            ResultSet rs = stmt.executeQuery(sqlTableCheck);
            rs.next();
    
            return rs.getInt("COUNT(*)") != 0;
        }  
    }

    public static Boolean tableEmpty(String tableName) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            System.out.println(String.format("Checking if %s is empty", tableName));
            String sqlTableCheck = String.format("SELECT 1 FROM '%s' LIMIT 1;", tableName);
            ResultSet rs = stmt.executeQuery(sqlTableCheck);
            rs.next();
    
            return rs.getRow() != 0;
        }  
    }

    public static void createGeneratedTraceMatrixTable(String tableName, String filePath) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean exists = tableExists(tableName);

            if (exists) {
                updateGeneratedTraceMatrixTable(stmt, tableName, filePath);
            } else {
                newGeneratedTraceMatrixTable(stmt, tableName, filePath);
            }
        }
    }

    public static void newGeneratedTraceMatrixTable(Statement stmt, String tableName, String filePath) throws Exception {
        System.out.println(String.format("CREATING NEW GENERATED TABLE: %s...", tableName));

        String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) +
            "id INT AUTO_INCREMENT PRIMARY KEY,\n" + 
            "source VARCHAR(255) NOT NULL,\n" +
            "target VARCHAR(255) NOT NULL,\n" + 
            "score FLOAT NOT NULL,\n" + 
            "approval INT NOT NULL DEFAULT 2,\n" + 
            "UNIQUE KEY source_target (source,target)\n" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED NEW GENERATED TABLE: %s.", tableName));

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            "(source, target, score);";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED GENERATED FILE: %s INTO TABLE: %s.", filePath, tableName));

        String sqlTrim = String.format("UPDATE %s SET\n", tableName) + 
        "source = TRIM(TRIM(BOTH '\r' from source)),\n" +
        "target = TRIM(TRIM(BOTH '\r' from target));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
    }

    public static void updateGeneratedTraceMatrixTable(Statement stmt, String tableName, String filePath) throws Exception {
        System.out.println(String.format("UPDATING GENERATED TABLE: %s...", tableName));

        String tempTableName = String.format("temp_%s", tableName);
        String newTable = String.format("new_%s", tableName);

        String sqlCreateTempTable = String.format("CREATE TEMPORARY TABLE %s\n", tempTableName) + 
        String.format("SELECT * FROM %s\n", tableName) + "LIMIT 0;";
        
        stmt.executeUpdate(sqlCreateTempTable);
        System.out.println("CREATED TEMPORARY TABLE.");

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tempTableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            "(source, target, score);";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED DATA FILE: %s INTO TEMPORARY TABLE.", filePath));

        String sqlTrim = String.format("UPDATE %s SET\n", tempTableName) + 
            "source = TRIM(TRIM(BOTH '\r' from source)),\n" +
            "target = TRIM(TRIM(BOTH '\r' from target));";
            
        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");

        if (tableExists(newTable)){
            String sqlDelete = String.format("DROP TABLE %s",newTable);
            stmt.executeUpdate(sqlDelete);
            System.out.println("DELETED ABANDONED GENERATED TABLE");
        }

        String sqlCreateNewTable = String.format("CREATE TABLE %s (\n", newTable) + // Create New Table.
            "id INT AUTO_INCREMENT PRIMARY KEY,\n" + 
            "source VARCHAR(255) NOT NULL,\n" +
            "target VARCHAR(255) NOT NULL,\n" + 
            "score FLOAT NOT NULL,\n" + 
            "approval INT NOT NULL DEFAULT 2,\n" + 
            "UNIQUE KEY source_target (source,target)\n" +
        ");";

        stmt.executeUpdate(sqlCreateNewTable);
        System.out.println("CREATED NEW GENERATED TABLE.");

        String sqlJoin = String.format("INSERT INTO %s (source, target, score, approval)\n", newTable) +
            "SELECT temp.source, temp.target, temp.score, IFNULL(old.approval,2)\n" +
            String.format("FROM %s temp\n", tempTableName) +
            String.format("LEFT JOIN %s old\n", tableName) +
            "ON temp.source = old.source AND temp.target = old.target;";

        stmt.executeUpdate(sqlJoin);
        System.out.println("UPDATED TABLE.");

        String dropTables = String.format(String.format("DROP TABLES %s, %s", tempTableName, tableName));
        stmt.executeUpdate(dropTables);
        System.out.println("DELETED TEMPORARY AND OLD TABLE.");

        String renameNewTable = String.format("RENAME TABLE %s TO %s", newTable, tableName);
        stmt.executeUpdate(renameNewTable);
        System.out.println("RENAMED NEW TABLE TO OLD TABLE.");
    }

    public static void clearTimTables() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean artifactsExists = tableExists("tim_artifacts");
            Boolean traceExists = tableExists("tim_trace_matrix");

            if (artifactsExists) {
                String sqlClearArtifactsTable = String.format("TRUNCATE TABLE %s\n", "tim_artifacts");
                stmt.executeUpdate(sqlClearArtifactsTable);
                System.out.println("CLEARED TABLE tim_artifacts");
            }

            if (traceExists) {
                String sqlClearTraceTable = String.format("TRUNCATE TABLE %s\n", "tim_trace_matrix");
                stmt.executeUpdate(sqlClearTraceTable);
                System.out.println("CLEARED TABLE tim_trace_matrix");
            }
        }
    }

    public static void createTimArtifactsTable(String artifactName, String artifactTableName) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean exists = tableExists("tim_artifacts");

            if (exists) {
                updateTimArtifactsTable(stmt, artifactName, artifactTableName);
            } else {
                newTimArtifactsTable(stmt);
                updateTimArtifactsTable(stmt, artifactName, artifactTableName);
            }
        }
    }

    public static void newTimArtifactsTable(Statement stmt) throws Exception {
        System.out.println(String.format("CREATING NEW TIM ARTIFACTS TABLE: %s...", "tim_artifacts"));
        String sqlCreateTable = String.format("CREATE TABLE %s (\n", "tim_artifacts") + 
            "artifact VARCHAR(255) PRIMARY KEY,\n" +
            "db_table VARCHAR(255) NOT NULL" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED NEW TIM ARTIFACTS TABLE: %s.", "tim_artifacts"));
    }

    public static void updateTimArtifactsTable(Statement stmt, String artifactName, String artifactTableName) throws Exception {
        System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_artifacts"));
        String sqlUpdateTable = String.format("INSERT INTO %s (artifact, db_table)\n", "tim_artifacts") + 
            String.format("VALUES ('%s', '%s')\n", artifactName, artifactTableName) +
            String.format("ON DUPLICATE KEY UPDATE artifact = '%s', db_table = '%s'", artifactName, artifactTableName);

        stmt.executeUpdate(sqlUpdateTable);
        System.out.println(String.format("UPDATED TIM ARTIFACTS TABLE: %s.", "tim_artifacts"));
    }

    public static void createTimTraceMatrixTable(String traceMatrixName, String traceMatrixTableName, String sourceArtifact, String targetArtifact, Boolean generated) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean exists = tableExists("tim_trace_matrix");

            if (exists) {
                updateTimTraceMatrixTable(stmt, traceMatrixName, traceMatrixTableName, sourceArtifact, targetArtifact, generated);
            } else {
                newTimTraceMatrixTable(stmt);
                updateTimTraceMatrixTable(stmt, traceMatrixName, traceMatrixTableName, sourceArtifact, targetArtifact, generated);
            }
        }
    }

    public static void newTimTraceMatrixTable(Statement stmt) throws Exception {
        String sqlCreateTable = String.format("CREATE TABLE %s (\n", "tim_trace_matrix") + 
            "trace_matrix VARCHAR(255) PRIMARY KEY,\n" +
            "source_artifact VARCHAR(255) NOT NULL,\n" +
            "target_artifact VARCHAR(255) NOT NULL,\n" +
            "is_generated TINYINT NOT NULL,\n" +
            "db_table VARCHAR(255) NOT NULL" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
    }

    public static void updateTimTraceMatrixTable(Statement stmt, String traceMatrixName, String traceMatrixTableName, String sourceArtifact, String targetArtifact, Boolean generated) throws Exception {
        System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_trace_matrix"));
        String sqlUpdateTable = String.format("INSERT INTO %s (trace_matrix, source_artifact, target_artifact, is_generated, db_table)\n", "tim_trace_matrix") + 
            String.format("VALUES ('%s', '%s', '%s', %s, '%s')\n", traceMatrixName, sourceArtifact, targetArtifact, generated, traceMatrixTableName) +
            String.format("ON DUPLICATE KEY UPDATE trace_matrix = '%s', source_artifact = '%s', target_artifact = '%s', is_generated = %s, db_table = '%s';", traceMatrixName, sourceArtifact, targetArtifact, generated, traceMatrixTableName);


        stmt.executeUpdate(sqlUpdateTable);
        System.out.println(String.format("UPDATED TIM TRACE MATRIX TABLE: %s.", "tim_trace_matrix"));
    }

    public static void createArtifactTable(String tableName, String filePath, String colHeader) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            if (!tableExists("artifact_errors")) {
                System.out.println("CREATING NEW ARTIFACT ERROR TABLE: artifact_errors...");
                String sqlCreateErrorTable = "CREATE TABLE artifact_errors (\n" +
                    "artifact VARCHAR(255),\n" + 
                    "id VARCHAR(255),\n" +
                    "error VARCHAR(255) NOT NULL,\n" +
                    "PRIMARY KEY (artifact, id)" +
                ");";
                stmt.executeUpdate(sqlCreateErrorTable);
                System.out.println("CREATED NEW ARTIFACT ERROR TABLE: artifact_errors...");
            }

            if (tableExists(tableName)) {
                overwriteArtifactTable(stmt, tableName, filePath, colHeader);
            } else {
                newArtifactTable(stmt, tableName, filePath, colHeader);
            }
        }
    }

    public static void newArtifactTable(Statement stmt, String tableName, String filePath, String colHeader) throws Exception {
        String intTableName = "intermediate_" + tableName;

        if (tableExists(intTableName)) {
            String.format("TRUNCATE TABLE %S", intTableName);
        } else {
            System.out.println(String.format("CREATING Intermediate ARTIFACT TABLE: %s...", intTableName));
            String sqlCreateTempTable = String.format("CREATE TABLE %s (\n", intTableName) +
                "db_id INT AUTO_INCREMENT PRIMARY KEY,\n" +
                "id VARCHAR(255),\n" +
                "summary TEXT NOT NULL,\n" + 
                "content TEXT NOT NULL" +
            ");";
            stmt.executeUpdate(sqlCreateTempTable);
            System.out.println(String.format("CREATED Intermediate ARTIFACT TABLE: %s.", intTableName));
        }

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, intTableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO TABLE: %s.", filePath, intTableName));

        String sqlTrim = String.format("UPDATE %s SET\n", intTableName) +
            "id = TRIM(TRIM(BOTH '\r' from id)),\n" + 
            "summary = TRIM(TRIM(BOTH '\r' from summary)),\n" +
            "content = TRIM(TRIM(BOTH '\r' from content));";

        stmt.executeUpdate(sqlTrim);
        System.out.println(String.format("TRIMMED columns for TABLE %s", intTableName));

        String sqlDeleteErrors = String.format("DELETE FROM artifact_errors\n") +
            String.format("WHERE artifact = '%s'", tableName);
        
        stmt.executeUpdate(sqlDeleteErrors);


        String sqlInsertDups = "INSERT INTO artifact_errors (artifact, id, error)\n" +
            String.format("SELECT '%s', t1.id, 'DUPLICATE ARTIFACT ID' FROM %s t1\n", tableName, intTableName) +
            String.format("INNER JOIN %s t2\n", intTableName) +
            "WHERE t1.db_id > t2.db_id AND t1.id = t2.id;";
        
        stmt.executeUpdate(sqlInsertDups);
        System.out.println("INSERTED Duplicates into TABLE artifact_errors\n");

        System.out.println(String.format("CREATING NEW ARTIFACT TABLE: %s...", tableName));
        String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) + 
            "id VARCHAR(255) PRIMARY KEY,\n" +
            "summary TEXT NOT NULL,\n" + 
            "content TEXT NOT NULL" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED NEW ARTIFACT TABLE: %s.", tableName));

        String sqlUpdateTable = String.format("INSERT INTO %s (id, summary, content)\n", tableName) +
        String.format("SELECT id, summary, content FROM %s\n", intTableName) +
        String.format("ON DUPLICATE KEY UPDATE id = %s.id;", tableName);

        stmt.executeUpdate(sqlUpdateTable);
        System.out.println(String.format("INSERTED DATA from %s into NEW ARTIFACT TABLE: %s.", intTableName, tableName));


        stmt.executeUpdate(String.format("DROP TABLE %s", intTableName));
        System.out.println(String.format("DELETED TABLE: %s.", intTableName));
    }

    public static void overwriteArtifactTable(Statement stmt, String tableName, String filePath, String colHeader) throws Exception {
        System.out.println(String.format("OVERWRITING ARTIFACT TABLE: %s", tableName));
        String sqlClearTable = String.format("TRUNCATE TABLE %s\n", tableName);
        stmt.executeUpdate(sqlClearTable);

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO ARTIFACT TABLE: %s.", filePath, tableName));

        String sqlTrim = String.format("UPDATE %s SET\n", tableName) + 
        "summary = TRIM(TRIM(BOTH '\r' from summary)),\n" +
        "content = TRIM(TRIM(BOTH '\r' from content));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
    }

    public static void createTraceMatrixTable(String tableName, String filePath, String colHeader) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean exists = tableExists(tableName);

            if (exists) {
                overwriteTraceMatrixTable(stmt, tableName, filePath, colHeader);
            } else {
                newTraceMatrixTable(stmt, tableName, filePath, colHeader);
            }
        }
    }

    public static void newTraceMatrixTable(Statement stmt, String tableName, String filePath, String colHeader) throws Exception {
        System.out.println(String.format("CREATING NEW TRACE MATRIX TABLE: %s...", tableName));
        String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) + 
            "id INT AUTO_INCREMENT PRIMARY KEY,\n" + 
            "source VARCHAR(255) NOT NULL,\n" +
            "target VARCHAR(255) NOT NULL,\n" +
            "UNIQUE KEY source_target (source,target)" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED TRACE MATRIX TABLE: %s.", tableName));

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO ARTIFACT TABLE: %s.", filePath, tableName));

        String sqlTrim = String.format("UPDATE %s SET\n", tableName) + 
        "source = TRIM(TRIM(BOTH '\r' from source)),\n" +
        "target = TRIM(TRIM(BOTH '\r' from target));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
    }

    public static void overwriteTraceMatrixTable(Statement stmt, String tableName, String filePath, String colHeader) throws Exception {
        System.out.println(String.format("OVERWRITING TRACE MATRIX TABLE: %s", tableName));
        String sqlClearTable = String.format("TRUNCATE TABLE %s\n", tableName);
        stmt.executeUpdate(sqlClearTable);

        System.out.println(String.format("CLEARED TRACE MATRIX TABLE: %s.", tableName));

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO TRACE MATRIX TABLE: %s.", filePath, tableName));

        String sqlTrim = String.format("UPDATE %s SET\n", tableName) + 
        "source = TRIM(TRIM(BOTH '\r' from source)),\n" +
        "target = TRIM(TRIM(BOTH '\r' from target));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
    }

    public static void missingTraceArtifactsCheck() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean timTraceExists = tableExists("tim_trace_matrix");
            Boolean timArtifactsExists = tableExists("tim_artifacts");

            if (!(timArtifactsExists && timTraceExists)) {
                throw new Exception("Please upload Tim file");
            }

            String sqlTempTable =
                "CREATE TEMPORARY TABLE temp_artifact_check\n" +
                "select trace.artifact, IF(tim_artifacts.artifact IS NULL, 0, 1) as does_exists\n" +
                "from (SELECT source_artifact as artifact FROM tim_trace_matrix\n" +
                "UNION SELECT target_artifact FROM tim_trace_matrix) as trace\n" +
                "LEFT JOIN tim_artifacts ON trace.artifact = tim_artifacts.artifact;";
            
            stmt.executeUpdate(sqlTempTable);
            
            String sqlMissing = "select artifact from temp_artifact_check where does_exists = 0;";
            ResultSet rs = stmt.executeQuery(sqlMissing);
            
            List<String> missingArtifacts = new ArrayList<String>();
            
            while (rs.next()) {
                missingArtifacts.add(rs.getString(1));
            }

            if (missingArtifacts.size() != 0) {
                throw new Exception(String.format("Artifacts: %s do not appear under the datafiles section of your tim.json", missingArtifacts.toString()));
            }
        }
    }

    public static FileInfo getFileInfo() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            System.out.println("getFileInfo");
            FileInfo fileInfo = new FileInfo();

            String sqlArtifactSelect = "select db_table from tim_artifacts";
            ResultSet artifactRs = stmt.executeQuery(sqlArtifactSelect);
            
            System.out.println("tim_artifacts");
            while (artifactRs.next()) {
                String fileName = String.format("\"%s.csv\"", artifactRs.getString(1));
                System.out.println(String.format("Filename: %s, tablename: %s",fileName,artifactRs.getString(1)));

                fileInfo.expectedFiles.add(fileName);

                if (tableExists(artifactRs.getString(1))) {
                    fileInfo.uploadedFiles.add(fileName);
                }
            }
            
            String sqlTraceSelect = "select db_table, is_generated from tim_trace_matrix";
            ResultSet traceRs = stmt.executeQuery(sqlTraceSelect);

            System.out.println("tim_trace_matrix");
            while (traceRs.next()) {
                String fileName = String.format("\"%s.csv\"", traceRs.getString(1));
                System.out.println(String.format("Filename: %s, tablename: %s",fileName,traceRs.getString(1)));

                if (traceRs.getBoolean(2)){ //Generated
                    System.out.println("Generated");
                    fileInfo.expectedGeneratedFiles.add(fileName);

                    if (tableExists(traceRs.getString(1))) {
                        System.out.println("Exists");
                        fileInfo.generatedFiles.add(fileName);
                    }
                } else {
                    fileInfo.expectedFiles.add(fileName);

                    if (tableExists(traceRs.getString(1))) {
                        System.out.println("Exists");
                        fileInfo.uploadedFiles.add(fileName);
                    }
                }
            }

            String.format("Done getFileInfo");
            return fileInfo;
        }
    }

        // sql = "SELECT * FROM TEST";
        // ResultSet rs = stmt.executeQuery(sql);
        // List<ArrayList<Object>> result = new ArrayList<ArrayList<Object>>();
        
        // ArrayList<Object> header = new ArrayList<Object>();
        // header.add("\"SOURCE\"");
        // header.add("\"TARGET\"");
        // header.add("\"SCORE\"");
        // header.add("\"APPROVAL\"");
        // result.add(header);

        // while (rs.next()) {
        //     ArrayList<Object> row = new ArrayList<Object>();
        //     row.add(String.format("\"%s\"",rs.getString(1)));
        //     row.add(String.format("\"%s\"",rs.getString(2)));
        //     row.add(rs.getFloat(3));
        //     row.add(rs.getInt(4));
        //     result.add(row);
        // }

        // byte[] content = result.toString().getBytes();
        // String returnStr = Base64.getEncoder().encodeToString(content);
        
        // conn.close();
        // return returnStr;
}