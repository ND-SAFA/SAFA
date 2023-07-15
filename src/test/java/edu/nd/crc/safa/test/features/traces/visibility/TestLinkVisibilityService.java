package edu.nd.crc.safa.test.features.traces.visibility;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.tgen.services.LinkVisibilityService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;

public class TestLinkVisibilityService extends ApplicationBaseTest {
    @Test
    public void testLinkVisibility() {
        String childName = "S1";
        List<String> parentNames = List.of("UR-1", "R1", "R2", "R2");
        List<Double> scores = List.of(.66, 1.0, 1.0, 1.0);
        List<TraceAppEntity> traces = new ArrayList<>();
        for (int i = 0; i < parentNames.size(); i++) {
            String parentName = parentNames.get(i);
            Double score = scores.get(i);
            TraceAppEntity traceAppEntity = new TraceAppEntity(
                childName, parentName
            ).asGeneratedTrace(score);
            traces.add(traceAppEntity);
        }

        LinkVisibilityService.setLinksVisibility(traces);
        assertFalse(traces.get(0).isVisible());
        assertTrue(traces.get(1).isVisible());
        assertTrue(traces.get(2).isVisible());
        assertTrue(traces.get(3).isVisible());
    }
}
