package com.rrobotjang.userprofileservice.profile;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/profile")
public class UserProfileController {
    private final UserProfileService service;

    public UserProfileController(UserProfileService service) {
        this.service = service;
    }

    @GetMapping("/{userId}")
    public UserProfile getProfile(@PathVariable String userId) {
        return service.getProfile(userId);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserProfile upsert(@RequestBody UpsertRequest request) {
        return service.upsert(new UserProfileService.UpsertProfileRequest(
            request.userId(), request.email(), request.displayName()));
    }

    @GetMapping("/me")
    public Map<String, String> me() {
        return Map.of("message", "Profile endpoint reachable via API Gateway");
    }

    public record UpsertRequest(String userId, String email, String displayName) {}
}
