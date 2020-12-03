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
    PRIMARY KEY(user_id,refresh_token)
);