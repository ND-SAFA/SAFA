package edu.nd.crc.safa.features.flatfiles.services;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.repositories.ArtifactTypeRepository;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing, validating, and creating trace links.
 *
 * <p>A TraceMatrixDefinition is a JSON object defining:
 * source: String - the name of the source artifact's type
 * target: String - the name of the target artifact's type
 * file: String - name of uploaded file containing the matrices links.
 *
 * <p>Such that the keys are in lower case.
 */
@Component
@AllArgsConstructor
public class ArtifactTypeService {

    private final ArtifactTypeRepository artifactTypeRepository;

    public ArtifactType findArtifactType(Project project, String typeName)
        throws SafaError {
        Optional<ArtifactType> sourceTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName);

        if (sourceTypeQuery.isEmpty()) {
            List<ArtifactType> artifactTypes = this.artifactTypeRepository.findByProject(project);
            String errorMessage = getUnknownTypeError(typeName, artifactTypes);
            throw new SafaError(errorMessage);
        }
        return sourceTypeQuery.get();
    }

    private String getUnknownTypeError(String typeName, List<ArtifactType> artifactTypes) {
        return String.format(
            "Trace matrix definition references unknown type: %s. Defined types include: %s",
            typeName,
            artifactTypes);
    }
}
