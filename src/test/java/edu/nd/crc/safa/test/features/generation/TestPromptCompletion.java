package edu.nd.crc.safa.test.features.generation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.nd.crc.safa.features.generation.prompt.PromptResponse;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptRequest;
import edu.nd.crc.safa.test.services.requests.GenCommonRequests;

import org.junit.jupiter.api.Test;

class TestPromptCompletion extends GenerationalTest {

    /**
     * Tests that success of prompt completion request.
     */
    @Test
    void testCompletionSuccess() throws Exception {
        String prompt = "hello";
        TGenPromptRequest request = new TGenPromptRequest();
        request.setPrompt(prompt);

        PromptResponse mockResponse = new PromptResponse();
        mockResponse.setCompletion("hi");
        getServer().setResponse(mockResponse);

        PromptResponse response = GenCommonRequests.completePrompt(request);

        assertEquals("hi", response.getCompletion());
    }
}
