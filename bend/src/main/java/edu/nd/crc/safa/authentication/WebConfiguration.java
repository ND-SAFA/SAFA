package edu.nd.crc.safa.authentication;

import java.util.List;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.mvc.method.annotation.PrincipalMethodArgumentResolver;

/**
 * Additional configuration to support for Spring Boot 2.4+
 */
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    /**
     * Add resolvers to support custom controller method argument types.
     * Without this the principal session cannot be extracted inside method
     * controllers, and we cannot use{@link AuthenticationPrincipal} for
     * controller method parameters.
     *
     * @param resolvers initially an empty list
     */
    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
        resolvers.add(new PrincipalMethodArgumentResolver());
    }

}
