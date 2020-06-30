create table roles (
    id serial primary key,
    role_name varchar(500) NOT NULL
);

create table users (
    id serial,
    role_id integer not null,
    first_name varchar(500),
    last_name varchar(500),
    email varchar(500),
    username varchar(500) not null,
    password varchar(500),
    foreign key ("role_id") references "public"."roles"("id"),
    unique (id, username)
);

insert into roles
    (role_name)
    values
    ('superuser');

insert into users
    (first_name, last_name, email, role_id, username, password)
    values
    ('Paul', 'Piggott', 'p.piggott0814@gmail.com', 1, 'pauly_p14', 'lovespaghettisomuch'),
    ('Timothy', 'Piggott', 'tpiggott.projects@gmail.com', 1, 'timnthemilkman', 'needtochange');

create table scraped_accounts (
    id serial primary key,
    twitter_id bigint,
    twitter_handle varchar(500) not null,
    first_scraped_on timestamp with time zone,
    last_scraped_on timestamp with time zone,
    unique(id, twitter_handle)
);

create table scraped_tweets (
    id bigserial,
    twitter_id bigint,
    account_id bigint not null,
    name varchar(500),
    expiration_date timestamp with time zone,
    type varchar(500),
    strike numeric,
    bid numeric,
    ask numeric,
    interest numeric,
    volume numeric,
    iv numeric,
    pct_diff numeric,
    purchase numeric,
    extra varchar(500),
    scraped_on timestamp with time zone,
    tweet_time timestamp with time zone,
    foreign key("account_id") references "public"."scraped_accounts"("id"),
    unique(twitter_id, tweet_time)
);

insert into scraped_accounts
    (twitter_handle)
    values
    ('@unusual_whales');