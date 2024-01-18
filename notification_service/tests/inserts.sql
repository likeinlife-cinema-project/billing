CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.user (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    email TEXT NOT NULL,
    roles TEXT[],
    created TIMESTAMP WITH TIME ZONE DEFAULT now(),
    modified TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS user_email ON auth.user (email);

INSERT INTO auth.user (email, roles) VALUES ( 'likeinlife48@yandex.ru', '{"admin", "user"}');
INSERT INTO auth.user (email, roles) VALUES ( 'likeinlife@outlook.com', '{"subscriber", "user"}');
INSERT INTO auth.user (email, roles) VALUES ( 'test@example.com', '{"subscriber", "user"}');
INSERT INTO auth.user (email, roles) VALUES ( 'first@example.com', '{"subscriber", "user"}');
INSERT INTO auth.user (email, roles) VALUES ( 'second@example.com', '{"subscriber", "user"}');
INSERT INTO auth.user (email, roles) VALUES ( 'third@example.com', '{"subscriber", "user"}');
INSERT INTO auth.user (email, roles) VALUES ( 'fourth@example.com', '{"subscriber", "user"}');
