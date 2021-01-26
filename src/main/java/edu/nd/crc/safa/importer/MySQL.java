package edu.nd.crc.safa.importer;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
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
            throw new Exception("Could not connect to Database");
        }

        System.out.println("Connected to the database");
        System.out.println("Connected database successfully...");

        return conn;
    }

    public static void createGeneratedTable(String name, String filePath) throws Exception {
        Connection conn = startDB();
        //STEP 4: Execute a query
        System.out.println("Creating table in given database...");
        Statement stmt = conn.createStatement();
        String tableName = name.toUpperCase();
        
        try {
            String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName) +
                            "ID INT AUTO_INCREMENT PRIMARY KEY,\n" + 
                            "SOURCE VARCHAR(255) NOT NULL,\n" +
                            "TARGET VARCHAR(255) NOT NULL,\n" + 
                            "SCORE FLOAT NOT NULL,\n" + 
                            "APPROVAL INT NOT NULL DEFAULT 2,\n" + 
                            "UNIQUE KEY SOURCE_TARGET (SOURCE,TARGET)\n" +
                            ");";
        
            stmt.executeUpdate(sqlCreateTable);
            System.out.println(String.format("Created table: %s in given database...", tableName));

            String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName) +
                "FIELDS TERMINATED BY ','\n" +
                "ENCLOSED BY '\"'\n" +
                "LINES TERMINATED BY '\\n'\n" +
                "IGNORE 1 ROWS\n" +
                "(SOURCE, TARGET, SCORE);";

            stmt.executeUpdate(sqlLoadData);
            System.out.println(String.format("Loaded file: %s into table: %s...", filePath, tableName));
        } catch(SQLException e) {
            if (e.getErrorCode() == 1050){ // Table already exists error
                modifyGeneratedTable(stmt, tableName, filePath);
            } else {
                throw new SQLException(e);
            }
        }
        conn.close();
    }

    public static void modifyGeneratedTable(Statement stmt, String tableName, String filePath) throws Exception {
        System.out.println("Modify Generated Table...");

        String tempTableName = String.format("TEMP_%s", tableName);
        String newTable = String.format("NEW_%s", tableName);

        String sqlCreateTempTable = String.format("CREATE TEMPORARY TABLE %s\n", tempTableName) + 
        String.format("SELECT * FROM %s\n", tableName) +
        "LIMIT 0;";
        
        stmt.executeUpdate(sqlCreateTempTable);
        System.out.println("Created Temporary Table.");

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tempTableName) +
        "FIELDS TERMINATED BY ','\n" +
        "ENCLOSED BY '\"'\n" +
        "LINES TERMINATED BY '\\n'\n" +
        "IGNORE 1 ROWS\n" +
        "(SOURCE, TARGET, SCORE);";

        stmt.executeUpdate(sqlLoadData);
        System.out.println("Loaded Data into Temporary Table.");

        String sqlCreateNewTable = String.format("CREATE TABLE %s (\n", newTable) + // Create New Table.
        "ID INT AUTO_INCREMENT PRIMARY KEY,\n" + 
        "SOURCE VARCHAR(255) NOT NULL,\n" +
        "TARGET VARCHAR(255) NOT NULL,\n" + 
        "SCORE FLOAT NOT NULL,\n" + 
        "APPROVAL INT NOT NULL DEFAULT 2,\n" + 
        "UNIQUE KEY SOURCE_TARGET (SOURCE,TARGET)\n" +
        ");";

        stmt.executeUpdate(sqlCreateNewTable);
        System.out.println("Created New Table.");

        String sqlJoin = String.format("INSERT INTO %s (SOURCE, TARGET, SCORE, APPROVAL)\n", newTable) +
            "SELECT TEMP.SOURCE, TEMP.TARGET, TEMP.SCORE, IFNULL(OLD.APPROVAL,2)\n" +
            String.format("FROM %s TEMP\n", tempTableName) +
            String.format("LEFT JOIN %s OLD\n", tableName) +
            "ON TEMP.SOURCE = OLD.SOURCE AND TEMP.TARGET = OLD.TARGET\n";

        stmt.executeUpdate(sqlJoin);
        System.out.println("Performed Join operation between Temporary Table and Old Table. Stored result in New Table.");

        String dropTables = String.format(String.format("DROP TABLES %s, %s", tempTableName, tableName));
        stmt.executeUpdate(dropTables);
        System.out.println("Deleted Temporary Table and Old Table.");

        String renameNewTable = String.format("RENAME TABLE %s TO %s", newTable, tableName);
        stmt.executeUpdate(renameNewTable);
        System.out.println("Renamed New Table to Old Table. Modify Generated Table Complete!");
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