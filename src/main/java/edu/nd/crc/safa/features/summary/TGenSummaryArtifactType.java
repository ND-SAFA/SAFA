package edu.nd.crc.safa.features.summary;

import java.util.List;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Enumerates all the different types of artifacts that can be sumarized.
 */
@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum TGenSummaryArtifactType {
    /**
     * Identifies natural language artifacts.
     */
    NL("*"),
    /**
     * Identifies python files.
     */
    PY(".py"),
    /**
     * Identifies java files.
     */
    JAVA(".java");

    String fileExtension;

    /**
     * Returns the artifact type associated with file extension in name. If none exists then NL is returned.
     *
     * @param artifactName The name of the artifact potentially including file extension.
     * @return The artifact type of artifact name.
     */
    public static TGenSummaryArtifactType getArtifactType(String artifactName) {
        List<TGenSummaryArtifactType> artifactTypes = List.of(PY, JAVA);
        for (TGenSummaryArtifactType artifactType : artifactTypes) {
            if (artifactName.endsWith(artifactType.fileExtension)) {
                return artifactType;
            }
        }
        return NL;
    }
}
