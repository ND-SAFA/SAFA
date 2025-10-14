package edu.nd.crc.safa.features.artifacts.entities;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

public class ArtifactLookupTable {
    private final List<ArtifactVersion> artifactVersions;
    private final Map<String, ArtifactVersion> name2version;

    public ArtifactLookupTable(List<ArtifactVersion> artifactVersions) {
        this.artifactVersions = artifactVersions;
        this.name2version = ProjectDataStructures.createEntityLookup(
            artifactVersions, ArtifactVersion::getName);
    }

    /**
     * Converts artifact versions to generational artifacts.
     *
     * @return List of GEN artifacts.
     */
    public List<GenerationArtifact> getGenerationArtifacts() {
        return this.artifactVersions
            .stream()
            .map(GenerationArtifact::new)
            .toList();
    }

    /**
     * Retrieves artifact version for artifact with given name.
     *
     * @param name The name of the artifact.
     * @return Version of the artifact with given name.
     */
    public ArtifactVersion getByName(String name) {
        return name2version.get(name);
    }
}
