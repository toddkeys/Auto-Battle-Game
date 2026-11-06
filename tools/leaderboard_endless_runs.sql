-- Endless runs can exceed the original 200-round / 50-boss limits.
-- Apply to the live Supabase project in SQL Editor. Preserves all existing scores,
-- permissions, row-level security and lineup data. Safe to rerun.
begin;
alter table public.scores
  drop constraint if exists scores_round_check,
  add constraint scores_round_check check (round >= 1);
alter table public.scores
  drop constraint if exists scores_bosses_check,
  add constraint scores_bosses_check check (bosses >= 0);
commit;
