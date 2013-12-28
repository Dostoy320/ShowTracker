drop table if exists shows;
create table shows (
  show_id integer primary key autoincrement,
  show_name text not null,
  seasons_total integer not null
);

drop table if exists episodes;
create table episodes (
  ep_id integer primary key autoincrement,
  ep_season integer not null,
  ep_name text,
  show_id integer,
  FOREIGN KEY(show_id) REFERENCES shows(show_id)
);