package edu.nd.crc.safa.test.features.generation;

import static org.springframework.test.web.client.ExpectedCount.manyTimes;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;

import java.net.URI;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.CeleryStatus;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryResponse;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptResponse;
import edu.nd.crc.safa.features.generation.tgen.TGenTraceGenerationResponse;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Getter;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;

@ExtendWith(MockitoExtension.class)
class AbstractGenerationTest extends ApplicationBaseTest {
    private final ObjectMapper mapper = ObjectMapperConfig.create();
    @Getter
    @Autowired
    private GenApi api;

    public void setHGenResponse(HGenResponse response) {
        String endpoint = TGenConfig.getEndpoint("hgen");
        setJobResponse(endpoint, response);
    }

    public void setProjectSummaryResponse(ProjectSummaryResponse response) {
        String endpoint = TGenConfig.getEndpoint("project-summary");
        setJobResponse(endpoint, response);
    }

    public void setPromptResponse(TGenPromptResponse response) {
        String endpoint = TGenConfig.getEndpoint("complete");
        setResponse(endpoint, HttpMethod.POST, response);
    }

    public void setTraceResponse(TGenTraceGenerationResponse response) {
        String endpoint = TGenConfig.getEndpoint("predict");
        setJobResponse(endpoint, response);
    }


    public void setSearchResponse(TGenTraceGenerationResponse response) {
        String endpoint = TGenConfig.getEndpoint("predict-sync");
        setResponse(endpoint, HttpMethod.POST, response);
    }

    public void setCancelJob() {
        TGenStatus status = new TGenStatus();
        setResponse(TGenConfig.getEndpoint("cancel"), HttpMethod.POST, status);
    }

    public void setResponse(String endpoint, HttpMethod method, Object responseObject) {
        try {
            String responseString = mapper.writeValueAsString(responseObject);
            mockServer.expect(manyTimes(), requestTo(new URI(endpoint)))
                .andExpect(method(method))
                .andRespond(withStatus(HttpStatus.OK)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(responseString)
                );
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    private void setJobResponse(String endpoint, Object result) {
        String statusEndpoint = TGenConfig.getEndpoint("status");
        String resultEndpoint = TGenConfig.getEndpoint("results");

        TGenStatus status = new TGenStatus();
        TGenTask task = new TGenTask();
        status.setStatus(CeleryStatus.SUCCESS);

        setResponse(endpoint, HttpMethod.POST, task);
        setResponse(statusEndpoint, HttpMethod.POST, status);
        setResponse(resultEndpoint, HttpMethod.POST, result);
    }
}
