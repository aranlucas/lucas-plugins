# Eval

Compare how a skill, prompt, or workflow changes observable agent behavior.

1. State the behavior under study and write a small rubric with concrete outcomes. Keep the rubric out of candidate prompts.
2. Prepare isolated project-shaped workspaces with the appropriate variant and realistic starting artifacts. Give candidates the same organic user request. Do not reveal expected answers, variant labels, or the fact that other candidates exist.
3. Dispatch candidates through [T3 orchestration](../references/t3-orchestration.md), choosing runnable models and recording their exact settings. Keep candidate writes separate.
4. Collect actual outputs and supported task activity. Use `t3_thread_read` on returned child IDs when needed, including pagination. Do not scan unrelated transcripts. If reads or tool activity are unavailable, mark instruction-following evidence as limited.
5. Give a separate judge neutral output labels and the rubric, without model identity. Have the same judge score compared variants on the same scale.
6. Read each artifact yourself and reconcile the judge's findings. Grade behavior and evidence, not a candidate saying it followed the skill.
7. For a quantitative claim, use repeated comparable trials and report variability. A single exercise demonstrates that case, not a general improvement.

Report the request, variants, observable results, judge findings, limitations, and whether the change merits adoption.
