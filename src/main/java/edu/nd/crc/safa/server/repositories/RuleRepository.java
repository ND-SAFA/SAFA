package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.Rule;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RuleRepository extends CrudRepository<Rule, UUID> {

    List<Rule> findByProject(Project project);
}
