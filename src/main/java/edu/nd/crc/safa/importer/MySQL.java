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
   
    public static String simpleTransaction() throws Exception {
        String databaseURL = "jdbc:mysql://mysql:3306/safa-db";
        String user = "user";
        String password = "secret3";
        Connection conn = null;
        
        Class.forName("com.mysql.cj.jdbc.Driver");
        // conn = DriverManager.getConnection("jdbc:mysql://localhost/safa-db?" +
        // "user=root&password=secret2");
        conn = DriverManager.getConnection(databaseURL,user,password);
        if (conn != null) {
            System.out.println("Connected to the database");
            System.out.println("Connected database successfully...");

            //STEP 4: Execute a query
            System.out.println("Creating table in given database...");
            Statement stmt = conn.createStatement();
            
            String sql = "CREATE TABLE IF NOT EXISTS TEST " +
                            "(source VARCHAR(255) not NULL, " +
                            " target VARCHAR(255) not NULL, " + 
                            " score FLOAT not NULL, " + 
                            " approval INT not NULL, " + 
                            " PRIMARY KEY ( source ))"; 
        
            stmt.executeUpdate(sql);
            System.out.println("Created table in given database...");

            sql = "INSERT INTO TEST(source, target, score, approval)" + "VALUES('UAV-100', 'UAV-200', 0.15, 0)" + "ON DUPLICATE KEY UPDATE source = 'UAV-100', target = 'UAV-200', score = 0.15, approval = 0";
            stmt.executeUpdate(sql);

            sql = "SELECT * FROM TEST";
            ResultSet rs = stmt.executeQuery(sql);
            List<ArrayList<Object>> result = new ArrayList<ArrayList<Object>>();

            while (rs.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(rs.getString(1));
                row.add(rs.getString(2));
                row.add(rs.getFloat(3));
                row.add(rs.getInt(4));
                result.add(row);
            }

            byte[] content = result.toString().getBytes();
            String returnStr = Base64.getEncoder().encodeToString(content);
            
            conn.close();
            return returnStr;
        } else {
            throw new Exception("Could not connect to Database");
        }
    }   
}