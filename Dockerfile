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

# Install pinned Rust toolchain for Charon extraction (matches PINS.lock)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly-2024-05-01
ENV PATH="/home/coq/.cargo/bin:${PATH}"

COPY --chown=coq:coq . .

RUN chmod +x scripts/*.sh extract/*.sh

# Pre-compile Coq artifacts at build time so runtime supports --read-only
RUN if [ -f "upstream/domain-projection-spec/proofs/Invariants.v" ]; then \
      ./scripts/verify_coq.sh; \
    fi

# Enforce read-only perimeter on upstream tree
RUN if [ -d "upstream" ]; then chmod -R a-w upstream; fi

ENTRYPOINT ["/bin/bash", "-c", "./scripts/verify_provenance.sh PINS.lock && coqchk -silent -Q upstream/domain-projection-spec/proofs DPP -Q generated/coq ArcstoneExtracted -Q proofs ArcstoneRefinement ArcstoneRefinement.Refinement"]
