CREATE TABLE courses (
    id SERIAL,
    name VARCHAR (200) UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE questions (
    id SERIAL,
    text VARCHAR (500) NOT NULL,
    course_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id) REFERENCES courses (id)
);

CREATE TABLE answers (
    id SERIAL,
    text VARCHAR (200) NOT NULL,
    correct BOOLEAN NOT NULL,
    question_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (question_id) REFERENCES questions (id)
);

CREATE TABLE parameters (
    id SERIAL,
    name VARCHAR (50),
    value TEXT,
    PRIMARY KEY (id)
);

INSERT INTO parameters (name, value) VALUES ('MOODLE_HEADER', '');
INSERT INTO parameters (name, value) VALUES ('MOODLE_MASK', '');
INSERT INTO parameters (name, value) VALUES ('LATEX_MASK', '');
