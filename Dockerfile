# Ref: https://mitchellh.com/writing/nix-with-dockerfiles
# Use the latest NixOS image as the builder
FROM nixos/nix:latest AS builder

# Copy the source and setup the working directory
COPY ./flake.nix /tmp/build/flake.nix
COPY ./flake.lock /tmp/build/flake.lock
COPY ./pyproject.toml /tmp/build/pyproject.toml
COPY ./poetry.lock /tmp/build/poetry.lock
COPY ./app /tmp/build/app

WORKDIR /tmp/build

# Build the Nix environment with flakes enabled
# The --option filter-syscalls false is required for Nix to run in Docker
RUN nix \
    --extra-experimental-features "nix-command flakes" \
    --option filter-syscalls false \
    build

# Create a directory for the Nix store closure
# The Nix store closure is the set of dependencies required for the built application
RUN mkdir /tmp/nix-store-closure
RUN cp -R $(nix-store -qR result) /tmp/nix-store-closure

# Use a minimal base image for the final stage
FROM scratch

# Workaround to add a temporary directory in the scratch image
# This is necessary if your application requires a /tmp directory
COPY ./tmp /tmp

WORKDIR /app

# Copy the Nix store closure from the builder stage
COPY --from=builder /tmp/nix-store-closure /nix/store

# Copy the build result from the builder stage
COPY --from=builder /tmp/build/result /app

# Set the entry point to the built application
# Ensure that the path to the executable is correct
CMD ["/app/bin/bot"]
