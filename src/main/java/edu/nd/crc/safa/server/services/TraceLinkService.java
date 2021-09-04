package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.TraceLinkRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Responsible for providing an access to a project's
 * trace links.
 */
@Service
public class TraceLinkService {

    private final TraceLinkRepository traceLinkRepository;
    private ArtifactRepository artifactRepository;

    @Autowired
    public TraceLinkService(TraceLinkRepository traceLinkRepository) {
        this.traceLinkRepository = traceLinkRepository;
    }

    public String getLinkTypes(Project project) {
        List<TraceLink> traceLinks = this.traceLinkRepository.findByProject(project);
        Map<String, ArrayList<String>> sourceTargetMap = new HashMap<String, ArrayList<String>>();
        for (TraceLink traceLink : traceLinks) {
            String key = traceLink.getTraceType().toString();
            String val = traceLink.getTraceLinkId().toString();
            sourceTargetMap.computeIfAbsent(key, k -> new ArrayList<>()).add(val);
        }

        return sourceTargetMap.toString().replace("=", ":");
    }

    @Transactional(readOnly = true)
    public List<TraceLink> getArtifactLinks(Project project,
                                            String sourceName,
                                            String targetName,
                                            Double minScore) {
        List<Function<TraceLink, Boolean>> filters = getLinkArtifactFilters(sourceName, targetName);
        filters.add(t -> minScore != null && !(t.getScore() >= minScore));
        return getLinks(project, filters);
    }

    public List<TraceLink> getLink(Project project, String sourceName, String targetName) {
        return getLinks(project, getLinkArtifactFilters(sourceName, targetName));
    }

    private List<Function<TraceLink, Boolean>> getLinkArtifactFilters(String sourceName,
                                                                      String targetName) {
        List<Function<TraceLink, Boolean>> filters = new ArrayList<>();

        filters.add(t -> sourceName != null && !t.getSourceName().equals(sourceName));
        filters.add(t -> targetName != null && !t.getTargetName().equals(targetName));

        return filters;
    }

    public List<TraceLink> getLinks(Project project,
                                    List<Function<TraceLink, Boolean>> linkFilters) {
        List<TraceLink> projectLinks = traceLinkRepository.findByProject(project);
        List<TraceLink> queriedLinks = new ArrayList<>();
        for (TraceLink traceLink : projectLinks) {
            boolean filtersApproved = true;
            for (Function<TraceLink, Boolean> linkFilter : linkFilters) {
                filtersApproved = filtersApproved && linkFilter.apply(traceLink);
            }
            if (filtersApproved) {
                queriedLinks.add(traceLink);
            }
        }
        return queriedLinks;
    }
}
