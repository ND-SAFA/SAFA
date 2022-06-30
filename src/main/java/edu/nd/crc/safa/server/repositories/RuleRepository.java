package edu.nd.crc.safa.server.repositories;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Rule;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RuleRepository extends CrudRepository<Rule, UUID> {
}
