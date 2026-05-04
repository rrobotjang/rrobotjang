def test_serverless_handlers_importable():
    from app.lambda_handlers import flight_handler, payment_handler, monitoring_handler
    assert flight_handler is not None
    assert payment_handler is not None
    assert monitoring_handler is not None
