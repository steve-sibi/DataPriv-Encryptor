# PrivacyFusion: Differential Privacy & Homomorphic Encryption Toolkit

## Overview
**PrivacyFusion** is a toolkit designed to provide both differential privacy and homomorphic encryption solutions within a user-friendly interface. Built with PyQt and leveraging libraries like TenSEAL and Diffprivlib, PrivacyFusion enables users to explore secure and private data analysis techniques. This project demonstrates key privacy-preserving methods suitable for data science applications where security and confidentiality are paramount.

## Features
- **Differential Privacy Mechanisms:** Supports Gaussian and Laplace mechanisms, offering privacy guarantees by adding controlled noise to data outputs.
- **Partially Homomorphic Encryption:** Enables secure computations on encrypted data using TenSEAL, allowing certain operations without decrypting sensitive information.
- **User Interface:** Interactive PyQt interface to make complex privacy tools accessible to users with various experience levels.
- **Data Compatibility:** Supports data input and visualization through CSV file uploads, with integration for Pandas and Seaborn for data analysis.

## Project Structure
- **`differential_privacy_approach.py`**: Implements differential privacy mechanisms using the Diffprivlib library. The script includes a GUI where users can choose privacy parameters and apply different noise mechanisms to datasets.
- **`partially_homomorphic_encryption_approach.py`**: Provides a partially homomorphic encryption application built with TenSEAL. Users can encrypt data and perform basic operations in an encrypted format, showcasing secure data handling techniques.


