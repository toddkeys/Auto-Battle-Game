-- Online top-10 leaderboard for the game (Supabase).
-- Run in Supabase > SQL Editor for setup or an existing-table upgrade.
-- Players can read scores and add new ones; nobody can edit or delete them from the game.

create table if not exists public.scores (
  id         bigint generated always as identity primary key,
  board      text not null check (board ~ '^(normal|hard|daily-[0-9]{4}-[0-9]{2}-[0-9]{2})$'),
  name       text not null check (char_length(btrim(name)) between 1 and 16),
  round      int  not null check (round >= 1),
  bosses     int  not null default 0 check (bosses >= 0),
  created_at timestamptz not null default now()
);

create index if not exists scores_board_rank on public.scores (board, round desc, bosses desc, created_at);

alter table public.scores enable row level security;

drop policy if exists "anyone can read scores" on public.scores;
create policy "anyone can read scores" on public.scores for select to anon using (true);

drop policy if exists "anyone can add a score" on public.scores;
create policy "anyone can add a score" on public.scores for insert to anon with check (true);

-- the game may only fill in these four columns (id and created_at are set by the database)
revoke all on public.scores from anon;
grant select on public.scores to anon;
grant insert (board, name, round, bosses) on public.scores to anon;

-- Line-ups: the heroes each top-10 run ended with, as [{"t":type,"s":stars,"f":fused partner}] (up to 12).
-- Safe to run on the existing table: it only adds the column and lets the game fill it in.
alter table public.scores add column if not exists team jsonb
  check (team is null or (jsonb_typeof(team) = 'array' and jsonb_array_length(team) <= 12 and pg_column_size(team) < 2000));
grant insert (board, name, round, bosses, team) on public.scores to anon;

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
