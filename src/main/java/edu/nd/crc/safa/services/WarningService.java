package edu.nd.crc.safa.services;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.warnings.Rule;

import org.springframework.stereotype.Service;

@Service
public class WarningService {
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
}
