# Hermetic Refinement Verification Environment
# Target: Coq 8.18.0 + Charon + Aeneas
FROM coqorg/coq:8.18.0

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    pkg-config \
    libssl-dev \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Switch back to coq user
USER coq
WORKDIR /home/coq/harness

# Install Rust toolchain for Charon extraction
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
ENV PATH="/home/coq/.cargo/bin:${PATH}"

COPY --chown=coq:coq . .

RUN chmod +x scripts/*.sh extract/*.sh

ENTRYPOINT ["/bin/bash", "-c", "./scripts/verify_provenance.sh PINS.lock && ./scripts/verify_coq.sh"]
