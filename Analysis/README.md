# Analysis Notebooks

This directory contains the data and Jupyter notebooks used to reproduce the analyses and tables presented in the paper.

## Data Overview

### `tests_anti-bot_mechanisms.csv`

Dataset used for the anti-bot evaluation presented in Section 5. It contains the results of all experiments conducted against the evaluated anti-bot mechanisms.

### `active_tests_with_TLS_IP_layers.csv`

Dataset collected during the active experiments for the TLS and IP fingerprinting layers. It links TLS, IP, and tool information used throughout the multi-layer analysis presented in Section 6.1 and 6.2.

### `active_tests_browser_layers.csv`

Dataset collected during the active experiments for the browser fingerprinting layer. It contains the browser attributes used in the analysis presented in Section 6.3.

### `df_attributes_scores.csv`

Contains the discriminative scores computed for each browser fingerprinting attribute, including the A-Score metrics used in the browser-layer analysis.

### `df_values_scores.csv`

Contains the discriminative scores computed for individual attribute values. Together with `df_attributes_scores.csv`, this dataset enables the reproduction of Table 11 and the browser fingerprinting results discussed in Section 6.

## Notebook Overview

### `antibots_mechanisms.ipynb`

Reproduces the Tables 3 and 7 analysis of anti-bot mechanisms presented in Section 5 and Appendix D.

### `ip_layer.ipynb`

Reproduces the Table 4 from the IP-layer characterization presented in Section 6.1.

### `tls_layer.ipynb`

Reproduces the Tables 5, 9, and 10 from TLS-layer fingerprinting analysis presented in Section 6.2 and Appendix H.

### `browser_fingerprinting_layer.ipynb`

Reproduces the Table 11 andresults from browser-layer fingerprinting analysis presented in Section 6.3 and Appendix I.

### `bots_classification.ipynb`

Reproduces the Table 6 and Figure 2 from the multi-layer bots classification presented in Section 7.

## Notes

The notebooks are intended to reproduce the analyses and tables presented in the paper directly from the released datasets. They do not require access to the original honeysite infrastructure.
The code prioritizes readability and transparency over performance to facilitate inspection, modification, and reuse by other researchers.
