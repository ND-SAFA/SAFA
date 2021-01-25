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

    public static void createGeneratedTable(String tableName, String filePath) throws Exception {
        Connection conn = startDB();
        //STEP 4: Execute a query
        System.out.println("Creating table in given database...");
        Statement stmt = conn.createStatement();
        
        String sqlCreateTable = String.format("CREATE TABLE IF NOT EXISTS %s (\n", tableName.toUpperCase()) +
                        "ID INT AUTO_INCREMENT PRIMARY KEY,\n" + 
                        "SOURCE VARCHAR(255) NOT NULL,\n" +
                        "TARGET VARCHAR(255) NOT NULL,\n" + 
                        "SCORE FLOAT NOT NULL,\n" + 
                        "APROVAL INT DEFAULT 2,\n" + 
                        "UNIQUE KEY SOURCE_TARGET (SOURCE,TARGET)\n" +
                        ");";
    
        stmt.executeUpdate(sqlCreateTable);
        System.out.println(String.format("Created table: %s in given database...", tableName));

        String sqlLoadData = String.format("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s\n", filePath, tableName.toUpperCase()) +
            "FIELDS TERMINATED BY ','\n" +
            "ENCLOSED BY '\"'\n" +
            "LINES TERMINATED BY '\\n'\n" +
            "IGNORE 1 ROWS\n" +
            "(SOURCE, TARGET, SCORE);\n";

        stmt.executeUpdate(sqlLoadData);
        System.out.println(String.format("Loaded file: %s into table: %s...", filePath, tableName));
        conn.close();
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