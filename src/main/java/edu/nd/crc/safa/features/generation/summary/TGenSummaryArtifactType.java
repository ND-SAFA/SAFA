package edu.nd.crc.safa.features.generation.summary;

import java.nio.file.Path;
import java.util.List;
import java.util.Set;

import edu.nd.crc.safa.utilities.FileUtilities;

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
    JAVA(".java"),
    /**
     * Generic parser for code.
     */
    CODE(".*");

    private final String fileExtension;

    private static final List<TGenSummaryArtifactType> KNOWN_TYPES = List.of(JAVA, PY);
    private static final Set<TGenSummaryArtifactType> CODE_TYPES = Set.of(CODE, JAVA, PY);

    /**
     * Returns the artifact type associated with file extension in name. If none exists then NL is returned.
     *
     * @param artifactName The name of the artifact potentially including file extension.
     * @return The artifact type of artifact name.
     */
    public static TGenSummaryArtifactType getArtifactType(String artifactName) {
        if (artifactName == null) {
            return NL;
        }
        for (TGenSummaryArtifactType artifactType : KNOWN_TYPES) {
            if (artifactName.endsWith(artifactType.fileExtension)) {
                return artifactType;
            }
        }
        if (FileUtilities.isCodeFile(Path.of(artifactName))) {
            return CODE;
        }
        return NL;
    }

    /**
     * Returns whether artifact type is a code.
     *
     * @param artifactName The name of the artifact to extract type from.
     * @return True if code, false otherwise.
     */
    public static boolean isCode(String artifactName) {
        TGenSummaryArtifactType artifactType = TGenSummaryArtifactType.getArtifactType(artifactName);
        return CODE_TYPES.contains(artifactType);
    }
}
