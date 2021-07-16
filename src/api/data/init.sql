CREATE TABLE IF NOT EXISTS Guilds (
    id              BIGINT NOT NULL PRIMARY KEY,
    icon_url        VARCHAR(255) NOT NULL DEFAULT '',
    title           VARCHAR(255) NOT NULL DEFAULT '',
    config          TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS GuildAccess (
    guild_id        BIGINT NOT NULL,
    member_id       BIGINT NOT NULL,
    PRIMARY KEY (guild_id, member_id)
);
