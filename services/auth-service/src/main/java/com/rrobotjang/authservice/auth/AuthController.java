package com.rrobotjang.authservice.auth;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.rrobotjang.authservice.security.JwtService;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final JwtService jwtService;

    public AuthController(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    @PostMapping("/login")
    public Map<String, String> login(@RequestBody LoginRequest request) {
        String token = jwtService.generateToken(request.username());
        return Map.of("token", token, "tokenType", "Bearer");
    }

    @GetMapping("/validate")
    public Map<String, String> validate() {
        return Map.of("message", "Token is valid");
    }

    public record LoginRequest(String username) {}
}
