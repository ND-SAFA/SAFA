package edu.nd.crc.safa.importer;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class MySQL {

    public MySQL() {}
   
    public static void simpleTransaction() {

        String databaseURL = "jdbc:mysql://mysql:3306/safa-db";
        String user = "user";
        String password = "secret3";
        Connection conn = null;
        try {
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
                
                String sql = "CREATE TABLE TEST " +
                             "(id INTEGER not NULL, " +
                             " first VARCHAR(255), " + 
                             " last VARCHAR(255), " + 
                             " age INTEGER, " + 
                             " PRIMARY KEY ( id ))"; 
          
                stmt.executeUpdate(sql);
                System.out.println("Created table in given database...");
            }
        } catch (ClassNotFoundException ex) {
            System.out.println("Could not find database driver class");
            ex.printStackTrace();
        } catch (SQLException ex) {
            System.out.println("An error occurred. Maybe user/password is invalid");
            ex.printStackTrace();
        } finally {
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
        }
    }
}