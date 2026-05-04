from dataclasses import dataclass


@dataclass
class IntentFeatures:
    prefers_low_price: bool = False
    avoids_night: bool = False
    prefers_less_fatigue: bool = False
    avoid_stops: bool = False


def parse_natural_language_intent(preferences: list[str]) -> IntentFeatures:
    text = " ".join(preferences).lower()
    return IntentFeatures(
        prefers_low_price=("싸" in text) or ("cheap" in text),
        avoids_night=("야간" in text and "싫" in text) or ("no night" in text),
        prefers_less_fatigue=("덜 피곤" in text) or ("less fatigue" in text),
        avoid_stops=("직항" in text) or ("경유 싫" in text) or ("no stop" in text),
    )
