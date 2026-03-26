# Prompt Based Structured Inference

Code for the paper: https://aclanthology.org/2026.eacl-long.160/

# Abstract

Large language models (LLMs) have demonstrated strong performance in a wide-range of language tasks without requiring task-specific fine-tuning. However, they remain prone to hallucinations and inconsistencies, and often struggle with complex reasoning, in part due to the limitations of autoregressive generation. We propose to address some of these issues, particularly for structured prediction, by combining LLMs with combinatorial inference to marry the predictive power of LLMs with the structural consistency provided by inference methods. We perform exhaustive experiments in an effort to understand which prompting strategies can best estimate confidence values for downstream symbolic inference, and find that, independent of prompting strategy, incorporating symbolic inference yields more consistent and accurate predictions than prompting alone. Finally, we show that calibration and fine-tuning with structured learning objectives further increases performance on challenging tasks, highlighting that structured learning remains valuable in the era of LLMs.
