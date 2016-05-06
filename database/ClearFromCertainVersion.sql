delete from `awfy_run` where `id` in
(
SELECT `run_id`
FROM `awfy_build`
WHERE `id` >= (
SELECT min( `id` )
FROM `awfy_build`
WHERE `cset` LIKE 'e99ad69147576ee654f0206066c64ca9ab1e9%' )
);

delete from `awfy_breakdown` where `build_id` in
(
SELECT `id`
FROM `awfy_build`
WHERE `id` >= (
SELECT min( `id` )
FROM `awfy_build`
WHERE `cset` LIKE 'e99ad69147576ee654f0206066c64ca9ab1e9%' )
);

delete from `awfy_score` where `build_id` in
(
SELECT `id`
FROM `awfy_build`
WHERE `id` >= (
SELECT min( `id` )
FROM `awfy_build`
WHERE `cset` LIKE 'e99ad69147576ee654f0206066c64ca9ab1e9%' )
);


/*
delete from `awfy_build` where `id` in
(
SELECT `id`
FROM `awfy_build`
WHERE `id` > (
SELECT min( `id` )
FROM `awfy_build`
WHERE `cset` LIKE '5564af55beecf97%' )
);*/
