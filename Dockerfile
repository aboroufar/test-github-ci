# ============================
# 1. BUILDER STAGE
# ============================
FROM python:3.10-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.8.21 /uv /uvx /bin/

ARG ROOT_PROJ_DIR=/app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install base build packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    ssh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $ROOT_PROJ_DIR

# Copy dependency files first
COPY uv.lock pyproject.toml ./


# --- Install dependencies using SSH secret ---
RUN --mount=type=secret,id=ssh_private_key \
    mkdir -p -m 0700 /root/.ssh && \
    echo "Host *\n\tStrictHostKeyChecking no\n" > /root/.ssh/config && \
    cp /run/secrets/ssh_private_key /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================
# 2. FINAL STAGE
# ============================
FROM python:3.10-slim AS runtime

ENV PATH="/app/.venv/bin:$PATH"

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -d /app -s /bin/false appuser

ARG ROOT_PROJ_DIR=/app
ENV ROOT_PROJ_DIR=$ROOT_PROJ_DIR

WORKDIR $ROOT_PROJ_DIR

COPY --from=build --chown=appuser:appgroup $ROOT_PROJ_DIR .
COPY --from=build --chown=appuser:appgroup /root/.ssh /appuser/.ssh

USER appuser

# Ensure the workers.sh script is executable
RUN chmod +x ./workers.sh

# Run the workers.sh script as the container's default command
CMD ["bash", "./workers.sh"]