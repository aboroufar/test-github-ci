#!/bin/bash
NUM_CORES=$(nproc)

echo "Starting RQ worker pool with $NUM_CORES workers..."

rq worker-pool default -n "$NUM_CORES" --job-class rq.job.Job --url redis://host.docker.internal:6379
