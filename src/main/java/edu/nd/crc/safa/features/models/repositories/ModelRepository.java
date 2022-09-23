package edu.nd.crc.safa.features.models.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.Model;

import org.springframework.data.repository.CrudRepository;

public interface ModelRepository extends CrudRepository<Model, UUID> {
}
