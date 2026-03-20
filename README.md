# Power BI Report Quality Checker 🔍

## Overview
Python tool that automatically analyzes Power BI .pbix files 
for quality issues before deployment to QA/Production.

## Problem
Before every Dev → QA → Prod deployment, reports need manual 
quality checks. This tool automates that process.

## Quality Checks
1. ✅ File Size — flags reports over 100MB
2. ✅ Visuals Per Page — flags pages with 10+ visuals
3. ✅ Row Level Security — checks if RLS is configured
4. ✅ Hidden Pages — detects hidden pages
5. ✅ Relationships — detects many-to-many and bidirectional relationships

## How It Works
.pbix is a ZIP file internally. This tool extracts it and reads:
- Report/Layout — pages and visuals
- DataModel — relationships
- SecurityBindings — RLS configuration

## Tech Stack
Python, zipfile, json, os

## Usage
python checker.py
