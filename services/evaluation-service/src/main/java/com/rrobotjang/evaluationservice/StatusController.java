package com.rrobotjang.evaluationservice;

import java.time.Instant;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class StatusController {

    @Value("${spring.application.name}")
    private String appName;

    @GetMapping("/status")
    public Map<String, Object> status() {
        return Map.of(
            "service", appName,
            "status", "UP",
            "timestamp", Instant.now().toString()
        );
    }
}
