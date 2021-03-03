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
import java.util.ArrayList;
import java.util.Base64;

@Component
public class MySQL {

    public MySQL() {}

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

    public static Boolean tableExists(Statement stmt, String tableName) throws Exception {
        String sqlTableCheck = String.format("SELECT COUNT(*) FROM information_schema.tables where table_schema = 'safa-db' AND table_name = '%s';", tableName);
        ResultSet rs = stmt.executeQuery(sqlTableCheck);
        rs.next();

        return rs.getInt("COUNT(*)") != 0;
    }

    public static void createGeneratedTraceMatrixTable(String tableName, String filePath) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean exists = tableExists(stmt, tableName);

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

        if (tableExists(stmt, newTable)){
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
            "ON temp.source = old.source AND temp.target = old.target\n";

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
            Boolean artifactsExists = tableExists(stmt, "tim_artifacts");
            Boolean traceExists = tableExists(stmt, "tim_trace_matrix");

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
            Boolean exists = tableExists(stmt, "tim_artifacts");

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
            Boolean exists = tableExists(stmt, "tim_trace_matrix");

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
            "source_artifact VARCHAR(255),\n" +
            "target_artifact VARCHAR(255),\n" +
            "is_generated TINYINT,\n" +
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
            Boolean exists = tableExists(stmt, tableName);

            if (exists) {
                overwriteArtifactTable(stmt, tableName, filePath, colHeader);
            } else {
                newArtifactTable(stmt, tableName, filePath, colHeader);
            }
        }
    }

    public static void newArtifactTable(Statement stmt, String tableName, String filePath, String colHeader) throws Exception {
        System.out.println(String.format("CREATING NEW ARTIFACT TABLE: %s...", tableName));
        String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) + 
            "id VARCHAR(255) PRIMARY KEY,\n" +
            "summary TEXT NOT NULL,\n" + 
            "content TEXT NOT NULL\n" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED NEW ARTIFACT TABLE: %s.", tableName));

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO TABLE: %s.", filePath, tableName));

        String sqlTrim = String.format("UPDATE %s SET\n", tableName) + 
        "summary = TRIM(TRIM(BOTH '\r' from summary)),\n" +
        "content = TRIM(TRIM(BOTH '\r' from content));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
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
            Boolean exists = tableExists(stmt, tableName);

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
            "UNIQUE KEY source_target (source,target)\n" +
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