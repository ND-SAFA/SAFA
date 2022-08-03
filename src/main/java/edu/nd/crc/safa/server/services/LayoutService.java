package edu.nd.crc.safa.server.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.layout.KlayLayoutGenerator;
import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.app.documents.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import org.springframework.stereotype.Service;

@Service
public class LayoutService {

    /**
     * Generates layout for given artifact tree.
     *
     * @param artifacts The artifact in the tree.
     * @param traces    The traces between artifacts.
     * @return Map of artifact Ids to their position.
     */
    public Map<String, LayoutPosition> generateLayoutForArtifactTree(
        List<ArtifactAppEntity> artifacts,
        List<TraceAppEntity> traces
    ) {
        KlayLayoutGenerator layoutGenerator = new KlayLayoutGenerator(artifacts, traces);
        return layoutGenerator.layout();
    }

    /**
     * Generates the layout for each document's artifact tree.
     *
     * @param projectArtifacts The artifacts in the project.
     * @param projectTraces    The traces in the project.
     * @param documents        The documents in the project.
     * @return Map of documentId to the layout associated with the document.
     */
    public Map<String, Map<String, LayoutPosition>> generateDocumentLayouts(
        List<ArtifactAppEntity> projectArtifacts,
        List<TraceAppEntity> projectTraces,
        List<DocumentAppEntity> documents
    ) {
        Map<String, Map<String, LayoutPosition>> documentLayouts = new HashMap<>();
        for (DocumentAppEntity documentAppEntity : documents) {
            String documentId = documentAppEntity.getDocumentId().toString();
            Map<String, LayoutPosition> documentLayout = generateDocumentLayout(
                projectArtifacts,
                projectTraces,
                documentAppEntity);
            documentLayouts.put(documentId, documentLayout);
        }
        return documentLayouts;
    }

    /**
     * Generates the layout for the document's artifact tree.
     *
     * @param projectArtifacts  The artifacts in the project.
     * @param projectTraces     The traces in the project.
     * @param documentAppEntity The documents containing the artifacts to filter.
     * @return Map of documentId to the layout associated with the document.
     */
    public Map<String, LayoutPosition> generateDocumentLayout(List<ArtifactAppEntity> projectArtifacts,
                                                              List<TraceAppEntity> projectTraces,
                                                              DocumentAppEntity documentAppEntity) {
        // Step - Filter projectArtifacts in document
        List<String> documentArtifactIds = documentAppEntity.getArtifactIds();
        List<ArtifactAppEntity> documentArtifacts =
            projectArtifacts
                .stream()
                .filter(a -> documentArtifactIds.contains(a.id))
                .collect(Collectors.toList());

        // Step - Filter projectTraces in document
        List<TraceAppEntity> documentTraces =
            projectTraces
                .stream()
                .filter(t -> documentArtifactIds.contains(t.getSourceId())
                    && documentArtifactIds.contains(t.getTargetId()))
                .collect(Collectors.toList());

        // Step - Generate layout
        return generateLayoutForArtifactTree(documentArtifacts,
            documentTraces);
    }
}
