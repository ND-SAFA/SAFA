package edu.nd.crc.safa.database.repositories;

import java.util.UUID;

import edu.nd.crc.safa.entities.TraceMatrix;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceMatrixRepository extends CrudRepository<TraceMatrix, UUID> {
}
