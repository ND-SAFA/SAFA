package edu.nd.crc.safa.features.organizations.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Team;

import org.springframework.data.repository.CrudRepository;

public interface TeamRepository extends CrudRepository<Team, UUID> {
}
