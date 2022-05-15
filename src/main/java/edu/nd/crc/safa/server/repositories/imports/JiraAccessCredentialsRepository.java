package edu.nd.crc.safa.server.repositories.imports;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JiraAccessCredentialsRepository extends JpaRepository<JiraAccessCredentials, UUID> {

    Optional<JiraAccessCredentials> findByUserAndCloudId(SafaUser user, String cloudId);
}
