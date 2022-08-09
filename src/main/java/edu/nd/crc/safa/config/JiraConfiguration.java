package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.jira.repositories.JiraProjectRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jira.services.JiraConnectionServiceImpl;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.codec.json.Jackson2JsonDecoder;
import org.springframework.http.codec.json.Jackson2JsonEncoder;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

/**
 * Responsible for configuring the jira connection service
 * implementation for the application.
 */
@Configuration
@AllArgsConstructor
public class JiraConfiguration {

    private static final String CONTENT_TYPE_HEADER_VALUE = "application/json";
    private static final Integer WEBCLIENT_MAX_MEMORY = 16 * 1024 * 1024;

    JiraProjectRepository jiraProjectRepository;

    @Bean
    public JiraConnectionService jiraConnectionService() {
        return new JiraConnectionServiceImpl(jiraProjectRepository);
    }

    @Bean
    public WebClient webClient() {
        ObjectMapper mapper = new ObjectMapper();

        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

        return WebClient.builder()
            .codecs(configure -> {
                configure.defaultCodecs().maxInMemorySize(WEBCLIENT_MAX_MEMORY);
                configure.defaultCodecs().enableLoggingRequestDetails(true);
                configure.defaultCodecs().jackson2JsonEncoder(
                    new Jackson2JsonEncoder(mapper, MediaType.APPLICATION_JSON));
                configure.defaultCodecs().jackson2JsonDecoder(
                    new Jackson2JsonDecoder(mapper, MediaType.APPLICATION_JSON));
            })
            .clientConnector(new ReactorClientHttpConnector(HttpClient.create().wiretap(true)))
            .defaultHeader(HttpHeaders.CONTENT_TYPE, CONTENT_TYPE_HEADER_VALUE)
            .defaultHeader(HttpHeaders.ACCEPT, "*/*")
            .build();
    }

}
