import schemathesis
from pathlib import Path
from src.config import BASE_URL

spec_path = Path(__file__).parent / "openapi.yaml"
schema = schemathesis.openapi.from_path(str(spec_path))


@schema.parametrize()
def test_api_contract(case):
    response = case.call(base_url=BASE_URL)
    case.validate_response(response, checks=(
        schemathesis.checks.status_code_conformance,
        schemathesis.checks.content_type_conformance,
    ))