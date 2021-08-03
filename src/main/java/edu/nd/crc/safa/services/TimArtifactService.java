package edu.nd.crc.safa.services;

import java.sql.SQLException;
import java.sql.Statement;

import javax.naming.OperationNotSupportedException;

import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.TIMFileRepository;
import edu.nd.crc.safa.server.error.ServerError;

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

    public void verifyArtifactUploaded() throws OperationNotSupportedException {
        //TODO: Implement verification check that all artifacts exist
        throw new OperationNotSupportedException("project upload verificatin is under construction");
    }
}
