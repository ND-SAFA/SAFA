package edu.nd.crc.safa.admin.usagestats.controllers;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class UsageStatisticsController extends BaseController {
    public UsageStatisticsController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }
}
