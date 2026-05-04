from app.services.intent import parse_natural_language_intent


def test_parse_korean_nl_preferences():
    intent = parse_natural_language_intent(["싸고 덜 피곤한 비행", "야간 출발 싫어", "경유 싫어"])
    assert intent.prefers_low_price
    assert intent.prefers_less_fatigue
    assert intent.avoids_night
    assert intent.avoid_stops
