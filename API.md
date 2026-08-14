# CareerPulse API Documentation 

## Overview

CareerPulse provides API endpoints used by the frontend to update application statuses and retrieve dashboard metrics.
All application-related API endpoints require the user to be authenticated. 

---

# 1. Update Application Status

## Endpoint

`PATCH /api/applications/<id>/status`

## Purpose

Updates the status of a specific job application. 
The application must belong to the currently authenticated user.

## Authentication 

Required.
The user must be logged in.

## Request Headers

```http
Content-Type: application/json
