package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;

import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.tgen.entities.ArtifactTypeTraceGenerationRequestDTO;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Payload used to create project via JSON.
 */
@NoArgsConstructor
@Data
public class CreateProjectByJsonPayload {
    /**
     * The project entities to commit.
     */
    ProjectAppEntity project;
    /**
     * The traces to generate.
     */
    List<@Valid ArtifactTypeTraceGenerationRequestDTO> requests = new ArrayList<>();
}
