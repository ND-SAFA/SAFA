package edu.nd.crc.safa.server.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TreeService {

    WarningService warningService;

    @Autowired
    public TreeService(WarningService warningService) {
        this.warningService = warningService;
    }
}
