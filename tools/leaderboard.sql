-- Online top-10 leaderboard for the game (Supabase).
-- Paste this whole file into Supabase > SQL Editor and press Run, once.
-- Players can read scores and add new ones; nobody can edit or delete them from the game.

create table if not exists public.scores (
  id         bigint generated always as identity primary key,
  board      text not null check (board ~ '^(normal|hard|daily-[0-9]{4}-[0-9]{2}-[0-9]{2})$'),
  name       text not null check (char_length(btrim(name)) between 1 and 16),
  round      int  not null check (round between 1 and 200),
  bosses     int  not null default 0 check (bosses between 0 and 50),
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
