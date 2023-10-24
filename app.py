#!/usr/bin/env python3
import aws_cdk as cdk

from infrastructure.app_builder import build_pipeline

app = cdk.App()
build_pipeline(app)
app.synth()
