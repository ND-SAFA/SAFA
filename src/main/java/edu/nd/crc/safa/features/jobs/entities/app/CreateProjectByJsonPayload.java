package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.generation.tgen.entities.TracingRequest;

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
    List<TracingRequest> requests = new ArrayList<>();
}
