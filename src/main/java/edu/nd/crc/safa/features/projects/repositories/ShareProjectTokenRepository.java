package edu.nd.crc.safa.features.projects.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.ShareProjectToken;

import org.springframework.data.repository.CrudRepository;

public interface ShareProjectTokenRepository extends CrudRepository<ShareProjectToken, UUID> {

}
