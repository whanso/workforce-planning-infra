#!/usr/bin/env python3

import aws_cdk as cdk

from workforce_planning_infra.workforce_planning_infra_stack import (
    WorkforcePlanningInfraStack,
)


app = cdk.App()
WorkforcePlanningInfraStack(app, "WorkforcePlanningInfraStack")

app.synth()
