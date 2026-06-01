#!/bin/bash

# Define variables

# Network interface
INTERFACE="YOUR_INTERFACE"

CAPTURE_FILTER="tcp port 443 or udp port 443"
ROTATION_DURATION=3600  # seconds

# Directory for storing dumps
OUTPUT_DIR="PATH/TO/YOUR/DIR"
RAW_DUMPS_DIRNAME="RAWS"
FILTERED_DUMPS_DIRNAME="FILTERED"

# Base filename for captures
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
RAW_FILE="$OUTPUT_DIR/$RAW_DUMPS_DIRNAME/capture_$TIMESTAMP.pcap.gz"
FILTERED_FILE="$OUTPUT_DIR/$FILTERED_DUMPS_DIRNAME/filtered_$TIMESTAMP.pcap.gz"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR/$RAW_DUMPS_DIRNAME"
mkdir -p "$OUTPUT_DIR/$FILTERED_DUMPS_DIRNAME"

echo "[INFO] Starting capture on $INTERFACE for TLS and QUIC Client Hellos"
# Run tshark with built-in rotation
tshark -i "$INTERFACE" \
  -f "$CAPTURE_FILTER" \
  -a duration:$ROTATION_DURATION \
  -w "$RAW_FILE"

# Filter pcaps after capturing 
# 2. Filter Client Hellos from TLS and QUIC:
#    - TLS Client Hello: tls.handshake.type == 1
#    - QUIC Initial with frame_type 0x06 (Client Hello): quic && quic.frame_type == 0x06
#    # Combine with 'or' in display filter
tshark -r "$RAW_FILE" \
       -Y '(tls.handshake.type == 1 or (quic && quic.frame_type == 0x06)) && (ip || ipv6)' \
       -w "$FILTERED_FILE"
