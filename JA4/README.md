## JA4 Fingerprints

This directory contains the JA4 fingerprints collected during our experiments, together with a decoded representation of their TLS and QUIC handshake characteristics.

For each observed JA4 fingerprint, the file provides:

* The JA4 identifier;
* The transport protocol (TCP or QUIC);
* The TLS version;
* The presence of SNI;
* The number of advertised cipher suites and extensions;
* The negotiated ALPN value;
* The list of cipher suites;
* The TLS extensions;
* The supported signature algorithms.

These files were generated from the network traces collected during our experiments and were used to analyze the network-layer characteristics of the evaluated LLM-based bots.

The purpose of this data is to facilitate the inspection and comparison of the JA4 fingerprints reported in the paper. It also allows researchers to reproduce our network-layer analysis or compare their own observations against the fingerprints collected in our study.

> **Note.** Some values may vary across browser versions, operating systems, network stacks, and software updates. Consequently, the fingerprints provided in this artifact should be considered representative of the experimental period rather than permanent identifiers.

