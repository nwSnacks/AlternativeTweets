drop table if exists scores;
create table scores (
    pub_date date primary key,
    username text not null,
    score integer not null
);
