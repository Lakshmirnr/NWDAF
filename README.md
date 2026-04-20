# Cross-Slice Policy Abuse Detection Framework (Production-Ready Research Version)

This repository implements a real-time detection and mitigation framework for cross-slice policy abuse in 5G networks using Open5GS.

## Key Features
- Real-time log streaming (tail -F)
- Sliding window feature extraction
- EWMA-based risk scoring
- Intent-aware anomaly detection
- Practical mitigation using Linux tc

## Usage
1. Place logs in /logs
2. Configure baseline and thresholds
3. Run:
   bash scripts/run.sh
