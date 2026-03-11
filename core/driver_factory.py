import requestsimport base64import jsonfrom typing import Any, Type, Literal, List, Optionalfrom pydantic import BaseModel, Fieldfrom crewai.tools import BaseTool # Import your secret manager moduleimport AVASecret class TestStepSchema(BaseModel):
    Step_ID: int = Field(..., description="Step identifier")
    Step_Desc: str = Field(..., description="Description of the test step")
    Expected_Result: str = Field(..., description="Expected outcome")
    Test_Data: Any = Field(None, description="Optional test data used") class ConnectorInput(BaseModel):
    testrail_operation: Literal["fetch_cases", "add_case", "update_case", "create_section", "get_case"]
    testrail_base_url: str    testrail_username: str    testrail_api_key: str = Field(..., description="The name of the secret key in AVASecret, e.g., 'HPX_TestRail'")
    # Made Optional so get_case can run without them    testrail_project_id: Optional[int] = None    testrail_suite_id: Optional[int] = None    testrail_section_id: Optional[int] = None# Accept strings to allow "C12345" formats    case_id: Optional[str] = Field(None, description="The internal TestRail ID of a single test case (e.g., C12345 or 12345).")
    case_ids: Optional[List[str]] = Field(None, description="A list of internal TestRail IDs (e.g., ['C12345', 'C12346']).")
    # Optional parameters for add_case / update_case    testCaseId: Optional[str] = None    testCaseDescription: Optional[str] = None    AcceptanceCriteriaId: Optional[str] = None    IssueId: Optional[str] = None    testSteps: List[TestStepSchema] = Field(default_factory=list)  class QeTestRailTool(BaseTool):
    name: str = "TestRail Connector Tool"    description: str = "Universal TestRail API Tool for fetch_cases, get_case, add_case, update_case, and create_section."    args_schema: Type[BaseModel] = ConnectorInput     def _run(self, **kwargs) -> Any:
        operation = kwargs.get("testrail_operation")
        username = kwargs.get("testrail_username")
        base_url = kwargs.get("testrail_base_url")
        # ---------------------------------------------------------# SECURE CREDENTIAL RESOLUTION# ---------------------------------------------------------# The agent passes the name of the secret (e.g., "HPX_TestRail")        secret_name = kwargs.get("testrail_api_key")
        try:
            # Resolve the actual API key behind the scenes            actual_api_key = AVASecret.getValue(secret_name)
        except Exception as e:
            return {"error": f"Failed to resolve API key from AVASecret using identifier '{secret_name}'. Error: {str(e)}"}         # Build headers using the resolved, real actual_api_key        headers = self._build_headers(username, actual_api_key)         # Normalize test case IDif not kwargs.get("test_case_id") and kwargs.get("testCaseId"):
            kwargs["test_case_id"] = kwargs["testCaseId"]         # Route the operationsif operation == "fetch_cases":
            return self._fetch_cases(kwargs, headers, base_url)
        elif operation == "get_case":
            return self._get_case(kwargs, headers, base_url)
        elif operation == "add_case":
            return self._add_case(kwargs, headers, base_url)
        elif operation == "update_case":
            return self._update_case(kwargs, headers, base_url)
        elif operation == "create_section":
            return self._create_section(kwargs, headers, base_url)
        else:
            return {"error": f"Unsupported operation: {operation}"}     def _build_headers(self, username: str, api_key: str) -> dict:
        token = base64.b64encode(f"{username}:{api_key}".encode()).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {token}"        }     # ==========================================# Get single or multiple test cases by ID# ==========================================def _get_case(self, kwargs: dict, headers: dict, base_url: str) -> Any:
        case_id = kwargs.get("case_id")
        case_ids = kwargs.get("case_ids")
        # Consolidate into a single list of strings        raw_ids = []
        if case_ids and isinstance(case_ids, list):
            raw_ids.extend([str(c) for c in case_ids])
        if case_id and str(case_id) not in raw_ids:
            raw_ids.append(str(case_id))
        if not raw_ids:
            return {"error": "Missing required field: Provide 'case_id' or 'case_ids' to fetch test case details."}         fetched_cases = []
        errors = []         # Iterate through IDs, strip the 'C' prefix, and fetch detailsfor raw_cid in raw_ids:
            clean_cid = raw_cid.strip().lstrip("cC")
            if not clean_cid:
                continue             url = f"{base_url}/index.php?/api/v2/get_case/{clean_cid}"try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                fetched_cases.append(response.json())
            except requests.exceptions.HTTPError as http_err:
                errors.append({"case_id": raw_cid, "error": f"HTTP error occurred: {http_err}", "details": response.text if 'response' in locals() else 'No response'})
            except Exception as e:
                errors.append({"case_id": raw_cid, "error": str(e)})         # Determine overall status        status = "success"if errors:
            status = "partial_success" if fetched_cases else "error"         return {
            "status": status,
            "fetched_cases": fetched_cases,
            "errors": errors if errors else None        }     # ==========================================# Fetch all cases in a section# ==========================================def _fetch_cases(self, kwargs: dict, headers: dict, base_url: str) -> Any:
        project_id = kwargs.get("testrail_project_id")
        suite_id = kwargs.get("testrail_suite_id")
        section_id = kwargs.get("testrail_section_id")         if not project_id or not suite_id or not section_id:
            return {"error": "testrail_project_id, testrail_suite_id, and testrail_section_id are required for fetch_cases."}         url = f"{base_url}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}"try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            cases = response.json()
            test_cases = []
            for case in cases:
                step_lines = (case.get("custom_steps") or "").strip().split("\n")
                expected_lines = (case.get("custom_expected") or "").strip().split("\n")
                steps = []
                for idx, step in enumerate(step_lines):
                    if not step.strip(): continue                    steps.append({
                        "Step_ID": idx + 1,
                        "Step_Desc": step.strip(),
                        "Expected_Result": expected_lines[idx].strip() if idx < len(expected_lines) else ""                    })
                test_cases.append({
                    "TC_ID": case.get("id"),
                    "TC_Name": case.get("title"),
                    "Steps": steps,
                    "Acceptance_Criteria_ID": case.get("custom_acceptance_criteria", "")
                })
            return {"test_cases": test_cases}         except requests.RequestException as e:
            return {"error": f"Failed to fetch test cases: {str(e)}"}     # ==========================================# Add a new test case# ==========================================def _add_case(self, kwargs: dict, headers: dict, base_url: str) -> Any:
        try:
            testCaseId = kwargs.get("testCaseId")
            testCaseDescription = kwargs.get("testCaseDescription")
            AcceptanceCriteriaId = kwargs.get("AcceptanceCriteriaId")
            IssueId = kwargs.get("IssueId")
            testSteps = kwargs.get("testSteps", [])
            section_id = kwargs.get("testrail_section_id")             if not testCaseId or not testSteps or not section_id:
                return {"error": "Missing required fields: testCaseId, testSteps, or testrail_section_id"}             use_separated_steps = True            custom_steps_separated = []
            custom_steps = ""            custom_expected = ""for step in testSteps:
                is_dict = isinstance(step, dict)
                step_id = step.get("Step_ID") if is_dict else step.Step_ID
                desc = step.get("Step_Desc", "").strip() if is_dict else step.Step_Desc.strip()
                expected = step.get("Expected_Result", "").strip() if is_dict else step.Expected_Result.strip()
                test_data = step.get("Test_Data") if is_dict else step.Test_Data                 if use_separated_steps:
                    custom_steps_separated.append({
                        "content": f"{desc}{' [Test Data: ' + str(test_data) + ']' if test_data else ''} [Acceptance Criteria: {AcceptanceCriteriaId}]",
                        "expected": expected
                    })
                else:
                    step_line = f"{step_id}. {desc}"if test_data:
                        step_line += f" [Test Data: {test_data}]"                    step_line += f" [Acceptance Criteria: {AcceptanceCriteriaId}]\n"                    custom_steps += step_line
                    expected_line = f"{step_id}. {expected}\n"                    custom_expected += expected_line
            payload = {
                "title": f"Test Case {testCaseId}",
                "template_id": 1,
                "type_id": 6,
                "priority_id": 2,
                "estimate": "5m",
                "refs": IssueId,
                "custom_preconds": testCaseDescription or "",
            }
            if use_separated_steps:
                payload["custom_steps_separated"] = custom_steps_separated
            else:
                payload["custom_steps"] = custom_steps
                payload["custom_expected"] = custom_expected             url = f"{base_url}/index.php?/api/v2/add_case/{section_id}"            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            test_case = response.json()
            return {
                "status": "success",
                "case": test_case,
                "outputUrl": f"{base_url.replace('/api/v2', '')}/index.php?/cases/view/{test_case.get('id', 'unknown')}"            }
        except requests.exceptions.HTTPError as http_err:
            return {"status": "error", "message": f"HTTP error occurred: {http_err}", "details": response.text if 'response' in locals() else 'No response'}
        except Exception as e:
            return {"status": "error", "message": str(e)}     # ==========================================# Update an existing test case# ==========================================def _update_case(self, kwargs: dict, headers: dict, base_url: str) -> Any:
        case_id = kwargs.get("case_id")
        test_case_id = kwargs.get("test_case_id")
        project_id = kwargs.get("testrail_project_id")
        # Clean the case_id if it was passed with a "C" prefixif case_id:
            case_id = str(case_id).strip().lstrip("cC")         if not case_id and test_case_id:
            if not project_id:
                return {"error": "testrail_project_id is required to resolve a custom test_case_id into a system case_id."}
            search_url = f"{base_url}/index.php?/api/v2/get_cases/{project_id}"try:
                resp = requests.get(search_url, headers=headers)
                resp.raise_for_status()
                for case in resp.json():
                    if case.get("custom_test_case_id", "").strip().upper() == test_case_id.strip().upper():
                        case_id = case["id"]
                        breakexcept Exception as e:
                return {"error": f"Failed to resolve test case ID. Reason: {str(e)}"}         if not case_id:
            return {"error": "Unable to resolve or find case_id to update."}         payload = {}         if kwargs.get("feasibility_score") is not None:
            payload["custom_case_custom_feasibility_score"] = kwargs["feasibility_score"]         if kwargs.get("automation_feasibility"):
            map_val = {"Yes": 1, "No": 2, "May Be": 3}
            feasibility = map_val.get(kwargs["automation_feasibility"].strip().title())
            if feasibility:
                payload["custom_case_automation_feasibility"] = feasibility         if kwargs.get("estimate"): payload["estimate"] = kwargs["estimate"]
        if kwargs.get("milestone_id"): payload["milestone_id"] = kwargs["milestone_id"]
        if kwargs.get("refs"): payload["refs"] = kwargs["refs"]
        if kwargs.get("preconds"): payload["custom_preconds"] = kwargs["preconds"]
        if kwargs.get("steps_text"): payload["custom_steps"] = kwargs["steps_text"]
        if kwargs.get("expected_result_text"): payload["custom_expected"] = kwargs["expected_result_text"]
        if kwargs.get("mission"): payload["custom_mission"] = kwargs["mission"]
        if kwargs.get("goals"): payload["custom_goals"] = kwargs["goals"]         if kwargs.get("steps") and kwargs.get("expected_result"):
            payload["custom_steps_separated"] = [
                {"content": s, "expected": e}
                for s, e in zip(kwargs["steps"], kwargs["expected_result"])
            ]         url = f"{base_url}/index.php?/api/v2/update_case/{case_id}"try:
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": f"Failed to update test case. Reason: {str(e)}"}     # ==========================================# Create a new section# ==========================================def _create_section(self, kwargs: dict, headers: dict, base_url: str) -> Any:
        project_id = kwargs.get("testrail_project_id")
        suite_id = kwargs.get("testrail_suite_id")
        section_name = kwargs.get("section_name")         if not project_id or not suite_id or not section_name:
            return {"error": "testrail_project_id, testrail_suite_id, and section_name are required for create_section."}         url = f"{base_url}/index.php?/api/v2/add_section/{project_id}"        payload = {
            "suite_id": suite_id,
            "name": section_name
        }         try:
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": f"Failed to create section. Reason: {str(e)}"} 
 
