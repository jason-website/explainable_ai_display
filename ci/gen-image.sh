#!/usr/bin/env bash
set +x
docker build --no-cache  -t explainable-ai-display .
docker tag explainable-ai-display jason0722985179/explanation-ai-display:1.3
