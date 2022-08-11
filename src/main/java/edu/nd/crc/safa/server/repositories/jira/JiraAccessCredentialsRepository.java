package edu.nd.crc.safa.server.repositories.jira;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.accounts.SafaUser;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;

import org.springframework.context.annotation.Scope;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
@Scope("singleton")
public interface JiraAccessCredentialsRepository extends JpaRepository<JiraAccessCredentials, UUID> {

    Optional<JiraAccessCredentials> findByUserAndCloudId(SafaUser user, String cloudId);
}
