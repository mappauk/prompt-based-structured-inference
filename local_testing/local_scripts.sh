### analysis 
python -m src.analysis.mf_role_data_analysis C:\src\MoralDistillation\data C:\Users\mpauk\Downloads\ilp_output.json
python -m src.analysis.mf_data_analysis C:\src\MoralDistillation\data C:\Users\mpauk\Documents\MoralDistillationResults\True-False\few_shot
python -m src.analysis.coref_analysis C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\Users\mpauk\Downloads\coref_genia_few_shot_mv.json

### moral foundations

#tf 
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_ilp_tf C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_few_shot_tf C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples

#mv
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_ilp_mv C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_few_shot_mv C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples

#mv2
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_ilp_mv2 C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_few_shot_mv2 C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples


#gz
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_ilp_gz C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples
python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_few_shot_gz C:\src\MoralDistillation\data\moral_foundation_congress C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples

### coreference genia

#tf 
python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_tf C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\genia_coref_examples.json
python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_tf C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\genia_coref_examples.json

#mv
python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_mv C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\genia_coref_examples.json
python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_mv C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\genia_coref_examples.json

#gz
python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_gz C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\genia_coref_examples.json
python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_gz C:\src\MoralDistillation\data\coref\GENIA_MedCo_coreference_corpus_1.0\test C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\genia_coref_examples.json

### coreference conll

#tf
python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_tf C:\src\MoralDistillation\data\coref\conll-2012\v12\data\test\data\english\annotations C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\ontonotes_coref_examples.json
python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_tf C:\src\MoralDistillation\data\coref\conll-2012\v12\data\test\data\english\annotations C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\ontonotes_coref_examples.json

#mv
python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_mf C:\src\MoralDistillation\data\coref\conll-2012\v12\data\test\data\english\annotations C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\ontonotes_coref_examples.json
python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_mf C:\src\MoralDistillation\data\coref\conll-2012\v12\data\test\data\english\annotations C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\ontonotes_coref_examples.json

#gz
python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_gz C:\src\MoralDistillation\data\coref\conll-2012\v12\data\test\data\english\annotations C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\ontonotes_coref_examples.json
python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_gz C:\src\MoralDistillation\data\coref\conll-2012\v12\data\test\data\english\annotations C:\src\MoralDistillation\output\test.json C:\src\MoralDistillation\data\few_shot_examples\ontonotes_coref_examples.json




## gen z test


python -m src.experiments.genz_test C:\src\MoralDistillation\output\test.json