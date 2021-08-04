package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.database.repositories.TraceLinkRepository;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.TraceLink;
import edu.nd.crc.safa.output.error.ServerError;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for providing an access to a project's
 * trace links.
 */
@Service
public class TraceLinkService {

    private TraceLinkRepository traceLinkRepository;

    @Autowired
    public TraceLinkService(TraceLinkRepository traceLinkRepository) {
        this.traceLinkRepository = traceLinkRepository;
    }

    public String getLinkTypes(Project project) throws ServerError {
        List<TraceLink> traceLinks = this.traceLinkRepository.findByProject(project);
        Map<String, ArrayList<String>> sourceTargetMap = new HashMap<String, ArrayList<String>>();
        for (TraceLink traceLink : traceLinks) {
            String key = traceLink.getTraceType().toString();
            String val = traceLink.getTraceLinkId().toString();
            sourceTargetMap.computeIfAbsent(key, k -> new ArrayList<>()).add(val);
        }

        String dataDict = sourceTargetMap.toString().replace("=", ":");
        return dataDict;
    }
}
