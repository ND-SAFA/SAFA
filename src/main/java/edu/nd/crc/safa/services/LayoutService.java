package edu.nd.crc.safa.services;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import edu.nd.crc.safa.error.ServerError;

import org.springframework.stereotype.Service;

@Service
public class LayoutService {
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
}
