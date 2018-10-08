---
title: "Anti-Microbial Peptide Classification Benchmark Utility"
layout: default
---

## Team Members

* Yuya Jeremy Ong
* Andrew Hankinson
* Aaron Wilhelm

## Introduction
Recently, the research for Antimicrobial Peptides (AMP) has become a critical component
of developing new and novel agents necessary for fighting against new strain of
drug-resistant microbes like bacteria and fungi. However, for researchers to be
able to experiment with various strains of these AMPs require lots of time and
expensive costs to test the validity of each variant - and thus not a scalable in
practice.

To reduce the overall search space for the possible AMPs to experiment on, researchers
have turned to machine learning and computational model-based approaches for determining
if a given sequence of protiens are in fact AMPs or Non-AMPs. Currently, there are
various online web-services which allow for researchers to classify whether the
given sequences are AMPs. Using these services, they can immensely accelerate their work.

However, one critical concern for these models is the validity of their robustness
and integrity with regard to their prediction accuracy. Thus, a careful review of
each of these services would need to be evaluated to ensure that the reported
results from these papers are in fact correct. Furthermore, upon an observation
of a very small samples which were randomly shuffled, we have found that the
models have incorrectly misclassified these samples as valid AMPs.

From the basis of this observation, we have curated a synthesized dataset comprised
of both real AMP sequences, as well as a collection of randomly shuffled AMP sequences
of various k-groups - establishing a dataset to expose non-robust models. Through
establishing a proper baseline on this dataset, we will systematically experiment on
various online services listed by Gabere et. al to formulate a proper baseline and
devise new models which will attempt to out-perform the state-of-the-art models.

## Project Aim
The aim of this project is broken down into the following set of phases:
* Build a data pipeline to preprocess and merge a collection of AMP dataset.
* Develop and process the AMP dataset over a set of randomization functions to generate synthesized Non-AMP datasets.
* Develop a online web-scraping system for the listed online services suggested by Gabere et. al's work.
* Compute various metrics on the resulting model performance and conduct a comparative analysis.
* If time persists, develop a model on our new dataset using various ML and Deep Learning methods.

## References
* Gabere, M. N., & Noble, W. S. (2017). Empirical comparison of web-based antimicrobial peptide prediction tools. Bioinformatics, 33(13), 1921-1929.
