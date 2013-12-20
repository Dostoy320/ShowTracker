drop table if exists shows;
create table shows (
  id integer primary key autoincrement,
  show text not null,
  season integer not null,
  ep_number integer not null,
  ep_title text not null
);