CREATE TABLE follow_list (
    channel_id INTEGER,
    twitter_user_id INTEGER,
    PRIMARY KEY(channel_id,twitter_user_id)
);
CREATE TABLE code_temp (
    code TEXT NOT NULL
);
CREATE TABLE spt_users (
    user_id INTEGER NOT NULL,
    refresh_token TEXT NOT NULL,
    PRIMARY KEY(user_id)
);

CREATE TABLE fish (
    fisher_id INTEGER NOT NULL,
    times_fished INTEGER NOT NULL,
    total_fish INTEGER NOT NULL,
    last_fished REAL NOT NULL,
    exp_points INTEGER NOT NULL,
    coins INTEGER NOT NULL,
    PRIMARY KEY(fisher_id)
);

CREATE TABLE cookies (
    nommer_id INTEGER NOT NULL,
    cookies_grabbed INTEGER NOT NULL,
    total_cookies INTEGER NOT NULL,
    last_cookie REAL NOT NULL,
    cookies_gifted INTEGER NOT NULL,
    coookies_received INTEGER NOT NULL
)