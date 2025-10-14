package edu.nd.crc.safa.features.rules.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.entities.db.Rule;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RuleRepository extends CrudRepository<Rule, UUID> {

    List<Rule> findByProject(Project project);
}
