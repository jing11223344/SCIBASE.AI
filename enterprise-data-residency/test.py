#!/usr/bin/env python3
"""Tests for Enterprise Data Residency Compliance Module."""

import sys
sys.path.insert(0, '.')

from src.index import DataResidencyCompliance, REGION_RULES, CROSS_BORDER_RULES

passed = 0
failed = 0


def check(condition: bool, msg: str):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {msg}")
    else:
        failed += 1
        print(f"  FAIL: {msg}")


print("=== Enterprise Data Residency Compliance Tests ===\n")

# Test 1: Constructor
compliance = DataResidencyCompliance()
check(isinstance(compliance, DataResidencyCompliance), "Constructor creates instance")

# Test 2: Data classification
classification = compliance.classify_data('project-alpha', 'eu-west', 'restricted')
check(classification['resource'] == 'project-alpha', "Classifies data with correct resource name")
check('GDPR' in classification['compliance_frameworks'], "Applies GDPR framework for EU region")
check(classification['encryption_required'] is True, "Requires encryption for EU region")

# Test 3: Cross-border transfer blocking
blocked = compliance.check_transfer('eu-west', 'cn-east')
check(blocked['allowed'] is False, "Blocks EU->CN transfer (GDPR)")
check('GDPR' in blocked['reason'], "Provides GDPR reason for block")

# Test 4: Transfer allowed
allowed = compliance.check_transfer('eu-west', 'us-east')
check(allowed['allowed'] is True, "Allows EU->US transfer")

# Test 5: Encryption requirement
no_enc = compliance.check_transfer('eu-west', 'us-east', encrypted=False)
check(no_enc['allowed'] is False, "Blocks unencrypted EU transfer")

# Test 6: Audit report
report = compliance.generate_audit_report()
check(report['total_events'] >= 4, f"Audit report has {report['total_events']} events")
check(report['blocked_transfers'] >= 2, f"Reports {report['blocked_transfers']} blocked transfers")

# Test 7: REGION_RULES structure
check(len(REGION_RULES) > 0, "REGION_RULES has defined regions")
check(REGION_RULES['eu-west']['encryption_required'] is True, "EU regions require encryption")

# Test 8: CROSS_BORDER_RULES structure
check(len(CROSS_BORDER_RULES) > 0, "Has cross-border rules")
check(any(not r['allowed'] for r in CROSS_BORDER_RULES), "Some transfers are blocked by default")

print(f"\n=== Results: {passed} passed, {failed} failed ===")
sys.exit(1 if failed > 0 else 0)
