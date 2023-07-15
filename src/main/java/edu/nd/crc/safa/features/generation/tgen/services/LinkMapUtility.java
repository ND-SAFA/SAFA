package edu.nd.crc.safa.features.generation.tgen.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.function.Function;

import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

public class LinkMapUtility {

    /**
     * Groups links by child name.
     *
     * @param links The links to group.
     * @return Hashmap of child name to child links.
     */
    public static HashMap<String, List<TraceAppEntity>> createChildLinkMap(List<TraceAppEntity> links) {
        return createLinkMap(links, TraceAppEntity::getSourceName);
    }

    /**
     * Groups links by parent name.
     *
     * @param links The links to group.
     * @return Hashmap of parent name to parent links.
     */
    public static HashMap<String, List<TraceAppEntity>> createParentMap(List<TraceAppEntity> links) {
        return createLinkMap(links, TraceAppEntity::getTargetName);
    }

    public static HashMap<String, List<TraceAppEntity>> createLinkMap(List<TraceAppEntity> links,
                                                                      Function<TraceAppEntity, String> grouper) {
        HashMap<String, List<TraceAppEntity>> child2links = new HashMap<>();
        links.forEach(t -> {
            String groupName = grouper.apply(t);
            if (!child2links.containsKey(groupName)) {
                child2links.put(groupName, new ArrayList<>());
            }

            child2links.get(groupName).add(t);
        });
        return child2links;
    }
}
