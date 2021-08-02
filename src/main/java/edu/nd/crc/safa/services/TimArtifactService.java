package edu.nd.crc.safa.services;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.TIMFileRepository;
import edu.nd.crc.safa.error.ServerError;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TimArtifactService {

    SessionFactory sessionFactory;
    ArtifactRepository artifactRepository;
    TIMFileRepository timFileRepository;

    @Autowired
    public TimArtifactService(SessionFactory sessionFactory,
                              ArtifactRepository artifactRepository,
                              TIMFileRepository timFileRepository) {
        this.sessionFactory = sessionFactory;
        this.artifactRepository = artifactRepository;
        this.timFileRepository = timFileRepository;
    }

    public void createTimArtifactsTable(String artifact, String tablename, String filename)
        throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            Boolean exists = tableExists("tim_artifact");

            if (exists) {
                updateTimArtifactsTable(stmt, artifact, tablename, filename);
            } else {
                newTimArtifactsTable(stmt);
                updateTimArtifactsTable(stmt, artifact, tablename, filename);
            }
        } catch (SQLException e) {
            throw new ServerError("creating TIM artifact table", e);
        }
    }

    public void clearTimTables() throws ServerError {

        try (Session session = sessionFactory.openSession()) {
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
        } catch (SQLException e) {
            throw new ServerError("clearing TIM tables", e);
        }
    }

    public void newTimArtifactsTable(Statement stmt) throws ServerError {
        try {
            System.out.println(String.format("CREATING NEW TIM ARTIFACTS TABLE: %s...", "tim_artifact"));
            String sqlCreateTable = String.format("CREATE TABLE %s (\n", "tim_artifact")
                + "artifact VARCHAR(255) PRIMARY KEY,\n"
                + "tablename VARCHAR(255) NOT NULL,\n"
                + "filename VARCHAR(255) NOT NULL"
                + ");";

            stmt.executeUpdate(sqlCreateTable);
            System.out.println(String.format("CREATED NEW TIM ARTIFACTS TABLE: %s.", "tim_artifact"));
        } catch (SQLException e) {
            throw new ServerError("new TIM artifact table", e);
        }
    }

    public void updateTimArtifactsTable(Statement stmt, String artifact, String tablename, String filename)
        throws ServerError {
        try {
            System.out.println(String.format("Updating TIM ARTIFACTS TABLE: %s...", "tim_artifact"));
            String sqlUpdateTable = String.format("INSERT INTO %s (artifact, tablename, filename)\n", "tim_artifact")
                + String.format("VALUES ('%s', '%s', '%s')\n", artifact, tablename, filename)
                + String.format("ON DUPLICATE KEY UPDATE artifact = '%s', tablename = '%s', filename = '%s'",
                artifact, tablename, filename);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println(String.format("UPDATED TIM ARTIFACTS TABLE: %s.", "tim_artifact"));
        } catch (SQLException e) {
            throw new ServerError("updating TIM artifact table", e);
        }
    }

    public void traceArtifactCheck() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            Boolean timTraceExists = tableExists("tim_trace_matrix");
            Boolean timArtifactsExists = tableExists("tim_artifact");

            if (timTraceExists && timArtifactsExists) {
                String sqlCheck = "SELECT trace.artifact FROM\n"
                    +
                    "(SELECT source_artifact AS artifact FROM tim_trace_matrix UNION SELECT target_artifact FROM"
                    + " tim_trace_matrix) AS trace\n"
                    + "LEFT JOIN tim_artifact ON tim_artifact.artifact = trace.artifact\n"
                    + "WHERE tim_artifact.artifact IS NULL;";

                ResultSet rs = stmt.executeQuery(sqlCheck);

                List<String> missingArtifacts = new ArrayList<String>();

                while (rs.next()) {
                    missingArtifacts.add(rs.getString(1));
                }

                if (missingArtifacts.size() != 0) {
                    throw new ServerError(String.format("Artifacts: %s do not appear under the datafiles section of "
                        + "your tim.json", missingArtifacts.toString()));
                }
            }
        } catch (SQLException e) {
            throw new ServerError("trace artifact check", e);
        }
    }
}
