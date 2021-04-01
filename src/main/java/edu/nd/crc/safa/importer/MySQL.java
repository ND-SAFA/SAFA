package edu.nd.crc.safa.importer;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import org.springframework.stereotype.Component;
import java.util.List;
import java.util.Set;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.HashSet;

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
            String sqlTableCheck = String.format("SELECT 1 FROM information_schema.tables where table_schema = 'safa-db' AND table_name = '%s' limit 1;", tableName);
            ResultSet rs = stmt.executeQuery(sqlTableCheck);
            rs.next();
    
            return rs.getRow() != 0;
        }  
    }

    public static Boolean fileExists(String tableName, String filename) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            System.out.println(String.format("Checking if filename: %s exists in table: %s", tableName, filename));
            String sqlTableCheck = String.format("SELECT 1 FROM %s where filename = '%s' limit 1;", tableName, filename);
            ResultSet rs = stmt.executeQuery(sqlTableCheck);
            rs.next();
    
            return rs.getRow() != 0;
        }  
    }
    
    public static void createTableList(String tableName, Boolean generated) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            if (!tableExists("uploaded_and_generated_tables")) {
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", "uploaded_and_generated_tables") + 
                    "tablename VARCHAR(255) PRIMARY KEY,\n" +
                    "is_generated TINYINT NOT NULL" +
                    ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println(String.format("CREATED TABLE: %s.", "uploaded_and_generated_tables"));
            }

            System.out.println(String.format("Updating TABLE: %s...", "uploaded_and_generated_tables"));
            String sqlUpdateTable = String.format("INSERT INTO %s (tablename, is_generated)\n", "uploaded_and_generated_tables") + 
                String.format("VALUES ('%s', %s)\n", tableName, generated) +
                String.format("ON DUPLICATE KEY UPDATE tablename = '%s', is_generated = %s", tableName, generated);
    
            stmt.executeUpdate(sqlUpdateTable);
            System.out.println(String.format("UPDATED TABLE: %s.", "uploaded_and_generated_tables"));
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

        createTableList(tableName, true);
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
        }
    }

    public static void createTimArtifactsTable(String artifact, String filename) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean exists = tableExists("tim_artifact");

            if (exists) {
                updateTimArtifactsTable(stmt, artifact, filename);
            } else {
                newTimArtifactsTable(stmt);
                updateTimArtifactsTable(stmt, artifact, filename);
            }
        }
    }

    public static void newTimArtifactsTable(Statement stmt) throws Exception {
        System.out.println(String.format("CREATING NEW TIM ARTIFACTS TABLE: %s...", "tim_artifact"));
        String sqlCreateTable = String.format("CREATE TABLE %s (\n", "tim_artifact") + 
            "artifact VARCHAR(255) PRIMARY KEY,\n" +
            "tablename VARCHAR(255) NOT NULL" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED NEW TIM ARTIFACTS TABLE: %s.", "tim_artifact"));
    }

    public static void updateTimArtifactsTable(Statement stmt, String artifact, String tablename) throws Exception {
        System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_artifact"));
        String sqlUpdateTable = String.format("INSERT INTO %s (artifact, tablename)\n", "tim_artifact") + 
            String.format("VALUES ('%s', '%s')\n", artifact, tablename) +
            String.format("ON DUPLICATE KEY UPDATE artifact = '%s', tablename = '%s'", artifact, tablename);

        stmt.executeUpdate(sqlUpdateTable);
        System.out.println(String.format("UPDATED TIM ARTIFACTS TABLE: %s.", "tim_artifact"));
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
            "tablename VARCHAR(255) NOT NULL" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
    }

    public static void updateTimTraceMatrixTable(Statement stmt, String traceMatrixName, String traceMatrixTableName, String sourceArtifact, String targetArtifact, Boolean generated) throws Exception {
        System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_trace_matrix"));
        String sqlUpdateTable = String.format("INSERT INTO %s (trace_matrix, source_artifact, target_artifact, is_generated, tablename)\n", "tim_trace_matrix") + 
            String.format("VALUES ('%s', '%s', '%s', %s, '%s')\n", traceMatrixName, sourceArtifact, targetArtifact, generated, traceMatrixTableName) +
            String.format("ON DUPLICATE KEY UPDATE trace_matrix = '%s', source_artifact = '%s', target_artifact = '%s', is_generated = %s, tablename = '%s';", traceMatrixName, sourceArtifact, targetArtifact, generated, traceMatrixTableName);


        stmt.executeUpdate(sqlUpdateTable);
        System.out.println(String.format("UPDATED TIM TRACE MATRIX TABLE: %s.", "tim_trace_matrix"));
    }

    public static void createArtifactTableHelper (Statement stmt, String intTableName, String tableName, String filePath, String colHeader) throws Exception {

        if (tableExists(intTableName)) {
            String sqlTruncate = String.format("TRUNCATE TABLE %s", intTableName);
            stmt.executeUpdate(sqlTruncate);
        } else {
            System.out.println("CREATING INTERMEDIATE ARTIFACT TABLE");
            String sqlCreateTempTable = String.format("CREATE TABLE %s (\n", intTableName) +
                "db_id INT AUTO_INCREMENT PRIMARY KEY,\n" +
                "id VARCHAR(255) NOT NULL,\n" +
                "summary TEXT NOT NULL,\n" + 
                "content TEXT NOT NULL\n" +
            ");";
            stmt.executeUpdate(sqlCreateTempTable);
            System.out.println("CREATED INTERMEDIATE ARTIFACT TABLE");
        }

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, intTableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO INTERMEDIATE TABLE", filePath));

        String sqlTrim = String.format("UPDATE %s SET\n", intTableName) +
            "id = TRIM(TRIM(BOTH '\r' from id)),\n" + 
            "summary = TRIM(TRIM(BOTH '\r' from summary)),\n" +
            "content = TRIM(TRIM(BOTH '\r' from content));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED columns for INTERMEDIATE TABLE");

        String sqlDeleteErrors = String.format("DELETE FROM artifact_error\n") +
            String.format("WHERE tablename = '%s';", tableName);
        
        stmt.executeUpdate(sqlDeleteErrors);

        String sqlInsertDups = "INSERT INTO artifact_error (tablename, id, line, descr)\n" +
            String.format("SELECT '%s', t1.id, t1.db_id, 'DUPLICATE ARTIFACT ID: LINE SKIPPED.' FROM %s t1\n", tableName, intTableName) +
            String.format("INNER JOIN %s t2\n", intTableName) +
            "WHERE t1.db_id > t2.db_id AND t1.id = t2.id;";
        
        stmt.executeUpdate(sqlInsertDups);
        System.out.println("INSERTED Duplicates into TABLE artifact_error\n");

        String sqlLineUpdate = "UPDATE artifact_error SET line = line + 1\n" +
            String.format("WHERE tablename = '%s';", tableName);

        stmt.executeUpdate(sqlLineUpdate);
        System.out.println("Updated Line numbers.\n");
    }
    
    public static void createArtifactTable(String tableName, String filePath, String colHeader) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            String intTableName = "intermediate_" + tableName;
            if (!tableExists("artifact_error")) {
                System.out.println("CREATING NEW ARTIFACT ERROR TABLE: artifact_error...");
                String sqlCreateErrorTable = "CREATE TABLE artifact_error (\n" +
                    "db_id INT AUTO_INCREMENT PRIMARY KEY," +
                    "tablename VARCHAR(255),\n" + 
                    "id VARCHAR(255),\n" +
                    "line INT,\n" +
                    "descr VARCHAR(255) NOT NULL" +
                ");";
                stmt.executeUpdate(sqlCreateErrorTable);
                System.out.println("CREATED NEW ARTIFACT ERROR TABLE: artifact_error...");
            }

            createArtifactTableHelper(stmt, intTableName, tableName, filePath, colHeader);

            if (tableExists(tableName)) {
                String sqlTruncateArtifactTable = String.format("TRUNCATE TABLE %s", tableName);
                stmt.executeUpdate(sqlTruncateArtifactTable);
            } else {
                System.out.println("CREATING NEW ARTIFACT TABLE");
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) +
                    "id VARCHAR(255) PRIMARY KEY,\n" +
                    "summary TEXT NOT NULL,\n" + 
                    "content TEXT NOT NULL" +
                ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println("CREATED NEW ARTIFACT TABLE");
            }

            String sqlUpdateTable = String.format("INSERT INTO %s (id, summary, content)\n", tableName) +
                String.format("SELECT id, summary, content FROM %s\n", intTableName) +
                String.format("ON DUPLICATE KEY UPDATE id = %s.id;", tableName);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println("INSERTED DATA into ARTIFACT TABLE");


            stmt.executeUpdate(String.format("DROP TABLE %s", intTableName));
            System.out.println("DELETED INTERMEDIATE ARTIFACT TABLE");

            createTableList(tableName, false);
        }
    }

    public static void createTraceMatrixHelper (Statement stmt, String intTableName, String tableName, String filePath, String colHeader) throws Exception {
        if (tableExists(intTableName)) {
            String sqlTruncate = String.format("TRUNCATE TABLE %s", intTableName);
            stmt.executeUpdate(sqlTruncate);
        } else {
            System.out.println("CREATING INTERMEDIATE TRACE MATRIX TABLE");
            String sqlCreateTable = String.format("CREATE TABLE %s (\n", intTableName) +
                "db_id INT AUTO_INCREMENT PRIMARY KEY,\n" + 
                "source_id VARCHAR(255),\n" +
                "target_id VARCHAR(255)" +
            ");";
            stmt.executeUpdate(sqlCreateTable);
            System.out.println("CREATED INTERMEDIATE TRACE MATRIX TABLE");
        }

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, intTableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            colHeader + ";";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED FILE: %s INTO INTERMEDIATE TRACE MATRIX TABLE.", filePath));

        String sqlTrim = String.format("UPDATE %s SET\n", intTableName) +
            "source_id = TRIM(TRIM(BOTH '\r' from source_id)),\n" +
            "target_id = TRIM(TRIM(BOTH '\r' from target_id));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED columns for INTERMEDIATE TABLE");

        String sqlDeleteErrors = String.format("DELETE FROM trace_matrix_error\n") +
            String.format("WHERE tablename = '%s';", tableName);
        
        stmt.executeUpdate(sqlDeleteErrors);

        String sqlInsertDups = "INSERT INTO trace_matrix_error (tablename, source_id, target_id, line, descr)\n" +
            String.format("SELECT '%s', t1.source_id, t1.target_id, t1.db_id, 'DUPLICATE LINK: LINE SKIPPED.' FROM %s t1\n", tableName, intTableName) +
            String.format("INNER JOIN %s t2\n", intTableName) +
            "WHERE t1.db_id > t2.db_id AND t1.source_id = t2.source_id AND t1.target_id = t2.target_id;";
        
        stmt.executeUpdate(sqlInsertDups);
        System.out.println("INSERTED Duplicates into TABLE trace_matrix_error\n");

        String sqlLineUpdate = "UPDATE trace_matrix_error SET line = line + 1\n" +
            String.format("WHERE tablename = '%s';", tableName);
        
        stmt.executeUpdate(sqlLineUpdate);
        System.out.println("Updated Line numbers.\n");
    }

    public static void createTraceMatrixTable(String tableName, String filePath, String colHeader) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            String intTableName = "intermediate_" + tableName;

            if (!tableExists("trace_matrix_error")) {
                System.out.println("CREATING NEW Trace Matrix ERROR TABLE: trace_matrix_error...");
                String sqlCreateErrorTable = "CREATE TABLE trace_matrix_error (\n" +
                    "db_id INT AUTO_INCREMENT PRIMARY KEY," +
                    "tablename VARCHAR(255),\n" + 
                    "source_id VARCHAR(255),\n" + 
                    "target_id VARCHAR(255),\n" +
                    "line INT,\n" +
                    "descr VARCHAR(255) NOT NULL" +
                ");";
                stmt.executeUpdate(sqlCreateErrorTable);
                System.out.println("CREATED NEW ARTIFACT ERROR TABLE: trace_matrix_error...");
            }

            createTraceMatrixHelper(stmt, intTableName, tableName, filePath, colHeader);

            if (tableExists(tableName)) {
                String sqlTruncateArtifactTable = String.format("TRUNCATE TABLE %s", tableName);
                stmt.executeUpdate(sqlTruncateArtifactTable);
            } else {
                System.out.println(String.format("CREATING NEW TRACE MATRIX TABLE: %s...", tableName));
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) + 
                    "source_id VARCHAR(255),\n" +
                    "target_id VARCHAR(255),\n" +
                    "PRIMARY KEY (source_id, target_id)" +
                ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println("CREATED NEW TRACE MATRIX TABLE");
            }

            String sqlUpdateTable = String.format("INSERT INTO %s (source_id, target_id)\n", tableName) +
            String.format("SELECT source_id, target_id FROM %s\n", intTableName) +
            String.format("ON DUPLICATE KEY UPDATE source_id = %s.source_id, target_id = %s.target_id;", tableName, tableName);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println("INSERTED DATA from %s into TRACE MATRIX TABLE: %s.");


            stmt.executeUpdate(String.format("DROP TABLE %s", intTableName));
            System.out.println("DELETED INTERMEDIATE TRACE MATRIX TABLE");

            createTableList(tableName, false);
        }
    }

    public static FileInfo getFileInfo() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean timTraceExists = tableExists("tim_trace_matrix");
            Boolean timArtifactsExists = tableExists("tim_artifact");
            FileInfo fileInfo = new FileInfo();

            if (timArtifactsExists) {
                String sqlTimArtifact = "select tablename from tim_artifact";
                ResultSet timArtifactRs = stmt.executeQuery(sqlTimArtifact);
                
                while (timArtifactRs.next()) {
                    String filename = String.format("\"%s.csv\"",timArtifactRs.getString(1));
                    fileInfo.expectedFiles.add(filename);
    
                    if (tableExists(timArtifactRs.getString(1))){
                        fileInfo.uploadedFiles.add(filename);
                    }
                }
            }

            if (timTraceExists) {
                String sqlTraceSelect = "select tablename, is_generated from tim_trace_matrix";
                ResultSet timTraceRs = stmt.executeQuery(sqlTraceSelect);
        
                while (timTraceRs.next()) {
                    if (timTraceRs.getBoolean(2)){ //Generated
                        String filename = String.format("\"%s\"",timTraceRs.getString(1));
                        fileInfo.expectedGeneratedFiles.add(filename);

                        if (tableExists(timTraceRs.getString(1))){
                            fileInfo.generatedFiles.add(filename);
                        }
                    }
                    else {
                        String filename = String.format("\"%s.csv\"",timTraceRs.getString(1));
                        fileInfo.expectedFiles.add(filename);

                        if (tableExists(timTraceRs.getString(1))){
                            fileInfo.uploadedFiles.add(filename);
                        }
                    }
                }
            }

            return fileInfo;
        }
    }

    public static void traceArtifactCheck() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            Boolean timTraceExists = tableExists("tim_trace_matrix");
            Boolean timArtifactsExists = tableExists("tim_artifact");

            if (timTraceExists && timArtifactsExists) {
                String sqlCheck = "SELECT trace.artifact FROM\n" +
                    "(SELECT source_artifact AS artifact FROM tim_trace_matrix UNION SELECT target_artifact FROM tim_trace_matrix) AS trace\n" +
                    "LEFT JOIN tim_artifact ON tim_artifact.artifact = trace.artifact\n" +
                    "WHERE tim_artifact.artifact IS NULL;";
                
                ResultSet rs = stmt.executeQuery(sqlCheck);
                
                List<String> missingArtifacts = new ArrayList<String>();
            
                while (rs.next()) {
                    missingArtifacts.add(rs.getString(1));
                }

                if (missingArtifacts.size() != 0) {
                    throw new Exception(String.format("Artifacts: %s do not appear under the datafiles section of your tim.json", missingArtifacts.toString()));
                }
            }
        }
    }

    public static String getLinkErrors() throws Exception {
        HashMap<String, Set<String>> artifact_map = new HashMap<String, Set<String>>();
        String errorText = "";
        
        List<List<String>> artifact_rows = getTimArtifactData();

        for (List<String> artifact_row : artifact_rows) {
            String artifact_name = artifact_row.get(0);
            String artifact_tablename  = artifact_row.get(1);
            Set<String> ids = new HashSet<String>();

            List<List<String>> artifact_data_rows = getArtifactData(artifact_tablename);
            for (List<String> row : artifact_data_rows) {
                ids.add(row.get(0));
            }

            artifact_map.put(artifact_name,ids);
        }

        List<List<String>> trace_rows = getTimTraceData();

        for (List<String> trace_row : trace_rows) {
            if (trace_row.get(3).equals("1")) {
                continue;
            }

            String tracematrix = trace_row.get(0);

            String source_artifact = trace_row.get(1);
            Set<String> source_ids = artifact_map.get(source_artifact);

            String target_artifact = trace_row.get(2);
            Set<String> target_ids = artifact_map.get(target_artifact);

            String trace_tablename = trace_row.get(4);

            if (source_ids == null && target_ids == null){
                errorText += String.format("ERROR: TRACE MATRIX: %s DESC: source artifact: %s and target artifact: %s does not exist in the database. Make sure these artifacts are part of your tim file.\n", tracematrix, source_artifact, target_artifact);
                continue;
            }

            if (source_ids == null){
                errorText += String.format("ERROR: TRACE MATRIX: %s DESC: source artifact %s does not exist in the database. Make sure this artifact is part of your tim file.\n", tracematrix, source_artifact);
                continue;
            } 

            if (target_ids == null){
                errorText += String.format("ERROR: TRACE MATRIX: %s DESC: target artifact %s does not exist in the database. Make sure this artifact is part of your tim file.\n", tracematrix, target_artifact);
                continue;
            } 

            int line_num = 0;
            List<List<String>> trace_data_rows = getNonGeneratedTraceData(trace_tablename);
            
            for (List<String> row : trace_data_rows) {
                String sid = row.get(0);
                String tid = row.get(1);
                line_num++;

                if (!source_ids.contains(sid)) {
                    errorText += String.format("ERROR: TRACE MATRIX: %s Line Number: %s DESC: source artifact %s does not contain ID: %s\n", tracematrix, line_num, source_artifact, sid);

                }

                if (!target_ids.contains(tid)) {
                    errorText += String.format("ERROR: TRACE MATRIX: %s Line Number: %s DESC: source artifact %s does not contain ID: %s\n", tracematrix, line_num, target_artifact, tid);
                }                
            }
        }
        
        return Base64.getEncoder().encodeToString(errorText.getBytes());
    }

    public static String getUploadErrorLog() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            System.out.println("Upload Flatfile Error Log...");

            if ( !(tableExists("artifact_error") && tableExists("trace_matrix_error")) ){
                System.out.println("Upload Flatfile Error Log: Empty...");
                return "";
            }
            
            List<ArrayList<Object>> result = new ArrayList<ArrayList<Object>>();

            ArrayList<Object> artifactHeader = new ArrayList<Object>();
            artifactHeader.add("\"FILE NAME\"");
            artifactHeader.add("\"ID\"");
            artifactHeader.add("\"LINE\"");
            artifactHeader.add("\"DESC\"");
            result.add(artifactHeader);

            String sqlArtifactError = "SELECT tablename, id, line, descr FROM artifact_error";
            ResultSet rsArtifactError = stmt.executeQuery(sqlArtifactError);

            while (rsArtifactError.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(String.format("\"%s\"",rsArtifactError.getString(2)));
                row.add(String.format("\"%s\"",rsArtifactError.getString(3)));
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

            String sqlTraceError = "SELECT tablename, source_id, target_id, line, descr FROM trace_matrix_error";
            ResultSet rsTraceError = stmt.executeQuery(sqlTraceError);

            while (rsTraceError.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(String.format("\"%s\"",rsTraceError.getString(2)));
                row.add(String.format("\"%s\"",rsTraceError.getString(3)));
                row.add(String.format("\"%s\"",rsTraceError.getString(4)));
                row.add(rsTraceError.getInt(5));
                row.add(String.format("\"%s\"",rsTraceError.getString(6)));
                result.add(row);
            }
            
            byte[] content = result.toString().getBytes();
            String returnStr = Base64.getEncoder().encodeToString(content);
            
            return returnStr;
        }
    }

    public static String clearUploadedFlatfiles() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            if (tableExists("uploaded_and_generated_tables")) {
                String sqlUploadedFiles = "SELECT tablename\n" +
                    "FROM uploaded_and_generated_tables\n" +
                    "WHERE is_generated = 0;";

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

                String deleteTables = tables.toString().replace("[","").replace("]", "");
                String sqlDropTables = String.format("DROP TABLES %s;", deleteTables);
                stmt.executeUpdate(sqlDropTables);

                String sqlDeleteTables = "DELETE FROM uploaded_and_generated_tables WHERE is_generated = 0;";
                stmt.executeUpdate(sqlDeleteTables);

                return "Uploaded files have successfully been cleared";
            }
            else {
                return "No uploaded files";
            }
        }
    }

    public static String clearGeneratedFlatfiles() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            if (tableExists("uploaded_and_generated_tables")) {
                String sqlUploadedFiles = "SELECT tablename\n" +
                    "FROM uploaded_and_generated_tables\n" +
                    "WHERE is_generated = 1;";

                ResultSet rs = stmt.executeQuery(sqlUploadedFiles);
                ArrayList<String> tables = new ArrayList<String>();

                while (rs.next()) {
                    tables.add(rs.getString(1));
                }

                if (tables.size() == 0) {
                    stmt.executeUpdate("DROP TABLE uploaded_and_generated_tables");
                    return "No generated files";
                }

                String deleteTables = tables.toString().replace("[","").replace("]", "");
                String sqlDropTables = String.format("DROP TABLES %s;", deleteTables);
                stmt.executeUpdate(sqlDropTables);

                String sqlDeleteTables = "DELETE FROM uploaded_and_generated_tables WHERE is_generated = 1;";
                stmt.executeUpdate(sqlDeleteTables);

                return "Generated files have successfully been cleared";
            }
            else {
                return "No generated files";
            }
        }
    }

    public static List<List<String>> generateInfo() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();
    
            String sqlUploadedFiles = "SELECT tim_source.tablename as source_tablename,\n" +
                "tim_target.tablename as target_tablename,\n" +
                "tim_trace_matrix.tablename as dest_tablename\n" +
                "FROM tim_trace_matrix\n" +
                "LEFT JOIN tim_artifact as tim_source\n" + 
                "ON tim_source.artifact = tim_trace_matrix.source_artifact\n" +
                "AND is_generated = 1\n" +
                "LEFT JOIN tim_artifact as tim_target\n" +
                "ON tim_target.artifact = tim_trace_matrix.target_artifact\n" +
                "AND is_generated = 1\n" +
                "where tim_source.tablename IS NOT NULL AND tim_target.tablename IS NOT NULL;";
            
            ResultSet rs = stmt.executeQuery(sqlUploadedFiles);
            
            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getString(3));
                data.add(row);
            }

            return data;
        }
    }

    public static List<List<String>> getArtifactData(String tablename) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();
    
            String sqlGetData = String.format("SELECT id, summary, content FROM %s;", tablename);
             
            ResultSet rs = stmt.executeQuery(sqlGetData);
            
            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getString(3));
                data.add(row);
            }

            return data;
        }
    }

    public static List<List<String>> getNonGeneratedTraceData(String tablename) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();
    
            String sqlGetData = String.format("SELECT source_id, target_id FROM %s;", tablename);
             
            ResultSet rs = stmt.executeQuery(sqlGetData);
            
            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                data.add(row);
            }

            return data;
        }
    }

    public static List<List<String>> getGeneratedTraceData(String tablename) throws Exception {
        try (Statement stmt = startDB().createStatement()) {
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
        }
    }

    public static List<List<String>> getTimArtifactData() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();

            String sqlGetData = String.format("SELECT artifact, tablename FROM %s;", "tim_artifact");
             
            ResultSet rs = stmt.executeQuery(sqlGetData);
            
            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                data.add(row);
            }

            return data;
        }
    }

    public static List<List<String>> getTimTraceData() throws Exception {
        try (Statement stmt = startDB().createStatement()) {
            List<List<String>> data = new ArrayList<List<String>>();

            String sqlGetData = String.format("SELECT trace_matrix, source_artifact, target_artifact, is_generated, tablename FROM %s;", "tim_trace_matrix");
             
            ResultSet rs = stmt.executeQuery(sqlGetData);
            
            while (rs.next()) {
                List<String> row = new ArrayList<String>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getString(3));
                row.add(rs.getString(4));
                row.add(rs.getString(5));
                data.add(row);
            }

            return data;
        }
    }
}