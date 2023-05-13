package edu.nd.crc.safa.features.tgen.api;

import edu.nd.crc.safa.features.common.SafaRequestBuilder;

import com.fasterxml.jackson.databind.JavaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * Allows for requests to tgen with automatic parsing of reponses.
 */
@Service
public class TGenRequestBuilder extends SafaRequestBuilder {
    public TGenRequestBuilder(WebClient webClient) {
        super(webClient);
    }


    /**
     * Overrides sendRequest to expect a SafaResponse with parametized type defined in request meta.
     *
     * @param requestMeta Details request to make and with what parameters.
     * @param <T>         The object expected in body of response.
     * @return The parsed object from response. Error is thrown if something occurs.
     */
    @Override
    public <T> T sendRequest(SafaRequestBuilder.RequestMeta<T> requestMeta) {
        Class<T> requestType = (Class<T>) requestMeta.getResponseClass();
        JavaType responseType = objectMapper.getTypeFactory().constructParametricType(SafaResponse.class, requestType);

        SafaResponse<T> responseJson = super.sendRequest(new RequestMeta<>(
            requestMeta.getEndpoint(),
            requestMeta.getHttpMethod(),
            requestMeta.getHeaders(),
            requestMeta.getPayload(),
            responseType,
            requestMeta.getTimeout()
        ));
        return responseJson.getBody();
    }
}
