package edu.nd.crc.safa.server.services.jira;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.springframework.data.jpa.repository.JpaRepository;

public interface JiraAccessCredentialsRepository extends JpaRepository<JiraAccessCredentials, UUID> {

    Optional<JiraAccessCredentials> findByUser(SafaUser user);
}
