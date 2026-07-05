#!/usr/bin/env node
/**
 * Enterprise Data Residency Compliance Module Demo
 * 
 * Demonstrates automated data classification, cross-border transfer controls,
 * and regulatory audit trail generation for EU/GDPR, China/PIPL, and US/CMMC.
 */

const { DataResidencyCompliance } = require('./src/index');

console.log('=== Enterprise Data Residency Compliance Demo ===\n');

const compliance = new DataResidencyCompliance();

// Classify data in different regions
console.log('--- Data Classification ---');
const euData = compliance.classifyData('research-project-x', 'eu-west', 'restricted');
console.log(JSON.stringify(euData, null, 2));

const usData = compliance.classifyData('marketing-data', 'us-east', 'public');
console.log('\n' + JSON.stringify(usData, null, 2));

// Check transfer rules
console.log('\n--- Transfer Checks ---');
console.log('EU->CN:', JSON.stringify(compliance.checkTransfer('eu-west', 'cn-east')));
console.log('EU->US:', JSON.stringify(compliance.checkTransfer('eu-west', 'us-east')));
console.log('CN->US:', JSON.stringify(compliance.checkTransfer('cn-east', 'us-east')));

// Generate audit report
console.log('\n--- Audit Report ---');
const report = compliance.generateAuditReport();
console.log('Total events:', report.totalEvents);
console.log('Blocked transfers:', report.blockedTransfers);
console.log('Classifications:', report.classifications);

console.log('\nDemo complete.');
