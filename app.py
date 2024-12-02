#!/usr/bin/env python3

import aws_cdk as cdk

from presentation_decomposer_lambda.presentation_decomposer_lambda_stack import PresentationDecomposerLambdaStack


app = cdk.App()
PresentationDecomposerLambdaStack(app, "PresentationDecomposerLambdaStack")

app.synth()
