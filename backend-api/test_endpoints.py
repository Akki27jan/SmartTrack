"""
Smoke test for all SmartTrack API endpoints.
Run:  python test_endpoints.py
Make sure the server is running on http://localhost:8000
"""

import json
import urllib.request
import urllib.error
import sys

BASE = "http://localhost:8000"
passed = 0
failed = 0


def test(method, path, body=None, expect_status=200, label=""):
    global passed, failed
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    if body:
        req.add_header("Content-Type", "application/json")

    try:
        resp = urllib.request.urlopen(req)
        status = resp.status
        result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        status = e.code
        result = json.loads(e.read().decode())

    ok = status == expect_status
    icon = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1

    suffix = f" ({label})" if label else ""
    print(f"  [{icon}] {method:6} {path}{suffix}")
    if not ok:
        print(f"         Expected {expect_status}, got {status}")
    else:
        # Show key info from response
        for key in ["Company_ID", "Employee_ID", "HR_ID", "Audit_Log_ID", "notification_id", "message"]:
            if key in result:
                print(f"         {key}: {result[key]}")
    return result


print("=" * 60)
print("  SMARTTRACK API - ENDPOINT SMOKE TEST")
print("=" * 60)

# ── 1. Root ──
print("\n[ Root ]")
test("GET", "/")

# ── 2. Company Signup ──
print("\n[ Company Signup ]")
r = test("POST", "/company/signup", {
    "Name": "Infosys Technologies",
    "Gstin": "29AABCI1234F1Z5",
    "Address": "44 Electronics City, Bangalore 560100",
    "Password": "Infosys@2026",
    "Domain": "IT Services"
})
company_id = r.get("Company_ID", "UNKNOWN")

test("POST", "/company/signup", {
    "Name": "Infosys Technologies",
    "Gstin": "29AABCI1234F1Z5",
    "Address": "44 Electronics City, Bangalore 560100",
    "Password": "Infosys@2026",
    "Domain": "IT Services"
}, expect_status=400, label="duplicate GSTIN")

# ── 3. Employee Signup ──
print("\n[ Employee Signup ]")
r = test("POST", "/employee/signup", {
    "Name": "Akshat Dubey",
    "Email": "akshat.dubey@example.com",
    "Password": "Akshat@123"
})
employee_id = r.get("Employee_ID", "UNKNOWN")

test("POST", "/employee/signup", {
    "Name": "Akshat Dubey",
    "Email": "akshat.dubey@example.com",
    "Password": "Akshat@123"
}, expect_status=400, label="duplicate email")

# ── 4. HR Signup ──
print("\n[ HR Signup ]")
r = test("POST", "/hr/signup", {
    "Company_ID": company_id,
    "Name": "Rajesh Kumar",
    "Company_Email": "rajesh.kumar@infosys.com",
    "Password": "HrSecure@789"
})
hr_id = r.get("HR_ID", "UNKNOWN")

test("POST", "/hr/signup", {
    "Company_ID": "NONEXISTENT",
    "Name": "Ghost HR",
    "Company_Email": "ghost@nowhere.com",
    "Password": "Pass@123"
}, expect_status=400, label="bad Company_ID")

test("POST", "/hr/signup", {
    "Company_ID": company_id,
    "Name": "Rajesh Kumar",
    "Company_Email": "rajesh.kumar@infosys.com",
    "Password": "HrSecure@789"
}, expect_status=400, label="duplicate email")

# ── 5. Company Login ──
print("\n[ Company Login ]")
test("POST", "/company/login", {
    "Gstin": "29AABCI1234F1Z5",
    "Password": "Infosys@2026"
})

test("POST", "/company/login", {
    "Gstin": "29AABCI1234F1Z5",
    "Password": "WrongPassword"
}, expect_status=401, label="wrong password")

# ── 6. Employee Login ──
print("\n[ Employee Login ]")
test("POST", "/employee/login", {
    "Email": "akshat.dubey@example.com",
    "Password": "Akshat@123"
})

test("POST", "/employee/login", {
    "Email": "akshat.dubey@example.com",
    "Password": "WrongPassword"
}, expect_status=401, label="wrong password")

# ── 7. HR Login ──
print("\n[ HR Login ]")
test("POST", "/hr/login", {
    "Company_Email": "rajesh.kumar@infosys.com",
    "Password": "HrSecure@789"
})

test("POST", "/hr/login", {
    "Company_Email": "rajesh.kumar@infosys.com",
    "Password": "WrongPassword"
}, expect_status=401, label="wrong password")

# ── 8. Send Employee Notification ──
print("\n[ Notifications ]")
test("POST", "/employee/notification", {
    "Employee_ID": employee_id,
    "Type": "info",
    "Subject": "Welcome Aboard",
    "Message": "Your onboarding is scheduled for Monday 10 AM."
})

test("POST", "/employee/notification", {
    "Employee_ID": "NONEXISTENT",
    "Type": "info",
    "Subject": "Test",
    "Message": "Test"
}, expect_status=404, label="bad Employee_ID")

# ── 9. Send Company Notification ──
test("POST", "/company/notification", {
    "Company_ID": company_id,
    "Type": "alert",
    "Subject": "System Maintenance",
    "Message": "Scheduled downtime Saturday 2-4 AM IST."
})

test("POST", "/company/notification", {
    "Company_ID": "NONEXISTENT",
    "Type": "alert",
    "Subject": "Test",
    "Message": "Test"
}, expect_status=404, label="bad Company_ID")

# ── 10. Get Notifications ──
print("\n[ Get Notifications ]")
test("GET", f"/employee/{employee_id}/notifications")
test("GET", f"/company/{company_id}/notifications")

# ── 11. Create Audit Log ──
print("\n[ Audit Logs ]")
test("POST", "/audit-log", {
    "HR_ID": hr_id,
    "Action_Type": "ONBOARD",
    "Employee_ID": employee_id
})

test("POST", "/audit-log", {
    "HR_ID": "NONEXISTENT",
    "Action_Type": "ONBOARD",
    "Employee_ID": employee_id
}, expect_status=404, label="bad HR_ID")

test("POST", "/audit-log", {
    "HR_ID": hr_id,
    "Action_Type": "TERMINATE",
    "Employee_ID": "NONEXISTENT"
}, expect_status=404, label="bad Employee_ID")

# ── 12. Get Audit Logs ──
print("\n[ Get Audit Logs ]")
test("GET", f"/audit-logs/hr/{hr_id}")
test("GET", f"/audit-logs/employee/{employee_id}")

# ── Summary ──
print("\n" + "=" * 60)
total = passed + failed
if failed == 0:
    print(f"  ALL {total} TESTS PASSED!")
else:
    print(f"  RESULTS: {passed}/{total} passed, {failed}/{total} failed")
print("=" * 60)

if failed > 0:
    sys.exit(1)
