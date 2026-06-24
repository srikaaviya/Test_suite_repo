import schemathesis
from pathlib import Path

spec_path = Path(__file__).parent / "openapi.yaml"
schema = schemathesis.openapi.from_path(str(spec_path))


@schema.parametrize()
def test_api_contract(case):
    response = case.call()
    case.validate_response(response)