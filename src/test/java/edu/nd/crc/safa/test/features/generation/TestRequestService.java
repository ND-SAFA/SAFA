package edu.nd.crc.safa.test.features.generation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.common.RequestService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.ExpectedCount;
import org.springframework.test.web.client.MockRestServiceServer;

@ExtendWith(MockitoExtension.class)
public class TestRequestService extends ApplicationBaseTest {
    private final ObjectMapper mapper = ObjectMapperConfig.create();
    @Autowired
    RequestService requestService;
    
    @BeforeEach
    public void init() {
        mockServer = MockRestServiceServer.createServer(restTemplate);
    }

    @Test
    public void firstTest() throws URISyntaxException, JsonProcessingException {
        String endpoint = "https://tgen.safa.ai/models";
        List<String> models = List.of("anthropic", "openai");
        mockServer.expect(ExpectedCount.once(),
                requestTo(new URI(endpoint)))
            .andExpect(method(HttpMethod.GET))
            .andRespond(withStatus(HttpStatus.OK)
                .contentType(MediaType.APPLICATION_JSON)
                .body(mapper.writeValueAsString(models))
            );

        List<String> response = restTemplate.exchange(endpoint, HttpMethod.GET, null,
            new ParameterizedTypeReference<List<String>>() {
            }).getBody();

        assertEquals(response.get(0), "anthropic");
    }
}
