-- SQLite
DELETE FROM django_migrations WHERE app = "core";
DROP TABLE IF EXISTS core_UserProfile;
DROP TABLE IF EXISTS core_comment;
DROP TABLE IF EXISTS core_follow;
DROP TABLE IF EXISTS core_location;
DROP TABLE IF EXISTS core_message;
DROP TABLE IF EXISTS core_snapshot;
DROP TABLE IF EXISTS core_tag;
DROP TABLE IF EXISTS core_userimage;
