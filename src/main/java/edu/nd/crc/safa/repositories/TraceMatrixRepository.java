package edu.nd.crc.safa.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.TraceMatrix;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TraceMatrixRepository extends CrudRepository<TraceMatrix, UUID> {

    List<TraceMatrix> findByProject(Project project);
}
