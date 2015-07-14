delete from `awfy_run` where `id` in
(select `run_id` from `awfy_build` where `mode_id` = 28);

delete from `awfy_breakdown` where `build_id` in
(select `id` from `awfy_build` where `mode_id` = 28);

delete from `awfy_score` where `build_id` in
(select `id` from `awfy_build` where `mode_id` = 28);

delete from `awfy_build` where `mode_id` = 28;
