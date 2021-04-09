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

CREATE TABLE cookies (
    nommer_id INTEGER NOT NULL,
    last_grabbed REAL NOT NULL,
    total_cookies INTEGER NOT NULL,
    total_cookies_grabbed INTEGER NOT NULL,
    total_cookies_gifted INTEGER NOT NULL,
    total_grab_attempts INTEGER NOT NULL,
    total_cookies_received INTEGER NOT NULL,
    PRIMARY KEY(nommer_id)
);

CREATE TABLE prefixes (
    guild_id INTEGER NOT NULL,
    prefix TEXT NOT NULL,
    PRIMARY KEY(guild_id)
);