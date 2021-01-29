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
        String databaseURL = "jdbc:mysql://mysql:3306/safa-db";
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

    public static void createGeneratedTable(String tableName, String filePath) throws Exception {
        Connection conn = startDB();

        try (Statement stmt = conn.createStatement()) {
            Boolean exists = tableExists(stmt, tableName);

            if (exists) {
                updateGeneratedTable(stmt, tableName, filePath);
            } else {
                newGeneratedTable(stmt, tableName, filePath);
            }
        }
    }

    public static void newGeneratedTable(Statement stmt, String tableName, String filePath) throws Exception {
        System.out.println(String.format("CREATING NEW GENERATED TABLE: %s...", tableName));

        String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) +
            "ID INT AUTO_INCREMENT PRIMARY KEY,\n" + 
            "SOURCE VARCHAR(255) NOT NULL,\n" +
            "TARGET VARCHAR(255) NOT NULL,\n" + 
            "SCORE FLOAT NOT NULL,\n" + 
            "APPROVAL INT NOT NULL DEFAULT 2,\n" + 
            "UNIQUE KEY SOURCE_TARGET (SOURCE,TARGET)\n" +
        ");";

        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("CREATED NEW GENERATED TABLE: %s.", tableName));

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            "(SOURCE, TARGET, SCORE);";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED GENERATED FILE: %s INTO TABLE: %s.", filePath, tableName));

        String sqlTrim = String.format("UPDATE %s SET\n", tableName) + 
        "SOURCE = TRIM(TRIM(BOTH '\r' from SOURCE)),\n" +
        "TARGET = TRIM(TRIM(BOTH '\r' from TARGET));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
    }

    public static void updateGeneratedTable(Statement stmt, String tableName, String filePath) throws Exception {
        System.out.println(String.format("UPDATING GENERATED TABLE: %s...", tableName));

        String tempTableName = String.format("TEMP_%s", tableName);
        String newTable = String.format("NEW_%s", tableName);

        String sqlCreateTempTable = String.format("CREATE TEMPORARY TABLE %s\n", tempTableName) + 
        String.format("SELECT * FROM %s\n", tableName) + "LIMIT 0;";
        
        stmt.executeUpdate(sqlCreateTempTable);
        System.out.println("CREATED TEMPORARY TABLE.");

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tempTableName) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            "(SOURCE, TARGET, SCORE);";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("LOADED DATA FILE: %s INTO TEMPORARY TABLE.", filePath));

        String sqlTrim = String.format("UPDATE %s SET\n", tempTableName) + 
            "SOURCE = TRIM(TRIM(BOTH '\r' from SOURCE)),\n" +
            "TARGET = TRIM(TRIM(BOTH '\r' from TARGET));";
            
        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");

        if (tableExists(stmt, newTable)){
            String sqlDelete = String.format("DROP TABLE %s",newTable);
            stmt.executeUpdate(sqlDelete);
            System.out.println("DELETED ABANDONED GENERATED TABLE");
        }

        String sqlCreateNewTable = String.format("CREATE TABLE %s (\n", newTable) + // Create New Table.
            "ID INT AUTO_INCREMENT PRIMARY KEY,\n" + 
            "SOURCE VARCHAR(255) NOT NULL,\n" +
            "TARGET VARCHAR(255) NOT NULL,\n" + 
            "SCORE FLOAT NOT NULL,\n" + 
            "APPROVAL INT NOT NULL DEFAULT 2,\n" + 
            "UNIQUE KEY SOURCE_TARGET (SOURCE,TARGET)\n" +
        ");";

        stmt.executeUpdate(sqlCreateNewTable);
        System.out.println("CREATED NEW GENERATED TABLE.");

        String sqlJoin = String.format("INSERT INTO %s (SOURCE, TARGET, SCORE, APPROVAL)\n", newTable) +
            "SELECT TEMP.SOURCE, TEMP.TARGET, TEMP.SCORE, IFNULL(OLD.APPROVAL,2)\n" +
            String.format("FROM %s TEMP\n", tempTableName) +
            String.format("LEFT JOIN %s OLD\n", tableName) +
            "ON TEMP.SOURCE = OLD.SOURCE AND TEMP.TARGET = OLD.TARGET\n";

        stmt.executeUpdate(sqlJoin);
        System.out.println("UPDATED TABLE.");

        String dropTables = String.format(String.format("DROP TABLES %s, %s", tempTableName, tableName));
        stmt.executeUpdate(dropTables);
        System.out.println("DELETED TEMPORARY AND OLD TABLE.");

        String renameNewTable = String.format("RENAME TABLE %s TO %s", newTable, tableName);
        stmt.executeUpdate(renameNewTable);
        System.out.println("RENAMED NEW TABLE TO OLD TABLE.");
    }

    public static void createArtifactTable(String tableName, String filePath, String colHeader) throws Exception {
        Connection conn = startDB();

        try (Statement stmt = conn.createStatement()) {
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
            "ID VARCHAR(255) PRIMARY KEY,\n" +
            "SUMMARY TEXT NOT NULL,\n" + 
            "CONTENT TEXT NOT NULL\n" +
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
        "SUMMARY = TRIM(TRIM(BOTH '\r' from SUMMARY)),\n" +
        "CONTENT = TRIM(TRIM(BOTH '\r' from CONTENT));";

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
        "SUMMARY = TRIM(TRIM(BOTH '\r' from SUMMARY)),\n" +
        "CONTENT = TRIM(TRIM(BOTH '\r' from CONTENT));";

        stmt.executeUpdate(sqlTrim);
        System.out.println("TRIMMED WHITESPACE STORED IN COLUMNS");
    }

    public static void createTraceMatrixTable(String tableName, String filePath, String colHeader) throws Exception {
        Connection conn = startDB();

        try (Statement stmt = conn.createStatement()) {
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
            "ID INT AUTO_INCREMENT PRIMARY KEY,\n" + 
            "SOURCE VARCHAR(255) NOT NULL,\n" +
            "TARGET VARCHAR(255) NOT NULL,\n" +
            "UNIQUE KEY SOURCE_TARGET (SOURCE,TARGET)\n" +
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
        "SOURCE = TRIM(TRIM(BOTH '\r' from SOURCE)),\n" +
        "TARGET = TRIM(TRIM(BOTH '\r' from TARGET));";

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
        "SOURCE = TRIM(TRIM(BOTH '\r' from SOURCE)),\n" +
        "TARGET = TRIM(TRIM(BOTH '\r' from TARGET));";

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